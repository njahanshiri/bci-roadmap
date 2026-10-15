"""Other data types (phase 5): Sleep-EDF sleep staging (EEG / EOG) and PTB-XL ECG classification."""
import ast
import glob
import os

import mne
import numpy as np
import pandas as pd
from scipy.signal import welch
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer

from common import classical, deep, download, evaluate, log_error, resnet1d, unzip
from common import _safe
from eeg import braindecode_builder

# ------------------------------------------------------------------ Sleep-EDF-20

STAGES = {"Sleep stage W": "W", "Sleep stage 1": "N1", "Sleep stage 2": "N2", "Sleep stage 3": "N3",
          "Sleep stage 4": "N3", "Sleep stage R": "REM"}
INPUTS = {"EEG": ["EEG Fpz-Cz"], "EOG": ["EOG horizontal"], "EEG+EOG": ["EEG Fpz-Cz", "EOG horizontal"]}


def load_sleep_edf(n_subjects):
    """Sleep-EDF-20: first 20 Sleep Cassette subjects, both nights, 30-s epochs at 100 Hz.

    Wake is trimmed to 30 min before the first and after the last sleep epoch; N3 and N4 are
    merged; movement and unscored epochs are dropped (the usual Sleep-EDF-20 setup).
    """
    from mne.datasets.sleep_physionet.age import fetch_data
    files = fetch_data(subjects=list(range(n_subjects)), recording=[1, 2], on_missing="warn")
    X, y, meta = [], [], []
    for psg, hyp in files:
        raw = mne.io.read_raw_edf(psg, preload=True, verbose=False)
        Xr, yr, ch_names = sleep_epochs(raw, mne.read_annotations(hyp))
        name = os.path.basename(psg)  # SC4ssN...: ss = subject, N = night
        X.append(Xr)
        y += yr
        meta += [dict(subject=name[3:5], session=name[5], run="0")] * len(yr)
    return np.concatenate(X), np.asarray(y), pd.DataFrame(meta), ch_names


def sleep_epochs(raw, ann):
    """30-s epochs of one recording, wake trimmed to 30 min around sleep."""
    sleep = [(o, o + dur) for o, dur, d in zip(ann.onset, ann.duration, ann.description) if d in STAGES and STAGES[d] != "W"]
    tmin, tmax = max(0, sleep[0][0] - 1800), min(raw.times[-1], sleep[-1][1] + 1800)
    ann = ann.copy().crop(tmin, tmax)
    raw.set_annotations(ann, emit_warning=False)
    ev, ev_id = mne.events_from_annotations(raw, event_id={k: i for i, k in enumerate(STAGES)},
                                            chunk_duration=30.0, verbose=False)
    ep = mne.Epochs(raw, ev, ev_id, tmin=0, tmax=30 - 1 / raw.info["sfreq"], baseline=None,
                    picks=sorted({c for v in INPUTS.values() for c in v}), preload=True, verbose=False)
    inv = {v: k for k, v in ev_id.items()}
    return ep.get_data(copy=False).astype(np.float32) * 1e6, [STAGES[inv[c]] for c in ep.events[:, 2]], ep.ch_names


def band_powers(X, sfreq=100):
    """Log power in delta, theta, alpha, sigma, beta per channel."""
    f, p = welch(X, fs=sfreq, nperseg=256, axis=-1)
    bands = [(0.5, 4), (4, 8), (8, 12), (12, 16), (16, 30)]
    return np.log(np.concatenate([p[..., (f >= a) & (f < b)].mean(-1) for a, b in bands], axis=1) + 1e-12)


SLEEP_DEEP = {"SleepStagerChambon2018": dict(lr=1e-3, weight_decay=0.0),
              "DeepSleepNet": dict(lr=1e-3, weight_decay=1e-3),
              "AttnSleep": dict(lr=1e-3, weight_decay=1e-3)}


def run_sleep(results, args):
    print("\n[phase 5] Sleep-EDF-20")
    try:
        X, y, meta, ch_names = load_sleep_edf(2 if args.quick else 20)
    except Exception as e:
        log_error("phase5", f"Sleep-EDF: could not load ({type(e).__name__}: {e})")
        return
    protocol = "cross_subject"  # 20 subjects -> leave-one-subject-out = the standard 20-fold subject-wise CV
    for inp, chans in INPUTS.items():
        dname = f"SleepEDF-20 ({inp})"
        if args.datasets and dname not in args.datasets and "SleepEDF-20" not in args.datasets:
            continue
        Xi = X[:, [ch_names.index(c) for c in chans]]
        rf = make_pipeline(FunctionTransformer(band_powers),
                           RandomForestClassifier(n_estimators=300, n_jobs=-1, random_state=0))
        _safe(evaluate, "phase5", results, dname, protocol, "BandPower+RF", classical(rf), Xi, y, meta, args.seeds,
              needs_seed=False)
        for mname, train in SLEEP_DEEP.items():
            if args.models and mname not in args.models:
                continue
            if mname == "AttnSleep" and len(chans) > 1:
                print(f"  - {dname} | {mname}: not applicable (single-channel model)")
                continue
            make = deep(braindecode_builder(mname, 100), epochs=min(args.epochs, 50), batch_size=128, **train)
            _safe(evaluate, "phase5", results, dname, protocol, mname, make, Xi, y, meta, args.seeds)


# ------------------------------------------------------------------ PTB-XL

PTBXL_ZIP = "https://physionet.org/content/ptb-xl/get-zip/1.0.3/"
PTBXL_FILE = "https://physionet.org/files/ptb-xl/1.0.3/{f}"
SUPERCLASSES = ["CD", "HYP", "MI", "NORM", "STTC"]


def load_ptbxl(root, quick):
    """100-Hz records, 5 diagnostic superclasses (multi-label), Strodthoff et al. folds."""
    import wfdb
    found = glob.glob(os.path.join(root, "**", "ptbxl_database.csv"), recursive=True)
    if found:
        base = os.path.dirname(found[0])
    elif quick:
        base = os.path.join(root, "quick")
        for f in ("ptbxl_database.csv", "scp_statements.csv"):
            download(PTBXL_FILE.format(f=f), os.path.join(base, f), quiet=True)
    else:
        unzip(download(PTBXL_ZIP, os.path.join(root, "ptbxl.zip")), root)
        base = os.path.dirname(glob.glob(os.path.join(root, "**", "ptbxl_database.csv"), recursive=True)[0])
    db = pd.read_csv(os.path.join(base, "ptbxl_database.csv"), index_col="ecg_id")
    scp = pd.read_csv(os.path.join(base, "scp_statements.csv"), index_col=0)
    scp = scp[scp.diagnostic == 1]
    labels = db.scp_codes.apply(lambda s: {scp.loc[k, "diagnostic_class"] for k in ast.literal_eval(s) if k in scp.index})
    db = db[labels.apply(len) > 0]
    labels = labels[db.index]
    if quick:  # a few records from the train folds and the test fold
        db = pd.concat([db[db.strat_fold <= 8].head(80), db[db.strat_fold == 10].head(40)])
        labels = labels[db.index]
        for f in db.filename_lr:
            for ext in ("hea", "dat"):
                download(PTBXL_FILE.format(f=f"{f}.{ext}"), os.path.join(base, f"{f}.{ext}"), quiet=True)
    X = np.stack([wfdb.rdsamp(os.path.join(base, f))[0].T for f in db.filename_lr]).astype(np.float32)
    Y = np.array([[c in s for c in SUPERCLASSES] for s in labels], dtype=np.float32)
    run = np.where(db.strat_fold <= 8, "train", np.where(db.strat_fold == 10, "test", "val"))
    meta = pd.DataFrame(dict(subject="all", session="0", run=run))
    return X, Y, meta


def run_ptbxl(results, args):
    if args.datasets and "PTB-XL" not in args.datasets:
        return
    print("\n[phase 5] PTB-XL (superdiagnostic, 5 labels)")
    try:
        X, Y, meta = load_ptbxl(os.path.join(args.data_dir, "ptbxl"), args.quick)
    except Exception as e:
        log_error("phase5", f"PTB-XL: could not load ({type(e).__name__}: {e})")
        return
    models = {"ResNet1D": (resnet1d, dict(lr=1e-3, weight_decay=1e-2)),
              "DeepConvNet": (braindecode_builder("Deep4Net", 100), dict(lr=1e-3, weight_decay=5e-4)),
              "ShallowConvNet": (braindecode_builder("ShallowFBCSPNet", 100), dict(lr=1e-3, weight_decay=0.0))}
    for mname, (build, train) in models.items():
        if args.models and mname not in args.models:
            continue
        make = deep(build, epochs=min(args.epochs, 50), batch_size=128, multilabel=True, **train)
        _safe(evaluate, "phase5", results, "PTB-XL", "standard", mname, make, X, Y, meta, args.seeds, multilabel=True)


def run_other(results, args):
    run_sleep(results, args)
    run_ptbxl(results, args)
