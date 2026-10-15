"""More EEG benchmarks (phase 6): SSVEP, BCI Competition III, seizures, clinical TUH sets, emotion, speech,
attention, gaze, grasp-and-lift and the HBN / NeurIPS 2025 challenge tasks.

Datasets already run in eeg.py are not repeated here. Protocols and published numbers follow
projects/eeg/DATASETS.md (Parts A and B). Results go to the shared results CSV under phase "phase6".

| Dataset | Obtained | Protocol(s) | Models | Tested here |
|---|---|---|---|---|
| BETA (40-target SSVEP) | auto (figshare, 60-80 MB/subject) | `leave_one_run_out` (leave one of 4 blocks out); one dataset row per data length (0.4-1.8 s), ITR with 0.55 s gaze shift | CCA, FBCCA, TRCA (ensemble, filter bank); EEGNet, ShallowConvNet (0.4 s and 1.0 s) | yes, 2 subjects |
| BCI3-IVa (118 ch, right hand vs foot) | auto (bbci.de, terms click-through, no registration; 100 Hz version + true labels) | `standard` (official labelled/unlabelled split per subject) | CSP+LDA, TS+LR, MDM; EEGNet, ShallowConvNet | yes, 2 subjects |
| BCI3-IIIa (60 ch, 4-class MI) | auto (bbci.de GDF + true labels) | `standard` | as IVa | yes, 2 subjects |
| CHB-MIT | auto (PhysioNet open-data mirror on AWS) | `leave_one_run_out` = patient-specific (leave one seizure record out, all hours tested); `cross_subject` (patient folds, 2-s features); `standard` = BIOT/CBraMod split (patients 1-19 train, 22-23 test, 10-s segments, 16 bipolar ch, 200 Hz) | Spectral+SVM (patient-specific), Spectral+RF; BandPower+RF, EEGNet, CBraMod (segments); LaBraM is skipped (bipolar channels have no electrode positions) | yes, 2 patients x 3 records |
| Siena | auto (PhysioNet mirror) | `leave_one_run_out` (patient-specific, patients with >= 2 seizure records), `cross_subject` (LOSO) | Spectral+SVM, Spectral+RF | yes, 2 patients x 1-2 records |
| Bonn (sanity check only) | auto (UPF repository, CC BY 4.0) | `within_session:5` on A vs E and AB vs CD vs E | BandPower+RF, EEGNet | yes, all data |
| THINGS-EEG | not done | - | - | no: a fair 200-way zero-shot baseline needs an image encoder (CLIP) on 655 MB of images plus 1 GB/subject of EEG; no image model is in requirements.txt |
| EEGEyeNet (LR, angle/amplitude, position) | `--path eegeyenet=` (open data, but hosted on an OSF Google Drive add-on that cannot be scripted; put the official prepared `*_synchronised_min.npz` files there) | `standard` = official subject-ID split (sorted IDs, 70/15/15; validation unused) | Bins+LR / Bins+Ridge; EEGNet, ShallowConvNet | synthetic npz in the official format only |
| HBN-EEG challenge 1 (response time) and 2 (externalizing) | auto (eegdash `EEGChallengeDataset`, challenge copy at 100 Hz) | `standard` = train releases R1-R4, R6-R11 -> test on R5 (the challenge's validation release; release 12 is hidden) | Bins+Ridge; EEGNet, ShallowConvNet regressors | yes, mini releases R1 -> R5, 6 recordings each |
| KU Leuven AAD (attended ear) | auto (Zenodo, 290 MB/subject) | `leave_one_run_out` (trial-disjoint: leave out one pair of consecutive trials, one per attended ear), 5-s windows | TS+LR, CSP+LDA; EEGNet | yes, 1 subject, 12 trials |
| Thinking Out Loud (inner speech, 4 words) | auto (OpenNeuro derivatives on S3, 120-240 MB/session) | `cross_session`, `cross_subject`; 1.5-3.5 s after cue, inner-speech condition | TS+LR, MDM; EEGNet, ShallowConvNet | yes, 1 subject x 2 sessions |
| Kara One (11 imagined prompts) | auto (2.2 GB tar.bz2 per participant, streamed; only the .cnt, epoch indices, labels and released features are kept) | `cross_subject` (LOSO); `within_session:5` | Features+SVM on the released per-trial features (thinking period); EEGNet on raw thinking epochs | partial: loader for indices/labels/features checked on one participant; not run in quick mode (2.2 GB) |
| WAY-EEG-GAL (grasp-and-lift, original figshare data) | auto (figshare, 830 MB/participant; quick runs read single series over HTTP ranges) | `standard` = series 1-7 train, 8-9 test per participant (the Kaggle copy has 10 series); 6 events, labels +-150 ms | Bins+LR (one-vs-rest); EEGNet (multi-label) | yes, 1 participant, 2 series |
| TUSZ | `--path tusz=` | `standard` (train -> eval) with OVLP and SzCORE-style event scoring | Spectral+RF; EEGNet on 10-s segments | synthetic files in the official format only |
| TUEV | `--path tuev=` | `standard` (train -> eval), 5-s windows centred on each event, BIOT style | BandPower+RF; EEGNet, ShallowConvNet; LaBraM, CBraMod, EEGPT (fine-tuned) | synthetic files in the official format only |
| TUAR | `--path tuar=` | `cross_subject`, 5-s windows, 5 artifact types (multi-label) | BandPower+LR; EEGNet | synthetic files in the official format only |
| SEED / SEED-IV | `--path seed=` / `--path seed_iv=` | `standard` (subject-dependent: first 9/16 trials train), `cross_subject` (LOSO, session 1) | DE+SVM; EEGNet | synthetic files in the official format only |
| SEED-V | `--path seed_v=` | `standard` (CBraMod 5:5:5 trial split per session, pooled; validation unused) | DE+SVM; EEGNet; LaBraM, CBraMod, EEGPT | no (raw .cnt cannot be synthesized here) |
| DEAP (arousal, valence) | `--path deap=` | `leave_one_run_out` (leave one trial out), `cross_session` (trial-wise 10-fold) | BandPower+SVM, TS+LR; EEGNet, DeepConvNet (10-fold only) | synthetic files in the official format only |
| DREAMER | `--path dreamer=` | `leave_one_run_out` (leave one trial out; published numbers are leaky segment splits, so none are compared) | BandPower+SVM, TS+LR; EEGNet | synthetic files in the official format only |
| Kaggle ErrP (BCI Challenge NER 2015) | `--path kaggle_errp=` | `cross_subject` on the 16 training subjects (per-subject AUC) | XDAWNCov+TS+LR; EEGNet | synthetic files in the official format only |
| Kaggle HMS | `--path kaggle_hms=` (needs pyarrow) | `cross_subject` (patient folds), KL divergence to the vote distribution | BandPower+LR; EEGNet (KL loss) | synthetic files in the official format only |

Notes
- Every dataset load and every model run is wrapped, so failures are logged and the run continues.
- "standard" protocols encode official splits in meta (subject "all" where the split is not per subject).
- Seizure event metrics: window predictions per record in time order; OVLP (any overlap) sensitivity and false
  alarms per 24 h; plus a simplified re-implementation of SzCORE event scoring (events merged under 90 s, split
  above 5 min, reference extended 30 s before and 60 s after). Training sets keep all seizure windows and an
  evenly spaced subset of background windows; test records are scored in full.
- BETA: a 0.14 s visual-latency offset is applied after stimulus onset (a choice made here).
"""
import glob
import io
import json
import os
import re
import tarfile
import time
import urllib.request
import warnings
import zipfile
from datetime import datetime, timezone
from functools import partial

import mne
import numpy as np
import pandas as pd
import scipy.io as sio
import torch
from pyriemann.estimation import XdawnCovariances
from pyriemann.tangentspace import TangentSpace
from scipy.signal import cheb1ord, cheby1, filtfilt, resample_poly, welch
from sklearn import metrics as skm
from sklearn.base import BaseEstimator, ClassifierMixin, clone
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression, RidgeCV
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler
from sklearn.svm import SVC, LinearSVC

from common import (NotApplicable, TorchClassifier, _safe, channel_stats, classical, deep, download, evaluate,
                    git_commit, itr_bits_per_min, log_error, predict_scores, set_seed, splits, take)
from eeg import (DEEP, FOUNDATION, FOUNDATION_TRAIN, TUAB_CHANNELS, _deep_kw, _tuh_name, braindecode_builder,
                 crop_to_patches, foundation_builder, mi_classical)

warnings.filterwarnings("ignore")
mne.set_log_level("ERROR")
PHASE = "phase6"
UA = {"User-Agent": "bci-roadmap-benchmarks"}


# ================================================================== shared helpers

def _root(args, *p):
    path = os.path.join(args.data_dir, "eeg_more", *p)
    os.makedirs(path, exist_ok=True)
    return path


def _want(args, *names):
    return not args.datasets or any(n in args.datasets for n in names)


def _model_ok(args, name):
    return not args.models or name in args.models


def _gated(args, key, name):
    path = (getattr(args, "paths", None) or {}).get(key)
    if not path:
        print(f"\n[{PHASE}] {name} skipped (access-gated: pass --path {key}=FOLDER)")
    return path


def _json(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
        return json.load(r)


def _text(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
        return r.read().decode("latin-1")


def _deep_models(results, dname, protocol, X, y, meta, args, sfreq, names=("EEGNet", "ShallowConvNet"),
                 epoch_cap=None, fold_hook=None, multilabel=False, extra=None):
    """Braindecode models from eeg.DEEP with their default training settings."""
    for m in names:
        if not _model_ok(args, m):
            continue
        cls_name, train = DEEP[m]
        kw = _deep_kw(train, min(args.epochs, epoch_cap or args.epochs), args.batch_size)
        make = deep(braindecode_builder(cls_name, sfreq), multilabel=multilabel, **kw)
        _safe(evaluate, PHASE, results, dname, protocol, m, make, X, y, meta, args.seeds,
              fold_hook=fold_hook, multilabel=multilabel, extra=extra)


def _resample(X, sf_in, sf_out, chunk=1024):
    if sf_in == sf_out:
        return X
    from fractions import Fraction
    f = Fraction(int(sf_out), int(sf_in))
    out = [resample_poly(np.asarray(X[i:i + chunk], dtype=np.float32), f.numerator, f.denominator, axis=-1)
           for i in range(0, len(X), chunk)]
    return np.concatenate(out).astype(np.float32)


def _foundation_models(results, dname, protocol, X, y, meta, args, sfreq, ch_names, names=tuple(FOUNDATION),
                       fold_hook=None, extra=None):
    """LaBraM / CBraMod / EEGPT fine-tuned from their pretrained weights (eeg.py builders)."""
    for m in names:
        if not _model_ok(args, m):
            continue
        _, _, sf, patch, _ = FOUNDATION[m]
        try:
            Xm = crop_to_patches(_resample(X, sfreq, sf), sf, patch)
            info = mne.create_info(list(ch_names), sf, "eeg")
            make = deep(foundation_builder(m, info), **_deep_kw(FOUNDATION_TRAIN, args.foundation_epochs, args.batch_size))
        except NotApplicable as e:
            print(f"  - {dname} | {m}: not applicable ({e})")
            continue
        except Exception as e:
            log_error(PHASE, f"{dname} | {m}: setup failed ({type(e).__name__}: {e})")
            continue
        _safe(evaluate, PHASE, results, dname, protocol, f"{m} (fine-tuned)", make, Xm, y, meta, args.seeds,
              fold_hook=fold_hook, extra=extra)


def evaluate_custom(phase, results, dataset, protocol, model_name, make_model, X, y, meta, seeds, scorer,
                    needs_seed=True, extra=None):
    """Like common.evaluate, but scorer(est, X_test, y_test, meta_test) -> {metric: value}.

    Used for regression, soft-label (KL) and seizure event metrics, which need more than (y_true, y_pred).
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    y_split = y if np.ndim(y) == 1 else np.zeros(len(y))
    for seed in (seeds if needs_seed else seeds[:1]):
        if results.is_done(dataset, protocol, model_name, seed):
            print(f"  = {dataset} | {protocol} | {model_name} | seed {seed}: done, skipping")
            continue
        rows, t_unit = [], time.time()
        try:
            folds = list(splits(meta, y_split, protocol, seed))
        except NotApplicable as e:
            print(f"  - {dataset} | {protocol}: not applicable ({e})")
            return
        for fold, tr, te in folds:
            set_seed(seed)
            est = make_model(seed)
            t0 = time.time()
            est.fit(take(X, tr), y[tr])
            train_s = time.time() - t0
            for metric, value in scorer(est, take(X, te), y[te], meta.iloc[te].reset_index(drop=True)).items():
                rows.append(dict(phase=phase, dataset=dataset, protocol=protocol, model=model_name, seed=seed,
                                 fold=fold, metric=metric, value=float(value), n_train=len(tr), n_test=len(te),
                                 train_s=round(train_s, 2), device=device, commit=git_commit(),
                                 time=datetime.now(timezone.utc).isoformat(timespec="seconds"), **(extra or {})))
        results.add(rows)
        first = rows[0]["metric"] if rows else "-"
        mean = np.mean([r["value"] for r in rows if r["metric"] == first]) if rows else np.nan
        print(f"  + {dataset} | {protocol} | {model_name} | seed {seed}: {len(folds)} folds, "
              f"mean {first} {mean:.4f}, {time.time() - t_unit:.0f}s")


class TorchRegressor(TorchClassifier):
    """Fixed-epoch trainer for regression ("mse", targets standardized on the training set) or for
    soft labels ("kl", targets are distributions). Same schedule and input scaling as TorchClassifier."""

    def __init__(self, build, loss="mse", epochs=300, lr=1e-3, weight_decay=0.0, batch_size=64,
                 multilabel=False, scale="channel", device=None, workers=2, verbose=False):
        super().__init__(build, epochs, lr, weight_decay, batch_size, multilabel, scale, device, workers, verbose)
        self.loss = loss

    def fit(self, X, y):
        self.mu_, self.sd_ = channel_stats(X)
        Y = np.asarray(y, dtype=np.float32)
        self.squeeze_ = Y.ndim == 1
        Y = Y[:, None] if self.squeeze_ else Y
        if self.loss == "mse":
            self.ym_, self.ys_ = Y.mean(0), Y.std(0) + 1e-8
            Y = (Y - self.ym_) / self.ys_
            loss_fn = torch.nn.MSELoss()
        else:
            Y = Y / np.maximum(Y.sum(1, keepdims=True), 1e-8)
            loss_fn = lambda z, t: torch.nn.functional.kl_div(torch.log_softmax(z, 1), t, reduction="batchmean")
        dev = self._dev()
        self.module_ = self.build(n_chans=X.shape[1], n_times=X.shape[2], n_outputs=Y.shape[1]).to(dev)
        opt = torch.optim.AdamW(self.module_.parameters(), lr=self.lr, weight_decay=self.weight_decay)
        sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=max(1, self.epochs))
        loader = self._loader(X, torch.as_tensor(Y), shuffle=True)
        self.module_.train()
        for _ in range(self.epochs):
            for xb, yb in loader:
                xb, yb = xb.to(dev, non_blocking=True), yb.to(dev, non_blocking=True)
                opt.zero_grad(set_to_none=True)
                loss_fn(self.module_(xb), yb).backward()
                opt.step()
            sched.step()
        return self

    def predict(self, X):
        z = self._logits(X).numpy()
        if self.loss == "kl":
            return torch.softmax(torch.as_tensor(z), 1).numpy()
        out = z * self.ys_ + self.ym_
        return out[:, 0] if self.squeeze_ else out

    def predict_proba(self, X):
        return self.predict(X)


def deep_regressor(build, **kw):
    return lambda seed: TorchRegressor(build, **kw)


def _reg_models(results, dname, protocol, X, y, meta, args, sfreq, scorer, names=("EEGNet", "ShallowConvNet"),
                loss="mse", epoch_cap=None, extra=None):
    for m in names:
        if not _model_ok(args, m):
            continue
        cls_name, train = DEEP[m]
        kw = _deep_kw(train, min(args.epochs, epoch_cap or args.epochs), args.batch_size)
        make = deep_regressor(braindecode_builder(cls_name, sfreq), loss=loss, **kw)
        _safe(evaluate_custom, PHASE, results, dname, protocol, m, make, X, y, meta, args.seeds, scorer=scorer,
              extra=extra)


def regression_scores(est, X, y, meta):
    p = np.asarray(est.predict(X), dtype=float).ravel()
    y = np.asarray(y, dtype=float).ravel()
    rmse = np.sqrt(np.mean((p - y) ** 2))
    return {"rmse": rmse, "nrmse": rmse / (y.std() + 1e-12), "mae": np.mean(np.abs(p - y)),
            "pearson_r": np.corrcoef(p, y)[0, 1] if p.std() > 0 else np.nan}


# ------------------------------------------------------------------ feature transforms

def band_powers(X, sfreq, bands=((1, 4), (4, 8), (8, 13), (13, 20), (20, 30))):
    """Log band power per channel (Welch)."""
    X = np.asarray(X, dtype=np.float32)
    f, p = welch(X, fs=sfreq, nperseg=min(X.shape[-1], int(2 * sfreq)), axis=-1)
    return np.log(np.concatenate([p[..., (f >= a) & (f < b)].mean(-1) for a, b in bands], axis=1) + 1e-12)


def diff_entropy(X, sfreq):
    """Differential entropy per channel in delta, theta, alpha, beta, gamma (Gaussian assumption: 0.5 log(2 pi e var))."""
    from scipy.signal import butter, sosfiltfilt
    X = np.asarray(X, dtype=np.float32)
    out = []
    for a, b in ((1, 4), (4, 8), (8, 14), (14, 31), (31, 50)):
        sos = butter(4, [a, min(b, sfreq / 2 - 1)], btype="band", fs=sfreq, output="sos")
        out.append(0.5 * np.log(2 * np.pi * np.e * sosfiltfilt(sos, X, axis=-1).var(-1) + 1e-12))
    return np.concatenate(out, axis=1)


def time_bins(X, n_bins=10):
    """Mean amplitude in n_bins equal time bins per channel (keeps the slow, EOG-like signal)."""
    X = np.asarray(X, dtype=np.float32)
    n = X.shape[-1] // n_bins * n_bins
    return X[..., :n].reshape(X.shape[0], X.shape[1], n_bins, -1).mean(-1).reshape(len(X), -1)


def _chunked(fn):
    return FunctionTransformer(lambda X: np.concatenate([fn(X[i:i + 2048]) for i in range(0, len(X), 2048)]))


# ================================================================== BETA (SSVEP)

BETA_ARTICLE = "https://api.figshare.com/v2/articles/12264401/files?page_size=100"
BETA_CHANNELS = ["PZ", "PO5", "PO3", "POZ", "PO4", "PO6", "O1", "OZ", "O2"]
BETA_LENGTHS = [0.4, 0.6, 1.0, 1.4, 1.8]
BETA_DEEP_LENGTHS = [0.4, 1.0]
SSVEP_LATENCY_S = 0.14
GAZE_S = 0.55  # BETA paper's gaze-shift time for ITR


def load_beta(root, subjects):
    files = {f["name"]: f["download_url"] for f in _json(BETA_ARTICLE)}
    Xs, ys, metas, freqs = [], [], [], None
    for s in subjects:
        path = download(files[f"S{s}.mat"], os.path.join(root, f"S{s}.mat"))
        d = sio.loadmat(path, struct_as_record=False)["data"][0, 0]
        sup = d.suppl_info[0, 0]
        names = [str(np.ravel(c)[0]).upper() for c in sup.chan[:, 3]]
        eeg = d.EEG[[names.index(c) for c in BETA_CHANNELS], :750]  # 0.5 s pre + 2 s (S1-15) or more; keep 3 s
        freqs = np.ravel(sup.freqs).astype(float)
        n_blocks, n_targets = eeg.shape[2], eeg.shape[3]
        X = eeg.transpose(2, 3, 0, 1).reshape(n_blocks * n_targets, len(BETA_CHANNELS), -1)
        Xs.append(X.astype(np.float32))
        ys.append(np.tile(np.arange(n_targets), n_blocks))
        metas.append(pd.DataFrame(dict(subject=str(s), session="0", run=np.repeat(np.arange(n_blocks), n_targets).astype(str))))
    return np.concatenate(Xs), np.concatenate(ys), pd.concat(metas, ignore_index=True), freqs


class SSVEPDecoder(BaseEstimator, ClassifierMixin):
    """CCA (Lin 2006), FBCCA (Chen 2015) and ensemble filter-bank TRCA (Nakanishi 2018).

    Input: full epochs (n, ch, t) at sfreq; the analysis window starts at `start` s and lasts `length` s.
    Filtering is applied to the full epoch before cropping, to limit edge effects.
    """

    def __init__(self, method="cca", freqs=None, sfreq=250, start=0.64, length=1.0, n_harm=5, n_fb=5):
        self.method, self.freqs, self.sfreq, self.start, self.length = method, freqs, sfreq, start, length
        self.n_harm, self.n_fb = n_harm, n_fb

    def _bank(self, X):
        a, b = int(round(self.start * self.sfreq)), int(round((self.start + self.length) * self.sfreq))
        if self.method == "cca":
            return [np.asarray(X, dtype=np.float64)[..., a:b]]
        nyq, out = self.sfreq / 2, []
        for m in range(1, self.n_fb + 1):
            n, wn = cheb1ord([8 * m / nyq, 90 / nyq], [(8 * m - 2) / nyq, 100 / nyq], 3, 40)
            bb, aa = cheby1(n, 0.5, wn, btype="bandpass")
            out.append(filtfilt(bb, aa, np.asarray(X, dtype=np.float64), axis=-1)[..., a:b])
        return out

    def _refs(self, n):
        t = np.arange(n) / self.sfreq
        return [np.concatenate([[np.sin(2 * np.pi * h * f * t), np.cos(2 * np.pi * h * f * t)]
                                for h in range(1, self.n_harm + 1)]) for f in self.freqs]

    @staticmethod
    def _cca(x, Qy):
        Qx, _ = np.linalg.qr((x - x.mean(1, keepdims=True)).T)
        return np.linalg.svd(Qx.T @ Qy, compute_uv=False)[0]

    def fit(self, X, y):
        self.classes_ = np.unique(y)
        if self.method != "trca":
            return self
        self.W_, self.T_ = [], []
        for Xb in self._bank(X):
            Xb = Xb - Xb.mean(-1, keepdims=True)
            W, T = [], []
            for c in self.classes_:
                x = Xb[y == c]
                s = x.sum(0)
                S = s @ s.T - np.einsum("nct,ndt->cd", x, x)
                cat = np.concatenate(list(x), axis=1)
                Q = cat @ cat.T
                vals, vecs = np.linalg.eig(np.linalg.solve(Q, S))
                W.append(np.real(vecs[:, np.argmax(np.real(vals))]))
                T.append(x.mean(0))
            self.W_.append(np.stack(W, 1))
            self.T_.append(np.stack(T))
        return self

    def decision_function(self, X):
        bank = self._bank(X)
        w = np.arange(1, len(bank) + 1) ** -1.25 + 0.25
        R = np.zeros((len(X), len(self.classes_)))
        if self.method == "trca":
            for m, Xb in enumerate(bank):
                Xb = Xb - Xb.mean(-1, keepdims=True)
                W, T = self.W_[m], self.T_[m]
                tw = np.einsum("cw,kct->kwt", W, T).reshape(len(T), -1)
                for i, x in enumerate(Xb):
                    xw = (W.T @ x).ravel()
                    R[i] += w[m] * np.array([np.corrcoef(xw, t)[0, 1] for t in tw])
            return R
        Qys = [np.linalg.qr(r.T)[0] for r in self._refs(bank[0].shape[-1])]  # one reference set per target
        R = np.zeros((len(X), len(Qys)))
        for m, Xb in enumerate(bank):
            for i, x in enumerate(Xb):
                r = np.array([self._cca(x, Q) for Q in Qys])
                R[i] += (w[m] * r ** 2) if self.method == "fbcca" else r
        return R[:, self.classes_.astype(int)]  # targets are coded 0..n-1 in frequency order

    def predict(self, X):
        return self.classes_[np.argmax(self.decision_function(X), 1)]


def run_beta(results, args):
    if not _want(args, "BETA"):
        return
    print(f"\n[{PHASE}] BETA")
    try:
        X, y, meta, freqs = load_beta(_root(args, "beta"), [1, 2] if args.quick else range(1, 71))
    except Exception as e:
        log_error(PHASE, f"BETA: could not load ({type(e).__name__}: {e})")
        return
    onset = 0.5 + SSVEP_LATENCY_S
    for L in ([0.4, 1.0] if args.quick else BETA_LENGTHS):
        dname = f"BETA ({L} s)"
        hook = lambda yt, yp, L=L: {"itr_bits_min": itr_bits_per_min(40, float(np.mean(yt == yp)), L + GAZE_S)}
        for method, mname in (("cca", "CCA"), ("fbcca", "FBCCA"), ("trca", "TRCA")):
            est = SSVEPDecoder(method, freqs, 250, onset, L)
            _safe(evaluate, PHASE, results, dname, "leave_one_run_out", mname, classical(est), X, y, meta, args.seeds,
                  needs_seed=False, fold_hook=hook)
        if L in BETA_DEEP_LENGTHS:
            a = int(round(onset * 250))
            Xc = np.ascontiguousarray(X[..., a:a + int(round(L * 250))])
            _deep_models(results, dname, "leave_one_run_out", Xc, y, meta, args, 250, fold_hook=hook)


# ================================================================== BCI Competition III IVa and IIIa

BCI3 = "https://www.bbci.de/competition"
IVA_SUBJECTS = ["aa", "al", "av", "aw", "ay"]
IIIA_SUBJECTS = ["k3", "k6", "l1"]


def _bandpass(x, sfreq, lo=8.0, hi=30.0):
    return mne.filter.filter_data(np.nan_to_num(x).astype(np.float64), sfreq, lo, hi, verbose=False)


def load_iva(root, subjects):
    """100-Hz version; 8-30 Hz; epochs 0.5-2.5 s after the cue; labels from the published true_labels files."""
    Xs, ys, metas = [], [], []
    for s in subjects:
        z = zipfile.ZipFile(download(f"{BCI3}/download/competition_iii/berlin/100Hz/data_set_IVa_{s}_mat.zip",
                                     os.path.join(root, f"data_set_IVa_{s}_mat.zip")))
        m = sio.loadmat(io.BytesIO(z.read([n for n in z.namelist() if n.endswith(".mat")][0])),
                        squeeze_me=True, struct_as_record=False)
        t = sio.loadmat(download(f"{BCI3}/iii/results/berlin_IVa/true_labels_{s}.mat",
                                 os.path.join(root, f"true_labels_{s}.mat")), squeeze_me=True)
        fs = float(m["nfo"].fs)
        cnt = _bandpass(m["cnt"].astype(np.float32).T * 0.1, fs)  # int16 in 0.1 uV units
        pos = np.asarray(m["mrk"].pos, dtype=int)
        a, b = int(0.5 * fs), int(2.5 * fs)
        Xs.append(np.stack([cnt[:, p + a:p + b] for p in pos]).astype(np.float32))
        ys.append(np.where(np.asarray(t["true_y"]) == 1, "right_hand", "feet"))
        train = ~np.isnan(np.asarray(m["mrk"].y, dtype=float))
        metas.append(pd.DataFrame(dict(subject=s, session="0", run=np.where(train, "0train", "1test"))))
    return np.concatenate(Xs), np.concatenate(ys), pd.concat(metas, ignore_index=True)


def load_iiia(root, subjects):
    """GDF; 8-30 Hz; epochs 0.5-3.5 s after the cue (cue at 3 s after trial start); labels from true_label files."""
    names = {1: "left_hand", 2: "right_hand", 3: "feet", 4: "tongue"}
    Xs, ys, metas = [], [], []
    for s in subjects:
        raw = mne.io.read_raw_gdf(download(f"{BCI3}/download/competition_iii/graz/{s}b.gdf",
                                           os.path.join(root, f"{s}b.gdf")), preload=True, verbose=False)
        labels = np.loadtxt(download(f"{BCI3}/iii/results/graz_IIIa/true_label_{s}.txt",
                                     os.path.join(root, f"true_label_{s}.txt"))).astype(int)
        fs = raw.info["sfreq"]
        data = _bandpass(raw.get_data() * 1e6, fs)
        ev, eid = mne.events_from_annotations(raw, verbose=False)
        code = {v: k for k, v in eid.items()}
        starts = ev[np.array([code[c] == "768" for c in ev[:, 2]])]
        cues = ev[np.array([code[c] in ("769", "770", "771", "772", "783") for c in ev[:, 2]])]
        if len(starts) != len(labels):
            raise ValueError(f"{s}: {len(starts)} trial starts vs {len(labels)} labels")
        X, run = [], []
        for st in starts[:, 0]:
            c = cues[(cues[:, 0] >= st) & (cues[:, 0] < st + 8 * fs)]
            X.append(data[:, st + int(3.5 * fs):st + int(6.5 * fs)])
            run.append("0train" if len(c) and code[c[0, 2]] != "783" else "1test")
        Xs.append(np.stack(X).astype(np.float32))
        ys.append(np.array([names[k] for k in labels]))
        metas.append(pd.DataFrame(dict(subject=s, session="0", run=run)))
    return np.concatenate(Xs), np.concatenate(ys), pd.concat(metas, ignore_index=True)


def run_bci3(results, args):
    for name, loader, subjects, sf in (("BCI3-IVa", load_iva, IVA_SUBJECTS, 100), ("BCI3-IIIa", load_iiia, IIIA_SUBJECTS, 250)):
        if not _want(args, name):
            continue
        print(f"\n[{PHASE}] {name}")
        try:
            X, y, meta = loader(_root(args, "bci3"), subjects[:2] if args.quick else subjects)
        except Exception as e:
            log_error(PHASE, f"{name}: could not load ({type(e).__name__}: {e})")
            continue
        for mname, pipe in mi_classical().items():
            _safe(evaluate, PHASE, results, name, "standard", mname, classical(pipe), X, y, meta, args.seeds,
                  needs_seed=False)
        _deep_models(results, name, "standard", X, y, meta, args, sf)


# ================================================================== seizure detection (CHB-MIT, Siena, TUSZ)

PHYSIONET = "https://physionet-open.s3.amazonaws.com"  # PhysioNet's open-data mirror (much faster than physionet.org)
BIPOLAR16 = ["FP1-F7", "F7-T7", "T7-P7", "P7-O1", "FP2-F8", "F8-T8", "T8-P8", "P8-O2",
             "FP1-F3", "F3-C3", "C3-P3", "P3-O1", "FP2-F4", "F4-C4", "C4-P4", "P4-O2"]
REF19 = [c for c in TUAB_CHANNELS if c not in ("A1", "A2")]
TUH_BIPOLAR16 = [p.replace("T7", "T3").replace("T8", "T4").replace("P7", "T5").replace("P8", "T6") for p in BIPOLAR16]
FEAT_WIN_S, SEG_S, SEG_SF = 2.0, 10.0, 200
BG_PER_HOUR = 60  # background 10-s segments kept per hour of a training record (all seizure segments are kept)


def shoeb_features(sig, fs, win_s=FEAT_WIN_S, context=3):
    """Per 2-s window and channel: log energy in 8 bands of 3 Hz from 0.5 to 24.5 Hz, stacked with the
    previous two windows (6 s of context), following Shoeb & Guttag 2010."""
    w = int(win_s * fs)
    n = sig.shape[1] // w
    if n == 0:
        return np.zeros((0, sig.shape[0] * 8 * context), np.float32)
    x = sig[:, :n * w].reshape(sig.shape[0], n, w).transpose(1, 0, 2)
    spec = np.abs(np.fft.rfft(x - x.mean(-1, keepdims=True), axis=-1)) ** 2
    f = np.fft.rfftfreq(w, 1 / fs)
    E = np.stack([spec[..., (f >= a) & (f < a + 3)].sum(-1) for a in np.arange(0.5, 24.5, 3)], -1)
    E = np.log(E + 1e-6).reshape(n, -1)
    stacked = [np.concatenate([E[:1].repeat(k, 0), E[:n - k]]) for k in range(context)]
    return np.concatenate(stacked, 1).astype(np.float32)


def _labels_for(starts, length, seizures):
    """1 if the window centre lies inside a seizure."""
    c = starts + length / 2
    return np.array([any(a <= t < b for a, b in seizures) for t in c], dtype=int)


def _record_arrays(sig, fs, seizures, keep_all_segments, cache):
    """Features (2-s) for every window; raw 10-s segments at 200 Hz (all, or seizures + background subset)."""
    if os.path.exists(cache + ".npz"):
        d = np.load(cache + ".npz")
        return d["F"], d["yf"], d["tf"], d["S"], d["ys"], d["ts"]
    F = shoeb_features(sig, fs)
    tf = np.arange(len(F)) * FEAT_WIN_S
    yf = _labels_for(tf, FEAT_WIN_S, seizures)
    n_seg = int(sig.shape[1] / fs // SEG_S)
    ts = np.arange(n_seg) * SEG_S
    ys = _labels_for(ts, SEG_S, seizures)
    if not keep_all_segments:
        bg = np.flatnonzero(ys == 0)
        k = max(1, int(round(n_seg * SEG_S / 3600 * BG_PER_HOUR)))
        keep = np.union1d(np.flatnonzero(ys == 1), bg[np.linspace(0, len(bg) - 1, min(k, len(bg))).astype(int)] if len(bg) else [])
        ts, ys = ts[keep.astype(int)], ys[keep.astype(int)]
    S = np.stack([sig[:, int(t * fs):int(t * fs) + int(SEG_S * fs)] for t in ts]) if len(ts) else np.zeros((0, sig.shape[0], int(SEG_S * fs)))
    S = _resample(S, fs, SEG_SF) if len(S) else np.zeros((0, sig.shape[0], int(SEG_S * SEG_SF)), np.float32)
    np.savez(cache + ".npz", F=F, yf=yf, tf=tf, S=S.astype(np.float32), ys=ys, ts=ts)
    return F, yf, tf, S.astype(np.float32), ys, ts


def _pick(raw, names, rename=lambda c: c.upper()):
    """Signals (len(names), n) in uV in the requested order; missing channels are zero-filled."""
    have = {rename(c): c for c in raw.ch_names}
    found = [have[n] for n in names if n in have]
    if not found:
        raise ValueError("none of the requested channels found")
    data = raw.copy().pick(found).get_data() * 1e6
    out = np.zeros((len(names), raw.n_times), np.float32)
    for i, n in enumerate(names):
        if n in have:
            out[i] = data[found.index(have[n])]
    return out


def assemble_seizure(records, read_fn, cache_dir, segments=True):
    """records: list of dicts(patient, record, url_or_path, seizures, group). Returns feature and segment sets."""
    os.makedirs(cache_dir, exist_ok=True)
    F, Fm, S, Sm, fy, sy = [], [], [], [], [], []
    for r in records:
        cache = os.path.join(cache_dir, re.sub(r"[^\w.-]", "_", r["record"]))
        try:
            if os.path.exists(cache + ".npz"):
                arrays = _record_arrays(None, None, None, None, cache)
            else:
                sig, fs = read_fn(r)
                arrays = _record_arrays(sig, fs, r["seizures"], r.get("group") == "test", cache)
        except Exception as e:
            log_error(PHASE, f"{r['record']}: skipped ({type(e).__name__}: {e})")
            continue
        f, yf, tf, s, ys, ts = arrays
        base = dict(subject=r["patient"], session="0", record=r["record"], group=r.get("group", ""))
        F.append(f), fy.append(yf), Fm.append(pd.DataFrame(dict(base, t=tf, run=r.get("fold", "0"))))
        if segments:
            S.append(s), sy.append(ys), Sm.append(pd.DataFrame(dict(base, t=ts, run=r.get("group", ""))))
    feat = (np.concatenate(F), np.concatenate(fy), pd.concat(Fm, ignore_index=True)) if F else None
    seg = (np.concatenate(S), np.concatenate(sy), pd.concat(Sm, ignore_index=True)) if segments and S else None
    return feat, seg


def _runs(mask):
    d = np.diff(np.r_[0, np.asarray(mask, int), 0])
    return list(zip(np.flatnonzero(d == 1), np.flatnonzero(d == -1)))


def _merge_split(events, gap=90.0, max_len=300.0):
    out = []
    for a, b in sorted(events):
        if out and a - out[-1][1] < gap:
            out[-1] = (out[-1][0], max(out[-1][1], b))
        else:
            out.append((a, b))
    split = []
    for a, b in out:
        while b - a > max_len:
            split.append((a, a + max_len))
            a += max_len
        split.append((a, b))
    return split


def event_scores(meta, y_true, y_pred, step, min_consec=1):
    """OVLP sensitivity / false alarms per 24 h, and simplified SzCORE event scoring, over all test records."""
    ov = lambda e, f: e[0] < f[1] and f[0] < e[1]
    tot = dict(ref=0, tp=0, fa=0, sref=0, stp=0, shyp=0, shit=0)
    hours = 0.0
    for _, idx in meta.groupby("record").indices.items():
        idx = idx[np.argsort(meta.t.values[idx])]
        t = meta.t.values[idx].astype(float)
        hours += len(idx) * step / 3600
        ref = [(t[a], t[b - 1] + step) for a, b in _runs(y_true[idx] == 1)]
        hyp = [(t[a], t[b - 1] + step) for a, b in _runs(y_pred[idx] == 1) if b - a >= min_consec]
        tot["ref"] += len(ref)
        tot["tp"] += sum(any(ov(r, h) for h in hyp) for r in ref)
        tot["fa"] += sum(not any(ov(h, r) for r in ref) for h in hyp)
        sref, shyp = _merge_split(ref), _merge_split(hyp)
        ext = [(a - 30, b + 60) for a, b in sref]
        tot["sref"] += len(sref)
        tot["stp"] += sum(any(ov(r, h) for h in shyp) for r in ext)
        tot["shyp"] += len(shyp)
        tot["shit"] += sum(any(ov(h, r) for r in ext) for h in shyp)
    sens = tot["tp"] / tot["ref"] if tot["ref"] else np.nan
    ssens = tot["stp"] / tot["sref"] if tot["sref"] else np.nan
    sprec = tot["shit"] / tot["shyp"] if tot["shyp"] else np.nan
    return {"ovlp_sensitivity": sens, "fa_per_24h": tot["fa"] / max(hours, 1e-9) * 24,
            "szcore_sensitivity": ssens, "szcore_precision": sprec,
            "szcore_f1": 2 * ssens * sprec / (ssens + sprec) if ssens + sprec > 0 else 0.0,
            "szcore_fp_per_24h": (tot["shyp"] - tot["shit"]) / max(hours, 1e-9) * 24, "test_hours": hours}


def seizure_scorer(step, min_consec):
    def score(est, X, y, meta):
        pred = np.asarray(est.predict(X)).astype(int)
        s = predict_scores(est, X)
        s = s[:, 1] if s is not None and s.ndim == 2 else s
        out = {"balanced_accuracy": skm.balanced_accuracy_score(y, pred)}
        if s is not None and 0 < y.sum() < len(y):
            out.update(roc_auc=skm.roc_auc_score(y, s), pr_auc=skm.average_precision_score(y, s))
        out.update(event_scores(meta, y, pred, step, min_consec))
        return out
    return score


class Subsample(BaseEstimator, ClassifierMixin):
    """Keeps every positive window and at most `ratio` x as many negatives (fixed seed) before fitting."""

    def __init__(self, est, ratio=20, seed=0):
        self.est, self.ratio, self.seed = est, ratio, seed

    def fit(self, X, y):
        pos, neg = np.flatnonzero(y == 1), np.flatnonzero(y != 1)
        rng = np.random.default_rng(self.seed)
        neg = rng.choice(neg, min(len(neg), max(1, self.ratio * len(pos))), replace=False)
        keep = np.sort(np.r_[pos, neg])
        self.est_ = clone(self.est).fit(X[keep], y[keep])
        self.classes_ = self.est_.classes_
        return self

    def predict(self, X):
        return self.est_.predict(X)

    def decision_function(self, X):
        s = predict_scores(self.est_, X)
        return s[:, 1] if s is not None and s.ndim == 2 else s


def spectral_svm():
    return Subsample(make_pipeline(StandardScaler(), SVC(kernel="rbf", class_weight="balanced")), ratio=20)


def spectral_rf():
    return Subsample(RandomForestClassifier(n_estimators=300, class_weight="balanced_subsample", n_jobs=-1,
                                            random_state=0), ratio=20)


def patient_specific_meta(meta, y):
    """Assign a fold (run) per record: each seizure record is its own fold; seizure-free records are spread
    round-robin over the folds. Patients with fewer than 2 seizure records are dropped."""
    meta = meta.copy()
    meta["run"] = ""
    for p, m in meta.groupby("subject"):
        recs = m.record.unique()
        sz = [r for r in recs if y[m.index[m.record == r]].any()]
        if len(sz) < 2:
            continue
        free = [r for r in recs if r not in sz]
        fold = {r: str(i) for i, r in enumerate(sz)}
        fold.update({r: str(i % len(sz)) for i, r in enumerate(free)})
        meta.loc[m.index, "run"] = m.record.map(fold)
    return meta


def run_seizure_protocols(results, name, feat, seg, args, ch_names, cross_patient_segments=False):
    if feat is not None:
        F, yf, mf = feat
        score = seizure_scorer(FEAT_WIN_S, 2)
        ps = patient_specific_meta(mf, yf)
        keep = np.flatnonzero(ps.run.values != "")
        if len(keep):
            _safe(evaluate_custom, PHASE, results, name, "leave_one_run_out", "Spectral+SVM", lambda s: spectral_svm(),
                  F[keep], yf[keep], ps.iloc[keep].reset_index(drop=True), args.seeds, scorer=score, needs_seed=False)
        else:
            print(f"  - {name} | patient-specific: no patient with 2 seizure records")
        _safe(evaluate_custom, PHASE, results, name, "cross_subject", "Spectral+RF", lambda s: spectral_rf(),
              F, yf, mf, args.seeds, scorer=score, needs_seed=False)
    if cross_patient_segments and seg is not None:
        S, ys, ms = seg
        ms = ms.assign(subject="all", run=ms.run.map({"train": "0train", "test": "1test"}).fillna("val"))
        score = seizure_scorer(SEG_S, 1)
        bp = Subsample(make_pipeline(_chunked(partial(band_powers, sfreq=SEG_SF)),
                                     RandomForestClassifier(n_estimators=300, class_weight="balanced_subsample",
                                                            n_jobs=-1, random_state=0)), ratio=1000)
        _safe(evaluate_custom, PHASE, results, name, "standard", "BandPower+RF", classical(bp), S, ys, ms, args.seeds,
              scorer=score, needs_seed=False)
        for m in ("EEGNet",):
            if _model_ok(args, m):
                cls_name, train = DEEP[m]
                make = deep(braindecode_builder(cls_name, SEG_SF), **_deep_kw(train, min(args.epochs, 50), args.batch_size))
                _safe(evaluate_custom, PHASE, results, name, "standard", m, make, S, ys, ms, args.seeds, scorer=score)
        for m in ("CBraMod", "LaBraM"):
            if not _model_ok(args, m):
                continue
            _, _, sf, patch, _ = FOUNDATION[m]
            try:
                make = deep(foundation_builder(m, mne.create_info(list(ch_names), sf, "eeg")),
                            **_deep_kw(FOUNDATION_TRAIN, args.foundation_epochs, args.batch_size))
            except NotApplicable as e:
                print(f"  - {name} | {m}: not applicable ({e})")
                continue
            except Exception as e:
                log_error(PHASE, f"{name} | {m}: setup failed ({type(e).__name__}: {e})")
                continue
            _safe(evaluate_custom, PHASE, results, name, "standard", f"{m} (fine-tuned)", make,
                  crop_to_patches(_resample(S, SEG_SF, sf), sf, patch), ys, ms, args.seeds, scorer=score)


# ---------------------------------------------------------------- CHB-MIT

def chbmit_records(quick):
    base = f"{PHYSIONET}/chbmit/1.0.0"
    recs = [r.strip() for r in _text(f"{base}/RECORDS").split() if r.strip().endswith(".edf")]
    if quick:  # 2 patients x (2 seizure records + 1 seizure-free record)
        recs = ["chb01/chb01_01.edf", "chb01/chb01_03.edf", "chb01/chb01_04.edf",
                "chb22/chb22_01.edf", "chb22/chb22_20.edf", "chb22/chb22_25.edf"]
    out, summaries = [], {}
    for r in recs:
        p = r.split("/")[0]
        if p not in summaries:
            summaries[p] = parse_chb_summary(_text(f"{base}/{p}/{p}-summary.txt"))
        n = int(p[3:])
        group = "train" if n <= 19 or (quick and n == 1) else ("test" if n in (22, 23) else "val")
        out.append(dict(patient=p, record=r, url=f"{base}/{r}", seizures=summaries[p].get(os.path.basename(r), []),
                        group=group))
    return out


def parse_chb_summary(text):
    """{file name: [(start_s, end_s), ...]} from a chbNN-summary.txt."""
    out, cur, starts = {}, None, []
    for line in text.splitlines():
        if line.startswith("File Name:"):
            cur = line.split(":", 1)[1].strip()
            out[cur] = []
        m = re.match(r"Seizure\s*\d*\s*Start Time:\s*(\d+)", line)
        if m:
            starts.append(int(m.group(1)))
        m = re.match(r"Seizure\s*\d*\s*End Time:\s*(\d+)", line)
        if m and cur:
            out[cur].append((starts.pop(0), int(m.group(1))))
    return out


def run_chbmit(results, args):
    if not _want(args, "CHB-MIT"):
        return
    print(f"\n[{PHASE}] CHB-MIT")
    root = _root(args, "chbmit")

    def read(r):
        path = download(r["url"], os.path.join(root, "edf", r["record"]), quiet=True)
        raw = mne.io.read_raw_edf(path, preload=False, verbose=False)
        names = {c: c.upper().split("-0")[0] if c.upper().endswith("-0") else c.upper() for c in raw.ch_names}
        return _pick(raw, BIPOLAR16, rename=lambda c: names[c]), raw.info["sfreq"]

    try:
        feat, seg = assemble_seizure(chbmit_records(args.quick), read, os.path.join(root, "cache"))
    except Exception as e:
        log_error(PHASE, f"CHB-MIT: could not load ({type(e).__name__}: {e})")
        return
    run_seizure_protocols(results, "CHB-MIT", feat, seg, args, BIPOLAR16, cross_patient_segments=True)


# ---------------------------------------------------------------- Siena

SIENA_CHANNELS = ["FP1", "F3", "C3", "P3", "O1", "F7", "T3", "T5", "FZ", "CZ", "PZ",
                  "FP2", "F4", "C4", "P4", "O2", "F8", "T4", "T6"]


def _clock(s):
    h, m, sec = map(int, re.findall(r"\d+", s)[:3])
    return h * 3600 + m * 60 + sec


def parse_siena(text):
    """{file name: [(start_s, end_s)]} relative to the file's registration start (handles midnight wrap)."""
    out, cur, reg = {}, None, {}
    for line in text.splitlines():
        line = line.strip()
        if line.lower().startswith("file name"):
            cur = line.split(":", 1)[1].strip()
            out.setdefault(cur, [])
        elif re.match(r"registration start time", line, re.I) and cur:
            reg[cur] = _clock(line.split(":", 1)[1])
        elif re.match(r"(seizure )?start time", line, re.I) and cur:
            start = _clock(line.split(":", 1)[1])
        elif re.match(r"(seizure )?end time", line, re.I) and cur:
            end = _clock(line.split(":", 1)[1])
            r0 = reg.get(cur, start)
            a, b = (start - r0) % 86400, (end - r0) % 86400
            out[cur].append((a, b if b >= a else a + 60))
    return out


def run_siena(results, args):
    if not _want(args, "Siena"):
        return
    print(f"\n[{PHASE}] Siena")
    root, base = _root(args, "siena"), f"{PHYSIONET}/siena-scalp-eeg/1.0.0"
    try:
        recs = [r for r in _text(f"{base}/RECORDS").split() if r.endswith(".edf")]
        if args.quick:
            recs = ["PN00/PN00-1.edf", "PN00/PN00-2.edf", "PN12/PN12-3.edf"]
        lists, records = {}, []
        for r in recs:
            p = r.split("/")[0]
            if p not in lists:
                lists[p] = parse_siena(_text(f"{base}/{p}/Seizures-list-{p}.txt"))
            records.append(dict(patient=p, record=r, url=f"{base}/{r}", seizures=lists[p].get(os.path.basename(r), [])))

        def read(r):
            raw = mne.io.read_raw_edf(download(r["url"], os.path.join(root, "edf", r["record"]), quiet=True),
                                      preload=False, verbose=False)
            return _pick(raw, SIENA_CHANNELS, rename=lambda c: c.upper().replace("EEG ", "").strip()), raw.info["sfreq"]

        feat, _ = assemble_seizure(records, read, os.path.join(root, "cache"), segments=False)
    except Exception as e:
        log_error(PHASE, f"Siena: could not load ({type(e).__name__}: {e})")
        return
    run_seizure_protocols(results, "Siena", feat, None, args, SIENA_CHANNELS)


# ---------------------------------------------------------------- TUSZ (gated)

def run_tusz(results, args):
    path = _gated(args, "tusz", "TUSZ")
    if not path or not _want(args, "TUSZ"):
        return
    print(f"\n[{PHASE}] TUSZ from {path}")
    try:
        edfs = sorted(glob.glob(os.path.join(path, "**", "*.edf"), recursive=True))
        edfs = [e for e in edfs if re.search(r"[/\\](train|eval)[/\\]", e)]
        if args.quick:
            edfs = [e for e in edfs if "/train/" in e][:4] + [e for e in edfs if "/eval/" in e][:4]
        records = []
        for e in edfs:
            ev = pd.read_csv(e[:-4] + ".csv_bi", comment="#")
            sz = [(float(a), float(b)) for a, b, lab in zip(ev.start_time, ev.stop_time, ev.label) if lab != "bckg"]
            split = "test" if "/eval/" in e.replace("\\", "/") else "train"
            records.append(dict(patient=os.path.basename(e).split("_")[0], record=os.path.relpath(e, path), url=e,
                                seizures=sz, group=split))

        def read(r):
            raw = mne.io.read_raw_edf(r["url"], preload=False, verbose=False)
            return _pick(raw, REF19, rename=_tuh_name), raw.info["sfreq"]

        feat, seg = assemble_seizure(records, read, _root(args, "tusz_cache"))
    except Exception as e:
        log_error(PHASE, f"TUSZ: could not load ({type(e).__name__}: {e})")
        return
    # official train -> eval for both feature and segment models
    F, yf, mf = feat
    mf = mf.assign(subject="all", run=mf.group.map({"train": "0train", "test": "1test"}))
    _safe(evaluate_custom, PHASE, results, "TUSZ", "standard", "Spectral+RF", lambda s: spectral_rf(), F, yf, mf,
          args.seeds, scorer=seizure_scorer(FEAT_WIN_S, 2), needs_seed=False)
    S, ys, ms = seg
    ms = ms.assign(subject="all", run=ms.run.map({"train": "0train", "test": "1test"}))
    if _model_ok(args, "EEGNet"):
        cls_name, train = DEEP["EEGNet"]
        make = deep(braindecode_builder(cls_name, SEG_SF), **_deep_kw(train, min(args.epochs, 50), args.batch_size))
        _safe(evaluate_custom, PHASE, results, "TUSZ", "standard", "EEGNet", make, S, ys, ms, args.seeds,
              scorer=seizure_scorer(SEG_S, 1))


# ================================================================== Bonn (sanity check)

BONN = {"Z": "bb2c41b0-6c8b-4c9c-b7c0-62f4f87c9b48", "O": "ca3563e5-09bb-4373-84b3-c707e724432a",
        "N": "8b2c6173-2538-41ac-bff9-d569755ade66", "F": "91342498-960f-410f-9df8-42f3c4da2b45",
        "S": "500b0f1d-aa9b-49c2-abd8-0410acd4b86c"}  # sets A, B, C, D, E
BONN_FS = 173.61


def load_bonn(root):
    X, sets = [], []
    for letter, uid in BONN.items():
        z = zipfile.ZipFile(download(f"https://repositori.upf.edu/server/api/core/bitstreams/{uid}/content",
                                     os.path.join(root, f"{letter}.zip")))
        for n in sorted(z.namelist()):
            if n.lower().endswith(".txt"):
                X.append(np.loadtxt(io.BytesIO(z.read(n)))[:4096])
                sets.append("ABCDE"["ZONFS".index(letter)])
    return np.asarray(X, dtype=np.float32)[:, None, :], np.asarray(sets)


def run_bonn(results, args):
    if not _want(args, "Bonn"):
        return
    print(f"\n[{PHASE}] Bonn (sanity check only; not clinical performance)")
    try:
        X, sets = load_bonn(_root(args, "bonn"))
    except Exception as e:
        log_error(PHASE, f"Bonn: could not load ({type(e).__name__}: {e})")
        return
    tasks = {"Bonn (A vs E)": {"A": "healthy", "E": "ictal"},
             "Bonn (AB vs CD vs E)": {"A": "healthy", "B": "healthy", "C": "interictal", "D": "interictal", "E": "ictal"}}
    for dname, mapping in tasks.items():
        keep = np.isin(sets, list(mapping))
        Xk, y = X[keep], np.array([mapping[s] for s in sets[keep]])
        meta = pd.DataFrame(dict(subject="all", session="0", run="0"), index=range(len(y)))
        rf = make_pipeline(_chunked(partial(band_powers, sfreq=BONN_FS, bands=((0.5, 4), (4, 8), (8, 13), (13, 20), (20, 30), (30, 40), (40, 60)))),
                           RandomForestClassifier(n_estimators=300, n_jobs=-1, random_state=0))
        _safe(evaluate, PHASE, results, dname, "within_session:5", "BandPower+RF", classical(rf), Xk, y, meta,
              args.seeds, needs_seed=False)
        _deep_models(results, dname, "within_session:5", Xk, y, meta, args, BONN_FS, names=("EEGNet",), epoch_cap=100)


# ================================================================== EEGEyeNet (official prepared files)

EEGEYENET_FILES = {"LR": "LR_task_with_antisaccade_synchronised_min.npz",
                   "Direction": "Direction_task_with_dots_synchronised_min.npz",
                   "Position": "Position_task_with_dots_synchronised_min.npz"}


def eegeyenet_split(ids):
    """Official split (EEGEyeNet utils.split): sorted unique IDs, first 70% train, next 15% val, last 15% test."""
    import math
    u = np.unique(ids)
    n_test, n_val = math.ceil(0.15 * len(u)), math.ceil(0.15 * len(u))
    n_train = len(u) - n_val - n_test
    return np.where(np.isin(ids, u[:n_train]), "0train", np.where(np.isin(ids, u[n_train:n_train + n_val]), "val", "1test"))


def load_eegeyenet(path, task, quick):
    with np.load(os.path.join(path, EEGEYENET_FILES[task])) as f:
        X, Y = f["EEG"], f["labels"]
    if X.shape[1] > X.shape[2]:  # files store (trial, time, channel)
        X = X.transpose(0, 2, 1)
    run = eegeyenet_split(Y[:, 0])
    if quick:
        rng = np.random.default_rng(0)
        idx = np.sort(np.concatenate([rng.choice(np.flatnonzero(run == r), min(200, (run == r).sum()), replace=False)
                                      for r in ("0train", "1test")]))
        X, Y, run = X[idx], Y[idx], run[idx]
    meta = pd.DataFrame(dict(subject="all", session="0", run=run))
    return np.ascontiguousarray(X, dtype=np.float32), Y, meta


def angle_scores(est, X, y, meta):
    p = np.asarray(est.predict(X))
    ang = np.arctan2(p[:, 1], p[:, 0])
    d = np.arctan2(np.sin(y[:, 2] - ang), np.cos(y[:, 2] - ang))
    return {"rmse": np.sqrt(np.mean(d ** 2))}


def position_scores(est, X, y, meta):
    p, y = np.asarray(est.predict(X)), y[:, 1:]  # labels: [id, x, y]
    return {"rmse": np.sqrt(np.mean((p - y) ** 2)), "euclidean_distance": np.linalg.norm(p - y, axis=1).mean()}


class _Target(BaseEstimator):
    """Fits est on f(y) (e.g. cos/sin of the angle, or one column)."""

    def __init__(self, est, fn):
        self.est, self.fn = est, fn

    def fit(self, X, y):
        self.est_ = clone(self.est)
        self.est_.fit(X, self.fn(y))
        return self

    def predict(self, X):
        return self.est_.predict(X)


def run_eegeyenet(results, args):
    path = _gated(args, "eegeyenet", "EEGEyeNet (download the prepared npz files from the OSF project)")
    if not path or not _want(args, "EEGEyeNet"):
        return
    sf = 500
    targets = {"amplitude": (lambda y: y[:, 1], lambda e, X, y, m: {"rmse": np.sqrt(np.mean((np.ravel(e.predict(X)) - y[:, 1]) ** 2))}),
               "angle": (lambda y: np.c_[np.cos(y[:, 2]), np.sin(y[:, 2])], angle_scores)}
    for task in EEGEYENET_FILES:
        print(f"\n[{PHASE}] EEGEyeNet {task}")
        try:
            X, Y, meta = load_eegeyenet(path, task, args.quick)
        except Exception as e:
            log_error(PHASE, f"EEGEyeNet {task}: could not load ({type(e).__name__}: {e})")
            continue
        if task == "LR":
            y = Y[:, 1].astype(int)
            lr = make_pipeline(_chunked(time_bins), StandardScaler(), LogisticRegression(max_iter=2000))
            _safe(evaluate, PHASE, results, "EEGEyeNet-LR", "standard", "Bins+LR", classical(lr), X, y, meta,
                  args.seeds, needs_seed=False)
            _deep_models(results, "EEGEyeNet-LR", "standard", X, y, meta, args, sf, epoch_cap=50)
            continue
        jobs = targets.items() if task == "Direction" else [("position", (lambda y: y[:, 1:], position_scores))]
        for tname, (fn, scorer) in jobs:
            dname = f"EEGEyeNet-{tname}"
            ridge = make_pipeline(_chunked(time_bins), StandardScaler(), RidgeCV(alphas=np.logspace(-1, 5, 13)))
            _safe(evaluate_custom, PHASE, results, dname, "standard", "Bins+Ridge", lambda s: _Target(ridge, fn),
                  X, Y, meta, args.seeds, scorer=scorer, needs_seed=False)
            for m in ("EEGNet", "ShallowConvNet"):
                if not _model_ok(args, m):
                    continue
                cls_name, train = DEEP[m]
                kw = _deep_kw(train, min(args.epochs, 50), args.batch_size)
                make = lambda s, cls_name=cls_name, kw=kw, fn=fn: _Target(
                    TorchRegressor(braindecode_builder(cls_name, sf), **kw), fn)
                _safe(evaluate_custom, PHASE, results, dname, "standard", m, make, X, Y, meta, args.seeds, scorer=scorer)


# ================================================================== HBN-EEG / NeurIPS 2025 EEG Foundation Challenge

HBN_TRAIN = ["R1", "R2", "R3", "R4", "R6", "R7", "R8", "R9", "R10", "R11"]
HBN_TEST = "R5"
HBN_SF = 100


def _hbn_release(release, cache, quick):
    from eegdash.dataset import EEGChallengeDataset
    from braindecode.datasets import BaseConcatDataset
    ds = EEGChallengeDataset(task="contrastChangeDetection", release=release, cache_dir=cache, mini=quick,
                             description_fields=["subject", "session", "run", "task", "age", "gender", "sex",
                                                 "p_factor", "externalizing"])
    return BaseConcatDataset(ds.datasets[:6]) if quick else ds


def hbn_challenge1(ds):
    """Windows 0.5-2.5 s after each contrast-change stimulus; target = response time (starter-kit recipe)."""
    from braindecode.preprocessing import Preprocessor, create_windows_from_events, preprocess
    from eegdash.hbn.windows import add_aux_anchors, add_extras_columns, annotate_trials_with_target, keep_only_recordings_with
    preprocess(ds, [Preprocessor(annotate_trials_with_target, target_field="rt_from_stimulus", epoch_length=2.0,
                                 require_stimulus=True, require_response=True, apply_on_array=False),
                    Preprocessor(add_aux_anchors, apply_on_array=False)], n_jobs=1)
    ds = keep_only_recordings_with("stimulus_anchor", ds)
    w = create_windows_from_events(ds, mapping={"stimulus_anchor": 0}, trial_start_offset_samples=int(0.5 * HBN_SF),
                                   trial_stop_offset_samples=int(2.5 * HBN_SF), window_size_samples=2 * HBN_SF,
                                   window_stride_samples=HBN_SF, preload=True)
    w = add_extras_columns(w, ds, desc="stimulus_anchor", keys=("target", "rt_from_stimulus"))
    X = np.stack([w[i][0] for i in range(len(w))]).astype(np.float32)
    return X, w.get_metadata()["target"].to_numpy(float)


def hbn_challenge2(ds):
    """Non-overlapping 2-s windows of each recording; target = the subject's externalizing score."""
    from braindecode.preprocessing import create_fixed_length_windows
    from braindecode.datasets import BaseConcatDataset
    ds = BaseConcatDataset([d for d in ds.datasets if pd.notna(d.description.get("externalizing"))])
    w = create_fixed_length_windows(ds, window_size_samples=2 * HBN_SF, window_stride_samples=2 * HBN_SF,
                                    drop_last_window=True, preload=True)
    X, y = [], []
    for d in w.datasets:
        for i in range(len(d)):
            X.append(d[i][0])
            y.append(float(d.description["externalizing"]))
    return np.stack(X).astype(np.float32), np.asarray(y)


def run_hbn(results, args):
    if not _want(args, "HBN-C1", "HBN-C2", "HBN"):
        return
    print(f"\n[{PHASE}] HBN-EEG challenge tasks (train releases -> release {HBN_TEST})")
    cache = _root(args, "hbn")
    try:
        train = [_hbn_release(r, cache, args.quick) for r in (["R1"] if args.quick else HBN_TRAIN)]
        test = _hbn_release(HBN_TEST, cache, args.quick)
    except Exception as e:
        log_error(PHASE, f"HBN: could not load ({type(e).__name__}: {e})")
        return
    for dname, fn in (("HBN-C1 (response time)", hbn_challenge1), ("HBN-C2 (externalizing)", hbn_challenge2)):
        try:
            parts = [fn(d) for d in train] + [fn(test)]
            X = np.concatenate([p[0] for p in parts])
            y = np.concatenate([p[1] for p in parts])
            run = np.concatenate([np.full(len(p[1]), "0train") for p in parts[:-1]] + [np.full(len(parts[-1][1]), "1test")])
            ok = np.isfinite(y)
            X, y = X[ok], y[ok]
            meta = pd.DataFrame(dict(subject="all", session="0", run=run[ok]))
        except Exception as e:
            log_error(PHASE, f"{dname}: could not build windows ({type(e).__name__}: {e})")
            continue
        ridge = make_pipeline(_chunked(time_bins), StandardScaler(), RidgeCV(alphas=np.logspace(-1, 5, 13)))
        _safe(evaluate_custom, PHASE, results, dname, "standard", "Bins+Ridge", classical(ridge), X, y, meta,
              args.seeds, scorer=regression_scores, needs_seed=False)
        _reg_models(results, dname, "standard", X, y, meta, args, HBN_SF, regression_scores, epoch_cap=50)


# ================================================================== KU Leuven auditory attention

KUL_RECORD = "https://zenodo.org/api/records/4004271/files/S{n}.mat/content"
KUL_SF, KUL_WIN_S = 128, 5


def load_kul(root, subjects, trials=None):
    """Attended ear (L/R) per non-overlapping 5-s window; run = trial pair, so splits are trial-disjoint."""
    Xs, ys, metas = [], [], []
    for n in subjects:
        m = sio.loadmat(download(KUL_RECORD.format(n=n), os.path.join(root, f"S{n}.mat")), squeeze_me=True,
                        struct_as_record=False)
        for t, tr in enumerate(np.atleast_1d(m["trials"])):
            if trials is not None and t not in trials:
                continue
            eeg = np.asarray(tr.RawData.EegData, dtype=np.float32).T  # (64, time)
            fs = float(tr.FileHeader.SampleRate)
            w = int(KUL_WIN_S * fs)
            k = eeg.shape[1] // w
            Xs.append(eeg[:, :k * w].reshape(eeg.shape[0], k, w).transpose(1, 0, 2))
            ys.append(np.full(k, str(tr.attended_ear)))
            # folds hold out a pair of consecutive trials (the attended ear alternates R, L), so every training
            # set stays balanced; leave-one-trial-out would bias the classifier against the held-out class
            metas.append(pd.DataFrame(dict(subject=str(n), session="0", run=str(t // 2)), index=range(k)))
    return np.concatenate(Xs), np.concatenate(ys), pd.concat(metas, ignore_index=True)


def run_kul(results, args):
    if not _want(args, "KUL-AAD"):
        return
    print(f"\n[{PHASE}] KU Leuven AAD (attended ear, trial-disjoint)")
    try:
        # quick: subject 1, its 12 short trials (trials 9-20)
        X, y, meta = load_kul(_root(args, "kul_aad"), [1] if args.quick else range(1, 17),
                              range(8, 20) if args.quick else None)
    except Exception as e:
        log_error(PHASE, f"KUL-AAD: could not load ({type(e).__name__}: {e})")
        return
    Xf = _bandpass(X.reshape(-1, X.shape[-1]), KUL_SF, 1.0, 32.0).reshape(X.shape).astype(np.float32)
    for mname in ("TS+LR", "CSP+LDA"):
        _safe(evaluate, PHASE, results, "KUL-AAD", "leave_one_run_out", mname, classical(mi_classical()[mname]),
              Xf, y, meta, args.seeds, needs_seed=False)
    _deep_models(results, "KUL-AAD", "leave_one_run_out", Xf, y, meta, args, KUL_SF, names=("EEGNet",), epoch_cap=100)


# ================================================================== Thinking Out Loud (inner speech)

TOL_URL = "https://s3.amazonaws.com/openneuro.org/ds003626/derivatives/sub-{s:02d}/ses-{e:02d}/sub-{s:02d}_ses-{e:02d}_{kind}"
TOL_WORDS = ["up", "down", "right", "left"]  # class codes 0-3 (authors' tutorial)


def load_tol(root, pairs, condition=1):
    """Processed epochs (256 Hz), 1.5-3.5 s after epoch start as in the authors' tutorial; condition 1 = inner speech."""
    Xs, ys, metas = [], [], []
    for s, e in pairs:
        fif = download(TOL_URL.format(s=s, e=e, kind="eeg-epo.fif"), os.path.join(root, f"sub-{s:02d}_ses-{e:02d}_eeg-epo.fif"))
        evf = download(TOL_URL.format(s=s, e=e, kind="events.dat"), os.path.join(root, f"sub-{s:02d}_ses-{e:02d}_events.dat"))
        ep = mne.read_epochs(fif, preload=True, verbose=False)
        ev = np.load(evf, allow_pickle=True)
        fs = ep.info["sfreq"]
        X = ep.get_data(copy=False)[:, :, int(1.5 * fs):int(3.5 * fs)] * 1e6
        keep = ev[:, 2] == condition
        Xs.append(X[keep].astype(np.float32))
        ys.append(np.array([TOL_WORDS[int(c)] for c in ev[keep, 1]]))
        metas.append(pd.DataFrame(dict(subject=str(s), session=str(e), run="0"), index=range(int(keep.sum()))))
    return np.concatenate(Xs), np.concatenate(ys), pd.concat(metas, ignore_index=True), fs


def run_tol(results, args):
    if not _want(args, "ThinkingOutLoud"):
        return
    print(f"\n[{PHASE}] Thinking Out Loud (inner speech, 4 words)")
    pairs = [(1, 1), (1, 3)] if args.quick else [(s, e) for s in range(1, 11) for e in (1, 2, 3)]
    try:
        X, y, meta, fs = load_tol(_root(args, "thinking_out_loud"), pairs)
    except Exception as e:
        log_error(PHASE, f"ThinkingOutLoud: could not load ({type(e).__name__}: {e})")
        return
    for protocol in ("cross_session", "cross_subject"):
        for mname in ("TS+LR", "MDM"):
            _safe(evaluate, PHASE, results, "ThinkingOutLoud", protocol, mname, classical(mi_classical()[mname]),
                  X, y, meta, args.seeds, needs_seed=False)
        _deep_models(results, "ThinkingOutLoud", protocol, X, y, meta, args, fs)


# ================================================================== Kara One (imagined speech)

KARA_URL = "http://www.cs.toronto.edu/~complingweb/data/karaOne/{p}.tar.bz2"
KARA_PARTICIPANTS = ["MM05", "MM08", "MM09", "MM10", "MM11", "MM12", "MM14", "MM15", "MM16", "MM18", "MM19",
                     "MM20", "MM21", "P02"]
KARA_SF, KARA_EPOCH_S = 250, 4.5


def fetch_kara(root, p):
    """Stream one participant's archive and keep only what is needed; returns the participant folder."""
    out = os.path.join(root, p)
    done = os.path.join(out, ".done")
    if os.path.exists(done):
        return out
    os.makedirs(out, exist_ok=True)
    req = urllib.request.Request(KARA_URL.format(p=p), headers=UA)
    with urllib.request.urlopen(req, timeout=300) as r, tarfile.open(fileobj=r, mode="r|bz2") as t:
        for m in t:
            base = os.path.basename(m.name)
            if m.isfile() and (base in ("epoch_inds.mat", "all_features_simple.mat", "labels.txt") or base.endswith(".cnt")):
                with open(os.path.join(out, "data.cnt" if base.endswith(".cnt") else base), "wb") as f:
                    f.write(t.extractfile(m).read())
    open(done, "w").close()
    return out


def load_kara(root, participants, with_raw):
    """Per trial: released EEG features of the imagined ('thinking') period (62 ch x 45 features) and, if with_raw,
    the first 4.5 s of the thinking period from the .cnt (62 EEG channels, 250 Hz)."""
    F, R, ys, metas = [], [], [], []
    for p in participants:
        d = fetch_kara(root, p)
        feats = sio.loadmat(os.path.join(d, "all_features_simple.mat"), squeeze_me=True, struct_as_record=False)["all_features"]
        prompts = [str(s).strip() for s in feats.prompts]
        F.append(np.stack([np.asarray(f, dtype=np.float32).ravel() for f in feats.eeg_features.thinking_feats]))
        if with_raw:
            inds = sio.loadmat(os.path.join(d, "epoch_inds.mat"), squeeze_me=True)["thinking_inds"]
            raw = mne.io.read_raw_cnt(os.path.join(d, "data.cnt"), preload=True, verbose=False)
            raw.pick([c for c in raw.ch_names if c.upper() not in ("M1", "M2", "EKG", "TRIGGER", "EMG", "VEO", "HEO")
                      and raw.get_channel_types([c])[0] == "eeg"])
            fs = raw.info["sfreq"]
            data = raw.get_data() * 1e6
            n = int(KARA_EPOCH_S * fs)
            R.append(_resample(np.stack([data[:, int(a):int(a) + n] for a, _ in (np.asarray(i, dtype=np.int64) for i in inds)]),
                               fs, KARA_SF))
        ys.append(np.array(prompts))
        metas.append(pd.DataFrame(dict(subject=p, session="0", run="0"), index=range(len(prompts))))
    return np.concatenate(F), (np.concatenate(R) if with_raw else None), np.concatenate(ys), pd.concat(metas, ignore_index=True)


def run_kara(results, args):
    if not _want(args, "KaraOne"):
        return
    if args.quick:
        print(f"\n[{PHASE}] Kara One skipped in quick mode (2.2 GB archive per participant)")
        return
    print(f"\n[{PHASE}] Kara One (11 imagined prompts)")
    try:
        F, R, y, meta = load_kara(_root(args, "karaone"), KARA_PARTICIPANTS, with_raw=True)
    except Exception as e:
        log_error(PHASE, f"KaraOne: could not load ({type(e).__name__}: {e})")
        return
    svm = make_pipeline(StandardScaler(), SVC(kernel="poly", degree=2))
    for protocol in ("cross_subject", "within_session:5"):
        _safe(evaluate, PHASE, results, "KaraOne", protocol, "Features+SVM", classical(svm), np.nan_to_num(F), y, meta,
              args.seeds, needs_seed=False)
        _deep_models(results, "KaraOne", protocol, R, y, meta, args, KARA_SF, names=("EEGNet",))


# ================================================================== WAY-EEG-GAL (grasp-and-lift)

WAY_COLLECTION = "https://api.figshare.com/v2/collections/988376/articles?page_size=50"
WAY_EVENTS = ["tHandStart", "tFirstDigitTouch", "tBothStartLoadPhase", "tLiftOff", "tReplace", "tBothReleased"]
WAY_SF, WAY_WIN_S, WAY_STEP_S, WAY_TOL_S = 100, 2.0, 0.1, 0.15


def way_urls():
    out = {}
    for a in _json(WAY_COLLECTION):
        n = int(re.search(r"Participant (\d+)", a["title"]).group(1))
        out[n] = _json(f"https://api.figshare.com/v2/articles/{a['id']}/files")[0]["download_url"]
    return out


def load_way(root, participants, series, quick):
    """Causal 2-s windows (EEG low-passed at 30 Hz, 100 Hz) every 0.1 s inside each lift; 6 binary labels,
    1 when the window end lies within +-150 ms of the event (as in the Kaggle labels)."""
    from emg_more import open_zip
    urls = way_urls()
    Xs, Ys, metas = [], [], []
    for p in participants:
        cache = os.path.join(root, f"P{p}_{'q' if quick else 'all'}.npz")
        if not os.path.exists(cache):
            z = open_zip(urls[p], os.path.join(root, f"P{p}.zip"), remote=quick)
            lifts = sio.loadmat(io.BytesIO(z.read(f"P{p}_AllLifts.mat")), squeeze_me=True, struct_as_record=False)["P"]
            cols, A = list(lifts.ColNames), lifts.AllLifts
            X, Y, run = [], [], []
            for s in series:
                ws = sio.loadmat(io.BytesIO(z.read(f"WS_P{p}_S{s}.mat")), squeeze_me=True, struct_as_record=False)["ws"]
                for k, win in enumerate(np.atleast_1d(ws.win)):
                    row = A[(A[:, cols.index("Run")] == s) & (A[:, cols.index("Lift")] == k + 1)]
                    if not len(row):
                        continue
                    ev = row[0, [cols.index(c) for c in WAY_EVENTS]]
                    eeg = mne.filter.filter_data(np.asarray(win.eeg, dtype=np.float64).T, 500, None, 30, verbose=False)
                    eeg = eeg[:, ::5].astype(np.float32)  # 100 Hz
                    w = int(WAY_WIN_S * WAY_SF)
                    for end in range(w, eeg.shape[1] + 1, int(WAY_STEP_S * WAY_SF)):
                        t = end / WAY_SF
                        X.append(eeg[:, end - w:end])
                        Y.append(np.abs(ev - t) <= WAY_TOL_S)
                        run.append(s)
            np.savez(cache, X=np.asarray(X, np.float32), Y=np.asarray(Y, np.float32), run=np.asarray(run))
        d = np.load(cache)
        Xs.append(d["X"]), Ys.append(d["Y"])
        metas.append(pd.DataFrame(dict(subject=str(p), session="0",
                                       run=np.where(d["run"] <= 7, "0train", "1test"))))
    return np.concatenate(Xs), np.concatenate(Ys), pd.concat(metas, ignore_index=True)


def run_way(results, args):
    if not _want(args, "WAY-EEG-GAL"):
        return
    print(f"\n[{PHASE}] WAY-EEG-GAL (grasp-and-lift events, series 1-7 -> 8-9)")
    try:
        X, Y, meta = load_way(_root(args, "way_eeg_gal"), [1] if args.quick else range(1, 13),
                              [1, 9] if args.quick else range(1, 10), args.quick)
    except Exception as e:
        log_error(PHASE, f"WAY-EEG-GAL: could not load ({type(e).__name__}: {e})")
        return
    lr = make_pipeline(_chunked(time_bins), StandardScaler(), OneVsRestClassifier(LogisticRegression(max_iter=1000)))
    _safe(evaluate, PHASE, results, "WAY-EEG-GAL", "standard", "Bins+LR", classical(lr), X, Y, meta, args.seeds,
          needs_seed=False, multilabel=True)
    _deep_models(results, "WAY-EEG-GAL", "standard", X, Y, meta, args, WAY_SF, names=("EEGNet",), epoch_cap=50,
                 multilabel=True)


# ================================================================== TUEV and TUAR (gated)

TUEV_CLASSES = {1: "spsw", 2: "gped", 3: "pled", 4: "eyem", 5: "artf", 6: "bckg"}
TUH_SF = 200


def _tuh_signals(edf):
    raw = mne.io.read_raw_edf(edf, preload=False, verbose=False)
    sig = _pick(raw, REF19, rename=_tuh_name)
    sig = _resample(sig[None], raw.info["sfreq"], TUH_SF)[0]
    return mne.filter.filter_data(sig.astype(np.float64), TUH_SF, 0.3, 75, verbose=False).astype(np.float32)


def _to_bipolar(X):
    i = {c: k for k, c in enumerate(REF19)}
    return np.stack([X[:, i[a]] - X[:, i[b]] for a, b in (p.split("-") for p in TUH_BIPOLAR16)], 1)


def weighted_f1(yt, yp):
    return {"weighted_f1": skm.f1_score(yt, yp, average="weighted")}


def run_tuev(results, args):
    path = _gated(args, "tuev", "TUEV")
    if not path or not _want(args, "TUEV"):
        return
    print(f"\n[{PHASE}] TUEV from {path}")
    try:
        edfs = sorted(glob.glob(os.path.join(path, "**", "*.edf"), recursive=True))
        if args.quick:
            edfs = [e for e in edfs if "/train/" in e][:3] + [e for e in edfs if "/eval/" in e][:3]
        X, y, meta = [], [], []
        half = int(2.5 * TUH_SF)
        for e in edfs:
            rec = np.atleast_2d(np.loadtxt(e[:-4] + ".rec", delimiter=","))
            sig = np.pad(_tuh_signals(e), ((0, 0), (half, half)))
            for _, start, stop, lab in rec[:, :4]:
                c = int((start + stop) / 2 * TUH_SF) + half
                X.append(sig[:, c - half:c + half])
                y.append(TUEV_CLASSES[int(lab)])
                meta.append(dict(subject=os.path.basename(e).split("_")[0], session="0",
                                 run="1test" if "/eval/" in e.replace("\\", "/") else "0train"))
        X, y, meta = np.stack(X).astype(np.float32), np.asarray(y), pd.DataFrame(meta).assign(subject="all")
    except Exception as e:
        log_error(PHASE, f"TUEV: could not load ({type(e).__name__}: {e})")
        return
    Xb = _to_bipolar(X)
    rf = make_pipeline(_chunked(partial(band_powers, sfreq=TUH_SF)), RandomForestClassifier(n_estimators=300, n_jobs=-1, random_state=0))
    _safe(evaluate, PHASE, results, "TUEV", "standard", "BandPower+RF", classical(rf), Xb, y, meta, args.seeds,
          needs_seed=False, fold_hook=weighted_f1)
    _deep_models(results, "TUEV", "standard", Xb, y, meta, args, TUH_SF, epoch_cap=50, fold_hook=weighted_f1)
    _foundation_models(results, "TUEV", "standard", Xb, y, meta, args, TUH_SF, TUH_BIPOLAR16, names=("CBraMod",),
                       fold_hook=weighted_f1)
    _foundation_models(results, "TUEV", "standard", X, y, meta, args, TUH_SF, REF19, names=("LaBraM", "EEGPT"),
                       fold_hook=weighted_f1)


TUAR_TYPES = ["eyem", "chew", "shiv", "musc", "elec"]


def run_tuar(results, args):
    path = _gated(args, "tuar", "TUAR")
    if not path or not _want(args, "TUAR"):
        return
    print(f"\n[{PHASE}] TUAR from {path}")
    try:
        edfs = sorted(glob.glob(os.path.join(path, "**", "*.edf"), recursive=True))[:6 if args.quick else None]
        X, Y, meta = [], [], []
        w = 5 * TUH_SF
        for e in edfs:
            ann = pd.read_csv(e[:-4] + ".csv", comment="#")
            sig = _tuh_signals(e)
            for k in range(sig.shape[1] // w):
                a, b = k * 5, (k + 1) * 5
                hit = ann[(ann.start_time < b) & (ann.stop_time > a)].label.astype(str)
                Y.append([any(t in l or (t == "elec" and l.startswith("el")) for l in hit) for t in TUAR_TYPES])
                X.append(sig[:, k * w:(k + 1) * w])
                meta.append(dict(subject=os.path.basename(e).split("_")[0], session="0", run="0"))
        X, Y, meta = np.stack(X).astype(np.float32), np.asarray(Y, np.float32), pd.DataFrame(meta)
    except Exception as e:
        log_error(PHASE, f"TUAR: could not load ({type(e).__name__}: {e})")
        return
    lr = make_pipeline(_chunked(partial(band_powers, sfreq=TUH_SF)), StandardScaler(),
                       OneVsRestClassifier(LogisticRegression(max_iter=1000)))
    _safe(evaluate, PHASE, results, "TUAR", "cross_subject", "BandPower+LR", classical(lr), X, Y, meta, args.seeds,
          needs_seed=False, multilabel=True)
    _deep_models(results, "TUAR", "cross_subject", X, Y, meta, args, TUH_SF, names=("EEGNet",), epoch_cap=50,
                 multilabel=True)


# ================================================================== SEED family (gated)

SEED_CHANNELS = ["FP1", "FPZ", "FP2", "AF3", "AF4", "F7", "F5", "F3", "F1", "FZ", "F2", "F4", "F6", "F8", "FT7",
                 "FC5", "FC3", "FC1", "FCZ", "FC2", "FC4", "FC6", "FT8", "T7", "C5", "C3", "C1", "CZ", "C2", "C4",
                 "C6", "T8", "TP7", "CP5", "CP3", "CP1", "CPZ", "CP2", "CP4", "CP6", "TP8", "P7", "P5", "P3", "P1",
                 "PZ", "P2", "P4", "P6", "P8", "PO7", "PO5", "PO3", "POZ", "PO4", "PO6", "PO8", "CB1", "O1", "OZ",
                 "O2", "CB2"]  # channel order of the SEED .mat files (as in torcheeg's SEED constants)
# SEED-IV session labels (0 neutral, 1 sad, 2 fear, 3 happy) from the dataset ReadMe (as in torcheeg's SEEDIVDataset)
SEED_IV_LABELS = [[1, 2, 3, 0, 2, 0, 0, 1, 0, 1, 2, 1, 1, 1, 2, 3, 2, 2, 3, 3, 0, 3, 0, 3],
                  [2, 1, 3, 0, 0, 2, 0, 2, 3, 3, 2, 3, 2, 0, 1, 1, 2, 1, 0, 3, 0, 1, 3, 1],
                  [1, 2, 2, 1, 3, 3, 3, 1, 1, 2, 1, 0, 2, 3, 3, 0, 2, 3, 0, 0, 2, 0, 1, 0]]
# SEED-V trial labels (0 disgust, 1 fear, 2 sad, 3 neutral, 4 happy) and trial start/end seconds per session,
# as in torcheeg's SEEDVDataset loader for the raw .cnt files
SEED_V_LABELS = [[4, 1, 3, 2, 0, 4, 1, 3, 2, 0, 4, 1, 3, 2, 0],
                 [2, 1, 3, 0, 4, 4, 0, 3, 2, 1, 3, 4, 1, 2, 0],
                 [2, 1, 3, 0, 4, 4, 0, 3, 2, 1, 3, 4, 1, 2, 0]]
SEED_V_TIMES = [([30, 132, 287, 555, 773, 982, 1271, 1628, 1730, 2025, 2227, 2435, 2667, 2932, 3204],
                 [102, 228, 524, 742, 920, 1240, 1568, 1697, 1994, 2166, 2401, 2607, 2901, 3172, 3359]),
                ([30, 299, 548, 646, 836, 1000, 1091, 1392, 1657, 1809, 1966, 2186, 2333, 2490, 2741],
                 [267, 488, 614, 773, 967, 1059, 1331, 1622, 1777, 1908, 2153, 2302, 2428, 2709, 2817]),
                ([30, 353, 478, 674, 825, 908, 1200, 1346, 1451, 1711, 2055, 2307, 2457, 2726, 2888],
                 [321, 418, 643, 764, 877, 1147, 1284, 1418, 1679, 1996, 2275, 2425, 2664, 2857, 3066])]
SEED_SF = 200


def _windows_1s(trial, sf=SEED_SF):
    k = trial.shape[1] // sf
    return trial[:, :k * sf].reshape(trial.shape[0], k, sf).transpose(1, 0, 2)


class _Writer:
    """Appends windows to a disk-backed .npy (memmap) so large sets never sit in RAM twice."""

    def __init__(self, path):
        self.path, self.parts, self.n = path, [], 0

    def add(self, x):
        p = f"{self.path}.part{len(self.parts)}.npy"
        np.save(p, x.astype(np.float32))
        self.parts.append(p)
        self.n += len(x)

    def close(self):
        first = np.load(self.parts[0], mmap_mode="r")
        out = np.lib.format.open_memmap(self.path, mode="w+", dtype=np.float32, shape=(self.n,) + first.shape[1:])
        i = 0
        for p in self.parts:
            a = np.load(p, mmap_mode="r")
            out[i:i + len(a)] = a
            i += len(a)
            os.remove(p)
        out.flush()
        return np.load(self.path, mmap_mode="r")


def load_seed(path, kind, quick, cache_dir):
    """SEED / SEED-IV preprocessed .mat (200 Hz) or SEED-V raw .cnt; 1-s windows; meta run = trial number."""
    cache = os.path.join(cache_dir, f"{kind}{'_quick' if quick else ''}")
    if os.path.exists(cache + ".npy") and os.path.exists(cache + ".csv"):
        meta = pd.read_csv(cache + ".csv", dtype=str)
        return np.load(cache + ".npy", mmap_mode="r"), meta.pop("label").to_numpy(), meta
    w, rows = _Writer(cache + ".npy"), []
    if kind == "seed":
        folder = (glob.glob(os.path.join(path, "**", "Preprocessed_EEG"), recursive=True) or [path])[0]
        seed_labels = sio.loadmat(os.path.join(folder, "label.mat"))["label"].ravel()
        files = sorted(f for f in glob.glob(os.path.join(folder, "*.mat")) if re.match(r"\d+_\d+\.mat", os.path.basename(f)))
        by_subj = {}
        for f in files:
            s, d = os.path.basename(f)[:-4].split("_")
            by_subj.setdefault(int(s), []).append((d, f))
        jobs = [(s, i + 1, f) for s, v in sorted(by_subj.items()) for i, (_, f) in enumerate(sorted(v))]
    elif kind == "seed_iv":
        jobs = []
        for sess in (1, 2, 3):
            for f in sorted(glob.glob(os.path.join(path, "**", str(sess), "*_*.mat"), recursive=True)):
                jobs.append((int(os.path.basename(f).split("_")[0]), sess, f))
    else:
        jobs = [(int(os.path.basename(f).split("_")[0]), int(os.path.basename(f).split("_")[1]), f)
                for f in sorted(glob.glob(os.path.join(path, "**", "*.cnt"), recursive=True))]
    if quick:
        subjects = sorted({j[0] for j in jobs})[:2]
        jobs = [j for j in jobs if j[0] in subjects and j[1] == 1]
    for s, sess, f in jobs:
        if kind == "seed_v":
            raw = mne.io.read_raw_cnt(f, preload=True, verbose=False)
            raw.drop_channels([c for c in ("M1", "M2", "VEO", "HEO") if c in raw.ch_names])
            raw.filter(0.3, 75, verbose=False).resample(SEED_SF, verbose=False)
            with open(cache + ".channels.json", "w") as fh:
                json.dump([c.upper() for c in raw.ch_names], fh)
            data = raw.get_data() * 1e6
            trials = [data[:, a * SEED_SF:b * SEED_SF] for a, b in zip(*SEED_V_TIMES[sess - 1])]
            labels = SEED_V_LABELS[sess - 1]
        else:
            m = sio.loadmat(f)
            keys = sorted((k for k in m if re.search(r"_eeg\d+$", k)), key=lambda k: int(re.search(r"(\d+)$", k).group(1)))
            trials = [m[k] for k in keys]
            labels = seed_labels if kind == "seed" else SEED_IV_LABELS[sess - 1]
        for t, (trial, lab) in enumerate(zip(trials, labels)):
            x = _windows_1s(np.asarray(trial, dtype=np.float32))
            if quick:
                x = x[:20]
            w.add(x)
            rows += [dict(subject=str(s), session=str(sess), trial=t + 1, label=str(lab))] * len(x)
    X = w.close()
    meta = pd.DataFrame(rows)
    meta.astype(str).to_csv(cache + ".csv", index=False)
    meta = pd.read_csv(cache + ".csv", dtype=str)
    return X, meta.pop("label").to_numpy(), meta


def de_svm():
    return make_pipeline(_chunked(partial(diff_entropy, sfreq=SEED_SF)), StandardScaler(), LinearSVC(C=1.0, max_iter=5000))


def run_seed(results, args):
    for key, name, n_train in (("seed", "SEED", 9), ("seed_iv", "SEED-IV", 16), ("seed_v", "SEED-V", None)):
        path = _gated(args, key, name)
        if not path or not _want(args, name):
            continue
        print(f"\n[{PHASE}] {name} from {path}")
        try:
            X, y, meta = load_seed(path, key, args.quick, _root(args, "seed_cache"))
        except Exception as e:
            log_error(PHASE, f"{name}: could not load ({type(e).__name__}: {e})")
            continue
        trial = meta.trial.astype(int).to_numpy()
        if key == "seed_v":  # CBraMod split: trials 1-5 train, 6-10 val (unused), 11-15 test, pooled over subjects
            dep = meta.assign(subject="all", session="0",
                              run=np.where(trial <= 5, "0train", np.where(trial <= 10, "val", "1test")))
        else:  # subject-dependent: first n_train trials of each session train, the rest test
            dep = meta.assign(run=np.where(trial <= n_train, "0train", "1test"))
        _safe(evaluate, PHASE, results, name, "standard", "DE+SVM", classical(de_svm()), X, y, dep, args.seeds,
              needs_seed=False, fold_hook=weighted_f1)
        _deep_models(results, name, "standard", X, y, dep, args, SEED_SF, names=("EEGNet",), epoch_cap=50,
                     fold_hook=weighted_f1)
        if key == "seed_v":
            chan_file = os.path.join(_root(args, "seed_cache"), f"seed_v{'_quick' if args.quick else ''}.channels.json")
            names = json.load(open(chan_file)) if os.path.exists(chan_file) else SEED_CHANNELS
            keep = [i for i, c in enumerate(names) if c not in ("CB1", "CB2")]
            Xk = np.asarray(X[:, keep]) if len(keep) < X.shape[1] else X
            _foundation_models(results, name, "standard", Xk, y, dep, args, SEED_SF, [names[i] for i in keep],
                               fold_hook=weighted_f1)
        else:  # subject-independent: leave one subject out, session 1 only
            s1 = np.flatnonzero(meta.session.values == "1")
            ind = meta.iloc[s1].reset_index(drop=True)
            _safe(evaluate, PHASE, results, name, "cross_subject", "DE+SVM", classical(de_svm()), X[s1], y[s1], ind,
                  args.seeds, needs_seed=False)


# ================================================================== DEAP and DREAMER (gated)

def load_deap(path, quick):
    import pickle
    files = sorted(glob.glob(os.path.join(path, "**", "s[0-9][0-9].dat"), recursive=True))[:2 if quick else None]
    X, lab, meta = [], [], []
    for f in files:
        with open(f, "rb") as fh:
            d = pickle.load(fh, encoding="latin1")
        eeg = d["data"][:, :32, 384:]  # drop the 3-s baseline; 128 Hz
        seg = eeg[:, :, :eeg.shape[2] // 512 * 512].reshape(40, 32, -1, 512).transpose(0, 2, 1, 3)  # 4-s segments
        for t in range(40):
            X.append(seg[t])
            lab += [d["labels"][t]] * seg.shape[1]
            meta += [dict(subject=os.path.basename(f)[1:3], trial=t)] * seg.shape[1]
    return np.concatenate(X).astype(np.float32), np.asarray(lab), pd.DataFrame(meta)


def load_dreamer(path, quick):
    f = glob.glob(os.path.join(path, "**", "DREAMER.mat"), recursive=True)[0]
    D = sio.loadmat(f, squeeze_me=True, struct_as_record=False)["DREAMER"]
    X, lab, meta = [], [], []
    for s, subj in enumerate(np.atleast_1d(D.Data)[:2 if quick else None]):
        for t, stim in enumerate(np.atleast_1d(subj.EEG.stimuli)):
            x = np.asarray(stim, dtype=np.float32).T  # (14, time) at 128 Hz
            k = x.shape[1] // 512
            X.append(x[:, :k * 512].reshape(14, k, 512).transpose(1, 0, 2))
            lab += [[subj.ScoreValence[t], subj.ScoreArousal[t], subj.ScoreDominance[t]]] * k
            meta += [dict(subject=str(s + 1), trial=t)] * k
    return np.concatenate(X), np.asarray(lab, dtype=float), pd.DataFrame(meta)


def _affect_classical():
    return {"BandPower+SVM": make_pipeline(_chunked(partial(band_powers, sfreq=128, bands=((4, 8), (8, 13), (13, 30), (30, 45)))),
                                           StandardScaler(), SVC(kernel="rbf")),
            "TS+LR": mi_classical()["TS+LR"]}


def run_affect(results, args):
    for key, name, loader, targets in (("deap", "DEAP", load_deap, {"valence": (0, 5), "arousal": (1, 5)}),
                                       ("dreamer", "DREAMER", load_dreamer, {"valence": (0, 3), "arousal": (1, 3), "dominance": (2, 3)})):
        path = _gated(args, key, name)
        if not path or not _want(args, name):
            continue
        print(f"\n[{PHASE}] {name} from {path}")
        try:
            X, lab, meta = loader(path, args.quick)
        except Exception as e:
            log_error(PHASE, f"{name}: could not load ({type(e).__name__}: {e})")
            continue
        loto = meta.assign(session="0", run=meta.trial.astype(str))[["subject", "session", "run"]]
        tenfold = meta.assign(session=(meta.trial % 10).astype(str), run="0")[["subject", "session", "run"]]
        for tname, (col, thr) in targets.items():
            dname = f"{name}-{tname}"
            y = np.where(lab[:, col] > thr, "high", "low")
            for mname, pipe in _affect_classical().items():
                _safe(evaluate, PHASE, results, dname, "leave_one_run_out", mname, classical(pipe), X, y, loto,
                      args.seeds, needs_seed=False, fold_hook=lambda yt, yp: {"f1_high": skm.f1_score(yt, yp, pos_label="high")})
            if key == "deap":  # trial-wise 10-fold (TSception protocol b), deep models
                _safe(evaluate, PHASE, results, dname, "cross_session", "BandPower+SVM",
                      classical(_affect_classical()["BandPower+SVM"]), X, y, tenfold, args.seeds, needs_seed=False)
                _deep_models(results, dname, "cross_session", X, y, tenfold, args, 128, names=("EEGNet", "DeepConvNet"),
                             epoch_cap=100)
            else:
                _deep_models(results, dname, "leave_one_run_out", X, y, loto, args, 128, names=("EEGNet",), epoch_cap=100)


# ================================================================== Kaggle sets (gated)

def load_errp(path, quick):
    """Training subjects only (test labels are not public): 0-1.25 s after each feedback onset, 56 EEG ch, 1-40 Hz."""
    labels = pd.read_csv(glob.glob(os.path.join(path, "**", "TrainLabels.csv"), recursive=True)[0]).set_index("IdFeedBack")
    files = sorted(glob.glob(os.path.join(path, "**", "train", "Data_S*_Sess*.csv"), recursive=True))
    if quick:
        subj = sorted({re.search(r"Data_(S\d+)_", f).group(1) for f in files})[:2]
        files = [f for f in files if re.search(r"Data_(S\d+)_", f).group(1) in subj and "Sess01" in f]
    X, y, meta = [], [], []
    for f in files:
        d = pd.read_csv(f)
        eeg = [c for c in d.columns if c not in ("Time", "EOG", "FeedBackEvent")]
        sig = mne.filter.filter_data(d[eeg].to_numpy(np.float64).T, 200, 1, 40, verbose=False)
        s, sess = re.search(r"Data_(S\d+)_(Sess\d+)", f).groups()
        for k, i in enumerate(np.flatnonzero(d.FeedBackEvent.to_numpy() == 1)):
            X.append(sig[:, i:i + 250])
            y.append(int(labels.loc[f"{s}_{sess}_FB{k + 1:03d}", "Prediction"]))
            meta.append(dict(subject=s, session=sess, run="0"))
    return np.stack(X).astype(np.float32), np.asarray(y), pd.DataFrame(meta)


HMS_CLASSES = ["seizure", "lpd", "gpd", "lrda", "grda", "other"]


def load_hms(path, quick):
    """One labelled sample per EEG id (its first label row): the central 10 s of the 50-s window, 19 EEG ch, 200 Hz."""
    root = os.path.dirname(glob.glob(os.path.join(path, "**", "train.csv"), recursive=True)[0])
    df = pd.read_csv(os.path.join(root, "train.csv")).sort_values(["eeg_id", "eeg_label_offset_seconds"])
    df = df.groupby("eeg_id").head(1)
    if quick:
        df = df[df.patient_id.isin(df.patient_id.unique()[:6])].head(60)
    X = []
    for eid, off in zip(df.eeg_id, df.eeg_label_offset_seconds):
        e = pd.read_parquet(os.path.join(root, "train_eegs", f"{eid}.parquet"))
        e = e.drop(columns=[c for c in e.columns if c.upper() == "EKG"])
        a = int((off + 20) * 200)
        X.append(np.nan_to_num(e.iloc[a:a + 2000].to_numpy(np.float32).T))
    votes = df[[f"{c}_vote" for c in HMS_CLASSES]].to_numpy(float)
    meta = pd.DataFrame(dict(subject=df.patient_id.astype(str).values, session="0", run="0"))
    return np.stack(X), votes / votes.sum(1, keepdims=True), meta


def kl_scores(est, X, y, meta):
    p = np.clip(np.asarray(est.predict_proba(X), dtype=float), 1e-15, 1)
    p = p / p.sum(1, keepdims=True)
    kl = np.sum(np.where(y > 0, y * np.log(np.clip(y, 1e-15, 1) / p), 0), 1).mean()
    return {"kl_divergence": kl, "accuracy_vs_consensus": np.mean(p.argmax(1) == y.argmax(1))}


class _ArgmaxLR(BaseEstimator):
    """Multinomial LR on band powers, trained on the consensus (argmax) label; predict_proba over all 6 classes."""

    def fit(self, X, Y):
        self.pipe_ = make_pipeline(_chunked(partial(band_powers, sfreq=200)), StandardScaler(),
                                   LogisticRegression(max_iter=2000)).fit(X, Y.argmax(1))
        return self

    def predict_proba(self, X):
        p = np.zeros((len(X), len(HMS_CLASSES)))
        p[:, self.pipe_.classes_] = self.pipe_.predict_proba(X)
        return p

    def predict(self, X):
        return self.predict_proba(X)


def run_kaggle(results, args):
    path = _gated(args, "kaggle_errp", "Kaggle ErrP (BCI Challenge @ NER 2015)")
    if path and _want(args, "KaggleErrP"):
        print(f"\n[{PHASE}] Kaggle ErrP from {path}")
        try:
            X, y, meta = load_errp(path, args.quick)
            pipe = make_pipeline(XdawnCovariances(nfilter=4, estimator="oas"), TangentSpace(),
                                 LogisticRegression(max_iter=2000))
            _safe(evaluate, PHASE, results, "KaggleErrP", "cross_subject", "XDAWNCov+TS+LR", classical(pipe), X, y,
                  meta, args.seeds, needs_seed=False)
            _deep_models(results, "KaggleErrP", "cross_subject", X, y, meta, args, 200, names=("EEGNet",), epoch_cap=100)
        except Exception as e:
            log_error(PHASE, f"KaggleErrP: could not load ({type(e).__name__}: {e})")
    path = _gated(args, "kaggle_hms", "Kaggle HMS")
    if path and _want(args, "KaggleHMS"):
        print(f"\n[{PHASE}] Kaggle HMS from {path}")
        try:
            X, Y, meta = load_hms(path, args.quick)
        except Exception as e:
            log_error(PHASE, f"KaggleHMS: could not load ({type(e).__name__}: {e})")
            return
        _safe(evaluate_custom, PHASE, results, "KaggleHMS", "cross_subject", "BandPower+LR", lambda s: _ArgmaxLR(),
              X, Y, meta, args.seeds, scorer=kl_scores, needs_seed=False)
        _reg_models(results, "KaggleHMS", "cross_subject", X, Y, meta, args, 200, kl_scores, names=("EEGNet",),
                    loss="kl", epoch_cap=50)


# ================================================================== entry point

def run(results, args):
    run_beta(results, args)
    run_bci3(results, args)
    run_chbmit(results, args)
    run_siena(results, args)
    run_bonn(results, args)
    if _want(args, "THINGS-EEG"):
        print(f"\n[{PHASE}] THINGS-EEG: not implemented (needs an image encoder for zero-shot identification)")
    run_eegeyenet(results, args)
    run_hbn(results, args)
    run_kul(results, args)
    run_tol(results, args)
    run_kara(results, args)
    run_way(results, args)
    run_tusz(results, args)
    run_tuev(results, args)
    run_tuar(results, args)
    run_seed(results, args)
    run_affect(results, args)
    run_kaggle(results, args)
