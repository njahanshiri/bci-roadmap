"""ECG benchmarks (phase 9): beat, rhythm, diagnostic, apnea, stress and Chagas tasks.

Source of truth for protocols and published numbers: projects/emg-eog-ecg/ecg/DATASETS.md.
PTB-XL superdiagnostic runs in other.py (phase 5); here only the other five Strodthoff tasks.

| Dataset (name in results) | How it is obtained | Protocol(s) | Models | Tested here |
|---|---|---|---|---|
| MIT-BIH Arrhythmia (`MITBIH`) | auto-download, PhysioNet per record | `standard` = de Chazal inter-patient DS1 -> DS2 (44 records, paced excluded); `within_session:5` = intra-patient random beat 5-fold (leaky, flagged) | RR+Morph+HGB, BeatCNN, ResNet1D | yes, quick (2+2 records) |
| INCART (`INCART`) | auto-download, PhysioNet per record | `cross_subject` (patients from the header; GroupKFold 5) | RR+Morph+HGB, BeatCNN, ResNet1D | yes, quick (2 patients) |
| PTB Diagnostic (`PTB`) | auto-download, PhysioNet per record | `cross_subject`, MI vs healthy control, 10-s windows, patient-grouped | Features+HGB, ResNet1D | yes, quick (6 patients) |
| PTB-XL all/diag/subdiag/form/rhythm (`PTB-XL-<task>`) | auto-download (same folder as other.py) | `standard` = Strodthoff folds 1-8 train, 10 test | Features+LR, ResNet1D | yes, quick (120 records) |
| CinC 2017 AF (`CinC2017`) | auto-download, training zip + REFERENCE-v3 | `within_session:5` = stratified 5-fold CV on the public training set (hidden test not public) | Features+HGB, ResNet1D | yes, quick (40 records) |
| CinC 2021 collection: CPSC 2018, CPSC-Extra, Georgia, Chapman-Shaoxing, Ningbo (`CinC2021`) | auto-download (full zip; quick: per record) | `cross_session` = leave-one-source-out (patient-disjoint); `cross_subject` = 5-fold over records (patient IDs not public) | Features+LR, ResNet1D | yes, quick (6 records per source) |
| CODE-15% -> CODE-test (`CODE-test`) | auto-download, Zenodo | `standard` = train on CODE-15%, test on CODE-test (827) | Features+LR, ResNet1D | yes, quick (part 17 only) |
| Apnea-ECG (`ApneaECG`) | auto-download, PhysioNet per record | `standard` = 35 learning records -> 35 test records, per-minute | Features+HGB, ResNet1D | yes, quick (2+2 records) |
| WESAD chest ECG (`WESAD-binary`, `WESAD-3class`) | auto-download (streams only the S*.pkl members of the remote zip; keeps chest ECG + labels) | `cross_subject` = LOSO over 15 subjects | Features+LDA, ResNet1D | yes, quick (2 subjects) |
| Chagas 2025 public data: CODE-15% + SaMi-Trop + PTB-XL (`Chagas2025`) | auto-download, Zenodo + Challenge labels | `standard` = patient-disjoint hold-out (~20%; hidden test not public) | Features+HGB, ResNet1D | yes, quick |
| MIMIC-IV-ECG (`MIMIC-IV-ECG`) | `--path mimic_iv_ecg=FOLDER` | `standard` = patient-disjoint hold-out; 20 most frequent machine-report statements (no standard benchmark) | Features+LR, ResNet1D | partial: real records in a mock folder |
| HEEDB (`HEEDB`) | `--path heedb=FOLDER` (BDSP credentialed) | `standard` = patient-disjoint hold-out; 20 most frequent 12SL v24 codes (no standard benchmark) | Features+LR, ResNet1D | partial: synthetic folder in the documented layout |

Signals for record-level tasks are resampled to 100 Hz. Large sets (CinC 2021, CODE, Chagas, MIMIC, HEEDB,
Apnea) are written once to float16 memmaps under `<data-dir>/ecg/` and read lazily. Extra package: h5py.
"""
import ast
import glob
import io
import os
import pickle
import re
import urllib.request
import zipfile
import zlib
from fractions import Fraction

import numpy as np
import pandas as pd
import torch
from scipy.signal import butter, find_peaks, resample_poly, sosfiltfilt
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import other
from common import _safe, classical, deep, download, evaluate, log_error, resnet1d, unzip

PHASE = "phase9"
PN = "https://physionet.org/files/"
PN_S3 = "https://physionet-open.s3.amazonaws.com/"  # PhysioNet's open-data mirror; much faster than physionet.org
UA = {"User-Agent": "bci-roadmap-benchmarks"}
GATED_MAX = 200_000  # ponytail: cap on MIMIC-IV-ECG / HEEDB records (memmap size, load time); raise on a big disk


# ------------------------------------------------------------------ helpers

def wanted(args, *names):
    return not args.datasets or any(n in args.datasets for n in names)


def attempt(name, fn, *a):
    print(f"\n[{PHASE}] {name}")
    try:
        return fn(*a)
    except Exception as e:
        log_error(PHASE, f"{name}: could not load ({type(e).__name__}: {e})")


def fit_len(x, n):
    """Crop or zero-pad the last axis to n samples."""
    x = x[..., :n]
    return np.pad(x, [(0, 0)] * (x.ndim - 1) + [(0, n - x.shape[-1])])


def resample(x, fs_in, fs_out=100):
    f = Fraction(int(fs_out), int(round(fs_in))).limit_denominator(1000)
    return resample_poly(x, f.numerator, f.denominator, axis=-1) if f != 1 else x


def holdout(ids):
    """Patient-disjoint split: patients whose id hashes to 0 mod 5 (~20%) are test."""
    return np.array(["test" if zlib.crc32(str(i).encode()) % 5 == 0 else "train" for i in ids])


def fetch(db, root, names, exts, base=PN_S3):
    for n in names:
        for e in exts:
            download(f"{base}{db}/{n}.{e}", os.path.join(root, f"{n}.{e}"), quiet=True)


class Rows:
    """Lazy row subset of a memmap. evaluate() indexes X[train_idx], which on a plain memmap
    would copy every training row into RAM; this keeps it on disk until the loader asks for a row."""

    def __init__(self, a, idx=None):
        self.a, self.idx = a, np.arange(len(a)) if idx is None else np.asarray(idx)

    def __len__(self):
        return len(self.idx)

    @property
    def shape(self):
        return (len(self.idx), *self.a.shape[1:])

    def __getitem__(self, i):
        j = self.idx[i]
        return Rows(self.a, j) if isinstance(i, np.ndarray) else np.asarray(self.a[j])


def cached(path, n, shape, rows):
    """Write records once into a float16 .npy memmap (at most n rows) plus a .csv table; later runs reuse both.

    rows yields (signal, info dict), or (None, None) for a record that failed to load.
    """
    if not os.path.exists(path + ".done"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        X = np.lib.format.open_memmap(path + ".npy", "w+", np.float16, (n, *shape))
        info = []
        for x, row in rows:
            if x is not None:
                X[len(info)] = np.clip(np.nan_to_num(x), -6e4, 6e4)
                info.append(row)
        X.flush()
        del X
        pd.DataFrame(info).to_csv(path + ".csv", index=False)
        open(path + ".done", "w").close()
    table = pd.read_csv(path + ".csv", low_memory=False)
    return np.load(path + ".npy", mmap_mode="r")[:len(table)], table


class HttpFile(io.RawIOBase):
    """Seekable read-only file over HTTP range requests: lets zipfile pull single members of a remote zip."""

    def __init__(self, url):
        r = urllib.request.urlopen(urllib.request.Request(url, headers={"Range": "bytes=0-0", **UA}), timeout=120)
        self.url, self.size, self.pos = r.geturl(), int(r.headers["Content-Range"].rsplit("/", 1)[1]), 0

    def readable(self):
        return True

    def seekable(self):
        return True

    def tell(self):
        return self.pos

    def seek(self, off, whence=0):
        self.pos = (off, self.pos + off, self.size + off)[whence]
        return self.pos

    def readinto(self, b):
        n = min(len(b), self.size - self.pos)
        if n <= 0:
            return 0
        req = urllib.request.Request(self.url, headers={"Range": f"bytes={self.pos}-{self.pos + n - 1}", **UA})
        data = urllib.request.urlopen(req, timeout=300).read()
        b[:len(data)] = data
        self.pos += len(data)
        return len(data)


# ------------------------------------------------------------------ features

def rpeaks(x, fs):
    """Energy QRS detector: 5-15 Hz band-pass, squared slope, 120-ms moving average, peaks >= 0.3 s apart."""
    e = np.diff(sosfiltfilt(butter(2, [5, 15], "band", fs=fs, output="sos"), x)) ** 2
    w = max(1, int(0.12 * fs))
    e = np.convolve(e, np.ones(w) / w, "same")
    return find_peaks(e, distance=int(0.3 * fs), height=0.3 * np.percentile(e, 99))[0]


def record_features(x, fs, lead):
    """HRV of the reference lead; per lead std, 1st/99th percentile, mean |slope| and a 20-point median beat."""
    nz = np.flatnonzero(np.any(x != 0, 0))  # drop zero padding
    x = x[:, nz[0]:nz[-1] + 1] if len(nz) else x
    c, pre, post = len(x), int(0.25 * fs), int(0.45 * fs)
    hrv, beat = [np.nan] * 8, np.full((c, 20), np.nan)
    if x.shape[1] > 2 * fs:
        pk = rpeaks(x[lead], fs)
        rr = np.diff(pk) / fs
        if len(rr) >= 3:
            d = np.diff(rr)
            hrv = [rr.mean(), rr.std(), np.median(rr), rr.min(), rr.max(), np.sqrt(np.mean(d ** 2)),
                   np.mean(np.abs(d) > 0.05), np.median(np.abs(d)) / np.median(rr)]
        pk = pk[(pk >= pre) & (pk + post <= x.shape[1])]
        if len(pk):
            beat = np.median(np.stack([x[:, p - pre:p + post] for p in pk]), 0)[:, np.linspace(0, pre + post - 1, 20).astype(int)]
    return np.r_[hrv, x.std(1), np.percentile(x, [1, 99], axis=1).ravel(), np.abs(np.diff(x, axis=1)).mean(1), beat.ravel()]


def features(X, fs, lead, cache=None, chunk=1024):
    """Features for all records, computed in chunks (works on memmaps); optionally cached as .npy."""
    if cache and os.path.exists(cache):
        return np.load(cache)
    F = np.asarray([record_features(x, fs, lead) for s in range(0, len(X), chunk)
                    for x in np.asarray(X[s:s + chunk], np.float32)], np.float32)
    if cache:
        np.save(cache, F)
    return F


def hgb():
    return make_pipeline(HistGradientBoostingClassifier(class_weight="balanced", random_state=0))


def lr_multilabel():
    return make_pipeline(SimpleImputer(), StandardScaler(), OneVsRestClassifier(LogisticRegression(max_iter=1000), n_jobs=-1))


def beat_cnn(n_chans, n_times, n_outputs):
    """Small CNN for single heartbeats: three conv-BN-ReLU-pool blocks, global average pooling, linear head."""
    nn = torch.nn

    def blk(i, o, k):
        return [nn.Conv1d(i, o, k, padding="same"), nn.BatchNorm1d(o), nn.ReLU(), nn.MaxPool1d(2)]
    return nn.Sequential(*blk(n_chans, 32, 7), *blk(32, 64, 5), *blk(64, 128, 3),
                         nn.AdaptiveAvgPool1d(1), nn.Flatten(), nn.Linear(128, n_outputs))


# ------------------------------------------------------------------ dataset-specific metrics

class Keep:
    """Wraps a model and keeps its last predict_proba output (evaluate() gives fold hooks only hard predictions)."""

    def __init__(self, est):
        self.est = est

    def fit(self, X, y):
        self.est.fit(X, y)
        self.classes_ = getattr(self.est, "classes_", None)
        return self

    def predict(self, X):
        return self.est.predict(X)

    def predict_proba(self, X):
        self.proba_ = np.asarray(self.est.predict_proba(X))
        return self.proba_


def with_hook(make, hook):
    if hook is None:
        return make, None
    box = {}

    def mk(seed):
        box["m"] = Keep(make(seed))
        return box["m"]
    return mk, lambda yt, yp: hook(yt, yp, box["m"])


def ratio(a, b):
    return a / b if b else np.nan


def aami_hook(y, p, m):
    """Sensitivity and positive predictive value for SVEB (S) and VEB (V), as in de Chazal 2004."""
    out = {}
    for c, name in (("S", "sveb"), ("V", "veb")):
        tp = np.sum((y == c) & (p == c))
        out[f"{name}_se"], out[f"{name}_ppv"] = ratio(tp, np.sum(y == c)), ratio(tp, np.sum(p == c))
    return out


def cinc2017_hook(y, p, m):
    """Official CinC 2017 score: mean F1 over Normal, AF and Other (Noisy excluded)."""
    f1 = {c: ratio(2 * np.sum((y == c) & (p == c)), np.sum(y == c) + np.sum(p == c)) for c in "NAO"}
    return {"cinc2017_f1": np.mean(list(f1.values())), "f1_normal": f1["N"], "f1_af": f1["A"], "f1_other": f1["O"]}


def apnea_hook(y, p, m):
    return {"sensitivity": ratio(np.sum((y == "A") & (p == "A")), np.sum(y == "A")),
            "specificity": ratio(np.sum((y == "N") & (p == "N")), np.sum(y == "N"))}


def cinc2021_hook(W, normal):
    """PhysioNet/CinC 2021 challenge score (official weights; outputs thresholded at 0.5)."""
    def score(L, O):
        n = np.maximum(1, (L | O).sum(1))
        return np.sum(W * ((L / n[:, None]).T @ O))

    def hook(y, p, m):
        L, O = y.astype(bool), m.proba_ >= 0.5
        inactive = np.zeros_like(L)
        inactive[:, normal] = True
        best, worst = score(L, L), score(L, inactive)
        return {"challenge_score": ratio(score(L, O) - worst, best - worst)}
    return hook


def chagas_hook(y, p, m):
    """PhysioNet 2025 score: true positive rate among the top 5% of records ranked by probability."""
    prob = m.proba_[:, list(m.classes_).index(1)]
    top = np.argsort(-prob, kind="stable")[:int(0.05 * len(y))]  # ponytail: official averages ties over permutations
    return {"chagas_score": ratio(np.sum(y[top] == 1), np.sum(y == 1))}


def f1_per_class(names):
    def hook(y, p, m):
        O = m.proba_ >= 0.5
        return {f"f1_{c}": ratio(2 * np.sum(y[:, j] * O[:, j]), y[:, j].sum() + O[:, j].sum()) for j, c in enumerate(names)}
    return hook


# ------------------------------------------------------------------ model sets and the runner

def run_models(results, args, dataset, protocols, models, y, meta, multilabel=False, hook=None):
    for protocol in protocols:
        for name, (make, X, seeded) in models.items():
            if args.models and name not in args.models:
                continue
            mk, fh = with_hook(make, hook)
            _safe(evaluate, PHASE, results, dataset, protocol, name, mk, X, y, meta, args.seeds,
                  multilabel=multilabel, needs_seed=seeded, fold_hook=fh)


def record_models(args, X, F, epochs, multilabel=False, clf=None):
    name, pipe = clf or (("Features+LR", lr_multilabel()) if multilabel else ("Features+HGB", hgb()))
    return {name: (classical(pipe), F, False),
            "ResNet1D": (deep(resnet1d, epochs=min(args.epochs, epochs), batch_size=128, lr=1e-3, weight_decay=1e-2,
                              multilabel=multilabel), X, True)}


def beat_models(args, beats, rr):
    """Classical: RR features + downsampled beat. Deep: beat waveform plus the RR features as constant channels."""
    F = np.c_[rr, beats[:, ::max(1, beats.shape[1] // 50)]]
    Xd = np.concatenate([beats[:, None], np.repeat(rr[:, :, None], beats.shape[1], 2)], 1)
    kw = dict(epochs=min(args.epochs, 30), batch_size=256, lr=1e-3, weight_decay=1e-2)
    return {"RR+Morph+HGB": (classical(hgb()), F, False),
            "BeatCNN": (deep(beat_cnn, **kw), Xd, True),
            "ResNet1D": (deep(resnet1d, **kw), Xd, True)}


# ------------------------------------------------------------------ beat datasets: MIT-BIH, INCART

MITDB_DS1 = ["101", "106", "108", "109", "112", "114", "115", "116", "118", "119", "122", "124", "201", "203", "205",
             "207", "208", "209", "215", "220", "223", "230"]
MITDB_DS2 = ["100", "103", "105", "111", "113", "117", "121", "123", "200", "202", "210", "212", "213", "214", "219",
             "221", "222", "228", "231", "232", "233", "234"]
AAMI = {**dict.fromkeys("NLRej", "N"), **dict.fromkeys("AaJS", "S"), **dict.fromkeys("VE", "V"), "F": "F",
        **dict.fromkeys("/fQ", "Q")}


def load_beats(root, db, records, lead):
    """AAMI-labelled beats (-0.25 s to +0.45 s around each annotation) on one lead, plus RR features:
    previous, next, mean of the last 10, previous/local, next/previous, record median."""
    import wfdb
    fetch(db, root, records, ("hea", "dat", "atr"))
    B, R, Y, rec, pat = [], [], [], [], []
    for r in records:
        p = os.path.join(root, r)
        sig = wfdb.rdrecord(p)
        fs, ch = sig.fs, sig.sig_name.index(lead) if lead in sig.sig_name else 0
        x = sosfiltfilt(butter(2, 0.5, "high", fs=fs, output="sos"), sig.p_signal[:, ch])
        ann = wfdb.rdann(p, "atr")
        sym = np.array(ann.symbol)
        keep = np.isin(sym, list(AAMI))
        pos, lab = ann.sample[keep], np.array([AAMI[s] for s in sym[keep]])
        rr = np.diff(pos) / fs
        pre, post = np.r_[rr[0], rr], np.r_[rr, rr[-1]]
        local = pd.Series(pre).rolling(10, min_periods=1).mean().values
        feats = np.c_[pre, post, local, pre / local, post / pre, np.full(len(pre), np.median(rr))]
        a, b = int(0.25 * fs), int(0.45 * fs)
        ok = (pos >= a) & (pos + b <= len(x))
        B.append(np.stack([x[q - a:q + b] for q in pos[ok]]))
        R.append(feats[ok])
        Y.append(lab[ok])
        m = re.search(r"patient (\d+)", " ".join(sig.comments or []))
        rec += [r] * ok.sum()
        pat += [m.group(1) if m else r] * ok.sum()
    return (np.concatenate(B).astype(np.float32), np.concatenate(R).astype(np.float32), np.concatenate(Y),
            np.array(rec), np.array(pat))


def run_mitbih(results, args, root):
    if not wanted(args, "MITBIH"):
        return
    ds1, ds2 = (MITDB_DS1[:2], MITDB_DS2[:2]) if args.quick else (MITDB_DS1, MITDB_DS2)
    data = attempt("MIT-BIH Arrhythmia", load_beats, os.path.join(root, "mitdb"), "mitdb/1.0.0", ds1 + ds2, "MLII")
    if data is None:
        return
    beats, rr, y, rec, _ = (a[::10] for a in data) if args.quick else data  # quick: every 10th beat (CPU-friendly)
    # standard: inter-patient DS1 -> DS2. within_session:5: all beats pooled, stratified 5-fold (intra-patient, leaky)
    meta = pd.DataFrame(dict(subject="all", session="0", run=np.where(np.isin(rec, ds1), "train", "test")))
    run_models(results, args, "MITBIH", ["standard", "within_session:5"], beat_models(args, beats, rr), y, meta,
               hook=aami_hook)


def run_incart(results, args, root):
    if not wanted(args, "INCART"):
        return
    recs = [f"I{i:02d}" for i in (range(1, 6) if args.quick else range(1, 76))]  # quick: patients 1-2
    data = attempt("INCART", load_beats, os.path.join(root, "incartdb"), "incartdb/1.0.0", recs, "II")
    if data is None:
        return
    beats, rr, y, _, pat = (a[::10] for a in data) if args.quick else data
    meta = pd.DataFrame(dict(subject=pat, session="0", run="0"))
    run_models(results, args, "INCART", ["cross_subject"], beat_models(args, beats, rr), y, meta, hook=aami_hook)


# ------------------------------------------------------------------ PTB Diagnostic

def load_ptb(root, quick):
    """12 standard leads, 1000 -> 100 Hz, non-overlapping 10-s windows; MI vs healthy control (from the header)."""
    import wfdb
    db = "ptbdb/1.0.0"
    names = open(download(PN_S3 + db + "/RECORDS", os.path.join(root, "RECORDS"), quiet=True)).read().split()
    if quick:
        controls = open(download(PN_S3 + db + "/CONTROLS", os.path.join(root, "CONTROLS"), quiet=True)).read().split()
        names = controls[:3] + [n for n in names if n not in controls][:3]
    fetch(db, root, names, ("hea",))
    X, y, pat = [], [], []
    for n in names:
        reason = next((c.split(":", 1)[1].strip() for c in wfdb.rdheader(os.path.join(root, n)).comments
                       if c.startswith("Reason for admission")), "")
        label = {"Myocardial infarction": "MI", "Healthy control": "HC"}.get(reason)
        if label is None:
            continue
        fetch(db, root, [n], ("dat",))
        x = resample(wfdb.rdsamp(os.path.join(root, n), channels=list(range(12)))[0].T, 1000)
        for s in range(0, x.shape[1] - 999, 1000):
            X.append(x[:, s:s + 1000])
            y.append(label)
            pat.append(n.split("/")[0])
    return np.asarray(X, np.float32), np.array(y), pd.DataFrame(dict(subject=pat, session="0", run="0"))


def run_ptb(results, args, root):
    if not wanted(args, "PTB"):
        return
    data = attempt("PTB Diagnostic (MI vs healthy)", load_ptb, os.path.join(root, "ptbdb"), args.quick)
    if data is None:
        return
    X, y, meta = data
    run_models(results, args, "PTB", ["cross_subject"], record_models(args, X, features(X, 100, 1), 50), y, meta)


# ------------------------------------------------------------------ PTB-XL (Strodthoff tasks other than superdiag)

def load_ptbxl_all(root, quick):
    """All 100-Hz PTB-XL records with SCP codes and folds; same folder and quick subset as other.load_ptbxl."""
    import wfdb
    found = glob.glob(os.path.join(root, "**", "ptbxl_database.csv"), recursive=True)
    if found:
        base = os.path.dirname(found[0])
    elif quick:
        base = os.path.join(root, "quick")
        for f in ("ptbxl_database.csv", "scp_statements.csv"):
            download(other.PTBXL_FILE.format(f=f), os.path.join(base, f), quiet=True)
    else:
        unzip(download(other.PTBXL_ZIP, os.path.join(root, "ptbxl.zip")), root)
        base = os.path.dirname(glob.glob(os.path.join(root, "**", "ptbxl_database.csv"), recursive=True)[0])
    db = pd.read_csv(os.path.join(base, "ptbxl_database.csv"), index_col="ecg_id")
    scp = pd.read_csv(os.path.join(base, "scp_statements.csv"), index_col=0)
    if quick:
        db = pd.concat([db[db.strat_fold <= 8].head(80), db[db.strat_fold == 10].head(40)])
        for f in db.filename_lr:
            for ext in ("hea", "dat"):
                download(other.PTBXL_FILE.format(f=f"{f}.{ext}"), os.path.join(base, f"{f}.{ext}"), quiet=True)
    X = np.stack([wfdb.rdsamp(os.path.join(base, f))[0].T for f in db.filename_lr]).astype(np.float32)
    return X, db, scp


def ptbxl_labels(db, scp, task):
    """Strodthoff et al. 2021 label sets: all statements, diagnostic, diagnostic subclasses, form, rhythm."""
    codes = db.scp_codes.apply(lambda s: set(ast.literal_eval(s)))
    col = {"diag": "diagnostic", "subdiag": "diagnostic", "form": "form", "rhythm": "rhythm"}.get(task)
    keep = set(scp.index[scp[col] == 1]) if col else None
    sets = codes.apply(lambda cs: cs if keep is None else {scp.diagnostic_subclass[c] if task == "subdiag" else c
                                                            for c in cs if c in keep})
    classes = sorted(set().union(*sets))
    return np.array([[c in s for c in classes] for s in sets], np.float32), classes


def run_ptbxl_tasks(results, args, root):
    tasks = [t for t in ("all", "diag", "subdiag", "form", "rhythm") if wanted(args, "PTB-XL", f"PTB-XL-{t}")]
    if not tasks:
        return
    data = attempt("PTB-XL (all, diag, subdiag, form, rhythm)", load_ptbxl_all, os.path.join(args.data_dir, "ptbxl"),
                   args.quick)
    if data is None:
        return
    X, db, scp = data
    F = features(X, 100, 1)
    for task in tasks:
        Y, _ = ptbxl_labels(db, scp, task)
        ok = (Y.sum(1) > 0) & (db.strat_fold != 9).values  # records with no label in the task are dropped
        run = np.where(db.strat_fold <= 8, "train", "test")[ok]
        meta = pd.DataFrame(dict(subject="all", session="0", run=run))
        run_models(results, args, f"PTB-XL-{task}", ["standard"], record_models(args, X[ok], F[ok], 50, multilabel=True),
                   Y[ok], meta, multilabel=True)


# ------------------------------------------------------------------ PhysioNet/CinC 2017 (AF)

def load_cinc2017(root, quick):
    """Single lead, 300 -> 100 Hz, cropped or zero-padded to 60 s; labels from REFERENCE-v3 (N, A, O, ~)."""
    import wfdb
    base = os.path.join(root, "training2017")
    if not os.path.isdir(base):
        unzip(download(PN_S3 + "challenge-2017/1.0.0/training2017.zip", os.path.join(root, "training2017.zip")), root)
    ref = pd.read_csv(download(PN_S3 + "challenge-2017/1.0.0/training/REFERENCE-v3.csv",
                               os.path.join(root, "REFERENCE-v3.csv"), quiet=True), header=None, names=["rec", "label"])
    if quick:
        ref = ref.groupby("label").head(10)
    X = np.stack([fit_len(resample(wfdb.rdsamp(os.path.join(base, os.path.basename(r)))[0].T, 300), 6000) for r in ref.rec])
    return X.astype(np.float32), ref.label.values


def run_cinc2017(results, args, root):
    if not wanted(args, "CinC2017"):
        return
    data = attempt("PhysioNet/CinC 2017", load_cinc2017, root, args.quick)
    if data is None:
        return
    X, y = data
    meta = pd.DataFrame(dict(subject="all", session="0", run="0"), index=range(len(y)))  # within_session:5 = stratified 5-fold CV
    run_models(results, args, "CinC2017", ["within_session:5"], record_models(args, X, features(X, 100, 0), 50), y, meta,
               hook=cinc2017_hook)


# ------------------------------------------------------------------ PhysioNet/CinC 2021 collection

C21 = "challenge-2021/1.0.3/"
C21_ZIP = "https://physionet.org/content/challenge-2021/get-zip/1.0.3/"
C21_SOURCES = ["cpsc_2018", "cpsc_2018_extra", "georgia", "chapman_shaoxing", "ningbo"]
C21_WEIGHTS = "https://raw.githubusercontent.com/physionetchallenges/evaluation-2021/main/weights.csv"


def c21_paths(root, quick):
    """Full: the whole Challenge zip (not on the S3 mirror), extracting only the five sources. Quick: 6 records per source."""
    if quick:
        paths = []
        for s in C21_SOURCES:
            d = os.path.join(root, "quick", s, "g1")
            names = open(download(f"{PN}{C21}training/{s}/g1/RECORDS", os.path.join(d, "RECORDS"), quiet=True)).read().split()[:6]
            fetch(f"{C21}training/{s}/g1", d, names, ("hea", "mat"), base=PN)
            paths += [os.path.join(d, n) for n in names]
        return paths
    base = os.path.join(root, "full")
    if not os.path.exists(base + ".done"):
        with zipfile.ZipFile(download(C21_ZIP, os.path.join(root, "challenge-2021.zip"))) as z:
            z.extractall(base, [m for m in z.namelist() if any(f"/training/{s}/" in m for s in C21_SOURCES)])
        open(base + ".done", "w").close()
    return sorted(p[:-4] for s in C21_SOURCES for p in glob.glob(os.path.join(base, "**", "training", s, "*", "*.hea"),
                                                                 recursive=True))


def c21_rows(paths):
    import wfdb
    for p in paths:
        try:
            r = wfdb.rdrecord(p)
            dx = next((c.split(":", 1)[1].strip() for c in r.comments if c.startswith("Dx")), "")
            yield fit_len(resample(r.p_signal.T, r.fs), 1000), dict(record=os.path.basename(p), source=p.split(os.sep)[-3], dx=dx)
        except Exception as e:
            print(f"      skip {p}: {e}")
            yield None, None


def run_cinc2021(results, args, root):
    if not wanted(args, "CinC2021"):
        return

    tag = "quick" if args.quick else "full"

    def load():
        paths = c21_paths(root, args.quick)
        X, t = cached(os.path.join(root, f"cache_{tag}"), len(paths), (12, 1000), c21_rows(paths))
        w = pd.read_csv(download(C21_WEIGHTS, os.path.join(root, "weights.csv"), quiet=True), index_col=0)
        col = {c: j for j, cs in enumerate(w.columns) for c in cs.split("|")}
        Y = np.zeros((len(t), len(w.columns)), np.float32)
        for i, dx in enumerate(t.dx.fillna("").astype(str)):
            for c in dx.split(","):
                if c.strip() in col:
                    Y[i, col[c.strip()]] = 1
        return X, t, Y, w.values, list(w.columns).index("426783006")

    data = attempt("PhysioNet/CinC 2021 (CPSC 2018, CPSC-Extra, Georgia, Chapman-Shaoxing, Ningbo)", load)
    if data is None:
        return
    X, t, Y, W, normal = data
    F = features(X, 100, 1, cache=os.path.join(root, f"cache_{tag}_feat.npy"))
    models = record_models(args, Rows(X), F, 30, multilabel=True)
    hook = cinc2021_hook(W, normal)
    # cross_session: leave-one-source-out (patient-disjoint). cross_subject: 5-fold over records (no patient IDs).
    for protocol, meta in [("cross_session", pd.DataFrame(dict(subject="all", session=t.source.values, run="0"))),
                           ("cross_subject", pd.DataFrame(dict(subject=t.record.values, session="0", run="0")))]:
        run_models(results, args, "CinC2021", [protocol], models, Y, meta, multilabel=True, hook=hook)


# ------------------------------------------------------------------ CODE-15%, CODE-test, SaMi-Trop, Chagas 2025

ZEN = "https://zenodo.org/api/records/{rec}/files/{f}/content"
CODE_CLASSES = ["1dAVb", "RBBB", "LBBB", "SB", "AF", "ST"]
CHAGAS_LABELS = "https://moody-challenge.physionet.org/2025/data/code15_chagas_labels.zip"


def h5_rows(path, keep):
    """keep: {row in the HDF5 'tracings' (N, 4096, 12) at 400 Hz: info}. Yields (12, 1024) at 100 Hz."""
    import h5py
    with h5py.File(path, "r") as f:
        t = f["tracings"]
        for s in range(0, t.shape[0], 1000):
            want = [i for i in range(s, min(s + 1000, t.shape[0])) if i in keep]
            if want:
                x = resample_poly(np.asarray(t[s:s + 1000], np.float32).transpose(0, 2, 1), 1, 4, axis=-1)
                for i in want:
                    yield x[i - s], keep[i]


def extract(zpath, suffix, dest):
    """Extract the first member ending in suffix (once); returns its path."""
    with zipfile.ZipFile(zpath) as z:
        m = next(n for n in z.namelist() if n.endswith(suffix))
        out = os.path.join(dest, m)
        if not os.path.exists(out):
            z.extract(m, dest)
    return out


def brazil_rows(root, quick, ptbxl_root):
    """CODE-15% (all 18 parts; quick: 400 exams of part 17), CODE-test, SaMi-Trop, then PTB-XL (Chagas negatives)."""
    import h5py
    d = os.path.join(root, "code15")
    exams = pd.read_csv(download(ZEN.format(rec=4916206, f="exams.csv"), os.path.join(d, "exams.csv")))
    lab = pd.read_csv(extract(download(CHAGAS_LABELS, os.path.join(d, "code15_chagas_labels.zip")), ".csv", d))
    exams = exams.merge(lab[["exam_id", "chagas"]], on="exam_id", how="left")
    for k in ([17] if quick else range(18)):
        h5 = extract(download(ZEN.format(rec=4916206, f=f"exams_part{k}.zip"), os.path.join(d, f"exams_part{k}.zip")), ".hdf5", d)
        with h5py.File(h5, "r") as f:
            pos = {int(e): i for i, e in enumerate(f["exam_id"][:])}
        keep = {pos[r["exam_id"]]: dict(source="code15", patient=f"c{r['patient_id']}", chagas=float(r["chagas"]),
                                        **{c: int(r[c]) for c in CODE_CLASSES})
                for r in exams[exams.trace_file == f"exams_part{k}.hdf5"].to_dict("records") if r["exam_id"] in pos}
        if quick:
            keep = dict(sorted(keep.items())[:400])
        yield from h5_rows(h5, keep)
        os.remove(h5)  # the zip stays; the extracted 2.7 GB HDF5 is not needed once cached

    d = os.path.join(root, "code_test")
    z = download(ZEN.format(rec=3765780, f="data.zip"), os.path.join(d, "data.zip"))
    gold = pd.read_csv(extract(z, "gold_standard.csv", d))
    yield from h5_rows(extract(z, ".hdf5", d), {i: dict(source="code_test", patient=f"t{i}",
                                                        **{c: int(gold[c][i]) for c in CODE_CLASSES}) for i in range(len(gold))})

    d = os.path.join(root, "samitrop")
    st = pd.read_csv(download(ZEN.format(rec=4905618, f="exams.csv"), os.path.join(d, "exams.csv")))
    h5 = extract(download(ZEN.format(rec=4905618, f="exams.zip"), os.path.join(d, "exams.zip")), ".hdf5", d)
    with h5py.File(h5, "r") as f:
        ids = f["exam_id"][:] if "exam_id" in f else st.exam_id.values
    ids = ids[:200] if quick else ids  # no patient IDs published: one exam = one patient
    yield from h5_rows(h5, {i: dict(source="samitrop", patient=f"s{e}", chagas=1.0) for i, e in enumerate(ids)})

    X, db, _ = load_ptbxl_all(ptbxl_root, quick)
    for x, pid in zip(X, db.patient_id):
        yield fit_len(x, 1024), dict(source="ptbxl", patient=f"p{int(pid)}", chagas=0.0)


def run_code_chagas(results, args, root):
    if not wanted(args, "CODE-test", "Chagas2025"):
        return

    def load():
        tag = "quick" if args.quick else "full"
        n = 400 + 827 + 200 + 120 if args.quick else 345_779 + 827 + 1_631 + 21_799
        return cached(os.path.join(root, f"brazil_{tag}"), n, (12, 1024),
                      brazil_rows(root, args.quick, os.path.join(args.data_dir, "ptbxl")))

    data = attempt("CODE-15% -> CODE-test, and Chagas 2025 public data", load)
    if data is None:
        return
    X, t = data
    F = features(X, 100, 1, cache=os.path.join(root, f"brazil_{'quick' if args.quick else 'full'}_feat.npy"))
    src = t.source.values
    if wanted(args, "CODE-test"):
        idx = np.flatnonzero(np.isin(src, ["code15", "code_test"]))
        meta = pd.DataFrame(dict(subject="all", session="0", run=np.where(src[idx] == "code15", "train", "test")))
        run_models(results, args, "CODE-test", ["standard"], record_models(args, Rows(X, idx), F[idx], 10, multilabel=True),
                   t.loc[idx, CODE_CLASSES].values.astype(np.float32), meta, multilabel=True, hook=f1_per_class(CODE_CLASSES))
    if wanted(args, "Chagas2025"):
        idx = np.flatnonzero(t.chagas.notna().values & np.isin(src, ["code15", "samitrop", "ptbxl"]))
        meta = pd.DataFrame(dict(subject="all", session="0", run=holdout(t.patient.values[idx])))
        y = t.chagas.values[idx].astype(float).astype(int)
        run_models(results, args, "Chagas2025", ["standard"], record_models(args, Rows(X, idx), F[idx], 10), y, meta,
                   hook=chagas_hook)


# ------------------------------------------------------------------ Apnea-ECG

APNEA_LEARN = [f"a{i:02d}" for i in range(1, 21)] + [f"b{i:02d}" for i in range(1, 6)] + [f"c{i:02d}" for i in range(1, 11)]
APNEA_TEST = [f"x{i:02d}" for i in range(1, 36)]


def apnea_rows(root, records):
    """Per scored minute: a 3-minute window centred on it (100 Hz, 18,000 samples), label A or N."""
    import wfdb
    for r in records:
        p = os.path.join(root, r)
        x = np.pad(wfdb.rdsamp(p)[0][:, 0], (6000, 12000))
        ann = wfdb.rdann(p, "apn")
        for s, a in zip(ann.sample, ann.symbol):
            yield x[None, s:s + 18000], dict(record=r, label=a)


def run_apnea(results, args, root):
    if not wanted(args, "ApneaECG"):
        return
    learn, test = (["a01", "c01"], ["x01", "x02"]) if args.quick else (APNEA_LEARN, APNEA_TEST)
    tag = "quick" if args.quick else "full"

    def load():
        fetch("apnea-ecg/1.0.0", root, learn + test, ("hea", "dat", "apn"))
        return cached(os.path.join(root, f"cache_{tag}"), 600 * len(learn + test), (1, 18000),
                      apnea_rows(root, learn + test))

    data = attempt("Apnea-ECG", load)
    if data is None:
        return
    X, t = data
    F = features(X, 100, 0, cache=os.path.join(root, f"cache_{tag}_feat.npy"))
    idx = np.arange(len(t))[::10 if args.quick else 1]  # quick: every 10th minute (CPU-friendly)
    meta = pd.DataFrame(dict(subject="all", session="0", run=np.where(t.record.isin(learn), "train", "test")[idx]))
    run_models(results, args, "ApneaECG", ["standard"], record_models(args, Rows(X, idx), F[idx], 30), t.label.values[idx],
               meta, hook=apnea_hook)


# ------------------------------------------------------------------ WESAD (chest ECG)

WESAD_URL = "https://uni-siegen.sciebo.de/s/HGdUkoNlW1Ub0Gx/download"
WESAD_SUBJECTS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17]


def load_wesad(root, subjects):
    """Chest ECG 700 -> 100 Hz; 60-s windows, 5-s step, inside baseline (1), stress (2) and amusement (3) segments."""
    need = [s for s in subjects if not os.path.exists(os.path.join(root, f"S{s}.npz"))]
    if need:  # stream only the S*.pkl members out of the 2.2 GB remote zip; keep chest ECG and labels (~20 MB each)
        os.makedirs(root, exist_ok=True)
        with zipfile.ZipFile(io.BufferedReader(HttpFile(WESAD_URL), 1 << 23)) as z:
            for s in need:
                with z.open(f"WESAD/S{s}/S{s}.pkl") as src:
                    d = pickle.load(src, encoding="latin1")
                np.savez(os.path.join(root, f"S{s}.npz"), ecg=d["signal"]["chest"]["ECG"][:, 0].astype(np.float32),
                         label=d["label"].astype(np.int8))
    X, y, subj = [], [], []
    for s in subjects:
        d = np.load(os.path.join(root, f"S{s}.npz"))
        ecg, lab = resample_poly(d["ecg"], 1, 7), d["label"][::7]
        n = min(len(ecg), len(lab))
        change = np.flatnonzero(np.diff(lab[:n])) + 1
        for a, b in zip(np.r_[0, change], np.r_[change, n]):
            if lab[a] in (1, 2, 3):
                for k in range(a, b - 6000 + 1, 500):
                    X.append(ecg[k:k + 6000])
                    y.append({1: "baseline", 2: "stress", 3: "amusement"}[lab[a]])
                    subj.append(str(s))
    return np.asarray(X, np.float32)[:, None], np.array(y), pd.DataFrame(dict(subject=subj, session="0", run="0"))


def run_wesad(results, args, root):
    if not wanted(args, "WESAD", "WESAD-binary", "WESAD-3class"):
        return
    data = attempt("WESAD (chest ECG)", load_wesad, root, WESAD_SUBJECTS[:2] if args.quick else WESAD_SUBJECTS)
    if data is None:
        return
    X, y, meta = data
    if args.quick:  # every 5th window (CPU-friendly)
        X, y, meta = X[::5], y[::5], meta.iloc[::5].reset_index(drop=True)
    F = features(X, 100, 0)
    lda = ("Features+LDA", make_pipeline(SimpleImputer(), StandardScaler(), LDA()))
    for name, labels in [("WESAD-binary", np.where(y == "stress", "stress", "non-stress")), ("WESAD-3class", y)]:
        if wanted(args, "WESAD", name):
            run_models(results, args, name, ["cross_subject"], record_models(args, X, F, 50, clf=lda), labels, meta)


# ------------------------------------------------------------------ gated: MIMIC-IV-ECG, HEEDB

def wfdb_rows(paths, infos):
    import wfdb
    for p, info in zip(paths, infos):
        try:
            r = wfdb.rdrecord(p)
            yield fit_len(resample(r.p_signal.T, r.fs), 1000), info
        except Exception as e:
            print(f"      skip {p}: {e}")
            yield None, None


def top_labels(sets, k=20):
    """Multi-hot matrix of the k most frequent labels."""
    top = pd.Series([c for s in sets for c in s]).value_counts().index[:k].tolist()
    return np.array([[c in s for c in top] for s in sets], np.float32), top


def load_mimic(root, cache, quick):
    """record_list.csv + machine_measurements.csv; labels = report_0..report_17 statements."""
    rl = pd.read_csv(os.path.join(root, "record_list.csv"))
    rep = [f"report_{i}" for i in range(18)]
    mm = pd.read_csv(os.path.join(root, "machine_measurements.csv"), usecols=lambda c: c == "study_id" or c in rep)
    df = rl.merge(mm, on="study_id")
    df = df.head(60) if quick else df.sample(n=min(len(df), GATED_MAX), random_state=0).sort_index()
    infos = [dict(patient=r["subject_id"], labels="|".join(sorted({str(r[c]).strip() for c in rep if c in r and pd.notna(r[c])})))
             for r in df.to_dict("records")]
    return cached(cache, len(df), (12, 1000), wfdb_rows([os.path.join(root, p) for p in df.path], infos))


def heedb_path(site, root, name):
    name = re.sub(r"\.(hea|mat|dat)$", "", str(name))
    for base in (site, os.path.join(site, "WFDB"), root):
        if os.path.exists(os.path.join(base, name) + ".hea"):
            return os.path.join(base, name)
    return os.path.join(site, name)


def load_heedb(root, cache, quick):
    """Per site: 12SL_diagnoses/diagnoses_v24.csv (FileName, codes) joined with metadata/metadata.csv (BDSPPatientID)."""
    parts = []
    for dx in glob.glob(os.path.join(root, "**", "12SL_diagnoses", "diagnoses_v24.csv"), recursive=True):
        site = os.path.dirname(os.path.dirname(dx))
        meta = pd.read_csv(os.path.join(site, "metadata", "metadata.csv"), usecols=["FileName", "BDSPPatientID"])
        parts.append(pd.read_csv(dx).merge(meta, on="FileName").assign(site=site))
    if not parts:
        raise FileNotFoundError("no */12SL_diagnoses/diagnoses_v24.csv under the HEEDB folder")
    df = pd.concat(parts, ignore_index=True)
    df = df.head(60) if quick else df.sample(n=min(len(df), GATED_MAX), random_state=0).sort_index()
    infos = [dict(patient=r["BDSPPatientID"], labels="|".join(sorted(set(re.findall(r"\d+", str(r["codes"]))))))
             for r in df.to_dict("records")]
    paths = [heedb_path(r["site"], root, r["FileName"]) for r in df.to_dict("records")]
    return cached(cache, len(df), (12, 1000), wfdb_rows(paths, infos))


def run_gated(results, args, root):
    for name, key, loader in [("MIMIC-IV-ECG", "mimic_iv_ecg", load_mimic), ("HEEDB", "heedb", load_heedb)]:
        if not wanted(args, name):
            continue
        folder = (getattr(args, "paths", None) or {}).get(key)
        if not folder:
            print(f"\n[{PHASE}] {name}: skipped (access-gated; pass --path {key}=FOLDER)")
            continue
        cache = os.path.join(root, key, "cache_quick" if args.quick else "cache_full")
        data = attempt(name, loader, folder, cache, args.quick)
        if data is None:
            continue
        X, t = data
        Y, _ = top_labels([set(str(s).split("|")) - {"", "nan"} for s in t["labels"]])
        F = features(X, 100, 1, cache=cache + "_feat.npy")
        meta = pd.DataFrame(dict(subject="all", session="0", run=holdout(t.patient.values)))
        run_models(results, args, name, ["standard"], record_models(args, Rows(X), F, 10, multilabel=True), Y, meta,
                   multilabel=True)


# ------------------------------------------------------------------ entry point

def run(results, args):
    root = os.path.join(args.data_dir, "ecg")
    for fn, sub in [(run_mitbih, ""), (run_incart, ""), (run_ptb, ""), (run_ptbxl_tasks, ""), (run_cinc2017, "cinc2017"),
                    (run_cinc2021, "cinc2021"), (run_code_chagas, ""), (run_apnea, "apnea_ecg"), (run_wesad, "wesad"),
                    (run_gated, "")]:
        try:
            fn(results, args, os.path.join(root, sub))
        except Exception as e:  # anything outside the per-model guards (features, labels) must not stop the phase
            log_error(PHASE, f"{fn.__name__}: {type(e).__name__}: {e}")
