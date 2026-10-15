"""Intracranial EEG benchmarks (phase 12): ECoG and sEEG decoding, speech/music, seizures and seizure-onset zones.

Source of truth for datasets, protocols and published numbers: projects/ecog-seeg/DATASETS.md.
Almost every model is patient-specific (one model per patient, channel counts differ); cross-patient results are
separate datasets/protocols (Mayo/FNUSA cross-institution, HUP SOZ `cross_subject`, Neuroprobe cross-session).

| Dataset (name in results) | How it is obtained | Protocol(s) | Models | Tested here |
|---|---|---|---|---|
| BCI Competition IV ds4 (`BCICIV-4`): 5-finger flexion regression | auto (bbci.de zip 206 MB + released test labels 21 MB) | `standard` = official 400 s train / 200 s test per subject; `pearson_r` = mean over 4 fingers (ring excluded), also `pearson_r_5fingers` | BandPower+Ridge, ResNet1D | yes, full (3 subjects) |
| Miller ECoG library, finger flexion (`Miller-FingerFlex`) | auto (Stanford Digital Repository `fingerflex.zip`, 580 MB; quick: 2 subjects read over HTTP ranges) | `standard` = first 400 s train, rest test (CORTEG convention; first 2/3 for the two shorter recordings); `pearson_r` over 5 fingers | BandPower+Ridge, ResNet1D | yes, quick (subjects mv, wm) |
| Brain Treebank via Neuroprobe (`BrainTreebank-Neuroprobe`): 15 binary tasks | official `neuroprobe` package (pip) for tasks, windows and splits; data auto-downloaded from braintreebank.dev (12 Lite sessions, 3.6-8 GB each), or `--path braintreebank=FOLDER` (an extracted copy); skipped in `--quick` unless `--path` is given | `within_session` (2 contiguous folds, test = 2nd half of the held-out fold, as in the package), `cross_session` (train on the other Lite movie); `roc_auc` = mean over tasks, `roc_auc_<task>` per task | BandPower+LR, ResNet1D (1-s windows at 128 Hz) | partial: real metadata and transcripts + synthetic all-zero h5 files for sub_3 trials 0-1 (code path only; 3 tasks, 200 windows) |
| Berezutskaya film (`Berezutskaya-SpeechMusic`, ds003688): speech vs music 2-s windows | auto (OpenNeuro S3, clinical-grid film run per subject, 50-400 MB) | `leave_one_run_out` = per patient, 6 folds each holding out one speech and one music 30-s block | BandPower+LR, ResNet1D | yes, quick (2 smallest subjects) |
| Podcast ECoG (`Podcast-ECoG`, ds005574): word-level encoding | auto (OpenNeuro S3, preprocessed high-gamma .fif 265-866 MB/subject + spaCy word vectors) | `leave_one_run_out` = 2-fold over story halves (as the dataset paper); `pearson_r` = mean over electrodes of r between predicted and true high gamma (0-0.5 s after word onset) | WordVec+Ridge | yes, quick (sub-08) |
| Chen 2024 public participant (`Chen2024-HB02`): spectrogram decoding | auto (Mendeley Data, HB02.h5, 1.2 GB) | `standard` = last 50 trials test (the file's TestNum_cum), 322 train; `pcc` = mean over test trials of Pearson r between true and decoded spectrogram | HG+Ridge (+-160 ms context) | yes, full |
| Verwoert/Herff Dutch sEEG (`Verwoert-SingleWordDutch`): log-mel reconstruction | auto (OSF zip, members read over HTTP ranges, ~240 MB/subject) | `leave_one_run_out` = 10 contiguous folds (paper: non-shuffled 10-fold); `pearson_r` mean over 23 mel bins | HG+PCA+LinReg (the paper's baseline) | yes, quick (sub-01) |
| Mayo / FNUSA graphoelements (`MayoFNUSA (FNUSA->Mayo)`, `MayoFNUSA (Mayo->FNUSA)`) | auto (figshare zips 2.4 + 6.1 GB; quick: 50 clips/class read over HTTP ranges) | `standard` = train one institution, test the other; 3 classes (power-line class removed, as the dataset's example code does) | BandPower+LR, ResNet1D (1 kHz) | yes, quick |
| HUP (`HUP-SOZ`, ds004100): seizure-onset-zone channel classification from the first interictal run | auto (OpenNeuro S3, ~18 MB/run) | `cross_subject` (GroupKFold 5 over patients), `roc_auc` | BandPower+LR, BandPower+RF | yes, quick (4 subjects) |
| Fragility (ds003029) | - | not run: the public BIDS release has no SOZ labels in its channels.tsv files (clinical metadata are in the paper's table) and marker names differ by centre | - | no |
| SWEC-ETHZ short-term (`SWEC-ETHZ-short`): seizure detection, 1-s windows | auto (ETHZ zips, members read over HTTP ranges; 16 patients, ~0.35-1 GB each) | `standard` = per patient, train on Sz1, test on all later seizures (ictal vs pre/post-ictal) | BandPower+LR, ResNet1D | yes, quick (ID3) |
| Bellier Pink Floyd (`Bellier-PinkFloyd`): 32-band spectrogram decoding from HFA | auto (Zenodo, 9-37 MB/patient) | `leave_one_run_out` = 5 contiguous folds per patient | HFA+Ridge (0-750 ms lags) | yes, quick (P1, P27) |
| Kaggle AES 2014 seizure prediction (`Kaggle-AES2014`) | `--path kaggle_aes2014=FOLDER` (`Dog_1/Dog_1_interictal_segment_0001.mat`, ...) | `leave_one_run_out` = per subject, 5 folds over 1-h clip sequences (test clips not used) | BandPower+LR | partial: synthetic folder in the contest layout |
| Kaggle UPenn-Mayo 2014 seizure detection (`Kaggle-UPennMayo`) | `--path kaggle_upenn_mayo=FOLDER` (`Dog_1/Dog_1_ictal_segment_1.mat`, ...) | `leave_one_run_out` = per subject, 5 folds grouped by seizure (interictal: blocks of 60 clips); `kaggle_score` = (AUC seizure + AUC early) / 2 | BandPower+LR, ResNet1D | partial: synthetic folder |
| Kaggle Melbourne 2016 (`Kaggle-Melbourne2016`) | `--path kaggle_melbourne=FOLDER` (`train_1/1_1_0.mat`, ...) | as AES 2014 | BandPower+LR | partial: synthetic folder |
| DARPA RAM free recall (`RAM-FR1`): recalled vs forgotten words | `--path ram=FOLDER`: BIDS layout of the RAM FR1 release (as OpenNeuro ds004789: `sub-*/ses-*/ieeg/*_task-FR1_acq-bipolar_ieeg.edf` + `_events.tsv`) | `cross_session` (per patient, leave one session out), `within_session:5` | BandPower+LR | partial: one real ds004789 session (R1031M ses-0) |

Notes
- Finger flexion: each channel is median-centred and clipped at 10 robust SDs (some files carry 1e6-scale spikes),
  then common-average referenced; log power in 5 bands (8-13, 13-30, 30-55, 70-115, 125-170 Hz) plus the
  local motor potential, in 50-ms frames; each frame's input is the 10 frames from -900 ms to 0 ms (100 ms apart).
  Targets are the glove values averaged per frame, so r is computed at 20 Hz, not at 1 kHz.
- No hyperparameter is tuned on test data: ridge strength is chosen by RidgeCV on contiguous folds of the training
  set; deep models train for a fixed number of epochs (min(--epochs, 50)).
- Quick runs download about 2.5 GB in all (Chen 1.2 GB is a single file; Miller, Verwoert, SWEC and Mayo/FNUSA members
  are read over HTTP ranges) and take about an hour on a laptop CPU, mostly downloads and range reads (cached
  afterwards); restrict with --datasets for a shorter check.
- Kaggle sets: the hidden test labels are not used. Our CV over training clips is not the contest split, so no
  leaderboard number is compared.
"""
import glob
import io
import os
import re
import shutil
import urllib.parse
import urllib.request
import zipfile
from functools import partial

import mne
import numpy as np
import pandas as pd
import scipy.io as sio
from scipy.signal import butter, hilbert, resample_poly, sosfiltfilt, welch
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression, RidgeCV
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import KFold, StratifiedGroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler

from common import (NotApplicable, _safe, classical, deep, download, evaluate, log_error, resnet1d, set_seed)
from ecg import wanted
from eeg_more import TorchRegressor, evaluate_custom
from emg_more import _HTTPFile, cached as _cached, open_zip

PHASE = "phase12"
S3 = "https://s3.amazonaws.com/openneuro.org"
DEEP = dict(lr=1e-3, weight_decay=1e-4, batch_size=128)
ECOG_BANDS = ((1, 4), (4, 8), (8, 13), (13, 30), (30, 55), (70, 150))
mne.set_log_level("ERROR")


# ================================================================== shared helpers

def attempt(name, fn, *a):
    print(f"\n[{PHASE}] {name}")
    try:
        return fn(*a)
    except Exception as e:
        log_error(PHASE, f"{name}: could not load ({type(e).__name__}: {e})")


def cached(path, fn):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return _cached(path, fn)


def gated(args, key, name):
    folder = args.paths.get(key)
    if not folder:
        print(f"\n[{PHASE}] {name}: skipped (access-gated; pass --path {key}=FOLDER)")
    return folder


def use(args, model):
    return not args.models or model in args.models


def epochs(args):
    return min(args.epochs, 50)


def openneuro(ds, rel, root):
    return download(f"{S3}/{ds}/{rel}", os.path.join(root, rel), quiet=True)


def s3_keys(prefix):
    """All (key, size) under an OpenNeuro S3 prefix."""
    out, token = [], None
    while True:
        url = f"{S3}?list-type=2&prefix={prefix}" + (f"&continuation-token={urllib.parse.quote(token)}" if token else "")
        with urllib.request.urlopen(url, timeout=120) as r:
            x = r.read().decode()
        out += [(k, int(s)) for k, s in re.findall(r"<Key>([^<]+)</Key>.*?<Size>(\d+)</Size>", x)]
        m = re.search(r"<NextContinuationToken>([^<]+)<", x)
        if not m:
            return out
        token = m.group(1)


def extract(z, member, dst):
    """Copy one zip member to dst (streamed, so remote members never sit in memory)."""
    if not os.path.exists(dst):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with z.open(member) as src, open(dst + ".part", "wb") as f:
            shutil.copyfileobj(src, f, 1 << 20)
        os.replace(dst + ".part", dst)
    return dst


class _Collect:
    """Stand-in for Results that keeps rows in memory, so a multi-patient unit is written only when complete."""

    def __init__(self):
        self.rows = []

    def is_done(self, *a):
        return False

    def add(self, rows):
        self.rows += rows


def per_subject(phase, results, dataset, protocol, model, make, subjects, seeds, scorer=None, needs_seed=True):
    """Patient-specific evaluation: evaluate() (or evaluate_custom() with scorer) on each patient separately,
    because channel counts differ. subjects: callables returning (X, y, meta) (cached, so cheap to call again)."""
    for seed in (seeds if needs_seed else seeds[:1]):
        if results.is_done(dataset, protocol, model, seed):
            print(f"  = {dataset} | {protocol} | {model} | seed {seed}: done, skipping")
            continue
        c = _Collect()
        for load in subjects:
            X, y, meta = load()
            if scorer:
                evaluate_custom(phase, c, dataset, protocol, model, make, X, y, meta, [seed], scorer)
            else:
                evaluate(phase, c, dataset, protocol, model, make, X, y, meta, [seed])
        if not c.rows:
            raise NotApplicable("no subject had a valid split")
        results.add(c.rows)


def guarded(name, loads):
    """Wrap per-subject loaders so a failing subject is logged and skipped; returns the working ones."""
    ok = []
    for load in loads:
        try:
            load()
            ok.append(load)
        except Exception as e:
            log_error(PHASE, f"{name}: {type(e).__name__}: {e}")
    return ok


def bandpower(X, fs, bands=ECOG_BANDS, chunk=1024):
    """Log Welch power per channel and band (bands above Nyquist are clipped); X (n, ch, t) -> (n, ch * bands)."""
    bands = [(a, min(b, fs / 2 - 1)) for a, b in bands if a < fs / 2 - 1]
    out = []
    for i in range(0, len(X), chunk):
        x = np.asarray(X[i:i + chunk], dtype=np.float32)
        f, p = welch(x, fs=fs, nperseg=min(x.shape[-1], int(fs)), axis=-1)
        out.append(np.log(np.concatenate([p[..., (f >= a) & (f < b)].mean(-1) for a, b in bands], axis=1) + 1e-20))
    return np.concatenate(out)


def bp_lr(fs, bands=ECOG_BANDS, C=0.1):
    return make_pipeline(FunctionTransformer(partial(bandpower, fs=fs, bands=bands)), StandardScaler(),
                         LogisticRegression(C=C, max_iter=2000, class_weight="balanced"))


def flat():
    return FunctionTransformer(lambda X: np.asarray(X, dtype=np.float32).reshape(len(X), -1))


def ridge():
    """Ridge with its strength picked on 5 contiguous folds of the training data only."""
    return make_pipeline(flat(), StandardScaler(), RidgeCV(alphas=np.logspace(0, 6, 7), cv=KFold(5)))


def regressor(args):
    return lambda seed: TorchRegressor(resnet1d, epochs=epochs(args), **DEEP)


def corr_cols(Y, P):
    """Pearson r per column (nan for constant columns)."""
    Y, P = np.asarray(Y, float), np.asarray(P, float)
    Y, P = Y - Y.mean(0), P - P.mean(0)
    den = np.sqrt((Y ** 2).sum(0) * (P ** 2).sum(0))
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(den > 0, (Y * P).sum(0) / den, np.nan)


def mean_r_scorer(est, X, Y, meta):
    return {"pearson_r": np.nanmean(corr_cols(Y, est.predict(X)))}


def lagged(F, lags):
    """F (frames, feat) -> (frames, feat, len(lags)) with F[t + lag]; indices clipped at the edges."""
    idx = np.clip(np.arange(len(F))[:, None] + np.asarray(lags), 0, len(F) - 1)
    return np.ascontiguousarray(F[idx].transpose(0, 2, 1), dtype=np.float32)


def contiguous_runs(n, k):
    return (np.arange(n) * k // n).astype(str)


def meta_table(n, subject, run, session="0", **cols):
    return pd.DataFrame(dict(subject=str(subject), session=session, run=run, **cols), index=range(n))


# ================================================================== finger flexion (BCI IV ds4, Miller)

FINGER_BANDS = ((8, 13), (13, 30), (30, 55), (70, 115), (125, 170))
FRAME = 50  # samples at 1 kHz -> 20 Hz frames
FINGER_LAGS = range(-18, 1, 2)  # frames: -900 ms .. 0 ms


def finger_frames(ecog, glove, fs=1000):
    """Artifact-clipped, common-average-referenced ECoG (T, ch) -> per-frame features (frames, ch * 6) and frame-mean glove."""
    x = np.asarray(ecog, dtype=np.float32)
    x = x - np.median(x, 0)
    lim = 10 * 1.4826 * np.median(np.abs(x), 0) + 1e-6  # clip artifacts (some files have spikes of 1e6-1e7)
    x = np.clip(x, -lim, lim)
    x = x - x.mean(1, keepdims=True)
    n = len(x) // FRAME
    fr = lambda a: a[:n * FRAME].reshape(n, FRAME, -1).mean(1)
    feats = [fr(x)]  # local motor potential
    for a, b in FINGER_BANDS:
        y = sosfiltfilt(butter(4, [a, b], "band", fs=fs, output="sos"), x, axis=0).astype(np.float32)
        feats.append(np.log(fr(y ** 2) + 1e-6))
    return np.concatenate(feats, 1).astype(np.float32), fr(np.asarray(glove, dtype=np.float32))


def finger_scorer(fingers):
    def score(est, X, Y, meta):
        r = corr_cols(Y, est.predict(X))
        out = {"pearson_r": np.nanmean(r[list(fingers)]), **{f"pearson_r_finger{j + 1}": r[j] for j in range(5)}}
        if len(fingers) < 5:
            out["pearson_r_5fingers"] = np.nanmean(r)
        return out
    return score


def finger_subject(path, fn):
    """Cache one subject: fn() -> (F_train, Y_train, F_test, Y_test) frame features."""
    def load():
        def build():
            Ftr, Ytr, Fte, Yte = fn()
            X = np.concatenate([lagged(Ftr, FINGER_LAGS), lagged(Fte, FINGER_LAGS)])
            run = np.r_[["train"] * len(Ftr), ["test"] * len(Fte)]
            return [X, np.concatenate([Ytr, Yte])], np.zeros(len(X)), meta_table(len(X), os.path.basename(path), run)
        (X, Y), _, meta = cached(path, build)
        return X, Y, meta
    return load


def bciiv4_subjects(root):
    d = os.path.join(root, "bciiv4")
    if not os.path.exists(os.path.join(d, "sub3_testlabels.mat")):
        z = download("https://www.bbci.de/competition/download/competition_iv/BCICIV_4_mat.zip", os.path.join(d, "comp.zip"))
        t = download("https://www.bbci.de/competition/iv/results/ds4/true_labels.zip", os.path.join(d, "labels.zip"))
        for f in (z, t):
            with zipfile.ZipFile(f) as zz:
                zz.extractall(d)

    def fn(s):
        m = sio.loadmat(os.path.join(d, f"sub{s}_comp.mat"))
        y = sio.loadmat(os.path.join(d, f"sub{s}_testlabels.mat"))["test_dg"]
        return finger_frames(m["train_data"], m["train_dg"]) + finger_frames(m["test_data"], y)
    return [finger_subject(os.path.join(d, "cache", f"sub{s}"), partial(fn, s)) for s in (1, 2, 3)]


MILLER_URL = "https://stacks.stanford.edu/file/druid:zk881ps0522/fingerflex.zip"
MILLER_SUBJECTS = ["bp", "cc", "ht", "jc", "jp", "mv", "wc", "wm", "zt"]


def miller_subjects(root, quick):
    d = os.path.join(root, "miller")
    names = ["mv", "wm"] if quick else MILLER_SUBJECTS
    z = []

    def fn(s):
        path = os.path.join(d, f"{s}_fingerflex.mat")
        if not os.path.exists(path):
            z[:] = z or [open_zip(MILLER_URL, os.path.join(d, "fingerflex.zip"), quick)]
            extract(z[0], f"fingerflex/data/{s}/{s}_fingerflex.mat", path)
        m = sio.loadmat(path)
        cut = min(400 * 1000, 2 * len(m["data"]) // 3)  # first 400 s (~2/3) train; 2/3 for shorter recordings
        return finger_frames(m["data"][:cut], m["flex"][:cut]) + finger_frames(m["data"][cut:], m["flex"][cut:])
    return [finger_subject(os.path.join(d, "cache", s), partial(fn, s)) for s in names]


def run_fingers(results, args, name, subjects, fingers):
    subjects = guarded(name, subjects)
    if not subjects:
        return
    score = finger_scorer(fingers)
    if use(args, "BandPower+Ridge"):
        _safe(per_subject, PHASE, results, name, "standard", "BandPower+Ridge",
              classical(make_pipeline(FunctionTransformer(lambda X: np.asarray(X)[:, :, 1::2]), ridge())),
              subjects, args.seeds, scorer=score, needs_seed=False)
    if use(args, "ResNet1D"):
        _safe(per_subject, PHASE, results, name, "standard", "ResNet1D", regressor(args), subjects, args.seeds, scorer=score)


# ================================================================== Brain Treebank / Neuroprobe

BTB = "https://braintreebank.dev/data"
NP_FS_OUT = 128


def fetch_braintreebank(root, trials, movies, sessions=True):
    """Metadata, the needed transcripts and the session h5 files (members of the official zips)."""
    for f in ("electrode_labels", "localization"):
        if not os.path.isdir(os.path.join(root, f)):
            with zipfile.ZipFile(download(f"{BTB}/{f}.zip", os.path.join(root, f + ".zip"), True)) as z:
                z.extractall(root)
    download(f"{BTB}/corrupted_elec.json", os.path.join(root, "corrupted_elec.json"), True)
    tz = None
    for m in movies:
        dst = os.path.join(root, "transcripts", m, "features.csv")
        if not os.path.exists(dst):
            tz = tz or open_zip(f"{BTB}/transcripts.zip", "", True)
            extract(tz, f"transcripts/{m}/features.csv", dst)
    for s, t in trials if sessions else []:
        name = f"sub_{s}_trial{t:03}.h5"
        if not os.path.exists(os.path.join(root, name)):
            extract(open_zip(f"{BTB}/subject_data/sub_{s}/trial{t:03}/{name}.zip", "", True), name, os.path.join(root, name))


def neuroprobe_xy(ds, idx):
    """Windows of a neuroprobe dataset (1 s at 2048 Hz) -> X (n, electrodes, 128 Hz samples), y."""
    X, y = [], []
    for i in idx:
        item = ds[int(i)]
        X.append(resample_poly(np.asarray(item["data"], dtype=np.float32), 1, 2048 // NP_FS_OUT, axis=-1))
        y.append(int(item["label"]))
    return np.stack(X).astype(np.float32), np.asarray(y)


def run_neuroprobe(results, args, root, quick):
    os.environ["ROOT_DIR_BRAINTREEBANK"] = root
    import torch
    from neuroprobe import BrainTreebankSubject, BrainTreebankSubjectTrialBenchmarkDataset
    from neuroprobe import config as C
    trials = list(C.NEUROPROBE_LITE_SUBJECT_TRIALS)
    if quick:  # only sessions already on disk
        trials = [st for st in trials if os.path.exists(os.path.join(root, f"sub_{st[0]}_trial{st[1]:03}.h5"))][:2]
    fetch_braintreebank(root, trials, {C.BRAINTREEBANK_SUBJECT_TRIAL_MOVIE_NAME_MAPPING[f"btbank{s}_{t}"] for s, t in trials},
                        sessions=not quick)
    tasks = C.NEUROPROBE_TASKS[:3] if quick else C.NEUROPROBE_TASKS
    subjects = {}

    def dataset(s, t, task):
        if s not in subjects:
            subjects[s] = BrainTreebankSubject(s, cache=False, dtype=torch.float32)
        return BrainTreebankSubjectTrialBenchmarkDataset(subjects[s], t, dtype=torch.float32, eval_name=task, lite=True,
                                                         max_samples=200 if quick else None)

    def folds(s, t, task, protocol):
        """(train set, train idx, test set, test idx) as the package's generate_splits_* build them."""
        ds = dataset(s, t, task)
        if protocol == "within_session":
            for tr, te in KFold(C.NEUROPROBE_LITE_N_FOLDS, shuffle=False).split(np.arange(len(ds))):
                yield ds, tr, ds, te[len(te) // 2:]
        else:
            other = [tt for ss, tt in C.NEUROPROBE_LITE_SUBJECT_TRIALS if ss == s and tt != t]
            if not other:
                return
            dtr = dataset(s, other[0], task)
            yield dtr, np.arange(len(dtr)), ds, np.arange(len(ds) // 2, len(ds))

    models = {"BandPower+LR": classical(bp_lr(NP_FS_OUT, ((1, 4), (4, 8), (8, 13), (13, 30), (30, 63)))),
              "ResNet1D": deep(resnet1d, epochs=epochs(args), **DEEP)}
    name = "BrainTreebank-Neuroprobe"
    for protocol in ("within_session", "cross_session"):
        for mname, make in models.items():
            if not use(args, mname):
                continue
            for seed in (args.seeds if mname == "ResNet1D" else args.seeds[:1]):
                if results.is_done(name, protocol, mname, seed):
                    print(f"  = {name} | {protocol} | {mname} | seed {seed}: done, skipping")
                    continue
                try:
                    rows = neuroprobe_unit(name, protocol, mname, make, seed, trials, tasks, folds, quick)
                except Exception as e:
                    log_error(PHASE, f"{name} | {protocol} | {mname}: {type(e).__name__}: {e}")
                    continue
                results.add(rows)


def neuroprobe_unit(name, protocol, mname, make, seed, trials, tasks, folds, quick):
    import time
    from datetime import datetime, timezone

    import torch
    from common import git_commit
    rows, t0 = [], time.time()
    for s, t in trials:
        aucs = {}
        for task in tasks:
            fold_aucs = []
            for dtr, tr, dte, te in folds(s, t, task, protocol):
                Xtr, ytr = neuroprobe_xy(dtr, tr)
                Xte, yte = neuroprobe_xy(dte, te)
                if len(np.unique(ytr)) < 2 or len(np.unique(yte)) < 2:
                    continue
                set_seed(seed)
                est = make(seed).fit(Xtr, ytr)
                p = est.predict_proba(Xte)
                fold_aucs.append(roc_auc_score(yte, p[:, list(est.classes_).index(1)]))
            if fold_aucs:
                aucs[task] = float(np.mean(fold_aucs))
        if not aucs:
            continue
        common = dict(phase=PHASE, dataset=name, protocol=protocol, model=mname, seed=seed, fold=f"sub{s}_trial{t}",
                      n_train=0, n_test=0, train_s=0.0, device="cuda" if torch.cuda.is_available() else "cpu",
                      commit=git_commit(), time=datetime.now(timezone.utc).isoformat(timespec="seconds"))
        rows.append(dict(common, metric="roc_auc", value=float(np.mean(list(aucs.values())))))
        rows += [dict(common, metric=f"roc_auc_{k}", value=v) for k, v in aucs.items()]
    if not rows:
        raise NotApplicable("no session with both classes")
    mean = np.mean([r["value"] for r in rows if r["metric"] == "roc_auc"])
    print(f"  + {name} | {protocol} | {mname} | seed {seed}: {len(trials)} sessions x {len(tasks)} tasks, "
          f"mean roc_auc {mean:.4f}, {time.time() - t0:.0f}s")
    return rows


# ================================================================== Berezutskaya film (ds003688)

def berezutskaya_subjects(root, quick):
    films = sorted([(k, s) for k, s in s3_keys("ds003688/sub-") if "task-film_acq-clinical" in k and k.endswith("_ieeg.eeg")])
    first = {}
    for k, s in films:  # first clinical film run per subject
        first.setdefault(k.split("/")[1], (k, s))
    items = sorted(first.values(), key=lambda ks: ks[1])[:2] if quick else list(first.values())
    return [partial(berezutskaya_subject, root, k) for k, _ in items]


def berezutskaya_subject(root, key):
    rel = key[len("ds003688/"):]
    sub = rel.split("/")[0]
    path = os.path.join(root, "cache", sub)

    def build():
        base = rel[:-len("_ieeg.eeg")]
        for ext in ("_ieeg.eeg", "_ieeg.vhdr", "_ieeg.vmrk", "_channels.tsv"):
            openneuro("ds003688", base + ext, root)
        events = re.sub(r"_acq-[^_]+", "", base) + "_events.tsv"
        ev = pd.read_csv(openneuro("ds003688", events, root), sep="\t")
        ch = pd.read_csv(os.path.join(root, base + "_channels.tsv"), sep="\t")
        good = ch[(ch.status == "good") & ch.type.str.upper().isin(["ECOG", "SEEG"])].name.tolist()
        raw = mne.io.read_raw_brainvision(os.path.join(root, base + "_ieeg.vhdr"), preload=False)
        fs = raw.info["sfreq"]
        blocks = ev[ev.trial_type.isin(["music", "speech"])].reset_index(drop=True)
        X, y, run = [], [], []
        for i, b in blocks.iterrows():
            seg = raw.get_data(picks=good, start=int(b.onset * fs), stop=int((b.onset + 30) * fs)) * 1e6
            if fs > 512:
                seg = resample_poly(seg, 512, int(fs), axis=-1)
            for w in range(15):  # 15 non-overlapping 2-s windows per 30-s block
                X.append(seg[:, w * 1024:(w + 1) * 1024])
                y.append(b.trial_type)
                run.append(str(min(i // 2, 5)))  # block pairs (music, speech); the 13th block joins pair 5
        X = np.stack(X).astype(np.float32)
        return [X], np.asarray(y), meta_table(len(X), sub, run)
    def load():
        (X,), y, meta = cached(path, build)
        return X, y, meta
    return load()


# ================================================================== Podcast (ds005574)

def podcast_words(root):
    tr = pd.read_csv(openneuro("ds005574", "stimuli/en_core_web_lg/transcript.tsv", root), sep="\t", index_col=0)
    import h5py
    with h5py.File(openneuro("ds005574", "stimuli/en_core_web_lg/features.hdf5", root)) as f:
        vec = f["vectors"][:]
    if len(vec) != len(tr):
        raise ValueError(f"{len(vec)} vectors for {len(tr)} transcript tokens")
    tr = tr.assign(row=np.arange(len(tr))).dropna(subset=["start"])
    words = tr.groupby("word_idx").agg(start=("start", "first"), rows=("row", list))
    W = np.stack([vec[r].mean(0) for r in words.rows]).astype(np.float32)
    return W, words.start.values


def podcast_subject(root, sub, W, onsets):
    def build():
        f = openneuro("ds005574", f"derivatives/ecogprep/{sub}/ieeg/{sub}_task-podcast_desc-highgamma_ieeg.fif", root)
        raw = mne.io.read_raw_fif(f, preload=True)
        raw.pick("data", exclude="bads")
        x, fs = raw.get_data(), raw.info["sfreq"]
        x = (x - x.mean(1, keepdims=True)) / (x.std(1, keepdims=True) + 1e-12)
        a = (onsets * fs).astype(int)
        keep = a + int(0.5 * fs) < x.shape[1]
        Y = np.stack([x[:, i:i + int(0.5 * fs)].mean(1) for i in a[keep]]).astype(np.float32)
        half = onsets[keep] < onsets.max() / 2
        return [W[keep], Y], np.zeros(len(Y)), meta_table(len(Y), sub, np.where(half, "0", "1"))

    def load():
        (X, Y), _, meta = cached(os.path.join(root, "cache", sub), build)
        return X, Y, meta
    return load


# ================================================================== Chen 2024 (HB02)

CHEN_URL = "https://data.mendeley.com/public-files/datasets/fp4bv9gtwk/files/1360e65e-9f66-49c7-8f42-b0ea9c677a6b/file_downloaded"
SPEECH_LAGS = range(-20, 21, 5)  # +-160 ms at 125 Hz (Chen), +-200 ms at 100 Hz (Verwoert)


def chen_load(root):
    def build():
        import h5py
        with h5py.File(download(CHEN_URL, os.path.join(root, "HB02.h5"))) as f:
            E = f["ecog_alldataset"][:].astype(np.float32)
            S = f["wave_re_spec_alldataset"][:].astype(np.float32)
            a, b = f["start_ind_re_valid_alldataset"][:], f["end_ind_re_valid_alldataset"][:]
            n_test = int(f["TestNum_cum"][0])
        frames = np.concatenate([np.arange(i, j) for i, j in zip(a, b)])
        trial = np.concatenate([[k] * (j - i) for k, (i, j) in enumerate(zip(a, b))])
        X = lagged(E, SPEECH_LAGS)[frames]
        run = np.where(trial >= len(a) - n_test, "test", "train")
        return [X, S[frames]], np.zeros(len(X)), meta_table(len(X), "HB02", run, trial=trial.astype(str))
    (X, Y), _, meta = cached(os.path.join(root, "cache", "hb02"), build)
    return X, Y, meta


def trial_pcc_scorer(est, X, Y, meta):
    """Mean over test trials of the Pearson r between the true and the decoded spectrogram (flattened)."""
    P = np.asarray(est.predict(X))
    Y = np.asarray(Y)
    r = [np.corrcoef(Y[i].ravel(), P[i].ravel())[0, 1] for i in meta.groupby("trial").indices.values()]
    return {"pcc": np.nanmean(r), "pearson_r_bins": np.nanmean(corr_cols(Y, P))}


# ================================================================== Verwoert / Herff SingleWordProductionDutch

VERWOERT_URL = "https://osf.io/download/g6q5m/"


def high_gamma_frames(eeg, fs, win=0.05, shift=0.01):
    """Reference pipeline (Verwoert et al.): 70-170 Hz band, 100/150 Hz notches, Hilbert envelope, 50-ms windows, 10-ms shift."""
    from scipy.signal import detrend, filtfilt, iirnotch
    x = detrend(np.asarray(eeg, dtype=np.float64), axis=0)
    x = sosfiltfilt(butter(4, [70, 170], "band", fs=fs, output="sos"), x, axis=0)
    for f0 in (100, 150):
        b, a = iirnotch(f0, 30, fs)
        x = filtfilt(b, a, x, axis=0)
    x = np.abs(hilbert(x, axis=0))
    n = int((len(x) / fs - win) / shift)
    return np.stack([x[int(i * shift * fs):int(i * shift * fs + win * fs)].mean(0) for i in range(n)]).astype(np.float32)


def mel_frames(audio, fs, n_frames, win=0.05, shift=0.01, n_mels=23, fs_out=16000):
    """Log-mel spectrogram (23 bins) of 50-ms Hann windows with 10-ms shift at 16 kHz."""
    a = resample_poly(np.asarray(audio, dtype=np.float64), fs_out, int(fs))
    a = a / (np.abs(a).max() + 1e-12)
    w, h = int(win * fs_out), int(shift * fs_out)
    spec = np.abs(np.fft.rfft(np.stack([a[i * h:i * h + w] * np.hanning(w) for i in range(n_frames)]), axis=1)) ** 2
    hz = lambda m: 700 * (10 ** (m / 2595) - 1)
    edges = hz(np.linspace(0, 2595 * np.log10(1 + fs_out / 2 / 700), n_mels + 2))
    f = np.fft.rfftfreq(w, 1 / fs_out)
    fb = np.stack([np.clip(np.minimum((f - lo) / (c - lo), (hi - f) / (hi - c)), 0, None)
                   for lo, c, hi in zip(edges, edges[1:], edges[2:])])
    return np.log(spec @ fb.T + 1e-10).astype(np.float32)


def verwoert_subjects(root, quick):
    z = []

    def load(sub):
        def build():
            import h5py
            path = os.path.join(root, f"{sub}_task-wordProduction_ieeg.nwb")
            if not os.path.exists(path):
                z[:] = z or [open_zip(VERWOERT_URL, "", True)]
                extract(z[0], f"SingleWordProductionDutch-iBIDS/{sub}/ieeg/{sub}_task-wordProduction_ieeg.nwb", path)
            with h5py.File(path) as f:
                eeg = f["acquisition/iEEG/data"][:]
                audio = f["acquisition/Audio/data"][:]
            F = high_gamma_frames(eeg, 1024)
            M = mel_frames(audio, 48000, len(F))
            X = lagged(F, SPEECH_LAGS)
            return [X, M], np.zeros(len(X)), meta_table(len(X), sub, contiguous_runs(len(X), 10))
        (X, M), _, meta = cached(os.path.join(root, "cache", sub), build)
        return X, M, meta
    return [partial(load, f"sub-{i:02d}") for i in ([1] if quick else range(1, 11))]


# ================================================================== Mayo / FNUSA

MAYO_FNUSA = {"Mayo": "https://ndownloader.figshare.com/files/21359865",
              "FNUSA": "https://ndownloader.figshare.com/files/21359868"}
HFO_BANDS = ((1, 4), (4, 8), (8, 13), (13, 30), (30, 80), (80, 250), (250, 500), (500, 1000))


def mayo_fnusa(root, quick, per_class=50):
    def build():
        X, F, y, inst = [], [], [], []
        for name, url in MAYO_FNUSA.items():
            local = os.path.join(root, f"Dataset_{name}.zip")
            # quick: ~60-kB clips read over HTTP ranges, so a small read buffer (open_zip's 1 MB would fetch 1 MB per clip)
            z = zipfile.ZipFile(io.BufferedReader(_HTTPFile(url), 64 << 10)) if quick and not os.path.exists(local) \
                else open_zip(url, local, False)
            csv = next(n for n in z.namelist() if n.endswith("segments.csv"))
            df = pd.read_csv(io.BytesIO(z.read(csv)))
            df = df[~df.category_name.str.startswith("powerline")]
            if quick:
                df = pd.concat([g.sample(min(len(g), per_class), random_state=0) for _, g in df.groupby("category_name")])
            folder = os.path.dirname(csv)
            for sid, cat in zip(df.segment_id, df.category_name):
                x = sio.loadmat(io.BytesIO(z.read(f"{folder}/{sid}.mat")))["data"].astype(np.float32)[:1, :15000]
                F.append(bandpower(x[None], 5000, HFO_BANDS)[0])
                X.append(resample_poly(x, 1, 5, axis=-1))
                y.append(cat)
                inst.append(name)
        return [np.stack(X), np.stack(F)], np.asarray(y), pd.DataFrame(dict(subject="all", session=inst, run="0"))
    (X, F), y, meta = cached(os.path.join(root, "cache", "quick" if quick else "all"), build)
    return X, F, y, meta


def run_mayo_fnusa(results, args, root):
    X, F, y, meta = mayo_fnusa(root, args.quick)
    for tr, te in (("FNUSA", "Mayo"), ("Mayo", "FNUSA")):
        name = f"MayoFNUSA ({tr}->{te})"
        if not wanted(args, name, "MayoFNUSA"):
            continue
        keep = np.flatnonzero(meta.session.isin([tr, te]).values)
        m = meta.iloc[keep].assign(session=np.where(meta.session.values[keep] == tr, "train", "test")).reset_index(drop=True)
        if use(args, "BandPower+LR"):
            pipe = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, class_weight="balanced"))
            _safe(evaluate, PHASE, results, name, "standard", "BandPower+LR", classical(pipe), F[keep], y[keep], m,
                  args.seeds, needs_seed=False)
        if use(args, "ResNet1D"):
            # ponytail: X[keep] copies the 1-kHz clips into RAM (~1.4 GB for FNUSA); use a lazy row view if that bites
            _safe(evaluate, PHASE, results, name, "standard", "ResNet1D", deep(resnet1d, epochs=epochs(args), **DEEP),
                  np.asarray(X[keep]), y[keep], m, args.seeds)


# ================================================================== HUP SOZ (ds004100)

def hup_channels(root, quick):
    part = pd.read_csv(openneuro("ds004100", "participants.tsv", root), sep="\t")
    rows = part.head(4) if quick else part
    feats, y, subj = [], [], []
    for sid in rows.participant_id:
        try:  # first interictal run of the subject
            edf = sorted(k for k, _ in s3_keys(f"ds004100/{sid}/") if "task-interictal" in k and k.endswith("_ieeg.edf"))[0]
            base = edf[len("ds004100/"):-len("_ieeg.edf")]
            ch = pd.read_csv(openneuro("ds004100", base + "_channels.tsv", root), sep="\t")
            raw = mne.io.read_raw_edf(openneuro("ds004100", base + "_ieeg.edf", root), preload=False)
        except Exception as e:
            log_error(PHASE, f"HUP-SOZ {sid}: {type(e).__name__}: {e}")
            continue
        ch = ch[(ch.status == "good") & ch.type.isin(["ECOG", "SEEG"]) & ch.name.isin(raw.ch_names)]
        if ch.empty:
            continue
        x = raw.get_data(picks=ch.name.tolist()) * 1e6
        fs = raw.info["sfreq"]
        n = x.shape[1] // int(fs) // 10 * 10
        wins = x[:, :n * int(fs)].reshape(len(ch), -1, int(fs)).transpose(1, 0, 2)  # 1-s windows
        f = bandpower(wins, fs, ECOG_BANDS[:-1] + ((70, 150),)).reshape(len(wins), len(ch), -1).mean(0)
        f = (f - f.mean(0)) / (f.std(0) + 1e-6)  # z-scored across the patient's channels
        feats.append(f)
        y += ch.status_description.fillna("").str.contains("soz").astype(int).tolist()
        subj += [sid] * len(ch)
    return np.concatenate(feats).astype(np.float32), np.asarray(y), pd.DataFrame(dict(subject=subj, session="0", run="0"))


def run_hup(results, args, root):
    X, y, meta = hup_channels(root, args.quick)
    models = {"BandPower+LR": make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, class_weight="balanced")),
              "BandPower+RF": RandomForestClassifier(300, class_weight="balanced", n_jobs=-1, random_state=0)}
    for mname, pipe in models.items():
        if use(args, mname):
            _safe(evaluate, PHASE, results, "HUP-SOZ", "cross_subject", mname, classical(pipe), X, y, meta, args.seeds,
                  needs_seed=False)


# ================================================================== SWEC-ETHZ short-term

SWEC_URL = "https://iis-people.ee.ethz.ch/~ieeg/BioCAS2018/dataset/{}.zip"
SWEC_PARTS = ["ID1", "ID2", "ID3", "ID4a", "ID4b", "ID5", "ID6", "ID7", "ID8", "ID9", "ID10", "ID11", "ID12",
              "ID13a", "ID13b", "ID14a", "ID14b", "ID15", "ID16"]


def read_mat(f):
    """MATLAB file of either version -> dict of arrays."""
    try:
        return sio.loadmat(f)
    except NotImplementedError:  # v7.3 (HDF5); h5py returns arrays transposed
        import h5py
        with h5py.File(f) as h:
            return {k: np.asarray(h[k]).T for k in h.keys() if isinstance(h[k], h5py.Dataset)}


def swec_subjects(root, quick):
    patients = {}
    for p in (["ID3"] if quick else SWEC_PARTS):
        patients.setdefault(re.sub(r"[ab]$", "", p), []).append(p)

    def load(pid, parts):
        def build():
            X, y, sess = [], [], []
            files = []
            for p in parts:
                z = open_zip(SWEC_URL.format(p), os.path.join(root, f"{p}.zip"), True)
                files += [(z, n) for n in z.namelist() if n.endswith(".mat")]
            files.sort(key=lambda zn: int(re.search(r"Sz(\d+)", zn[1]).group(1)))
            for k, (z, n) in enumerate(files):
                eeg = read_mat(io.BytesIO(z.read(n)))["EEG"].astype(np.float32)
                eeg = eeg if eeg.shape[0] > eeg.shape[1] else eeg.T  # documented as (time, channels)
                w = len(eeg) // 512
                win = eeg[:w * 512].reshape(w, 512, -1).transpose(0, 2, 1)
                t = np.arange(w)
                X.append(win)
                y += np.where((t >= 180) & (t + 1 <= w - 180), "ictal", "nonictal").tolist()
                sess += ["train" if k == 0 else "test"] * w
            X = np.concatenate(X)
            return [X], np.asarray(y), meta_table(len(X), pid, "0", session=sess)
        (X,), y, meta = cached(os.path.join(root, "cache", pid), build)
        return X, y, meta
    return [partial(load, pid, parts) for pid, parts in patients.items()]


# ================================================================== Bellier music (Zenodo)

BELLIER = "https://zenodo.org/api/records/7876019/files/{}/content"
BELLIER_LAGS = range(0, 76, 5)  # neural frames 0-750 ms after the stimulus frame (100 Hz)


def bellier_subjects(root, quick):
    def load(p):
        def build():
            S = sio.loadmat(download(BELLIER.format("thewall1_stim32.mat"), os.path.join(root, "thewall1_stim32.mat"), True))["stim32"]
            E = sio.loadmat(download(BELLIER.format(f"P{p}_HFA_data.mat"), os.path.join(root, f"P{p}_HFA_data.mat"), True))["ecog"]
            X = lagged(E.astype(np.float32), BELLIER_LAGS)
            return [X, S.astype(np.float32)], np.zeros(len(X)), meta_table(len(X), f"P{p}", contiguous_runs(len(X), 5))
        (X, S), _, meta = cached(os.path.join(root, "cache", f"P{p}"), build)
        return X, S, meta
    return [partial(load, p) for p in ([1, 27] if quick else range(1, 30))]


# ================================================================== Kaggle seizure sets (gated)

def hour_folds(groups, y, k=5):
    """Assign each clip a fold id (0..k-1), keeping clip groups (1-h sequences, seizures) together."""
    k = max(2, min([k] + [len(np.unique(groups[y == c])) for c in np.unique(y)]))
    fold = np.zeros(len(y), int)
    for i, (_, te) in enumerate(StratifiedGroupKFold(k, shuffle=True, random_state=0).split(y, y, groups)):
        fold[te] = i
    return fold.astype(str)


def mat_struct(path):
    m = sio.loadmat(path, squeeze_me=True, struct_as_record=False)
    return next(v for k, v in m.items() if not k.startswith("__"))


def clip_features(x, fs, seconds=60):
    """Log band power per channel (median over 1-min chunks of a long clip)."""
    n = int(fs * seconds)
    chunks = [x[:, i:i + n] for i in range(0, x.shape[1] - n + 1, n)] or [x]
    return np.median(np.stack([bandpower(c[None], fs, ((1, 4), (4, 8), (8, 13), (13, 30), (30, 70), (70, 180)))[0]
                               for c in chunks]), 0)


def kaggle_prediction_subjects(folder, kind, quick, cache):
    """AES 2014 (`Dog_1/Dog_1_preictal_segment_0001.mat`) or Melbourne 2016 (`train_1/1_12_1.mat`) training clips.

    Clips are grouped into their 1-h sequences of six; folds keep sequences together."""
    if kind == "aes":
        subjects = sorted(d for d in os.listdir(folder) if re.match(r"(Dog|Patient)_\d+$", d))
    else:
        subjects = sorted(d for d in os.listdir(folder) if re.match(r"train_\d+$", d))
    subjects = subjects[:2] if quick else subjects

    def load(s):
        def build():
            rows = []
            for f in sorted(glob.glob(os.path.join(folder, s, "*.mat"))):
                b = os.path.basename(f)
                if kind == "aes":
                    m = re.search(r"_(interictal|preictal)_segment_(\d+)\.mat$", b)
                    if not m:
                        continue
                    label, num = m.group(1), int(m.group(2))
                else:
                    m = re.match(r"\d+_(\d+)_([01])\.mat$", b)
                    if not m:
                        continue
                    label, num = ("preictal" if m.group(2) == "1" else "interictal"), int(m.group(1))
                rows.append((f, label, num))
            if quick:
                rows = [r for r in rows if r[1] == "preictal"][:12] + [r for r in rows if r[1] == "interictal"][:24]
            F, y, g = [], [], []
            for f, label, num in rows:
                st = mat_struct(f)
                if kind == "aes":
                    x, fs = np.asarray(st.data, dtype=np.float32), float(st.sampling_frequency)
                else:
                    x, fs = np.asarray(st.data, dtype=np.float32).T, float(st.iEEGsamplingRate)
                    if not np.any(x):  # all-zero dropout clips
                        continue
                F.append(clip_features(x, fs))
                y.append(label)
                g.append(f"{label}{(num - 1) // 6}")
            y, g = np.asarray(y), np.asarray(g)
            return [np.stack(F)], y, meta_table(len(y), s, hour_folds(g, y))
        (F,), y, meta = cached(os.path.join(cache, s), build)
        return F, y, meta
    return [partial(load, s) for s in subjects]


def kaggle_detection_subjects(folder, quick, cache, fs_out=400):
    subjects = sorted(d for d in os.listdir(folder) if re.match(r"(Dog|Patient)_\d+$", d))[:2 if quick else None]

    def load(s):
        def build():
            X, y, g = [], [], []
            for kind in ("ictal", "interictal"):
                files = glob.glob(os.path.join(folder, s, f"{s}_{kind}_segment_*.mat"))
                files.sort(key=lambda f: int(re.search(r"_(\d+)\.mat$", f).group(1)))
                if quick:  # consecutive ictal clips (seizure grouping needs them); interictal spread over the record
                    files = files[:60] if kind == "ictal" else files[::max(1, len(files) // 60)][:60]
                seizure = -1
                for f in files:
                    num = int(re.search(r"_(\d+)\.mat$", f).group(1))
                    m = sio.loadmat(f, squeeze_me=True)
                    x, fs = np.asarray(m["data"], dtype=np.float32), float(m["freq"])
                    x = resample_poly(x, fs_out, int(round(fs)), axis=-1)[:, :fs_out]
                    if x.shape[1] < fs_out:
                        x = np.pad(x, ((0, 0), (0, fs_out - x.shape[1])))
                    if kind == "ictal":
                        lat = float(m["latency"])
                        if lat == 0 or seizure < 0:  # latency restarts at 0 for each seizure
                            seizure += 1
                        y.append("early" if lat <= 15 else "late")  # Kaggle: early = within 15 s of onset
                        g.append(f"sz{seizure}")
                    else:
                        y.append("interictal")
                        g.append(f"ii{(num - 1) // 60}")
                    X.append(x)
            y, g = np.asarray(y), np.asarray(g)
            fold = hour_folds(g, np.where(y == "interictal", "interictal", "ictal"))
            return [np.stack(X)], y, meta_table(len(y), s, fold)
        (X,), y, meta = cached(os.path.join(cache, s), build)
        return X, y, meta
    return [partial(load, s) for s in subjects]


def kaggle_detection_scorer(est, X, y, meta):
    p = est.predict_proba(X)
    cls = list(est.classes_)
    early = p[:, cls.index("early")]
    seizure = early + p[:, cls.index("late")]
    out = {}
    if len(np.unique(y != "interictal")) == 2:
        out["auc_seizure"] = roc_auc_score(y != "interictal", seizure)
    if len(np.unique(y == "early")) == 2:
        out["auc_early"] = roc_auc_score(y == "early", early)
    if len(out) == 2:
        out["kaggle_score"] = (out["auc_seizure"] + out["auc_early"]) / 2
    return out


# ================================================================== RAM free recall (gated, BIDS)

RAM_BANDS = tuple(zip(np.geomspace(3, 180, 9)[:-1], np.geomspace(3, 180, 9)[1:]))


def ram_subjects(folder, quick, cache):
    runs = sorted(glob.glob(os.path.join(folder, "sub-*", "ses-*", "ieeg", "*_task-FR1_acq-bipolar_ieeg.edf")))
    by_sub = {}
    for f in runs:
        by_sub.setdefault(os.path.basename(f).split("_")[0], []).append(f)
    items = list(by_sub.items())[:2] if quick else list(by_sub.items())

    def load(sub, files):
        def build():
            F, y, sess = [], [], []
            for f in files:
                ev = pd.read_csv(f.replace("_acq-bipolar_ieeg.edf", "_events.tsv"), sep="\t")
                r = ev[ev.trial_type == "REC_WORD"]
                rec = set(zip(r.list, r.item_name))
                words = ev[ev.trial_type == "WORD"]
                raw = mne.io.read_raw_edf(f, preload=False)
                fs = raw.info["sfreq"]
                x = raw.get_data() * 1e6
                n = int(1.6 * fs)
                ok = [(int(s), (l, w) in rec) for s, l, w in zip(words["sample"], words.list, words.item_name) if s + n <= x.shape[1]]
                ep = np.stack([x[:, s:s + n] for s, _ in ok]).astype(np.float32)
                F.append(bandpower(ep, fs, RAM_BANDS))
                y += ["recalled" if r else "forgotten" for _, r in ok]
                sess += [os.path.basename(f).split("_")[1]] * len(ok)
            return [np.concatenate(F)], np.asarray(y), meta_table(len(y), sub, "0", session=sess)
        (F,), y, meta = cached(os.path.join(cache, sub), build)
        return F, y, meta
    return [partial(load, s, fs) for s, fs in items]


# ================================================================== runner

def run(results, args):
    root = os.path.join(args.data_dir, "ecog")
    quick = args.quick
    lr_only = lambda: make_pipeline(StandardScaler(), LogisticRegression(C=0.1, max_iter=2000, class_weight="balanced"))

    if wanted(args, "BCICIV-4"):
        subs = attempt("BCICIV-4", bciiv4_subjects, root)
        if subs:
            run_fingers(results, args, "BCICIV-4", subs, (0, 1, 2, 4))  # ring finger (4th) excluded

    if wanted(args, "Miller-FingerFlex"):
        subs = attempt("Miller-FingerFlex", miller_subjects, root, quick)
        if subs:
            run_fingers(results, args, "Miller-FingerFlex", subs, range(5))

    if wanted(args, "BrainTreebank-Neuroprobe", "BrainTreebank"):
        folder = args.paths.get("braintreebank")
        if quick and not folder:
            print(f"\n[{PHASE}] BrainTreebank-Neuroprobe: skipped in --quick (3.6-8 GB per session); "
                  "pass --path braintreebank=FOLDER")
        else:
            attempt("BrainTreebank-Neuroprobe", run_neuroprobe, results, args,
                    folder or os.path.join(root, "braintreebank"), quick)

    if wanted(args, "Berezutskaya-SpeechMusic"):
        subs = attempt("Berezutskaya-SpeechMusic", berezutskaya_subjects, os.path.join(root, "ds003688"), quick)
        subs = guarded("Berezutskaya-SpeechMusic", subs or [])
        for mname, make in (("BandPower+LR", classical(bp_lr(512))), ("ResNet1D", deep(resnet1d, epochs=epochs(args), **DEEP))):
            if subs and use(args, mname):
                _safe(per_subject, PHASE, results, "Berezutskaya-SpeechMusic", "leave_one_run_out", mname, make, subs,
                      args.seeds, needs_seed=mname == "ResNet1D")

    if wanted(args, "Podcast-ECoG"):
        d = os.path.join(root, "ds005574")
        words = attempt("Podcast-ECoG", podcast_words, d)
        if words is not None:
            subs = guarded("Podcast-ECoG", [podcast_subject(d, f"sub-{i:02d}", *words) for i in ([8] if quick else range(1, 10))])
            if subs and use(args, "WordVec+Ridge"):
                pipe = make_pipeline(StandardScaler(), RidgeCV(alphas=np.logspace(0, 6, 7), cv=KFold(5)))
                _safe(per_subject, PHASE, results, "Podcast-ECoG", "leave_one_run_out", "WordVec+Ridge", classical(pipe),
                      subs, args.seeds, scorer=mean_r_scorer, needs_seed=False)

    if wanted(args, "Chen2024-HB02"):
        data = attempt("Chen2024-HB02", chen_load, os.path.join(root, "chen2024"))
        if data is not None and use(args, "HG+Ridge"):
            _safe(evaluate_custom, PHASE, results, "Chen2024-HB02", "standard", "HG+Ridge", classical(ridge()), *data,
                  args.seeds, trial_pcc_scorer, needs_seed=False)

    if wanted(args, "Verwoert-SingleWordDutch"):
        subs = guarded("Verwoert-SingleWordDutch", verwoert_subjects(os.path.join(root, "verwoert"), quick))
        if subs and use(args, "HG+PCA+LinReg"):
            pipe = make_pipeline(flat(), StandardScaler(), PCA(50), LinearRegression())
            _safe(per_subject, PHASE, results, "Verwoert-SingleWordDutch", "leave_one_run_out", "HG+PCA+LinReg",
                  classical(pipe), subs, args.seeds, scorer=mean_r_scorer, needs_seed=False)

    if wanted(args, "MayoFNUSA", "MayoFNUSA (FNUSA->Mayo)", "MayoFNUSA (Mayo->FNUSA)"):
        attempt("MayoFNUSA", run_mayo_fnusa, results, args, os.path.join(root, "mayo_fnusa"))

    if wanted(args, "HUP-SOZ"):
        attempt("HUP-SOZ", run_hup, results, args, os.path.join(root, "ds004100"))

    if wanted(args, "Fragility"):
        print(f"\n[{PHASE}] Fragility (ds003029): not run (no SOZ labels in the public BIDS channels.tsv; "
              "marker names differ by centre)")

    if wanted(args, "SWEC-ETHZ-short"):
        print(f"\n[{PHASE}] SWEC-ETHZ-short")
        subs = guarded("SWEC-ETHZ-short", swec_subjects(os.path.join(root, "swec_short"), quick))
        for mname, make in (("BandPower+LR", classical(bp_lr(512, C=1.0))), ("ResNet1D", deep(resnet1d, epochs=epochs(args), **DEEP))):
            if subs and use(args, mname):
                _safe(per_subject, PHASE, results, "SWEC-ETHZ-short", "standard", mname, make, subs, args.seeds,
                      needs_seed=mname == "ResNet1D")

    if wanted(args, "Bellier-PinkFloyd"):
        print(f"\n[{PHASE}] Bellier-PinkFloyd")
        subs = guarded("Bellier-PinkFloyd", bellier_subjects(os.path.join(root, "bellier"), quick))
        if subs and use(args, "HFA+Ridge"):
            _safe(per_subject, PHASE, results, "Bellier-PinkFloyd", "leave_one_run_out", "HFA+Ridge", classical(ridge()),
                  subs, args.seeds, scorer=mean_r_scorer, needs_seed=False)

    for key, name, kind in (("kaggle_aes2014", "Kaggle-AES2014", "aes"), ("kaggle_melbourne", "Kaggle-Melbourne2016", "melb")):
        if wanted(args, name) and (folder := gated(args, key, name)):
            print(f"\n[{PHASE}] {name}")
            subs = guarded(name, kaggle_prediction_subjects(folder, kind, quick, os.path.join(root, key)))
            if subs and use(args, "BandPower+LR"):
                _safe(per_subject, PHASE, results, name, "leave_one_run_out", "BandPower+LR", classical(lr_only()), subs,
                      args.seeds, needs_seed=False)

    if wanted(args, "Kaggle-UPennMayo") and (folder := gated(args, "kaggle_upenn_mayo", "Kaggle-UPennMayo")):
        print(f"\n[{PHASE}] Kaggle-UPennMayo")
        subs = guarded("Kaggle-UPennMayo", kaggle_detection_subjects(folder, quick, os.path.join(root, "kaggle_upenn_mayo")))
        for mname, make in (("BandPower+LR", classical(bp_lr(400, ((1, 4), (4, 8), (8, 13), (13, 30), (30, 70), (70, 180)), C=1.0))),
                            ("ResNet1D", deep(resnet1d, epochs=epochs(args), **DEEP))):
            if subs and use(args, mname):
                _safe(per_subject, PHASE, results, "Kaggle-UPennMayo", "leave_one_run_out", mname, make, subs, args.seeds,
                      scorer=kaggle_detection_scorer, needs_seed=mname == "ResNet1D")

    if wanted(args, "RAM-FR1") and (folder := gated(args, "ram", "RAM-FR1")):
        print(f"\n[{PHASE}] RAM-FR1")
        subs = guarded("RAM-FR1", ram_subjects(folder, quick, os.path.join(root, "ram")))
        for protocol in ("cross_session", "within_session:5"):
            if subs and use(args, "BandPower+LR"):
                _safe(per_subject, PHASE, results, "RAM-FR1", protocol, "BandPower+LR", classical(lr_only()), subs,
                      args.seeds, needs_seed=False)
