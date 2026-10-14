"""EEG benchmarks: motor imagery (phase 1), SSVEP and P300 (phase 3), foundation models and TUAB (phase 4)."""
import warnings
from functools import lru_cache

import mne
import numpy as np
import pandas as pd
import torch
from mne.decoding import CSP, Vectorizer
from pyriemann.classification import MDM
from pyriemann.estimation import Covariances, XdawnCovariances
from pyriemann.spatialfilters import Xdawn
from pyriemann.tangentspace import TangentSpace
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC

from common import NotApplicable, classical, deep, evaluate, itr_bits_per_min, log_error

warnings.filterwarnings("ignore")
mne.set_log_level("ERROR")

# ------------------------------------------------------------------ datasets
# protocols: "standard" = official train/test split from MOABB session/run names.
MI_DATASETS = {
    "BNCI2014_001": dict(paradigm="mi", events=["left_hand", "right_hand", "feet", "tongue"], resample=250,
                         protocols=["standard", "cross_subject"]),
    "BNCI2014_004": dict(paradigm="lr", resample=250, protocols=["standard", "cross_subject"]),
    "Schirrmeister2017": dict(paradigm="mi", events=["left_hand", "right_hand", "feet", "rest"], resample=250,
                              fmax=120, protocols=["standard", "cross_subject"]),
    "PhysionetMI": dict(paradigm="mi", events=["left_hand", "right_hand", "hands", "feet"], resample=160,
                        protocols=["cross_subject_fixed:1-70:90-109", "cross_subject"]),
    "Lee2019_MI": dict(paradigm="lr", resample=250, protocols=["standard", "cross_session", "cross_subject"]),
    "Cho2017": dict(paradigm="lr", resample=256, protocols=["within_session:5", "cross_subject"]),
}
SSVEP_DATASETS = {
    # window = seconds of data after the dataset's stimulus-onset interval start
    "Nakanishi2015": dict(paradigm="ssvep", n_classes=12, window=1.0, resample=256,
                          protocols=["within_session:15"]),  # 15 blocks; block ids are not in MOABB metadata
    "Wang2016": dict(paradigm="ssvep", n_classes=40, window=1.0, resample=250, protocols=["within_session:6"]),
    "Lee2019_SSVEP": dict(paradigm="ssvep", n_classes=4, window=4.0, resample=250, protocols=["standard"]),
}
P300_DATASETS = {
    "BNCI2014_009": dict(paradigm="p300", resample=128, protocols=["within_session:5"]),
    "BI2013a": dict(paradigm="p300", resample=128, protocols=["within_session:5"]),
    "Lee2019_ERP": dict(paradigm="p300", resample=128, protocols=["within_session:5"]),
}
GAZE_SHIFT_S = 0.5  # used only for the ITR column of SSVEP results


def _paradigm(cfg, resample):
    from moabb import paradigms as P
    fmin, fmax = cfg.get("fmin", 4), cfg.get("fmax", 38)
    if cfg["paradigm"] == "mi":
        return P.MotorImagery(events=cfg["events"], n_classes=len(cfg["events"]), fmin=fmin, fmax=fmax, resample=resample)
    if cfg["paradigm"] == "lr":
        return P.LeftRightImagery(fmin=fmin, fmax=fmax, resample=resample)
    if cfg["paradigm"] == "ssvep":
        return P.SSVEP(n_classes=cfg["n_classes"], tmin=0.0, tmax=cfg["window"], resample=resample)
    if cfg["paradigm"] == "p300":
        return P.P300(resample=resample)
    raise ValueError(cfg["paradigm"])


@lru_cache(maxsize=2)
def load(name, resample, n_subjects, want_epochs):
    """Return X (µV, float32), y, meta, info, epochs-or-None. Cached for the run."""
    import moabb.datasets as D
    cfg = {**MI_DATASETS, **SSVEP_DATASETS, **P300_DATASETS}[name]
    ds = getattr(D, name)()
    subjects = ds.subject_list[:n_subjects] if n_subjects else ds.subject_list
    par = _paradigm(cfg, resample)
    if want_epochs:
        ep, y, meta = par.get_data(ds, subjects, return_epochs=True)
        X, info = ep.get_data(copy=True) * 1e6, ep.info
    else:
        X, y, meta = par.get_data(ds, subjects)
        X = X * 1e6
        info = None
        ep = None
    meta = meta.reset_index(drop=True).astype({"subject": str, "session": str, "run": str})
    return X.astype(np.float32), np.asarray(y), meta, info, ep


# ------------------------------------------------------------------ models

def mi_classical():
    return {
        "CSP+LDA": make_pipeline(CSP(n_components=8, log=True), LDA(solver="lsqr", shrinkage="auto")),
        "TS+LR": make_pipeline(Covariances("oas"), TangentSpace(metric="riemann"), LogisticRegression(max_iter=2000)),
        "MDM": make_pipeline(Covariances("oas"), MDM(metric="riemann")),
    }


def p300_classical():
    return {
        "XDAWN+LDA": make_pipeline(Xdawn(nfilter=2, estimator="scm"), Vectorizer(), LDA(solver="lsqr", shrinkage="auto")),
        "XDAWNCov+MDM": make_pipeline(XdawnCovariances(nfilter=4, estimator="oas", xdawn_estimator="scm"), MDM()),
        "XDAWNCov+TS+SVM": make_pipeline(XdawnCovariances(nfilter=4, estimator="oas", xdawn_estimator="scm"),
                                         TangentSpace(), SVC(kernel="linear")),
    }


def ssvep_classical():
    from moabb.pipelines import SSVEP_CCA, SSVEP_TRCA
    return {"CCA": SSVEP_CCA(n_harmonics=3), "TRCA": SSVEP_TRCA(n_fbands=5)}


# name -> (braindecode class, training settings). Defaults follow each model's braindecode/paper defaults.
DEEP = {
    "EEGNet": ("EEGNet", dict(lr=1e-3, weight_decay=0.0)),
    "ShallowConvNet": ("ShallowFBCSPNet", dict(lr=6.25e-4, weight_decay=0.0)),
    "DeepConvNet": ("Deep4Net", dict(lr=1e-2, weight_decay=5e-4)),
    "EEG-TCNet": ("EEGTCNet", dict(lr=1e-3, weight_decay=0.0)),
    "ATCNet": ("ATCNet", dict(lr=1e-3, weight_decay=0.0)),
    "EEGConformer": ("EEGConformer", dict(lr=2e-4, weight_decay=0.0)),
    "TCFormer": ("TCFormer", dict(lr=1e-3, weight_decay=1e-3)),
    "EEGInceptionERP": ("EEGInceptionERP", dict(lr=1e-3, weight_decay=0.0)),
}
MI_DEEP = ["EEGNet", "ShallowConvNet", "DeepConvNet", "EEG-TCNet", "ATCNet", "EEGConformer", "TCFormer"]
P300_DEEP = ["EEGNet", "EEGInceptionERP"]
SSVEP_DEEP = ["EEGNet"]


def braindecode_builder(cls_name, sfreq):
    import braindecode.models as M
    cls = getattr(M, cls_name)

    def build(n_chans, n_times, n_outputs):
        return cls(n_chans=n_chans, n_outputs=n_outputs, n_times=n_times, sfreq=sfreq,
                   input_window_seconds=n_times / sfreq)
    return build


# Foundation models: (braindecode class, Hugging Face repo, sampling rate, patch size, needs montage)
FOUNDATION = {
    "LaBraM": ("InterpolatedLaBraM", "braindecode/labram-pretrained", 200, 200, True),
    "CBraMod": ("CBraMod", "braindecode/cbramod-pretrained", 200, 200, False),
    "EEGPT": ("InterpolatedEEGPT", "braindecode/eegpt-pretrained", 256, 64, True),
}
FOUNDATION_TRAIN = dict(lr=1e-4, weight_decay=0.05, batch_size=32)


def transfer_pretrained(model, repo):
    """Copy every pretrained tensor whose shape fits; position embeddings are cropped to the input length."""
    from huggingface_hub import hf_hub_download
    from safetensors.torch import load_file
    src, own, n = load_file(hf_hub_download(repo, "model.safetensors")), model.state_dict(), 0
    for k, v in src.items():
        if k not in own:
            continue
        o = own[k]
        if o.shape == v.shape:
            own[k], n = v, n + 1
        elif o.ndim == v.ndim and all(a <= b for a, b in zip(o.shape, v.shape)) and "embed" in k:
            own[k], n = v[tuple(slice(0, s) for s in o.shape)], n + 1
    model.load_state_dict(own)
    return n, len(src)


def foundation_builder(name, info):
    import braindecode.models as M
    cls_name, repo, sf, _, needs_montage = FOUNDATION[name]
    cls = getattr(M, cls_name)
    chs = None
    if needs_montage:
        info = info.copy()
        info.set_montage("standard_1005", match_case=False, on_missing="ignore")
        if any(np.isnan(ch["loc"][:3]).any() or not np.any(ch["loc"][:3]) for ch in info["chs"]):
            raise NotApplicable("some channels have no standard 10-05 position")
        chs = info["chs"]

    def build(n_chans, n_times, n_outputs):
        kw = dict(n_outputs=n_outputs, n_times=n_times, sfreq=sf)
        model = cls(chs_info=chs, **kw) if needs_montage else cls(n_chans=n_chans, **kw)
        loaded, total = transfer_pretrained(model, repo)
        print(f"      {name}: loaded {loaded}/{total} pretrained tensors")
        return model
    return build


def crop_to_patches(X, sfreq, patch):
    """Crop epochs to whole seconds and a multiple of the model's patch size."""
    n = int(X.shape[-1] // sfreq * sfreq)
    n -= n % patch
    if n <= 0:
        raise NotApplicable("epochs shorter than one patch")
    return X[..., :n]


# ------------------------------------------------------------------ runners

def _subjects(quick):
    return 2 if quick else None


def _deep_kw(train, epochs, batch_size):
    return {**train, "epochs": epochs, "batch_size": train.get("batch_size", batch_size)}


def run_mi(results, args):
    for name, cfg in MI_DATASETS.items():
        if args.datasets and name not in args.datasets:
            continue
        print(f"\n[phase 1] {name}")
        try:
            X, y, meta, _, _ = load(name, cfg["resample"], _subjects(args.quick), False)
        except Exception as e:
            log_error("phase1", f"{name}: could not load ({type(e).__name__}: {e})")
            continue
        for protocol in cfg["protocols"]:
            for mname, pipe in mi_classical().items():
                _safe(evaluate, "phase1", results, name, protocol, mname, classical(pipe), X, y, meta, args.seeds,
                      needs_seed=False)
            for mname in MI_DEEP:
                if args.models and mname not in args.models:
                    continue
                cls_name, train = DEEP[mname]
                make = deep(braindecode_builder(cls_name, cfg["resample"]), **_deep_kw(train, args.epochs, args.batch_size))
                _safe(evaluate, "phase1", results, name, protocol, mname, make, X, y, meta, args.seeds)


def run_ssvep_p300(results, args):
    for group, dsets in (("ssvep", SSVEP_DATASETS), ("p300", P300_DATASETS)):
        for name, cfg in dsets.items():
            if args.datasets and name not in args.datasets:
                continue
            print(f"\n[phase 3] {name}")
            try:
                X, y, meta, info, ep = load(name, cfg["resample"], _subjects(args.quick), group == "ssvep")
            except Exception as e:
                log_error("phase3", f"{name}: could not load ({type(e).__name__}: {e})")
                continue
            for protocol in cfg["protocols"]:
                if group == "ssvep":
                    n_t, secs = cfg["n_classes"], cfg["window"] + GAZE_SHIFT_S
                    hook = lambda yt, yp, n_t=n_t, secs=secs: {
                        "itr_bits_min": itr_bits_per_min(n_t, float(np.mean(yt == yp)), secs)}
                    for mname, pipe in ssvep_classical().items():
                        _safe(evaluate, "phase3", results, name, protocol, mname, classical(pipe), ep, y, meta,
                              args.seeds, needs_seed=False, fold_hook=hook)
                    deep_names = SSVEP_DEEP
                else:
                    hook = None
                    for mname, pipe in p300_classical().items():
                        _safe(evaluate, "phase3", results, name, protocol, mname, classical(pipe), X, y, meta,
                              args.seeds, needs_seed=False)
                    deep_names = P300_DEEP
                for mname in deep_names:
                    if args.models and mname not in args.models:
                        continue
                    cls_name, train = DEEP[mname]
                    make = deep(braindecode_builder(cls_name, cfg["resample"]), **_deep_kw(train, args.epochs, args.batch_size))
                    _safe(evaluate, "phase3", results, name, protocol, mname, make, X, y, meta, args.seeds, fold_hook=hook)


FOUNDATION_DATASETS = {
    "BNCI2014_001": ["standard", "cross_subject"],
    "BNCI2014_004": ["standard", "cross_subject"],
    "PhysionetMI": ["cross_subject_fixed:1-70:90-109"],
}


def run_foundation(results, args):
    for name, protocols in FOUNDATION_DATASETS.items():
        if args.datasets and name not in args.datasets:
            continue
        cfg = MI_DATASETS[name]
        for mname, (_, _, sf, patch, _) in FOUNDATION.items():
            if args.models and mname not in args.models:
                continue
            print(f"\n[phase 4] {name} | {mname} (resampled to {sf} Hz)")
            try:
                X, y, meta, info, _ = load(name, sf, _subjects(args.quick), True)
                Xc = crop_to_patches(X, sf, patch)
                make = deep(foundation_builder(mname, info),
                            **_deep_kw(FOUNDATION_TRAIN, args.foundation_epochs, args.batch_size))
            except NotApplicable as e:
                print(f"  - {name} | {mname}: not applicable ({e})")
                continue
            except Exception as e:
                log_error("phase4", f"{name} | {mname}: setup failed ({type(e).__name__}: {e})")
                continue
            for protocol in protocols:
                _safe(evaluate, "phase4", results, name, protocol, f"{mname} (fine-tuned)", make, Xc, y, meta, args.seeds)
    if args.tuab_path:
        run_tuab(results, args)
    else:
        print("\n[phase 4] TUAB skipped (pass --tuab-path after getting TUH access)")


# ------------------------------------------------------------------ TUAB

TUAB_CHANNELS = ["FP1", "FP2", "F7", "F3", "FZ", "F4", "F8", "T3", "C3", "CZ", "C4", "T4",
                 "T5", "P3", "PZ", "P4", "T6", "O1", "O2", "A1", "A2"]


def _tuh_name(ch):
    return ch.upper().replace("EEG ", "").split("-")[0].strip()


def tuab_windows(concat_ds, sfreq=200, window_s=10, skip_s=60, max_windows=12):
    """Referential 21-channel montage, 0.1-75 Hz, 10-s windows; first max_windows per recording after skip_s."""
    from braindecode.preprocessing import Preprocessor, create_fixed_length_windows, preprocess

    def pick(raw):
        raw.rename_channels({c: _tuh_name(c) for c in raw.ch_names})
        missing = [c for c in TUAB_CHANNELS if c not in raw.ch_names]
        if missing:
            raise ValueError(f"missing {missing}")
        return raw.pick(TUAB_CHANNELS)

    preprocess(concat_ds, [Preprocessor(pick, apply_on_array=False), Preprocessor("resample", sfreq=sfreq),
                           Preprocessor("filter", l_freq=0.1, h_freq=75.0)], n_jobs=-1)
    w = create_fixed_length_windows(concat_ds, start_offset_samples=skip_s * sfreq,
                                    window_size_samples=window_s * sfreq, window_stride_samples=window_s * sfreq,
                                    drop_last_window=True, preload=False)
    X, y, meta = [], [], []
    for rec, wd in enumerate(w.datasets):
        desc = wd.description
        for i in range(min(max_windows, len(wd))):
            X.append(np.clip(wd[i][0] * 1e6, -800, 800).astype(np.float32))
            y.append(int(bool(desc["pathological"])))
            meta.append(dict(subject=str(desc.get("subject", rec)), session="0",
                             run="0train" if bool(desc["train"]) else "1test"))
    return np.stack(X), np.asarray(y), pd.DataFrame(meta)


def run_tuab(results, args):
    from braindecode.datasets import TUHAbnormal
    print(f"\n[phase 4] TUAB from {args.tuab_path}")
    try:
        ds = TUHAbnormal(args.tuab_path, target_name="pathological", preload=False, on_missing_files="warn")
        if args.quick:
            from braindecode.datasets import BaseConcatDataset
            ds = BaseConcatDataset(ds.datasets[:8])
        X, y, meta = tuab_windows(ds, max_windows=args.tuab_windows)
    except Exception as e:
        log_error("phase4", f"TUAB: could not load ({type(e).__name__}: {e})")
        return
    # "standard" = official TUAB train/eval split; windows from the first minutes of each recording
    protocol = "standard"
    names = ["ShallowConvNet", "DeepConvNet", "EEGNet"] + list(FOUNDATION)
    for mname in names:
        if args.models and mname not in args.models:
            continue
        if mname in FOUNDATION:
            info = mne.create_info(TUAB_CHANNELS, 200, "eeg")
            make = deep(foundation_builder(mname, info), **_deep_kw(FOUNDATION_TRAIN, args.foundation_epochs, args.batch_size))
            Xm, label = crop_to_patches(X, 200, FOUNDATION[mname][3]), f"{mname} (fine-tuned)"
        else:
            cls_name, train = DEEP[mname]
            make = deep(braindecode_builder(cls_name, 200), **_deep_kw(train, min(args.epochs, 50), args.batch_size))
            Xm, label = X, mname
        _safe(evaluate, "phase4", results, "TUAB", protocol, label, make, Xm, y, meta, args.seeds,
              extra=dict(note=f"{args.tuab_windows} windows/recording"))


def _safe(fn, phase, results, dataset, protocol, model, *a, **kw):
    try:
        fn(phase, results, dataset, protocol, model, *a, **kw)
    except NotApplicable as e:
        print(f"  - {dataset} | {protocol} | {model}: not applicable ({e})")
    except Exception as e:
        log_error(phase, f"{dataset} | {protocol} | {model}: {type(e).__name__}: {e}")
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
