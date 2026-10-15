"""Intracortical spikes benchmarks (phase 13): NLB, FALCON, speech/handwriting BCIs, reaching, mouse Neuropixels.

Source of truth for datasets, protocols and published numbers: projects/spikes-lfp/DATASETS.md.

| Dataset (name in results) | How it is obtained | Protocol(s) | Models | Tested here |
|---|---|---|---|---|
| NLB MC_Maze, MC_Maze_Large/_Medium/_Small, MC_RTT, Area2_Bump, DMFC_RSG (`NLB-<name>`) | official `nlb_tools` package; train NWB file auto-downloaded from DANDI (000128, 000138-000140, 000129, 000127, 000130) | `nlb_val`: fit on the official `train` trials, score on the official `val` trials of the public train file with `nlb_tools.evaluation.evaluate` (co_bps, vel_r2, psth_r2, fp_bps, tp_corr); 5 ms bins | Smoothing (official baseline script: Gaussian smoothing of held-in spikes, log, L2-penalised Poisson GLM to held-out units; its per-dataset default kernel and penalty), GRU-Poisson (bidirectional GRU, Poisson loss, also predicts the 200 ms forward window) | yes: MC_Maze_Small, MC_RTT, DMFC_RSG in quick; MC_Maze (0.7 GB), Area2_Bump (1.8 GB), L, M skipped in quick unless named |
| FALCON H1, M1 (M1-A), M2, H2, B1 (`FALCON-<task>`) | official `falcon-challenge` package (`load_nwb` and the evaluator's metric functions); NWB auto-downloaded from DANDI (000954, 000941, 000953, 000950, 001046) | train on held-in calibration files; `heldin_minival` = held-in minival files; `heldout_calib_zs` = zero-shot on the public held-out calibration files (one score per session) | WienerFilter (ridge on 5 causal lags), GRU (causal) for H1/M1/M2/B1; GRU-CTC (causal, characters, greedy, no LM) for H2 | yes, quick (1 held-in session + its minival + 1 held-out session) for H1, M1, H2, B1, and M2 when named (M2 is skipped in quick otherwise: smallest calibration file is 1.5 GB); GRU-CTC also checked on 8 H2 sessions (150 epochs: minival WER 0.10) |
| Brain-to-Text '24 (`B2T24`) | `--path b2t24=FOLDER` (Dryad `competitionData.tar.gz`, needs a Dryad login) | `standard`: official `train` -> `test` partition (last block per day, labelled); the competition holdout is hidden | GRU-CTC on characters (area 6v tx1 + spikePow, block z-scored as in the official notebook), greedy, no LM | partial: synthetic files in the official .mat layout |
| Brain-to-Text '25 (`B2T25`) | `--path b2t25=FOLDER` (Dryad `t15_copyTask_neuralData.zip` -> `hdf5_data_final`, needs a Dryad login) | `standard`: official `data_train` -> `data_val` (the Kaggle test split is hidden) | GRU-CTC (characters, no LM) | partial: synthetic files in the official HDF5 layout |
| Willett 2021 handwriting (`Willett2021-Handwriting`) | `--path handwriting=FOLDER` (Dryad `handwritingBCIData.tar.gz`, needs a Dryad login) | `HeldOutTrials`, `HeldOutBlocks` (official partition files) | GRU-CTC (characters, no LM; official single-letter normalisation) | partial: synthetic files in the official layout |
| O'Doherty / Sabes reaching (`ODoherty-Sabes`) | auto-download per session from Zenodo 583331 (84 MB - 2 GB per .mat) | `contiguous_5fold`: per session, 5 contiguous time blocks, each held out once; cursor velocity from 50 ms threshold-crossing counts per channel | WienerFilter, KalmanFilter, GRU | yes, quick (smallest session) |
| Churchland maze (`Churchland-Maze`, DANDI 000070) | streamed from DANDI with HTTP range reads (only units, hand position and trials are read) | `trial_blocks_5fold`: per session, 5 contiguous blocks of successful trials; hand velocity from 20 ms counts, -250 to +450 ms around movement onset | WienerFilter, KalmanFilter, GRU | yes, quick (1 session, units capped at ~5M spikes) |
| Allen Visual Coding Neuropixels (`Allen-VC-DriftingGratings`) | streamed from DANDI 000021 (Allen terms of use apply in addition to CC BY 4.0) | `within_session:5`; task: drifting-grating orientation (8-way) from spike counts during each 2 s presentation; units passing the AllenSDK default QC | LR | yes, quick (1 session, 60 units) |
| IBL Brain-wide Map (`IBL-BWM-Choice`) | official `ONE-api` with the public OpenAlyx credentials | `within_session:5`; task: choice (left/right) from spike counts in the 100 ms before first movement, probe00 | LR | yes, quick (1 session) |
| Steinmetz 2019 (`Steinmetz2019-Choice`) | NWB copy on DANDI 000017, auto-download per session | `within_session:5`; task: choice (left/right/no-go) from counts 0-400 ms after stimulus onset | LR | yes, quick (smallest session) |
| CRCNS pvc-8 (`CRCNS-pvc-8`), pvc-11 (`CRCNS-pvc-11`) | `--path crcns_pvc-8=FOLDER`, `--path crcns_pvc-11=FOLDER` (CRCNS account) | `within_session:5`; pvc-8: grating identity from counts 50-156 ms after onset; pvc-11: grating identity from counts over the 1.28 s presentation | LR | partial: synthetic files in the documented layout |
| other CRCNS sets (`crcns_<name>`) | `--path crcns_<name>=FOLDER` | - | - | no: no loader; a message is printed |

Notes:
- No task here has a public test split with labels for its leaderboard: NLB test data and FALCON evaluation data
  are hidden, so we score on the public validation (NLB `val`, FALCON minival) and held-out calibration data.
  Published numbers in sota/spikes.csv come from the hidden test sets and are flagged.
- GPFA (NLB baseline) is not run: it needs `elephant`; the smoothing baseline is the cheaper official baseline.
- Brain-to-Text and handwriting: no language model, so WER is far above published LM numbers.
- nlb_tools 0.0.4 pins pandas<=1.3.4; it is installed with `--no-deps` and two pandas-3 fixes are applied at run
  time (copy before an in-place nan_to_num in `resample`, and sorting the time index after loading).
"""
import glob
import inspect
import io
import json
import os
import re
import textwrap
import time
from datetime import datetime, timezone
from pathlib import Path

import h5py
import numpy as np
import scipy.io
import torch
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler

from common import _safe, classical, download, evaluate, git_commit, log_error, set_seed
from ecg import HttpFile, wanted

PHASE = "phase13"
DANDI = "https://api.dandiarchive.org/api"
SEQ_EPOCHS = 50  # cap for GRU regressors and GRU-Poisson
CTC_EPOCHS = 100  # cap for character CTC decoders
IBL_SESSIONS = 20  # ponytail: first 20 BWM sessions in a full run; raise for the whole map (~480 sessions)
DEV = "cuda" if torch.cuda.is_available() else "cpu"


# ------------------------------------------------------------------ small helpers

def attempt(name, fn, *a):
    print(f"\n[{PHASE}] {name}")
    try:
        return fn(*a)
    except Exception as e:
        log_error(PHASE, f"{name}: could not load ({type(e).__name__}: {e})")


def gated(args, key, name, how):
    folder = args.paths.get(key)
    if not folder:
        print(f"\n[{PHASE}] {name}: skipped (pass --path {key}=FOLDER; {how})")
    return folder


def model_ok(args, name):
    return not args.models or name in args.models


def big_in_quick(args, name, why):
    """Large downloads are skipped in --quick unless the dataset is named explicitly."""
    if args.quick and name not in (args.datasets or []):
        print(f"\n[{PHASE}] {name}: skipped in --quick ({why}); name it in --datasets to run it")
        return True
    return False


def _n(x):
    if isinstance(x, dict):
        return len(next(iter(x.values())))
    return len(x)


def bench(phase, results, dataset, protocol, model, make, folds, scorer, seeds, needs_seed=True):
    """Train once per fold, score every test set of the fold; one row per (test set, metric).

    folds: [(fold, X_train, Y_train, [(protocol, test_name, X_test, Y_test), ...])]. `protocol` is only a label
    for error messages; each test set carries its own protocol, so one fit can serve two protocols.
    """
    protocols = getattr(folds, "protocols", None) or sorted({t[0] for f in folds for t in f[3]})
    for seed in (seeds if needs_seed else seeds[:1]):
        todo = [p for p in protocols if not results.is_done(dataset, p, model, seed)]
        if not todo:
            print(f"  = {dataset} | {protocol} | {model} | seed {seed}: done, skipping")
            continue
        rows, t_unit = [], time.time()
        for fold, Xtr, Ytr, tests in folds:
            set_seed(seed)
            est = make(seed)
            t0 = time.time()
            est.fit(Xtr, Ytr)
            train_s = round(time.time() - t0, 2)
            for prot, name, Xte, Yte in tests:
                if prot not in todo:
                    continue
                for metric, value in scorer(Yte, est.predict(Xte)).items():
                    rows.append(dict(phase=phase, dataset=dataset, protocol=prot, model=model, seed=seed, fold=name,
                                     metric=metric, value=float(value), n_train=_n(Xtr), n_test=_n(Xte),
                                     train_s=train_s, device=DEV, commit=git_commit(),
                                     time=datetime.now(timezone.utc).isoformat(timespec="seconds")))
        results.add(rows)
        for prot in todo:
            r = [x for x in rows if x["protocol"] == prot]
            if r:
                m = r[0]["metric"]
                print(f"  + {dataset} | {prot} | {model} | seed {seed}: {len({x['fold'] for x in r})} test sets, "
                      f"mean {m} {np.nanmean([x['value'] for x in r if x['metric'] == m]):.4f}, "
                      f"{time.time() - t_unit:.0f}s")


# ------------------------------------------------------------------ DANDI and spike utilities

def dandi_assets(ds, root):
    """All assets of a dandiset (path, asset_id, size), cached as JSON."""
    path = os.path.join(root, f"dandi_{ds}.json")
    if not os.path.exists(path):
        import urllib.request
        out, url = [], f"{DANDI}/dandisets/{ds}/versions/draft/assets/?page_size=1000"
        while url:
            with urllib.request.urlopen(url, timeout=120) as r:
                d = json.load(r)
            out += [dict(path=a["path"], asset_id=a["asset_id"], size=a["size"]) for a in d["results"]]
            url = d.get("next")
        os.makedirs(root, exist_ok=True)
        with open(path, "w") as f:
            json.dump(out, f)
    with open(path) as f:
        return json.load(f)


def dandi_url(asset):
    return f"{DANDI}/assets/{asset['asset_id']}/download/"


def dandi_get(root, ds, asset):
    return download(dandi_url(asset), os.path.join(root, ds, asset["path"]), quiet=True)


def remote_h5(asset):
    """Open a DANDI NWB file over HTTP range requests (reads only what is accessed)."""
    return h5py.File(io.BufferedReader(HttpFile(dandi_url(asset)), 1 << 22), "r")


def ragged(group, name, rows):
    """Rows of an NWB ragged column (e.g. units/spike_times), one array per row."""
    idx = group[name + "_index"][:]
    data = group[name]
    return [np.asarray(data[(idx[i - 1] if i else 0):idx[i]], dtype=float).ravel() for i in rows]


def window_counts(trains, starts, stops):
    """Spike counts per window and unit -> (n_windows, n_units); trains must be sorted."""
    return np.stack([np.searchsorted(t, stops) - np.searchsorted(t, starts) for t in trains], 1).astype(np.float32)


def bin_counts(trains, edges):
    return np.stack([np.histogram(t, edges)[0] for t in trains], 1).astype(np.float32)


def levenshtein(a, b):
    d = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        prev, d[0] = d[0], i
        for j, y in enumerate(b, 1):
            prev, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, prev + (x != y))
    return d[-1]


def text_scores(true, pred):
    """Aggregate CER and WER (total edits / total reference length), as in the official scripts."""
    ce = sum(levenshtein(t, p) for t, p in zip(true, pred))
    we = sum(levenshtein(t.split(), p.split()) for t, p in zip(true, pred))
    return {"cer": ce / max(1, sum(map(len, true))), "wer": we / max(1, sum(len(t.split()) for t in true))}


def vw_r2(Ys, Ps):
    """Variance-weighted R2 over all segments, ignoring rows where the target is NaN."""
    Y, P = np.concatenate(Ys), np.concatenate(Ps)
    ok = ~np.isnan(Y).any(1)
    return {"r2": r2_score(Y[ok], P[ok], multioutput="variance_weighted")}


# ------------------------------------------------------------------ sequence decoders (lists of T x C segments)

def lagged(x, lags):
    """Causal history: [x_t, x_{t-1}, ..., x_{t-lags+1}] (zeros before the segment start)."""
    return np.concatenate([np.vstack([np.zeros((k, x.shape[1]), x.dtype), x[:len(x) - k]]) for k in range(lags)], 1)


class Wiener:
    """Linear filter on `lags` causal bins: ridge regression with alpha = 1% of the mean feature energy.

    Normal equations are accumulated per segment, so memory stays at one segment's design matrix.
    """

    def __init__(self, lags=5, ridge=1e-2):
        self.lags, self.ridge = lags, ridge

    def fit(self, Xs, Ys):
        n, s, ss = 0, 0.0, 0.0
        for x in Xs:
            L = lagged(np.asarray(x, np.float64), self.lags)
            n, s, ss = n + len(L), s + L.sum(0), ss + (L ** 2).sum(0)
        self.mu_ = s / n
        self.sd_ = np.sqrt(np.maximum(ss / n - self.mu_ ** 2, 0)) + 1e-6
        XtX = XtY = 0.0
        for x, y in zip(Xs, Ys):
            ok = ~np.isnan(y).any(1)
            L = np.c_[(lagged(np.asarray(x, np.float64), self.lags)[ok] - self.mu_) / self.sd_, np.ones(ok.sum())]
            XtX, XtY = XtX + L.T @ L, XtY + L.T @ y[ok]
        reg = self.ridge * np.trace(XtX[:-1, :-1]) / max(1, XtX.shape[0] - 1) * np.eye(len(XtX))
        reg[-1, -1] = 0
        self.W_ = np.linalg.solve(XtX + reg, XtY)
        return self

    def predict(self, Xs):
        return [np.c_[(lagged(np.asarray(x, np.float64), self.lags) - self.mu_) / self.sd_, np.ones(len(x))] @ self.W_
                for x in Xs]


class Kalman:
    """Kalman filter decoder (Wu et al. 2006 style): kinematic state, linear-Gaussian observation of z-scored counts."""

    def fit(self, Xs, Ys):
        Z = np.concatenate(Xs).astype(np.float64)
        self.zm_, self.zs_ = Z.mean(0), Z.std(0) + 1e-6
        Y = np.concatenate(Ys)
        self.ym_ = np.nanmean(Y, 0)
        prev = np.concatenate([y[:-1] for y in Ys]) - self.ym_
        nxt = np.concatenate([y[1:] for y in Ys]) - self.ym_
        ok = ~(np.isnan(prev).any(1) | np.isnan(nxt).any(1))
        self.A_ = np.linalg.lstsq(prev[ok], nxt[ok], rcond=None)[0]
        self.W_ = np.cov((nxt[ok] - prev[ok] @ self.A_).T).reshape(len(self.ym_), -1)
        Yc, Zc = Y - self.ym_, (Z - self.zm_) / self.zs_
        ok = ~np.isnan(Yc).any(1)
        self.H_ = np.linalg.lstsq(Yc[ok], Zc[ok], rcond=None)[0]
        self.Q_ = np.cov((Zc[ok] - Yc[ok] @ self.H_).T) + 1e-3 * np.eye(Z.shape[1])
        return self

    def predict(self, Xs):
        out, A, H, W, Q = [], self.A_, self.H_, self.W_, self.Q_
        for x in Xs:
            z = (np.asarray(x, np.float64) - self.zm_) / self.zs_
            s, P, pred = np.zeros(len(self.ym_)), W.copy(), np.empty((len(z), len(self.ym_)))
            for t in range(len(z)):
                s, P = s @ A, A.T @ P @ A + W
                K = np.linalg.solve(H.T @ P @ H + Q, H.T @ P).T  # (d x C)
                s = s + (z[t] - s @ H) @ K.T
                P = P - K @ H.T @ P
                pred[t] = s
            out.append(pred + self.ym_)
        return out


class _GRUNet(torch.nn.Module):
    def __init__(self, n_in, n_out, hidden=128, layers=1, bidirectional=False):
        super().__init__()
        self.inp = torch.nn.Linear(n_in, hidden)
        self.gru = torch.nn.GRU(hidden, hidden, layers, batch_first=True, bidirectional=bidirectional)
        self.out = torch.nn.Linear(hidden * (2 if bidirectional else 1), n_out)

    def forward(self, x):
        return self.out(self.gru(torch.relu(self.inp(x)))[0])


class GRUReg:
    """Causal GRU regressor trained on random windows of the training segments (MSE on standardised targets,
    NaN targets masked). Fixed epochs, last epoch used."""

    def __init__(self, epochs=SEQ_EPOCHS, win=100, batch=32, lr=1e-3, hidden=128):
        self.epochs, self.win, self.batch, self.lr, self.hidden = epochs, win, batch, lr, hidden

    def _x(self, x):
        return torch.as_tensor((np.sqrt(np.asarray(x, np.float32)) - self.xm_) / self.xs_)

    def fit(self, Xs, Ys):
        Xc = np.sqrt(np.concatenate(Xs).astype(np.float32))
        self.xm_, self.xs_ = Xc.mean(0), Xc.std(0) + 1e-6
        Yc = np.concatenate(Ys)
        self.ym_, self.ys_ = np.nanmean(Yc, 0), np.nanstd(Yc, 0) + 1e-6
        win = min(self.win, min(len(x) for x in Xs))
        segs = [(self._x(x), torch.as_tensor(((y - self.ym_) / self.ys_).astype(np.float32))) for x, y in zip(Xs, Ys)]
        starts = [(i, s) for i, (x, _) in enumerate(segs) for s in range(0, len(x) - win + 1, max(1, win // 2))]
        self.net_ = _GRUNet(Xc.shape[1], Yc.shape[1], self.hidden).to(DEV)
        opt = torch.optim.AdamW(self.net_.parameters(), lr=self.lr, weight_decay=1e-4)
        sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=max(1, self.epochs))
        for _ in range(self.epochs):
            for b in np.array_split(np.random.permutation(len(starts)), max(1, len(starts) // self.batch)):
                xb = torch.stack([segs[starts[k][0]][0][starts[k][1]:starts[k][1] + win] for k in b]).to(DEV)
                yb = torch.stack([segs[starts[k][0]][1][starts[k][1]:starts[k][1] + win] for k in b]).to(DEV)
                ok = ~torch.isnan(yb)
                loss = ((self.net_(xb) - torch.nan_to_num(yb)) ** 2)[ok].mean()
                opt.zero_grad(set_to_none=True)
                loss.backward()
                opt.step()
            sched.step()
        return self

    @torch.no_grad()
    def predict(self, Xs):
        self.net_.eval()
        return [self.net_(self._x(x)[None].to(DEV))[0].cpu().numpy() * self.ys_ + self.ym_ for x in Xs]


class _CTCNet(torch.nn.Module):
    def __init__(self, n_in, n_out, hidden=256, stride=2):
        super().__init__()
        self.conv = torch.nn.Conv1d(n_in, hidden, kernel_size=2 * stride, stride=stride)
        self.gru = torch.nn.GRU(hidden, hidden, 2, batch_first=True, dropout=0.2)
        self.out = torch.nn.Linear(hidden, n_out)

    def forward(self, x):  # x: batch x time x channels (causal: no future bins)
        h = torch.relu(self.conv(x.transpose(1, 2))).transpose(1, 2)
        return self.out(self.gru(h)[0])


class CTCDecoder:
    """Causal conv + 2-layer GRU emitting characters with CTC; greedy decoding, no language model."""

    def __init__(self, epochs=CTC_EPOCHS, stride=2, batch=16, lr=3e-3, hidden=256):
        self.epochs, self.stride, self.batch, self.lr, self.hidden = epochs, stride, batch, lr, hidden

    def _x(self, x):
        return torch.as_tensor(((np.asarray(x, np.float32) - self.xm_) / self.xs_))

    def _pad(self, xs):
        n = max(max(len(x) for x in xs), 2 * self.stride)
        return torch.stack([torch.nn.functional.pad(x, (0, 0, 0, n - len(x))) for x in xs])

    def _out_len(self, n):
        return max(1, (n - 2 * self.stride) // self.stride + 1)

    def fit(self, Xs, texts):
        Xc = np.concatenate(Xs).astype(np.float32)
        self.xm_, self.xs_ = Xc.mean(0), Xc.std(0) + 1e-6
        self.vocab_ = sorted({c for t in texts for c in t})
        ids = {c: i + 1 for i, c in enumerate(self.vocab_)}
        data = [(self._x(x), torch.tensor([ids[c] for c in t])) for x, t in zip(Xs, texts) if len(t)]
        self.net_ = _CTCNet(Xc.shape[1], len(self.vocab_) + 1, self.hidden, self.stride).to(DEV)
        opt = torch.optim.AdamW(self.net_.parameters(), lr=self.lr, weight_decay=1e-5)
        sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=max(1, self.epochs))
        ctc = torch.nn.CTCLoss(blank=0, zero_infinity=True)
        self.net_.train()
        for _ in range(self.epochs):
            for b in np.array_split(np.random.permutation(len(data)), max(1, len(data) // self.batch)):
                xb = self._pad([data[k][0] for k in b]).to(DEV)
                logp = torch.log_softmax(self.net_(xb), -1).transpose(0, 1)
                in_len = torch.tensor([min(self._out_len(len(data[k][0])), logp.shape[0]) for k in b])
                loss = ctc(logp, torch.cat([data[k][1] for k in b]).to(DEV), in_len,
                           torch.tensor([len(data[k][1]) for k in b]))
                opt.zero_grad(set_to_none=True)
                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.net_.parameters(), 1.0)
                opt.step()
            sched.step()
        return self

    @torch.no_grad()
    def predict(self, Xs):
        self.net_.eval()
        out = []
        for x in Xs:
            xt = self._x(x)
            best = self.net_(self._pad([xt]).to(DEV)).argmax(-1)[0, :self._out_len(len(xt))].cpu().numpy()
            keep = [k for i, k in enumerate(best) if k and (i == 0 or k != best[i - 1])]
            out.append("".join(self.vocab_[k - 1] for k in keep))
        return out


def regression_models(args, kalman=True, lags=5):
    models = {"WienerFilter": lambda s: Wiener(lags)}
    if kalman:
        models["KalmanFilter"] = lambda s: Kalman()
    models["GRU"] = lambda s: GRUReg(epochs=min(args.epochs, SEQ_EPOCHS))
    return {k: v for k, v in models.items() if model_ok(args, k)}


def block_folds(segs, Ys, blocks, protocol, prefix):
    """Leave-one-block-out folds over segments (blocks are contiguous in time)."""
    folds = []
    for b in sorted(set(blocks)):
        tr = [i for i, k in enumerate(blocks) if k != b]
        te = [i for i, k in enumerate(blocks) if k == b]
        folds.append((f"{prefix}/b{b}", [segs[i] for i in tr], [Ys[i] for i in tr],
                      [(protocol, f"{prefix}/b{b}", [segs[i] for i in te], [Ys[i] for i in te])]))
    return folds


def cached_segments(path, fn, *a):
    """(segments, targets, blocks) of one session, computed once and kept as .npz."""
    if not os.path.exists(path):
        segs, Ys, blocks = fn(*a)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        np.savez(path, X=np.concatenate(segs), Y=np.concatenate(Ys), lens=[len(x) for x in segs], blocks=blocks)
    d = np.load(path)
    cut = np.cumsum(d["lens"])[:-1]
    return np.split(d["X"], cut), np.split(d["Y"], cut), list(d["blocks"])


class SessionFolds:
    """Re-iterable block folds over many sessions, holding one session in memory at a time.

    sessions: [(name, loader)] where loader() -> (segments, targets, blocks); failures are logged and skipped.
    """

    def __init__(self, dataset, protocol, sessions):
        self.dataset, self.protocols, self.sessions = dataset, [protocol], sessions

    def __iter__(self):
        for name, load in self.sessions:
            try:
                data = load()
            except Exception as e:
                log_error(PHASE, f"{self.dataset} {name}: could not load ({type(e).__name__}: {e})")
                continue
            yield from block_folds(*data, self.protocols[0], name)


def run_regression(results, args, dataset, protocol, folds, kalman=True, lags=5, scorer=vw_r2):
    for name, make in regression_models(args, kalman, lags).items():
        _safe(bench, PHASE, results, dataset, protocol, name, make, folds, scorer, args.seeds,
              needs_seed=name == "GRU")


# ------------------------------------------------------------------ NLB

NLB = {"NLB-MC_Maze": ("000128", "mc_maze"), "NLB-MC_Maze_Large": ("000138", "mc_maze_large"),
       "NLB-MC_Maze_Medium": ("000139", "mc_maze_medium"), "NLB-MC_Maze_Small": ("000140", "mc_maze_small"),
       "NLB-MC_RTT": ("000129", "mc_rtt"), "NLB-Area2_Bump": ("000127", "area2_bump"),
       "NLB-DMFC_RSG": ("000130", "dmfc_rsg")}
NLB_QUICK = {"NLB-MC_Maze_Small", "NLB-MC_RTT", "NLB-DMFC_RSG"}
NLB_METRICS = {"co-bps": "co_bps", "vel R2": "vel_r2", "psth R2": "psth_r2", "fp-bps": "fp_bps", "tp corr": "tp_corr"}
_NLB_PATCHED = False


def nlb_compat():
    """nlb_tools 0.0.4 was written for pandas<=1.3: copy before an in-place nan_to_num (read-only views
    under copy-on-write). The unsorted time index after loading is fixed in nlb_load."""
    global _NLB_PATCHED
    if _NLB_PATCHED:
        return
    import nlb_tools.nwb_interface as ni
    src = textwrap.dedent(inspect.getsource(ni.NWBDataset.resample))
    ns = {}
    exec(src.replace(".to_numpy()", ".to_numpy(copy=True)"), vars(ni), ns)
    ni.NWBDataset.resample = ns["resample"]
    _NLB_PATCHED = True


def nlb_load(root, ds, name):
    from nlb_tools.make_tensors import make_eval_input_tensors, make_eval_target_tensors, make_train_input_tensors
    from nlb_tools.nwb_interface import NWBDataset
    nlb_compat()
    asset = next(a for a in dandi_assets(ds, root) if "desc-train" in a["path"])
    d = NWBDataset(dandi_get(root, ds, asset))
    d.data = d.data.sort_index()  # pandas>=2 concat no longer sorts the union of time indexes
    d.resample(5)
    tr = make_train_input_tensors(d, name, trial_split="train", save_file=False, include_forward_pred=True)
    ev = make_eval_input_tensors(d, name, trial_split="val", save_file=False)
    tg = make_eval_target_tensors(d, name, train_trial_split="train", eval_trial_split="val", include_psth=True,
                                  save_file=False)
    return {k: np.nan_to_num(np.asarray(v, np.float32)) for k, v in tr.items()}, \
        {k: np.nan_to_num(np.asarray(v, np.float32)) for k, v in ev.items()}, tg


# official per-dataset defaults of nlb_tools/examples/baselines/smoothing/run_smoothing.py: [kern_sd ms, alpha]
SMOOTH_DEFAULTS = {"mc_maze": (50, 0.01), "mc_rtt": (30, 0.1), "area2_bump": (30, 0.01), "dmfc_rsg": (60, 0.001),
                   "mc_maze_large": (40, 0.1), "mc_maze_medium": (60, 0.1), "mc_maze_small": (60, 0.1)}


class NLBSmoothing:
    """Official NLB smoothing baseline (run_smoothing.py): Gaussian-smoothed held-in spikes, log(x + 1e-4),
    Poisson GLM (L2 alpha) to each held-out unit; the script's default kernel and alpha per dataset."""

    def __init__(self, name):
        self.name = name
        self.sd, self.alpha = SMOOTH_DEFAULTS[name]

    def _sm(self, a):
        from scipy.signal import windows
        w = windows.gaussian(int(6 * self.sd / 5), int(self.sd / 5), sym=True)
        w /= w.sum()
        return np.apply_along_axis(lambda x: np.convolve(x, w, "same"), 1, a.astype(np.float64))

    def fit(self, tr, _):
        from sklearn.linear_model import PoissonRegressor
        self.tr_in_ = self._sm(tr["train_spikes_heldin"])
        X = np.log(self.tr_in_.reshape(-1, self.tr_in_.shape[-1]) + 1e-4)
        Y = tr["train_spikes_heldout"].reshape(-1, tr["train_spikes_heldout"].shape[-1])
        # same objective as the official lbfgs fit; newton-cholesky converges faster
        self.glms_ = [PoissonRegressor(alpha=self.alpha, solver="newton-cholesky", max_iter=500).fit(X, Y[:, j])
                      for j in range(Y.shape[1])]
        return self

    def _heldout(self, sm):
        X = np.log(sm.reshape(-1, sm.shape[-1]) + 1e-4)
        return np.clip(np.stack([g.predict(X) for g in self.glms_], -1), 1e-9, 1e20).reshape(*sm.shape[:2], -1)

    def predict(self, ev):
        ev_in = self._sm(ev["eval_spikes_heldin"])
        return {self.name: dict(train_rates_heldin=self.tr_in_, train_rates_heldout=self._heldout(self.tr_in_),
                                eval_rates_heldin=ev_in, eval_rates_heldout=self._heldout(ev_in))}


class NLBGRU:
    """Bidirectional GRU from held-in spikes (forward window zeroed, plus an 'observed' flag) to log-rates of all
    held-in and held-out units over the trial and the 200 ms forward window; Poisson loss, fixed epochs."""

    def __init__(self, name, epochs, batch=32, lr=2e-3, hidden=128):
        self.name, self.epochs, self.batch, self.lr, self.hidden = name, epochs, batch, lr, hidden

    def _inp(self, heldin, n_fwd):
        n, T, C = heldin.shape
        x = np.zeros((n, T + n_fwd, C + 1), np.float32)
        x[:, :T, :C] = np.sqrt(heldin) - self.mu_
        x[:, :T, C] = 1
        return torch.as_tensor(x)

    def fit(self, tr, _):
        hi, ho = tr["train_spikes_heldin"], tr["train_spikes_heldout"]
        self.T_, self.F_, self.Ci_ = hi.shape[1], tr["train_spikes_heldin_forward"].shape[1], hi.shape[2]
        self.mu_ = np.sqrt(hi).mean((0, 1))
        X = self._inp(hi, self.F_)
        Y = torch.as_tensor(np.concatenate([np.concatenate([hi, ho], 2), np.concatenate(
            [tr["train_spikes_heldin_forward"], tr["train_spikes_heldout_forward"]], 2)], 1))
        self.net_ = _GRUNet(X.shape[2], Y.shape[2], self.hidden, bidirectional=True).to(DEV)
        with torch.no_grad():  # start at each unit's mean rate
            self.net_.out.bias.copy_(torch.log(Y.float().mean((0, 1)) + 1e-3))
        opt = torch.optim.AdamW(self.net_.parameters(), lr=self.lr, weight_decay=1e-4)
        sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=max(1, self.epochs))
        loss_fn = torch.nn.PoissonNLLLoss(log_input=True)
        self.net_.train()
        for _ in range(self.epochs):
            for b in np.array_split(np.random.permutation(len(X)), max(1, len(X) // self.batch)):
                xb = X[b].clone()
                xb[..., :-1] = torch.nn.functional.dropout(xb[..., :-1], 0.3)  # input dropout regulariser
                loss = loss_fn(self.net_(xb.to(DEV)), Y[b].to(DEV))
                opt.zero_grad(set_to_none=True)
                loss.backward()
                opt.step()
            sched.step()
        self.train_rates_ = self._rates(hi)
        return self

    @torch.no_grad()
    def _rates(self, heldin):
        self.net_.eval()
        X = self._inp(heldin, self.F_)
        return torch.cat([torch.exp(self.net_(X[i:i + 256].to(DEV))).cpu() for i in range(0, len(X), 256)]).numpy()

    def predict(self, ev):
        r, tr, T, C = self._rates(ev["eval_spikes_heldin"]), self.train_rates_, self.T_, self.Ci_
        return {self.name: dict(train_rates_heldin=tr[:, :T, :C], train_rates_heldout=tr[:, :T, C:],
                                eval_rates_heldin=r[:, :T, :C], eval_rates_heldout=r[:, :T, C:],
                                eval_rates_heldin_forward=r[:, T:, :C], eval_rates_heldout_forward=r[:, T:, C:])}


def nlb_scorer(target, submission):
    from nlb_tools.evaluation import evaluate as nlb_evaluate
    out = {}
    for d in nlb_evaluate(target, submission):
        for k, v in next(iter(d.values())).items():
            key = NLB_METRICS.get(k.split("] ")[-1])
            if key and v is not None and np.isfinite(v):
                out[key] = v
    return out


def run_nlb(results, args, root):
    for dname, (ds, name) in NLB.items():
        if not wanted(args, dname, "NLB") or (dname not in NLB_QUICK and big_in_quick(args, dname, "large file")):
            continue
        data = attempt(dname, nlb_load, root, ds, name)
        if data is None:
            continue
        tr, ev, tg = data
        folds = [("val", tr, None, [("nlb_val", "val", ev, tg)])]
        if model_ok(args, "Smoothing"):
            _safe(bench, PHASE, results, dname, "nlb_val", "Smoothing", lambda s: NLBSmoothing(name), folds,
                  nlb_scorer, args.seeds, needs_seed=False)
        if model_ok(args, "GRU-Poisson"):
            _safe(bench, PHASE, results, dname, "nlb_val", "GRU-Poisson",
                  lambda s: NLBGRU(name, min(args.epochs, SEQ_EPOCHS * 2)), folds, nlb_scorer, args.seeds)


# ------------------------------------------------------------------ FALCON

FALCON = {"FALCON-H1": ("h1", "000954"), "FALCON-M1": ("m1", "000941"), "FALCON-M2": ("m2", "000953"),
          "FALCON-H2": ("h2", "000950"), "FALCON-B1": ("b1", "001046")}


def _ses(path):
    return Path(path).stem.split("_ses-")[1].replace("_behavior+ecephys", "")


def falcon_files(root, ds, quick):
    assets = dandi_assets(ds, root)
    pick = lambda kind: sorted((a for a in assets if f"-{kind}" in a["path"]), key=lambda a: a["path"])
    calib, minival, heldout = pick("held-in-calib"), pick("held-in-minival"), pick("held-out-calib")
    if quick:  # one held-in session (smallest calibration file that has a minival file) and one held-out session
        have = {_ses(a["path"]) for a in minival}
        calib = [min((a for a in calib if _ses(a["path"]) in have), key=lambda a: a["size"])]
        minival = [a for a in minival if _ses(a["path"]) == _ses(calib[0]["path"])]
        heldout = [min(heldout, key=lambda a: a["size"])]
    get = lambda lst: [dandi_get(root, ds, a) for a in lst]
    return get(calib), get(minival), get(heldout)


def falcon_group(task, path):
    """Session key as in the official evaluator (several files can belong to one session)."""
    from falcon_challenge.config import FalconConfig, FalconTask
    from falcon_challenge.evaluator import reduce_key
    return reduce_key(FalconConfig(task=FalconTask[task]).hash_dataset(Path(path).stem))


def falcon_load(task, path):
    """-> list of (X, Y) segments for one file. Y is NaN outside the evaluation mask (regression tasks),
    the cue string (H2), or (spectrogram, mask) per trial (B1)."""
    from falcon_challenge.config import FalconTask
    from falcon_challenge.dataloaders import load_nwb
    X, Y, change, mask = load_nwb(path, dataset=FalconTask[task])
    if task in ("h1", "m1", "m2"):
        Y = np.asarray(Y, np.float64).copy()
        Y[~np.asarray(mask, bool)] = np.nan
        return [(np.asarray(X, np.float32), Y)]
    if task == "h2":
        ends = np.flatnonzero(change) + 1
        trials = [X[a:b] for a, b in zip(np.r_[0, ends[:-1]], ends)]
        cues = ["".join(chr(c) for c in t if c) for t in Y]
        n = min(len(trials), len(cues))
        return [(np.asarray(trials[i], np.float32), cues[i]) for i in range(n)]
    # b1: 30 kHz threshold crossings -> counts in the spectrogram frames of each trial
    n = int(np.sum(change))
    frames, per = len(Y) // n, len(X) // n
    spf = per // frames
    C = np.asarray(X[:n * per], np.float32).reshape(n, per, -1)[:, :frames * spf]
    C = C.reshape(n, frames, spf, -1).sum(2)
    return [(C[i], (Y[i * frames:(i + 1) * frames], mask[i * frames:(i + 1) * frames])) for i in range(n)]


def falcon_scorer(task):
    from falcon_challenge.evaluator import FalconEvaluator as E
    if task in ("h1", "m1", "m2"):
        def score(Ys, Ps):
            Y, P = np.concatenate(Ys), np.concatenate(Ps)
            m = ~np.isnan(Y).any(1)
            return {"r2": E.compute_metrics_regression(P, Y[m], m, {"s": [len(m)]})["R2 Mean"]}
    elif task == "h2":
        def score(Ys, Ps):
            tg = [np.array([ord(c) for c in y], dtype=np.int32) for y in Ys]
            r = E.compute_metrics_edit_distance([[list(Ps)]], [[tg]], None)
            return {"wer": r["WER"], "cer": r["CER"]}
    else:
        def score(Ys, Ps):
            S = np.concatenate([y[0] for y in Ys])[:, None]
            M = np.concatenate([y[1] for y in Ys]).astype(bool)[:, None]
            return {"mse": E.compute_metrics_spectrogram_distance([np.concatenate(Ps)[:, None]], [S], [M])["MSE Mean"]}
    return score


class SpecTargets:
    """Adapter for B1: regress the spectrogram part of (spectrogram, mask) targets."""

    def __init__(self, est):
        self.est = est

    def fit(self, Xs, Ys):
        self.est.fit(Xs, [np.asarray(y[0], np.float64) for y in Ys])
        return self

    def predict(self, Xs):
        return self.est.predict(Xs)


def run_falcon(results, args, root):
    for dname, (task, ds) in FALCON.items():
        if not wanted(args, dname, "FALCON"):
            continue
        if task == "m2" and big_in_quick(args, dname, "smallest calibration file is 1.5 GB"):
            continue

        def load():
            calib, minival, heldout = falcon_files(root, ds, args.quick)
            train = [s for p in calib for s in falcon_load(task, p)]
            tests = []
            for prot, files in (("heldin_minival", minival), ("heldout_calib_zs", heldout)):
                groups = {}
                for p in files:
                    groups.setdefault(falcon_group(task, p), []).extend(falcon_load(task, p))
                tests += [(prot, g, [x for x, _ in segs], [y for _, y in segs]) for g, segs in sorted(groups.items())]
            return train, tests
        data = attempt(dname, load)
        if data is None:
            continue
        train, tests = data
        folds = [("calib", [x for x, _ in train], [y for _, y in train], tests)]
        score = falcon_scorer(task)
        if task == "h2":
            if model_ok(args, "GRU-CTC"):
                _safe(bench, PHASE, results, dname, "heldin_minival+heldout_calib_zs", "GRU-CTC",
                      lambda s: CTCDecoder(min(args.epochs, CTC_EPOCHS)), folds, score, args.seeds)
            continue
        for name, make in regression_models(args, kalman=False).items():
            mk = (lambda s, make=make: SpecTargets(make(s))) if task == "b1" else make
            _safe(bench, PHASE, results, dname, "heldin_minival+heldout_calib_zs", name, mk, folds, score,
                  args.seeds, needs_seed=name == "GRU")


# ------------------------------------------------------------------ Brain-to-Text and handwriting (gated)

def b2t_text(s):
    """Text normalisation of the official B2T scripts (remove_punctuation)."""
    s = re.sub(r"[^a-zA-Z\- ']", "", s)
    s = s.replace("- ", " ").replace("--", "").replace(" '", "'").lower()
    return " ".join(w for w in s.split() if w)


def b2t24_split(path):
    """One competitionData .mat: area 6v tx1 + spikePow (first 128 columns each), block-wise z-scored."""
    d = scipy.io.loadmat(path)
    X = [np.concatenate([d["tx1"][0, i][:, :128], d["spikePow"][0, i][:, :128]], 1).astype(np.float32)
         for i in range(d["sentenceText"].shape[0])]
    blocks = np.squeeze(d["blockIdx"])
    for b in np.unique(blocks):
        idx = np.flatnonzero(blocks == b)
        f = np.concatenate([X[i] for i in idx])
        m, s = f.mean(0), f.std(0) + 1e-8
        for i in idx:
            X[i] = (X[i] - m) / s
    return X, [b2t_text(str(t).strip()) for t in d["sentenceText"]]


def load_b2t24(folder, quick):
    files = sorted(glob.glob(os.path.join(folder, "**", "train", "t12.*.mat"), recursive=True))
    if not files:
        raise FileNotFoundError("no train/t12.*.mat under the b2t24 folder")
    Xtr, Ttr, tests = [], [], []
    for f in files[:1] if quick else files:
        x, t = b2t24_split(f)
        Xtr += x
        Ttr += t
        test = os.path.join(os.path.dirname(os.path.dirname(f)), "test", os.path.basename(f))
        if os.path.exists(test):
            tests.append(("standard", Path(f).stem, *b2t24_split(test)))
    return [("train", Xtr, Ttr, tests)]


def b2t25_split(path):
    X, T = [], []
    with h5py.File(path, "r") as f:
        for k in f:
            X.append(np.asarray(f[k]["input_features"][:], np.float32))
            lab = f[k].attrs.get("sentence_label", "")
            T.append(b2t_text(lab.decode() if isinstance(lab, bytes) else str(lab)))
    return X, T


def load_b2t25(folder, quick):
    files = sorted(glob.glob(os.path.join(folder, "**", "data_train.hdf5"), recursive=True))
    if not files:
        raise FileNotFoundError("no */data_train.hdf5 under the b2t25 folder")
    Xtr, Ttr, tests = [], [], []
    for f in files[:1] if quick else files:
        x, t = b2t25_split(f)
        Xtr += x
        Ttr += t
        val = os.path.join(os.path.dirname(f), "data_val.hdf5")
        if os.path.exists(val):
            tests.append(("standard", os.path.basename(os.path.dirname(f)), *b2t25_split(val)))
    return [("train", Xtr, Ttr, tests)]


def hw_session(root, s):
    """Sentences of one session, normalised with the single-letter block means and std (official preprocessing)."""
    d = scipy.io.loadmat(os.path.join(root, "Datasets", s, "sentences.mat"))
    sl = scipy.io.loadmat(os.path.join(root, "Datasets", s, "singleLetters.mat"))
    cube = d["neuralActivityCube"].astype(np.float64)
    sl_blocks = sl["blockList"].astype(np.int32).ravel()
    for b in d["blockList"].astype(np.int32).ravel():
        idx = np.flatnonzero(d["sentenceBlockNums"].ravel() == b)
        cube[idx] -= sl["meansPerBlock"][np.argmin(np.abs(sl_blocks - b))][None, None, :]
    cube /= sl["stdAcrossAllData"][None]
    nbins = np.ceil(d["numTimeBinsPerSentence"].ravel()).astype(int)
    X = [cube[i, :nbins[i]].astype(np.float32) for i in range(len(cube))]
    T = [str(d["sentencePrompt"][i, 0][0]).replace(" ", "").replace(">", " ").replace("~", ".").replace("#", "")
         for i in range(len(cube))]
    return X, T


def load_handwriting(folder, quick, part):
    roots = glob.glob(os.path.join(folder, "**", "Datasets"), recursive=True) + glob.glob(os.path.join(folder, "Datasets"))
    if not roots:
        raise FileNotFoundError("no Datasets/ folder under the handwriting folder")
    root = os.path.dirname(roots[0])
    cv = scipy.io.loadmat(os.path.join(root, "RNNTrainingSteps", f"trainTestPartitions_{part}.mat"))
    sessions = sorted(os.path.basename(p) for p in glob.glob(os.path.join(root, "Datasets", "t5.*")))
    Xtr, Ttr, tests = [], [], []
    for s in sessions[:1] if quick else sessions:
        X, T = hw_session(root, s)
        tr, te = np.ravel(cv[s + "_train"]).astype(int), np.ravel(cv[s + "_test"]).astype(int)
        Xtr += [X[i] for i in tr]
        Ttr += [T[i] for i in tr]
        if len(te):
            tests.append((part, s, [X[i] for i in te], [T[i] for i in te]))
    return [("train", Xtr, Ttr, tests)]


def run_text(results, args, dname, folds, stride):
    if folds and model_ok(args, "GRU-CTC"):
        prot = "+".join(sorted({t[0] for f in folds for t in f[3]}))
        _safe(bench, PHASE, results, dname, prot, "GRU-CTC",
              lambda s: CTCDecoder(min(args.epochs, CTC_EPOCHS), stride=stride), folds,
              lambda Y, P: text_scores(Y, P), args.seeds)


# ------------------------------------------------------------------ O'Doherty / Sabes and Churchland reaching

ZENODO = "https://zenodo.org/api/records/583331"


def odoherty_session(path, bin_s=0.05, seg_bins=200):
    """Threshold crossings per channel (all sorted units + hash) in 50 ms bins; cursor velocity (mm/s)."""
    with h5py.File(path, "r") as f:
        t = f["t"][0]
        pos = f["cursor_pos"][:].T
        trains = []
        for ch in range(f["spikes"].shape[1]):
            parts = []
            for u in range(f["spikes"].shape[0]):
                a = f[f["spikes"][u, ch]]
                if a.attrs.get("MATLAB_empty") or a.dtype.kind != "f":
                    continue
                parts.append(np.ravel(a[()]))
            trains.append(np.sort(np.concatenate(parts)) if parts else np.zeros(0))
    edges = np.arange(t[0], t[-1], bin_s)
    X = bin_counts(trains, edges)
    P = np.stack([np.interp(edges, t, pos[:, k]) for k in range(2)], 1)
    Y = np.diff(P, axis=0) / bin_s
    n = len(Y) // seg_bins
    segs = [X[i * seg_bins:(i + 1) * seg_bins] for i in range(n)]
    Ys = [Y[i * seg_bins:(i + 1) * seg_bins] for i in range(n)]
    return segs, Ys, [i * 5 // n for i in range(n)]


def run_odoherty(results, args, root):
    import urllib.request
    with urllib.request.urlopen(ZENODO, timeout=120) as r:
        files = sorted(json.load(r)["files"], key=lambda f: f["key"])
    if args.quick:
        files = [min(files, key=lambda f: f["size"])]

    def loader(fi):
        stem = fi["key"].replace(".mat", "")
        return lambda: cached_segments(os.path.join(root, "cache", stem + ".npz"), lambda: odoherty_session(
            download(fi["links"]["self"], os.path.join(root, fi["key"]), quiet=True)))
    folds = SessionFolds("ODoherty-Sabes", "contiguous_5fold", [(f["key"].replace(".mat", ""), loader(f)) for f in files])
    run_regression(results, args, "ODoherty-Sabes", "contiguous_5fold", folds, lags=5)


def churchland_session(asset, max_spikes=None, bin_s=0.02, pre=0.25, post=0.45):
    with remote_h5(asset) as f:
        idx = f["units/spike_times_index"][:]
        n_units = int(np.searchsorted(idx, max_spikes)) if max_spikes else len(idx)
        trains = ragged(f["units"], "spike_times", range(max(1, n_units)))
        hand = f["processing/behavior/Position/Hand"]
        hpos, ht = hand["data"][:], hand["timestamps"][:]
        tr = f["intervals/trials"]
        mb = tr["move_begins_time"][:]
        ok = (tr["task_success"][:] == 1) & (tr["discard_trial"][:] == 0) & np.isfinite(mb)
    nb = int(round((pre + post) / bin_s))
    segs, Ys = [], []
    for m in mb[ok]:
        edges = m - pre + bin_s * np.arange(nb + 1)
        segs.append(window_counts(trains, edges[:-1], edges[1:]))
        P = np.stack([np.interp(edges, ht, hpos[:, k]) for k in range(2)], 1)
        Ys.append(np.diff(P, axis=0) / bin_s)
    n = len(segs)
    return segs, Ys, [i * 5 // n for i in range(n)]


def run_churchland(results, args, root):
    assets = sorted(dandi_assets("000070", root), key=lambda a: a["path"])
    cap = 5e6 if args.quick else None
    sessions = [(_ses(a["path"]), lambda a=a: cached_segments(
        os.path.join(root, "cache", f"{_ses(a['path'])}{'_quick' if cap else ''}.npz"), churchland_session, a, cap))
        for a in (assets[:1] if args.quick else assets)]
    run_regression(results, args, "Churchland-Maze", "trial_blocks_5fold",
                   SessionFolds("Churchland-Maze", "trial_blocks_5fold", sessions), lags=3)


# ------------------------------------------------------------------ mouse Neuropixels decoding (no SOTA)

def lr():
    return make_pipeline(FunctionTransformer(np.sqrt), StandardScaler(),
                         LogisticRegression(C=0.1, max_iter=3000))


def keep_classes(X, y, meta, k=5):
    import pandas as pd
    vc = pd.Series(y).value_counts()
    ok = np.isin(y, vc.index[vc >= k])
    return X[ok], y[ok], meta[ok].reset_index(drop=True)


def run_classify(results, args, dname, parts):
    """parts: list of (X, y, session) -> within-session 5-fold LR."""
    import pandas as pd
    if not parts or not model_ok(args, "LR"):
        return
    n = max(p[0].shape[1] for p in parts)
    X = np.concatenate([np.pad(p[0], ((0, 0), (0, n - p[0].shape[1]))) for p in parts])
    y = np.concatenate([np.asarray(p[1]).astype(str) for p in parts])
    meta = pd.DataFrame(dict(subject=np.concatenate([[p[2]] * len(p[1]) for p in parts]), session="0", run="0"))
    X, y, meta = keep_classes(X, y, meta)
    _safe(evaluate, PHASE, results, dname, "within_session:5", "LR", classical(lr()), X, y, meta, args.seeds,
          needs_seed=False)


def allen_session(asset, max_units=None):
    with remote_h5(asset) as f:
        u = f["units"]
        qc = (u["presence_ratio"][:] >= 0.95) & (u["isi_violations"][:] <= 0.5) & (u["amplitude_cutoff"][:] <= 0.1)
        rows = np.flatnonzero(qc)[:max_units]
        trains = [np.sort(t) for t in ragged(u, "spike_times", rows)]
        g = f["intervals/drifting_gratings_presentations"]
        ori = np.asarray(g["orientation"][:], float)
        t0, t1 = g["start_time"][:], g["stop_time"][:]
    ok = np.isfinite(ori)
    return window_counts(trains, t0[ok], t1[ok]), ori[ok].astype(int).astype(str)


def run_allen(results, args, root):
    assets = sorted((a for a in dandi_assets("000021", root) if "probe" not in a["path"]), key=lambda a: a["path"])
    if args.quick:
        assets = [min(assets, key=lambda a: a["size"])]
    parts = []
    for a in assets:
        s = _ses(a["path"])
        d = attempt(f"Allen-VC-DriftingGratings {s}", allen_session, a, 60 if args.quick else None)
        if d is not None:
            parts.append((*d, s))
    run_classify(results, args, "Allen-VC-DriftingGratings", parts)


def steinmetz_session(path):
    with h5py.File(path, "r") as f:
        u = f["units"]
        trains = [np.sort(t) for t in ragged(u, "spike_times", range(len(u["spike_times_index"])))]
        tr = f["intervals/trials"]
        stim, choice = tr["visual_stimulus_time"][:], tr["response_choice"][:]
        inc = tr["included"][:].astype(bool) if "included" in tr else np.ones(len(stim), bool)
    ok = inc & np.isfinite(stim) & np.isfinite(choice)
    return window_counts(trains, stim[ok], stim[ok] + 0.4), choice[ok].astype(int).astype(str)


def run_steinmetz(results, args, root):
    assets = sorted(dandi_assets("000017", root), key=lambda a: a["path"])
    if args.quick:
        assets = [min(assets, key=lambda a: a["size"])]
    parts = []
    for a in assets:
        s = _ses(a["path"])
        d = attempt(f"Steinmetz2019-Choice {s}", lambda: steinmetz_session(dandi_get(root, "000017", a)))
        if d is not None:
            parts.append((*d, s))
    run_classify(results, args, "Steinmetz2019-Choice", parts)


def run_ibl(results, args, root):
    from one.api import ONE
    one = ONE(base_url="https://openalyx.internationalbrainlab.org", username="intbrainlab",
              password="international", silent=True, cache_dir=os.path.join(root, "one"))
    eids = sorted(one.search(project="ibl_neuropixel_brainwide_01", datasets="spikes.times.npy"))
    parts = []
    for eid in eids[:1 if args.quick else IBL_SESSIONS]:
        def load(eid=eid):
            cols = sorted(c for c in one.list_collections(eid) if c.startswith("alf/probe00"))
            col = "alf/probe00/pykilosort" if "alf/probe00/pykilosort" in cols else cols[-1]
            sp = one.load_object(eid, "spikes", collection=col, attribute=["times", "clusters"])
            trials = one.load_object(eid, "trials", collection="alf")  # choice etc. live in _ibl_trials.table.pqt
            order = np.argsort(sp["clusters"], kind="stable")
            cl, t = sp["clusters"][order], sp["times"][order]
            bounds = np.searchsorted(cl, np.arange(cl.max() + 2))
            trains = [np.sort(t[bounds[i]:bounds[i + 1]]) for i in range(cl.max() + 1)]
            fm, ch = np.asarray(trials["firstMovement_times"], float), np.asarray(trials["choice"])
            ok = np.isfinite(fm) & (ch != 0)
            return window_counts(trains, fm[ok] - 0.1, fm[ok]), ch[ok].astype(int).astype(str), eid
        d = attempt(f"IBL-BWM-Choice {eid}", load)
        if d is not None:
            parts.append(d)
    run_classify(results, args, "IBL-BWM-Choice", parts)


def pvc8_parts(folder, quick):
    """Grating images (index >= 540) from resp_train [neurons x images x trials x ms]; counts 50-156 ms."""
    parts = []
    for p in sorted(glob.glob(os.path.join(folder, "**", "[0-9][0-9].mat"), recursive=True))[:1 if quick else None]:
        r = scipy.io.loadmat(p, variable_names=["resp_train"])["resp_train"][:, 540:]
        c = r[..., 50:156].sum(-1)  # neurons x images x trials
        X = c.transpose(1, 2, 0).reshape(-1, c.shape[0]).astype(np.float32)
        y = np.repeat(np.arange(c.shape[1]), c.shape[2]).astype(str)
        parts.append((X, y, Path(p).stem))
    return parts


def pvc11_parts(folder, quick):
    """spikes_gratings/*.mat: data.EVENTS {units x stimuli x trials} spike times (s); counts over 0-1.28 s."""
    parts = []
    for p in sorted(glob.glob(os.path.join(folder, "**", "spikes_gratings", "*.mat"), recursive=True))[:1 if quick else None]:
        ev = scipy.io.loadmat(p, simplify_cells=True)["data"]["EVENTS"]
        nu, ns, nt = ev.shape
        X = np.array([[[np.sum((np.ravel(ev[u, s, k]) >= 0) & (np.ravel(ev[u, s, k]) < 1.28)) for u in range(nu)]
                       for k in range(nt)] for s in range(ns)], np.float32).reshape(-1, nu)
        y = np.repeat(np.arange(ns), nt).astype(str)
        parts.append((X, y, Path(p).stem))
    return parts


def run_crcns(results, args):
    loaders = {"crcns_pvc-8": ("CRCNS-pvc-8", pvc8_parts), "crcns_pvc-11": ("CRCNS-pvc-11", pvc11_parts)}
    for key, folder in args.paths.items():
        if not key.startswith("crcns_"):
            continue
        if key not in loaders:
            print(f"\n[{PHASE}] {key}: no loader for this CRCNS set (implemented: {', '.join(loaders)})")
            continue
        dname, fn = loaders[key]
        if wanted(args, dname, "CRCNS"):
            parts = attempt(dname, fn, folder, args.quick)
            run_classify(results, args, dname, parts or [])
    if not any(k.startswith("crcns_") for k in args.paths) and wanted(args, "CRCNS"):
        print(f"\n[{PHASE}] CRCNS: skipped (pass --path crcns_pvc-8=FOLDER or crcns_pvc-11=FOLDER; CRCNS account)")


# ------------------------------------------------------------------ runner

def run(results, args):
    root = os.path.join(args.data_dir, "spikes")
    os.makedirs(root, exist_ok=True)
    run_nlb(results, args, os.path.join(root, "nlb"))
    run_falcon(results, args, os.path.join(root, "falcon"))

    dryad = "Dryad needs a login; download {} by hand"
    if wanted(args, "B2T24") and (f := gated(args, "b2t24", "B2T24", dryad.format("competitionData.tar.gz"))):
        run_text(results, args, "B2T24", attempt("B2T24", load_b2t24, f, args.quick), stride=2)
    if wanted(args, "B2T25") and (f := gated(args, "b2t25", "B2T25", dryad.format("t15_copyTask_neuralData.zip"))):
        run_text(results, args, "B2T25", attempt("B2T25", load_b2t25, f, args.quick), stride=2)
    if wanted(args, "Willett2021-Handwriting") and (
            f := gated(args, "handwriting", "Willett2021-Handwriting", dryad.format("handwritingBCIData.tar.gz"))):
        for part in ("HeldOutTrials", "HeldOutBlocks"):
            run_text(results, args, "Willett2021-Handwriting",
                     attempt(f"Willett2021-Handwriting {part}", load_handwriting, f, args.quick, part), stride=2)

    if wanted(args, "ODoherty-Sabes"):
        attempt("ODoherty-Sabes", run_odoherty, results, args, os.path.join(root, "odoherty"))
    if wanted(args, "Churchland-Maze"):
        attempt("Churchland-Maze", run_churchland, results, args, os.path.join(root, "churchland"))
    if wanted(args, "Allen-VC-DriftingGratings"):
        attempt("Allen-VC-DriftingGratings", run_allen, results, args, os.path.join(root, "allen"))
    if wanted(args, "IBL-BWM-Choice"):
        attempt("IBL-BWM-Choice", run_ibl, results, args, os.path.join(root, "ibl"))
    if wanted(args, "Steinmetz2019-Choice"):
        attempt("Steinmetz2019-Choice", run_steinmetz, results, args, os.path.join(root, "steinmetz"))
    run_crcns(results, args)
