"""EMG benchmarks (phase 2): Ninapro DB5 and GRABMyo."""
import glob
import os

import numpy as np
import pandas as pd
import scipy.io as sio
from scipy.signal import resample_poly
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from common import classical, deep, download, evaluate, log_error, resnet1d, unzip
from eeg import _safe

EMG_DEEP_TRAIN = dict(lr=1e-3, weight_decay=1e-4)


def hudgins(X):
    """Classic time-domain features per channel: MAV, WL, ZC, SSC (Hudgins et al. 1993)."""
    X = np.asarray(X, dtype=np.float32)
    d = np.diff(X, axis=-1)
    mav = np.abs(X).mean(-1)
    wl = np.abs(d).sum(-1)
    zc = np.diff(np.signbit(X), axis=-1).sum(-1)
    ssc = np.diff(np.signbit(d), axis=-1).sum(-1)
    return np.concatenate([mav, wl, zc, ssc], axis=1)


def features(X, chunk=4096):
    """Hudgins features for all windows, computed in chunks (works on memmaps)."""
    return np.concatenate([hudgins(X[i:i + chunk]) for i in range(0, len(X), chunk)])


def emg_classical():
    """Pipelines on precomputed Hudgins features."""
    return {
        "Hudgins+LDA": make_pipeline(StandardScaler(), LDA(solver="lsqr", shrinkage="auto")),
        "Hudgins+RF": make_pipeline(RandomForestClassifier(n_estimators=300, n_jobs=-1, random_state=0)),
    }


def windows(sig, labels, reps, win, step):
    """Slide windows inside runs of constant (label, repetition); returns X (n, ch, win), y, rep."""
    X, y, r = [], [], []
    change = np.flatnonzero((np.diff(labels) != 0) | (np.diff(reps) != 0)) + 1
    for a, b in zip(np.r_[0, change], np.r_[change, len(labels)]):
        for s in range(a, b - win + 1, step):
            X.append(sig[s:s + win].T)
            y.append(labels[a])
            r.append(reps[a])
    return np.asarray(X, dtype=np.float32), np.asarray(y), np.asarray(r)


# ------------------------------------------------------------------ Ninapro DB5

DB5_URL = "https://ninapro.hevs.ch/files/DB5_Preproc/s{n}.zip"
DB5_OFFSETS = {1: 0, 2: 12, 3: 29}  # labels are numbered per exercise; shift to global movement ids


def load_db5(root, subjects):
    """Exercises B and C plus rest (41 classes), both Myo armbands (16 ch, 200 Hz), 200-ms windows, 100-ms step."""
    Xs, ys, metas = [], [], []
    for n in subjects:
        d = os.path.join(root, f"s{n}")
        if not glob.glob(os.path.join(d, "*.mat")):
            unzip(download(DB5_URL.format(n=n), os.path.join(root, f"s{n}.zip")), root)
        for ex in (2, 3):
            m = sio.loadmat(glob.glob(os.path.join(d, f"S{n}_E{ex}_A1.mat"))[0])
            lab = m["restimulus"].ravel().astype(int)
            lab = np.where(lab > 0, lab + DB5_OFFSETS[ex], 0)
            # rest samples carry repetition 0; give them the repetition of the movement they follow
            rep = pd.Series(m["rerepetition"].ravel().astype(float)).replace(0, np.nan).ffill().bfill().astype(int).values
            X, y, r = windows(m["emg"].astype(np.float32), lab, rep, win=40, step=20)
            Xs.append(X)
            ys.append(y)
            metas.append(pd.DataFrame(dict(subject=str(n), session="0", run=r.astype(str))))
    return np.concatenate(Xs), np.concatenate(ys).astype(str), pd.concat(metas, ignore_index=True)


# ------------------------------------------------------------------ GRABMyo

GRAB_ZIP = "https://physionet.org/content/grabmyo/get-zip/1.1.0/"
GRAB_FILE = "https://physionet.org/files/grabmyo/1.1.0/{rec}.{ext}"


def grab_records(participants, gestures=range(1, 18)):
    return [f"Session{s}/session{s}_participant{p}/session{s}_participant{p}_gesture{g}_trial{t}"
            for s in (1, 2, 3) for p in participants for g in gestures for t in range(1, 8)]


def fetch_grabmyo(root, participants, quick):
    """Full run: download the 9.8 GB zip once. Quick run: download only the needed records."""
    have = glob.glob(os.path.join(root, "**", "RECORDS"), recursive=True)
    if have:
        return os.path.dirname(have[0])
    if not quick:
        unzip(download(GRAB_ZIP, os.path.join(root, "grabmyo.zip")), root)
        return os.path.dirname(glob.glob(os.path.join(root, "**", "RECORDS"), recursive=True)[0])
    base = os.path.join(root, "quick")
    for rec in grab_records(participants, range(1, 4)):
        for ext in ("hea", "dat"):
            dst = os.path.join(base, rec + "." + ext)
            if not os.path.exists(dst):
                download(GRAB_FILE.format(rec=rec, ext=ext), dst, quiet=True)
    return base


def load_grabmyo(root, participants, quick, fs_out=1024):
    """28 electrodes (16 forearm + 12 wrist), resampled 2048 -> 1024 Hz, non-overlapping 200-ms windows.

    Windows are stored in a disk-backed memmap so the full dataset never has to fit in RAM.
    """
    import wfdb
    base = fetch_grabmyo(root, participants, quick)
    win = int(0.2 * fs_out)
    recs = grab_records(participants, range(1, 4) if quick else range(1, 18))
    n_win = (5 * fs_out) // win  # trials are 5 s
    path = os.path.join(root, f"windows_{'quick_' if quick else ''}{len(participants)}p_{fs_out}hz.f32")
    X = np.lib.format.open_memmap(path + ".npy", mode="w+" if not os.path.exists(path + ".npy") else "r+",
                                  dtype=np.float32, shape=(len(recs) * n_win, 28, win))
    fresh = not os.path.exists(path + ".done")
    ys, metas = [], []
    for i, rec in enumerate(recs):
        sess, part = rec.split("/")[0][-1], rec.split("_participant")[1].split("/")[0]
        gesture, trial = rec.split("_gesture")[1].split("_trial")
        if fresh:
            r = wfdb.rdrecord(os.path.join(base, rec))
            keep = [j for j, c in enumerate(r.sig_name) if c[0] in "FW"]
            sig = resample_poly(r.p_signal[:, keep], fs_out, r.fs, axis=0).astype(np.float32)
            for k in range(n_win):
                X[i * n_win + k] = sig[k * win:(k + 1) * win].T
        ys += [gesture] * n_win
        metas += [dict(subject=part, session=sess, run=trial)] * n_win
    if fresh:
        X.flush()
        open(path + ".done", "w").close()
    return X, np.asarray(ys), pd.DataFrame(metas)


# ------------------------------------------------------------------ runner

def run_emg(results, args):
    root = os.path.join(args.data_dir, "emg")
    if not args.datasets or "NinaproDB5" in args.datasets:
        print("\n[phase 2] NinaproDB5")
        try:
            X, y, meta = load_db5(os.path.join(root, "ninapro_db5"), [1, 2] if args.quick else range(1, 11))
        except Exception as e:
            log_error("phase2", f"NinaproDB5: could not load ({type(e).__name__}: {e})")
        else:
            F = features(X)
            for protocol in ["heldout_run:2,5", "cross_subject"]:
                for mname, pipe in emg_classical().items():
                    _safe(evaluate, "phase2", results, "NinaproDB5", protocol, mname, classical(pipe), F, y, meta,
                          args.seeds, needs_seed=False)
                if not args.models or "ResNet1D" in args.models:
                    make = deep(resnet1d, epochs=min(args.epochs, 100), batch_size=256, **EMG_DEEP_TRAIN)
                    _safe(evaluate, "phase2", results, "NinaproDB5", protocol, "ResNet1D", make, X, y, meta, args.seeds)

    if not args.datasets or "GRABMyo" in args.datasets:
        print("\n[phase 2] GRABMyo")
        try:
            X, y, meta = load_grabmyo(os.path.join(root, "grabmyo"), [1, 2] if args.quick else range(1, 44), args.quick)
        except Exception as e:
            log_error("phase2", f"GRABMyo: could not load ({type(e).__name__}: {e})")
            return
        F = features(X)
        # within-day (trials 6-7 held out), cross-day (day 3 held out), cross-subject (classical only: memory)
        for protocol in ["heldout_run:6,7", "heldout_session:3", "cross_subject"]:
            for mname, pipe in emg_classical().items():
                _safe(evaluate, "phase2", results, "GRABMyo", protocol, mname, classical(pipe), F, y, meta,
                      args.seeds, needs_seed=False)
            if protocol != "cross_subject" and (not args.models or "ResNet1D" in args.models):
                make = deep(resnet1d, epochs=min(args.epochs, 100), batch_size=256, **EMG_DEEP_TRAIN)
                _safe(evaluate, "phase2", results, "GRABMyo", protocol, "ResNet1D", make, X, y, meta, args.seeds)
