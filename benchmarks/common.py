"""Shared pieces: results store, metrics, splits, scaling, and the deep-model trainer."""
import math
import os
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from sklearn import metrics as skm
from sklearn.base import BaseEstimator, ClassifierMixin, clone
from sklearn.model_selection import GroupKFold, LeaveOneGroupOut, StratifiedKFold
from sklearn.preprocessing import LabelEncoder

ROOT = Path(__file__).parent
RESULTS_DIR = ROOT / "results"
KEY = ["dataset", "protocol", "model", "seed"]


class NotApplicable(Exception):
    """A protocol or model does not apply to this dataset; skipped, not an error."""


def git_commit():
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        return "unknown"


class Results:
    """Append-only CSV with one row per (dataset, protocol, model, seed, fold, metric).

    A (dataset, protocol, model, seed) unit is written only after all its folds finish,
    so an interrupted run resumes cleanly by skipping completed units.
    """

    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.done = set()
        if self.path.exists() and self.path.stat().st_size:
            df = pd.read_csv(self.path, dtype=str)
            self.done = set(map(tuple, df[KEY].drop_duplicates().values))

    def is_done(self, dataset, protocol, model, seed):
        return (str(dataset), str(protocol), str(model), str(seed)) in self.done

    def add(self, rows):
        if not rows:
            return
        df = pd.DataFrame(rows)
        df.to_csv(self.path, mode="a", header=not (self.path.exists() and self.path.stat().st_size), index=False)
        self.done |= set(map(tuple, df[KEY].astype(str).drop_duplicates().values))


def log_error(phase, msg):
    RESULTS_DIR.mkdir(exist_ok=True)
    with open(RESULTS_DIR / "errors.log", "a") as f:
        f.write(f"{datetime.now(timezone.utc).isoformat()} [{phase}] {msg}\n")
    print(f"  ! {msg}")


# ---------------------------------------------------------------- metrics

def scores(y_true, y_pred=None, y_score=None, multilabel=False):
    """Metrics for one fold. y_score: probabilities (n, k) or decision values."""
    if multilabel:
        y_true = np.asarray(y_true)
        ok = [j for j in range(y_true.shape[1]) if 0 < y_true[:, j].sum() < len(y_true)]
        return {"macro_auc": skm.roc_auc_score(y_true[:, ok], y_score[:, ok], average="macro") if ok else np.nan}
    out = {
        "accuracy": skm.accuracy_score(y_true, y_pred),
        "balanced_accuracy": skm.balanced_accuracy_score(y_true, y_pred),
        "kappa": skm.cohen_kappa_score(y_true, y_pred),
        "macro_f1": skm.f1_score(y_true, y_pred, average="macro"),
    }
    if y_score is not None:
        classes = np.unique(y_true)
        try:
            if y_score.ndim == 1 or y_score.shape[1] == 1:
                out["roc_auc"] = skm.roc_auc_score(y_true, np.ravel(y_score))
            elif y_score.shape[1] == 2:
                out["roc_auc"] = skm.roc_auc_score(y_true, y_score[:, 1])
            elif len(classes) == y_score.shape[1]:
                out["roc_auc"] = skm.roc_auc_score(y_true, y_score, multi_class="ovr", average="macro")
        except ValueError:
            pass
    return out


def itr_bits_per_min(n_targets, accuracy, seconds):
    """Wolpaw information transfer rate."""
    p, n = min(max(accuracy, 1e-12), 1.0), n_targets
    bits = math.log2(n) + p * math.log2(p) + ((1 - p) * math.log2((1 - p) / (n - 1)) if p < 1 else 0)
    return bits * 60.0 / seconds


def predict_scores(est, X):
    """Probabilities if the estimator has them, else decision values, else None."""
    for name in ("predict_proba", "decision_function"):
        if hasattr(est, name):
            try:
                s = np.asarray(getattr(est, name)(X))
                return s
            except Exception:
                continue
    return None


# ---------------------------------------------------------------- splits

def take(X, idx):
    """Index arrays and MNE Epochs alike."""
    return X[idx]


def splits(meta, y, protocol, seed=0):
    """Yield (fold_name, train_idx, test_idx) for a protocol over a metadata table.

    meta needs columns: subject, session, run (strings).
    """
    meta = meta.reset_index(drop=True)
    idx = np.arange(len(meta))
    name, _, arg = protocol.partition(":")

    if name == "standard":
        # Official train/test split, as labelled in MOABB session or run names.
        found = False
        for subj, m in meta.groupby("subject"):
            if m.session.str.contains("train").any() and m.session.str.contains("test").any():
                found = True
                yield str(subj), idx[m.index[m.session.str.contains("train")]], idx[m.index[m.session.str.contains("test")]]
            elif m.run.str.contains("train").any() and m.run.str.contains("test").any():
                for sess, ms in m.groupby("session"):
                    tr, te = ms.index[ms.run.str.contains("train")], ms.index[ms.run.str.contains("test")]
                    if len(tr) and len(te):
                        found = True
                        yield f"{subj}/{sess}", idx[tr], idx[te]
        if not found:
            raise NotApplicable("no train/test labels in session or run names")

    elif name == "within_session":
        k = int(arg or 5)
        for (subj, sess), m in meta.groupby(["subject", "session"]):
            cv = StratifiedKFold(k, shuffle=True, random_state=seed)
            for i, (tr, te) in enumerate(cv.split(m.index, y[m.index])):
                yield f"{subj}/{sess}/f{i}", idx[m.index[tr]], idx[m.index[te]]

    elif name in ("heldout_run", "heldout_session"):
        # e.g. "heldout_run:2,5" -> per subject and session, test on runs 2 and 5, train on the rest
        held = set(arg.split(","))
        col = "run" if name == "heldout_run" else "session"
        groups = ["subject", "session"] if col == "run" else ["subject"]
        for key, m in meta.groupby(groups):
            te = m[col].isin(held)
            if te.any() and (~te).any():
                yield "/".join(map(str, np.atleast_1d(key))), idx[m.index[~te]], idx[m.index[te]]

    elif name == "leave_one_run_out":
        # per subject and session, each run (repetition, trial) is the test set once: k-fold over runs
        for (subj, sess), m in meta.groupby(["subject", "session"]):
            for r in sorted(m.run.unique()):
                te = m.run == r
                if (~te).any():
                    yield f"{subj}/{sess}/test={r}", idx[m.index[~te]], idx[m.index[te]]

    elif name == "cross_session":
        for subj, m in meta.groupby("subject"):
            if m.session.nunique() < 2:
                raise NotApplicable("fewer than 2 sessions")
            for sess in m.session.unique():
                yield f"{subj}/test={sess}", idx[m.index[m.session != sess]], idx[m.index[m.session == sess]]

    elif name == "cross_subject":
        groups = meta.subject.values
        n = len(np.unique(groups))
        if n < 2:
            raise NotApplicable("fewer than 2 subjects")
        cv = LeaveOneGroupOut() if n <= 20 else GroupKFold(5)
        for tr, te in cv.split(idx, y, groups):
            yield "test=" + ",".join(map(str, sorted(np.unique(groups[te]))[:3])) + ("..." if len(np.unique(groups[te])) > 3 else ""), tr, te

    elif name == "cross_subject_fixed":
        # arg like "1-70:90-109" -> train subjects 1..70, test subjects 90..109
        (a, b), (c, d) = [tuple(map(int, r.split("-"))) for r in arg.split(":")]
        s = meta.subject.astype(int).values
        tr, te = idx[(s >= a) & (s <= b)], idx[(s >= c) & (s <= d)]
        if not len(tr) or not len(te):
            raise NotApplicable("fixed subject ranges not present")
        yield f"train={a}-{b},test={c}-{d}", tr, te

    else:
        raise ValueError(f"unknown protocol {protocol}")


# ---------------------------------------------------------------- evaluation loop

def evaluate(phase, results, dataset, protocol, model_name, make_model, X, y, meta, seeds,
             extra=None, multilabel=False, needs_seed=True, fold_hook=None):
    """Run one (dataset, protocol, model) over all folds and seeds, and store results."""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    for seed in (seeds if needs_seed else seeds[:1]):
        if results.is_done(dataset, protocol, model_name, seed):
            print(f"  = {dataset} | {protocol} | {model_name} | seed {seed}: done, skipping")
            continue
        rows, t_unit = [], time.time()
        try:
            folds = list(splits(meta, y, protocol, seed))
        except NotApplicable as e:
            print(f"  - {dataset} | {protocol}: not applicable ({e})")
            return
        for fold, tr, te in folds:
            set_seed(seed)
            est = make_model(seed)
            t0 = time.time()
            est.fit(take(X, tr), y[tr])
            train_s = time.time() - t0
            pred = np.asarray(est.predict(take(X, te))) if not multilabel else None
            score = predict_scores(est, take(X, te))
            fold_scores = scores(y[te], pred, score, multilabel=multilabel)
            if fold_hook:
                fold_scores.update(fold_hook(y[te], pred))
            for metric, value in fold_scores.items():
                rows.append(dict(phase=phase, dataset=dataset, protocol=protocol, model=model_name, seed=seed,
                                 fold=fold, metric=metric, value=float(value), n_train=len(tr), n_test=len(te),
                                 train_s=round(train_s, 2), device=device, commit=git_commit(),
                                 time=datetime.now(timezone.utc).isoformat(timespec="seconds"), **(extra or {})))
        results.add(rows)
        acc = np.mean([r["value"] for r in rows if r["metric"] in ("accuracy", "macro_auc")])
        print(f"  + {dataset} | {protocol} | {model_name} | seed {seed}: {len(folds)} folds, "
              f"mean {('accuracy' if not multilabel else 'macro_auc')} {acc:.4f}, {time.time() - t_unit:.0f}s")


def set_seed(seed):
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


# ---------------------------------------------------------------- deep-model trainer

class _Arrays(torch.utils.data.Dataset):
    """Serves (x, y) from a numpy array or memmap, standardizing one sample at a time."""

    def __init__(self, X, Y, mu, sd):
        self.X, self.Y, self.mu, self.sd = X, Y, mu, sd

    def __len__(self):
        return len(self.X)

    def __getitem__(self, i):
        x = np.asarray(self.X[i], dtype=np.float32)
        if self.mu is not None:
            x = (x - self.mu) / self.sd
        return torch.from_numpy(np.ascontiguousarray(x)), self.Y[i]


def channel_stats(X, chunk=2048):
    """Per-channel mean and std over trials and time, computed in chunks (no full copy)."""
    s = ss = 0.0
    n = 0
    for i in range(0, len(X), chunk):
        x = np.asarray(X[i:i + chunk], dtype=np.float64)
        s, ss, n = s + x.sum(axis=(0, 2)), ss + (x ** 2).sum(axis=(0, 2)), n + x.shape[0] * x.shape[2]
    mu = s / n
    sd = np.sqrt(np.maximum(ss / n - mu ** 2, 0)) + 1e-8
    return mu[:, None].astype(np.float32), sd[:, None].astype(np.float32)


class TorchClassifier(BaseEstimator, ClassifierMixin):
    """Fixed-epoch AdamW + cosine trainer for any (batch, channels, time) -> logits module.

    No early stopping and no checkpoint selection: the last epoch is evaluated, so the
    test set never influences training. Inputs are standardized per channel with
    statistics from the training set only.
    """

    def __init__(self, build, epochs=300, lr=1e-3, weight_decay=0.0, batch_size=64,
                 multilabel=False, scale="channel", device=None, workers=2, verbose=False):
        self.build, self.epochs, self.lr, self.weight_decay = build, epochs, lr, weight_decay
        self.batch_size, self.multilabel, self.scale = batch_size, multilabel, scale
        self.device, self.workers, self.verbose = device, workers, verbose

    def _dev(self):
        return self.device or ("cuda" if torch.cuda.is_available() else "cpu")

    def _loader(self, X, Y, shuffle):
        dev = self._dev()
        return torch.utils.data.DataLoader(
            _Arrays(X, Y, self.mu_, self.sd_), batch_size=self.batch_size if shuffle else 256, shuffle=shuffle,
            drop_last=shuffle and len(X) > self.batch_size, pin_memory=dev == "cuda",
            num_workers=self.workers if dev == "cuda" else 0, persistent_workers=False)

    def fit(self, X, y):
        self.mu_, self.sd_ = channel_stats(X) if self.scale == "channel" else (None, None)
        if self.multilabel:
            Y = torch.as_tensor(np.asarray(y, dtype=np.float32))
            n_out, loss_fn = Y.shape[1], torch.nn.BCEWithLogitsLoss()
        else:
            self.le_ = LabelEncoder().fit(y)
            self.classes_ = self.le_.classes_
            Y = torch.as_tensor(self.le_.transform(y), dtype=torch.long)
            n_out, loss_fn = len(self.classes_), torch.nn.CrossEntropyLoss()
        dev = self._dev()
        self.module_ = self.build(n_chans=X.shape[1], n_times=X.shape[2], n_outputs=n_out).to(dev)
        opt = torch.optim.AdamW(self.module_.parameters(), lr=self.lr, weight_decay=self.weight_decay)
        sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=max(1, self.epochs))
        loader = self._loader(X, Y, shuffle=True)
        self.module_.train()
        for ep in range(self.epochs):
            total = 0.0
            for xb, yb in loader:
                xb, yb = xb.to(dev, non_blocking=True), yb.to(dev, non_blocking=True)
                opt.zero_grad(set_to_none=True)
                loss = loss_fn(self.module_(xb), yb)
                loss.backward()
                opt.step()
                total += loss.item() * len(xb)
            sched.step()
            if self.verbose and (ep % 50 == 0 or ep == self.epochs - 1):
                print(f"      epoch {ep + 1}/{self.epochs} loss {total / len(X):.4f}")
        return self

    @torch.no_grad()
    def _logits(self, X):
        dev = self._dev()
        self.module_.eval()
        dummy = torch.zeros(len(X))
        return torch.cat([self.module_(xb.to(dev)).float().cpu() for xb, _ in self._loader(X, dummy, shuffle=False)])

    def predict_proba(self, X):
        z = self._logits(X)
        return (torch.sigmoid(z) if self.multilabel else torch.softmax(z, 1)).numpy()

    def predict(self, X):
        p = self.predict_proba(X)
        return (p > 0.5).astype(int) if self.multilabel else self.classes_[p.argmax(1)]


class ResNet1D(torch.nn.Module):
    """Three residual blocks (kernels 8, 5, 3), global average pooling, linear head.

    The time-series ResNet of Wang et al. (2017), as used for resnet1d_wang in the
    PTB-XL benchmark. Works for any channel count and window length.
    """

    def __init__(self, n_chans, n_outputs, n_filters=128, **_):
        super().__init__()

        def block(cin, cout):
            convs = []
            for i, k in enumerate((8, 5, 3)):
                convs += [torch.nn.Conv1d(cin if i == 0 else cout, cout, k, padding="same", bias=False),
                          torch.nn.BatchNorm1d(cout)] + ([torch.nn.ReLU()] if i < 2 else [])
            short = torch.nn.Sequential(torch.nn.Conv1d(cin, cout, 1, bias=False), torch.nn.BatchNorm1d(cout))
            return torch.nn.ModuleList([torch.nn.Sequential(*convs), short])

        self.blocks = torch.nn.ModuleList([block(n_chans, n_filters // 2), block(n_filters // 2, n_filters),
                                           block(n_filters, n_filters)])
        self.head = torch.nn.Linear(n_filters, n_outputs)

    def forward(self, x):
        for main, short in self.blocks:
            x = torch.relu(main(x) + short(x))
        return self.head(x.mean(-1))


def resnet1d(n_chans, n_times, n_outputs):
    return ResNet1D(n_chans, n_outputs)


def deep(build, **kw):
    """Factory: returns make_model(seed) for evaluate()."""
    return lambda seed: TorchClassifier(build, **kw)


def classical(pipeline):
    return lambda seed: clone(pipeline)


def quick_overrides(kw, quick):
    return {**kw, "epochs": 2} if quick else kw


def env_info():
    dev = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "cpu"
    return f"torch {torch.__version__}, device {dev}, cpu count {os.cpu_count()}"


# ---------------------------------------------------------------- downloads

def download(url, dst, quiet=False):
    """Download url to dst (skips if present); writes to dst.part first so interrupted downloads restart cleanly."""
    import shutil
    import urllib.request
    if os.path.exists(dst):
        return dst
    os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "bci-roadmap-benchmarks"})
    with urllib.request.urlopen(req, timeout=120) as r, open(dst + ".part", "wb") as f:
        total, done, last = int(r.headers.get("Content-Length") or 0), 0, 0
        while chunk := r.read(1 << 20):
            f.write(chunk)
            done += len(chunk)
            if not quiet and total and done - last > total / 20:
                last = done
                print(f"      {os.path.basename(dst)}: {done / total:.0%} of {total / 1e9:.2f} GB")
    shutil.move(dst + ".part", dst)
    return dst


def unzip(path, dest):
    import zipfile
    with zipfile.ZipFile(path) as z:
        z.extractall(dest)
    return dest


# ---------------------------------------------------------------- error-tolerant runner

def _safe(fn, phase, results, dataset, protocol, model, *a, **kw):
    try:
        fn(phase, results, dataset, protocol, model, *a, **kw)
    except NotApplicable as e:
        print(f"  - {dataset} | {protocol} | {model}: not applicable ({e})")
    except Exception as e:
        log_error(phase, f"{dataset} | {protocol} | {model}: {type(e).__name__}: {e}")
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
