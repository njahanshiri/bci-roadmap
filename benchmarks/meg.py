"""MEG benchmarks (phase 11): sanity sets, evoked decoding, motor, speech, vision, emotion, brain age.

Source of truth for datasets, protocols and published numbers: projects/meg/DATASETS.md.

| Dataset (name in results) | How it is obtained | Protocol(s) | Models | Tested here |
|---|---|---|---|---|
| MNE sample (`MNE-sample`): auditory/visual x left/right, 4 classes | MNE fetcher (`mne.datasets.sample`, 1.6 GB) | `within_session:5` | PCA+LR, XdawnCov+TS+LR, EEGNet | yes, full (1 subject) |
| MNE somato (`MNE-somato`): post-stimulus (0.5-1.5 s) vs pre-stimulus (-1.5 to -0.5 s) window | MNE fetcher (`mne.datasets.somato`, 0.6 GB) | `leave_one_run_out` (trials in 5 groups, both windows of a trial in one group) | PCA+LR, Cov+TS+LR, EEGNet | yes, full |
| Brainstorm auditory (`MNE-bst-auditory`): standard vs deviant tone | MNE fetcher (`mne.datasets.brainstorm.bst_auditory`, 1.6 GB, needs `--accept-licenses` (Brainstorm licence); skipped in `--quick` unless named) | `leave_one_run_out` (2 runs) | PCA+LR, XdawnCov+TS+LR, EEGNet | partial: same code path as MNE-sample; not downloaded |
| Wakeman & Henson faces (`WakemanHenson`): famous / unfamiliar / scrambled | auto-download per run from OpenNeuro ds000117 (16 subjects x 6 runs x ~0.87 GB) | `leave_one_run_out` (within subject), `cross_subject` (LOSO) | PCA+LR, EEGNet | yes, quick (2 subjects x run 1) |
| BCI Competition IV ds3 (`BCICIV-3`): 4 wrist-movement directions | auto-download (bbci.de, 15 MB, plus true test labels) | `standard` (official 160 train / 74 + 73 test trials) | PCA+LR, Cov+TS+LR, EEGNet, ShallowConvNet | yes, full |
| MEG-MASC (`MEG-MASC`): voiced vs voiceless phoneme, -0.2 to 0.6 s around phoneme onset | official `pnpl` package (`Gwilliams2022`, downloads from OSF) | `leave_one_run_out` = per subject and session, leave one story out (no segment shared across splits) | PCA+LR, EEGNet | yes, quick (subject 01, session 0, stories 0-1) |
| THINGS-MEG (`THINGS-MEG`): identity of the 200 repeated test images (200-way, single trial) | auto-download per run from OpenNeuro ds004212 (CTF .ds folders, 0.53 GB per run; all 480 runs are needed in a full run) | `cross_session` (per subject, leave one of 12 sessions out) | PCA+LR, EEGNet | yes, quick (BIGMEG1, run 1 of sessions 1-2) |
| LibriBrain speech (`LibriBrain-Speech`): speech vs silence | official `pnpl` package (`LibriBrain`, Hugging Face pnpl/LibriBrain) | `standard` = official train / test sessions (validation unused) | PCA+LR, ResNet1D | yes, quick (1 train session + test session, windows capped) |
| LibriBrain phonemes (`LibriBrain-Phoneme`, 39 classes, single 0.5-s windows; `LibriBrain-Phoneme-avg100`, groups of 100 same-phoneme windows averaged, as in the competition track) | official `pnpl` package | `standard` | PCA+LR, ResNet1D | yes, quick |
| Armeni 2022 (`Armeni2022`): voiced vs voiceless phoneme | `--path armeni=FOLDER` (Donders DUA); read with `pnpl` `Armeni2022` (downloads only if RADBOUD_USERNAME/RADBOUD_PASSWORD are set) | `leave_one_run_out` = per subject, leave one session (story) out | PCA+LR, EEGNet | no (gated) |
| MEG emotion videos (`Emotion-ds007640`): valence x arousal quadrant (4 classes), 4-s windows during clips | auto-download per session from OpenNeuro ds007640 (~1.1 GB each) | `cross_subject` (each session is one quadrant, so within-subject splits would decode the session) | BandPower+LR, EEGNet | partial: loader on sub-01 session 1 only (one class, so no model run) |
| Cam-CAN (`CamCAN`): brain age (regression, years) from resting MEG | `--path camcan=FOLDER` (data request) | `cross_subject` (GroupKFold 5), metric `mae` | BandPower+Ridge | partial: synthetic folder in the BIDS layout |
| MOUS (`MOUS-visual`, `MOUS-auditory`): sentence vs word list, epochs at the matched target word | `--path mous=FOLDER` (Donders DUA, BIDS with CTF .ds) | `cross_subject` (GroupKFold 5) | PCA+LR, EEGNet | no (gated) |
| HCP MEG (`HCP-MEG`): which task the subject is doing (rest / working memory / story-math / motor), 2-s windows | `--path hcp_meg=FOLDER` (ConnectomeDB, unprocessed 4D layout `<subject>/unprocessed/MEG/<n>-<task>/4D/c,rfDC`) | `cross_subject` (GroupKFold 5) | BandPower+LR, EEGNet | no (gated) |
| OMEGA (`OMEGA`): participant group from resting MEG | `--path omega=FOLDER` (controlled access, BIDS) | `cross_subject` (GroupKFold 5) | BandPower+LR | partial: synthetic folder in the BIDS layout |
| DECOMEG / Brain2Qwerty v1 (`Brain2Qwerty`): typed character (letters + space), -0.5 to 0.2 s around each keystroke | `--path brain2qwerty=FOLDER`: local copy of Hugging Face bcbl190626/SpanishBCBL (public, no login, ~262 GB); events built with the official `studies` package from github.com/facebookresearch/brain2qwerty (+ `neuralset`) | `leave_one_run_out` = per subject and recording, 5 sentence-disjoint folds | PCA+LR, EEGNet | no (needs the 262 GB data and the brain2qwerty repo) |

Notes:
- Epoch-based sets are band-passed (0.5-40 Hz unless stated), decimated to ~100 Hz, scaled to pT (pT/m for
  planar gradiometers) and written once to float16 memmaps under `<data-dir>/meg/cache/`; evaluate() reads
  them lazily, so memory stays at one fold. Subjects are loaded one at a time.
- LibriBrain and MEG-MASC windows come from pnpl at 250 Hz and are resampled to 50 Hz. LibriBrain speech
  windows (0.5 s, non-overlapping, as pnpl's default) are labelled by their centre sample; F1 is computed per
  window, not per sample as in the competition. The competition holdout labels are hidden, so the official
  test split is used and no competition leaderboard number is comparable.
- MEG-MASC: a simpler published-style task (phonetic-feature decoding), not the Defossez retrieval protocol,
  and not compared with it.
- Emotion set: clip onsets/offsets are triggers 112/113 on the `Stimulus` channel; this is inferred from the
  recordings (10 pairs per session = 10 trials in beh.tsv), not documented in the dataset README.
- Cam-CAN: deep regression and source-space features are not included (sensor band power only).
"""
import glob
import os
import re
import zlib

import mne
import numpy as np
import pandas as pd
from pyriemann.estimation import Covariances, XdawnCovariances
from pyriemann.tangentspace import TangentSpace
from scipy.signal import resample_poly
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression, RidgeCV
from sklearn.metrics import f1_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from common import NotApplicable, _safe, classical, deep, download, evaluate, log_error, resnet1d
from ecg import Rows, wanted
from eeg import DEEP, braindecode_builder
from eeg_more import band_powers, evaluate_custom, regression_scores, time_bins

PHASE = "phase11"
SF = 100  # Hz after decimation for epoch-based sets
SCALE = 1e12  # T -> pT
S3 = "https://s3.amazonaws.com/openneuro.org"
PNPL_CAP = 5000  # ponytail: max phoneme windows per pnpl run (MEG-MASC story / Armeni session); raise on a big disk
LIBRI_CLASSICAL_MAX = 100_000  # ponytail: classical models train on a random subset of LibriBrain train windows
mne.set_log_level("ERROR")


# ------------------------------------------------------------------ helpers

def attempt(name, fn, *a):
    print(f"\n[{PHASE}] {name}")
    try:
        return fn(*a)
    except Exception as e:
        log_error(PHASE, f"{name}: could not load ({type(e).__name__}: {e})")


def gated(args, key, name):
    folder = args.paths.get(key)
    if not folder:
        print(f"\n[{PHASE}] {name}: skipped (access-gated; pass --path {key}=FOLDER)")
    return folder


def openneuro(ds, rel, root):
    """One file from the public OpenNeuro S3 bucket, kept at <root>/<ds>/<rel>."""
    return download(f"{S3}/{ds}/{rel}", os.path.join(root, ds, rel), quiet=True)


def openneuro_dir(ds, rel, root):
    """A folder (e.g. a CTF .ds) from OpenNeuro S3: list its keys, download each."""
    import urllib.request
    dst = os.path.join(root, ds, rel)
    if not os.path.exists(dst + ".done"):
        with urllib.request.urlopen(f"{S3}?list-type=2&prefix={ds}/{rel}/") as r:
            keys = re.findall(r"<Key>(.*?)</Key>", r.read().decode())
        if not keys:
            raise FileNotFoundError(f"{ds}/{rel}")
        for k in keys:
            download(f"{S3}/{k}", os.path.join(root, k), quiet=True)
        open(dst + ".done", "w").close()
    return dst


def epoch(raw, onsets, tmin, tmax, band=(0.5, 40.0), sf=SF):
    """Filtered, decimated MEG epochs (pT) at onsets given in seconds from the start of the file.

    Reference channels are kept while filtering (CTF compensation needs them) and dropped from the output.
    Returns X (n, ch, t), indices of the onsets that fit in the recording, channel names.
    """
    raw.pick(mne.pick_types(raw.info, meg=True, ref_meg=True, exclude=()))
    raw.load_data()
    raw.filter(*band)
    fs = raw.info["sfreq"]
    onsets = np.asarray(onsets, dtype=float)
    ev = np.c_[np.round(onsets * fs).astype(int) + raw.first_samp, np.zeros(len(onsets), int), np.ones(len(onsets), int)]
    ep = mne.Epochs(raw, ev, tmin=tmin, tmax=tmax, baseline=None, decim=max(1, round(fs / sf)), preload=True,
                    reject=None, event_repeated="drop")
    picks = mne.pick_types(ep.info, meg=True, ref_meg=False, exclude=())
    X = ep.get_data(picks=picks) * SCALE
    return X.astype(np.float32), ep.selection, [ep.ch_names[i] for i in picks]


def store(path, n_max, parts):
    """Write parts (X, list of row dicts) once into a float16 .npy memmap (capacity n_max) plus a .csv table.

    A part whose shape differs from the first (e.g. a subject with another channel count) is logged and skipped.
    """
    if not os.path.exists(path + ".done"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        X, info = None, []
        for x, rows in parts:
            if X is None:
                X = np.lib.format.open_memmap(path + ".npy", "w+", np.float16, (n_max, *x.shape[1:]))
            if x.shape[1:] != X.shape[1:]:
                log_error(PHASE, f"{os.path.basename(path)}: skipped a part with shape {x.shape[1:]} != {X.shape[1:]}")
                continue
            k = min(len(x), n_max - len(info))
            X[len(info):len(info) + k] = np.clip(np.nan_to_num(x[:k]), -6e4, 6e4)
            info += rows[:k]
        if X is None or not info:
            raise RuntimeError("no data loaded")
        X.flush()
        del X
        pd.DataFrame(info).to_csv(path + ".csv", index=False)
        open(path + ".done", "w").close()
    table = pd.read_csv(path + ".csv", dtype=str, keep_default_na=False)
    return np.load(path + ".npy", mmap_mode="r")[:len(table)], table


def split_table(table):
    return table.label.values, table[["subject", "session", "run"]].reset_index(drop=True)


def guarded(name, gen):
    """Run a per-subject generator, logging (not raising) errors of single items; the generator yields
    callables so that one failing subject or run does not end the dataset."""
    for item in gen:
        try:
            out = item()
        except Exception as e:
            log_error(PHASE, f"{name}: {type(e).__name__}: {e}")
            continue
        if out is not None:
            yield out


def chunked(fn, X, chunk=2048):
    return np.concatenate([fn(np.asarray(X[i:i + chunk], dtype=np.float32)) for i in range(0, len(X), chunk)])


# ------------------------------------------------------------------ models

def lr():
    return LogisticRegression(max_iter=1000)


class ChannelScaler(TransformerMixin, BaseEstimator):
    """Divide each channel by its training-set std, so magnetometers and gradiometers get equal weight in
    covariance models (without it, Xdawn/OAS on mixed pT and pT/m units fail or fall to chance)."""

    def fit(self, X, y=None):
        self.sd_ = np.asarray(X).std(axis=(0, 2), keepdims=True)[0] + 1e-12
        return self

    def transform(self, X):
        return np.asarray(X) / self.sd_


PIPELINES = {  # name -> (feature function of (X, sf) or None for raw epochs, pipeline factory)
    "PCA+LR": (lambda X, sf: chunked(time_bins, X), lambda: make_pipeline(StandardScaler(), PCA(0.99), lr())),
    "BandPower+LR": (lambda X, sf: chunked(lambda x: band_powers(x, sf), X), lambda: make_pipeline(StandardScaler(), lr())),
    "XdawnCov+TS+LR": (None, lambda: make_pipeline(ChannelScaler(), XdawnCovariances(4, estimator="oas", xdawn_estimator="oas"),
                                                   TangentSpace(), lr())),
    "Cov+TS+LR": (None, lambda: make_pipeline(ChannelScaler(), Covariances("oas"), TangentSpace(), lr())),
}


def bench(results, args, dname, X, y, meta, protocols, sf, models=("PCA+LR", "EEGNet"), epochs=100, hook=None,
          batch_size=None):
    """Classical models on precomputed features (or raw epochs when small), deep models on the (lazy) epochs."""
    lazy = Rows(X) if isinstance(X, np.memmap) else X
    feats = {}
    for protocol in protocols:
        for m in models:
            if m in PIPELINES:
                fn, pipe = PIPELINES[m]
                if fn is None and X.nbytes > 4e9:
                    print(f"  - {dname} | {m}: skipped (epochs too large for an in-memory covariance model)")
                    continue
                if m not in feats:
                    feats[m] = fn(X, sf) if fn else np.asarray(X, dtype=np.float32)
                _safe(evaluate, PHASE, results, dname, protocol, m, classical(pipe()), feats[m], y, meta,
                      args.seeds, needs_seed=False, fold_hook=hook)
            elif not args.models or m in args.models:
                if m == "ResNet1D":
                    build, train = resnet1d, dict(lr=1e-3, weight_decay=1e-2)
                else:
                    cls, train = DEEP[m]
                    build = braindecode_builder(cls, sf)
                make = deep(build, epochs=min(args.epochs, epochs), batch_size=batch_size or args.batch_size, **train)
                _safe(evaluate, PHASE, results, dname, protocol, m, make, lazy, y, meta, args.seeds, fold_hook=hook)


def cache_path(args, name):
    return os.path.join(args.data_dir, "meg", "cache", f"{name}{'_quick' if args.quick else ''}")


# ------------------------------------------------------------------ MNE example datasets

def load_sample(root):
    p = mne.datasets.sample.data_path(path=root)
    raw = mne.io.read_raw_fif(os.path.join(p, "MEG", "sample", "sample_audvis_raw.fif"))
    ev = mne.find_events(raw, stim_channel="STI 014")
    ev = ev[np.isin(ev[:, 2], [1, 2, 3, 4])]
    names = {1: "auditory_left", 2: "auditory_right", 3: "visual_left", 4: "visual_right"}
    X, sel, _ = epoch(raw, (ev[:, 0] - raw.first_samp) / raw.info["sfreq"], 0.0, 0.5)
    y = np.array([names[c] for c in ev[sel, 2]])
    return X, y, pd.DataFrame(dict(subject="sample", session="0", run="0"), index=range(len(y)))


def load_somato(root):
    p = mne.datasets.somato.data_path(path=root)
    raw = mne.io.read_raw_fif(os.path.join(p, "sub-01", "meg", "sub-01_task-somato_meg.fif"))
    ev = mne.find_events(raw, stim_channel="STI 014")
    t = (ev[:, 0] - raw.first_samp) / raw.info["sfreq"]
    X, sel, _ = epoch(raw, np.r_[t - 1.5, t + 0.5], 0.0, 1.0, band=(1.0, 40.0))
    trial = np.r_[np.arange(len(t)), np.arange(len(t))][sel]
    y = np.where(sel < len(t), "pre_stimulus", "post_stimulus")
    return X, y, pd.DataFrame(dict(subject="01", session="0", run=(trial % 5).astype(str)))


def load_bst_auditory(root, accept=False):
    if not accept:
        raise NotApplicable("needs the Brainstorm licence (https://neuroimage.usc.edu/brainstorm/License); "
                            "rerun with --accept-licenses to accept it")
    p = mne.datasets.brainstorm.bst_auditory.data_path(path=root, accept=True)
    Xs, ys, runs = [], [], []
    for run, f in enumerate(["S01_AEF_20131218_01.ds", "S01_AEF_20131218_02.ds"], 1):
        raw = mne.io.read_raw_ctf(os.path.join(p, "MEG", "bst_auditory", f))
        ev = mne.find_events(raw, stim_channel="UPPT001")
        ev = ev[np.isin(ev[:, 2], [1, 2])]
        X, sel, _ = epoch(raw, (ev[:, 0] - raw.first_samp) / raw.info["sfreq"], 0.0, 0.5)
        Xs.append(X)
        ys += ["standard" if c == 1 else "deviant" for c in ev[sel, 2]]
        runs += [str(run)] * len(sel)
    return np.concatenate(Xs), np.array(ys), pd.DataFrame(dict(subject="S01", session="0", run=runs))


# ------------------------------------------------------------------ Wakeman & Henson (ds000117)

FACES = {"FF": "famous", "UF": "unfamiliar", "SF": "scrambled"}


def wh_run(root, s, r):
    base = f"sub-{s:02d}/ses-meg/meg/sub-{s:02d}_ses-meg_task-facerecognition_run-{r:02d}"
    ev = pd.read_csv(openneuro("ds000117", base + "_events.tsv", root), sep="\t")
    ev = ev[ev.trial_type.str[-2:].isin(list(FACES))]
    raw = mne.io.read_raw_fif(openneuro("ds000117", base + "_meg.fif", root))
    X, sel, _ = epoch(raw, ev.onset.values + 0.034, 0.0, 0.8)  # 34 ms trigger-to-screen delay
    labels = ev.trial_type.str[-2:].map(FACES).values[sel]
    return X, [dict(label=l, subject=f"{s:02d}", session="meg", run=str(r)) for l in labels]


def load_wh(args, root):
    subjects, runs = ([1, 2], [1]) if args.quick else (range(1, 17), range(1, 7))
    parts = guarded("WakemanHenson", (lambda s=s, r=r: wh_run(root, s, r) for s in subjects for r in runs))
    return store(cache_path(args, "wakeman_henson"), len(subjects) * len(runs) * 200, parts)


# ------------------------------------------------------------------ BCI Competition IV ds3

BCI3_URL = "https://www.bbci.de/competition/download/competition_iv/BCICIV_3_mat.zip"
BCI3_LABELS = "https://www.bbci.de/competition/iv/results/ds3/true_labels.zip"


def load_bci3(root):
    import scipy.io as sio
    from common import unzip
    print("  BCI Competition IV ds3: free for research; credit the Tuebingen MEG group and cite Waldert et al. 2008")
    for url in (BCI3_URL, BCI3_LABELS):
        dst = os.path.join(root, os.path.basename(url))
        if not os.path.exists(dst):
            unzip(download(url, dst, quiet=True), root)
    Xs, ys, metas = [], [], []
    for s in (1, 2):
        m = sio.loadmat(os.path.join(root, f"S{s}.mat"))
        tr = m["training_data"][0]  # per class: (trial, time, channel), fT
        te = m["test_data"]
        y_te = sio.loadmat(os.path.join(root, f"TrueLabelsS{s}.mat"))[f"TrueLabelsS{s}"].ravel()
        X = np.concatenate([*tr, te]).transpose(0, 2, 1) * 1e-3  # fT -> pT
        y = np.r_[np.repeat([1, 2, 3, 4], [len(c) for c in tr]), y_te]
        Xs.append(X.astype(np.float32))
        ys.append(y.astype(str))
        metas.append(pd.DataFrame(dict(subject=str(s), session="0", run=["train"] * (len(y) - len(y_te)) + ["test"] * len(y_te))))
    return np.concatenate(Xs), np.concatenate(ys), pd.concat(metas, ignore_index=True)


# ------------------------------------------------------------------ pnpl phoneme voicing (MEG-MASC, Armeni)

def pnpl_voicing(dataset_cls, task_cls, root, subject, download, run_field, **include):
    """Voiced / voiceless phoneme windows (-0.2..0.6 s) of one subject, at most PNPL_CAP per run, 250 -> 50 Hz."""
    ds = dataset_cls(data_path=root, task=task_cls(tmin=-0.2, tmax=0.6, label_type="voicing"),
                     include_subjects=[subject], standardize=False, download=download, **include)
    rng = np.random.default_rng(0)
    keys = pd.Series([(s[1], s[2]) for s in ds.samples])
    idx = np.concatenate([rng.permutation(np.flatnonzero(keys == k))[:PNPL_CAP] for k in keys.unique()])
    down = int(round(ds.sfreq / 50))
    X = np.stack([resample_poly(ds[int(i)][0].numpy() * SCALE, 1, down, axis=-1) for i in idx])
    rows = [dict(label="voiced" if ds.task.get_label(ds.samples[i]) else "voiceless", subject=subject,
                 session=ds.samples[i][1] if run_field == "task" else "0",
                 run=ds.samples[i][2] if run_field == "task" else ds.samples[i][1]) for i in idx]
    return X.astype(np.float32), rows


def load_masc(args, root):
    from pnpl.datasets import Gwilliams2022
    from pnpl.tasks.gwilliams2022 import PhonemeClassification
    subjects = ["01"] if args.quick else [f"{i:02d}" for i in range(1, 28)]
    include = dict(include_sessions=["0"], include_tasks=["0", "1"]) if args.quick else {}
    parts = guarded("MEG-MASC", (lambda s=s: pnpl_voicing(Gwilliams2022, PhonemeClassification, root, s, True,
                                                          "task", **include) for s in subjects))
    return store(cache_path(args, "meg_masc"), len(subjects) * 8 * PNPL_CAP, parts)


def load_armeni(args, folder):
    from pnpl.datasets import Armeni2022
    from pnpl.tasks.armeni2022 import PhonemeClassification
    subjects = ["001"] if args.quick else ["001", "002", "003"]
    include = dict(include_sessions=["001", "002"]) if args.quick else {}
    dl = bool(os.environ.get("RADBOUD_USERNAME"))
    parts = guarded("Armeni2022", (lambda s=s: pnpl_voicing(Armeni2022, PhonemeClassification, folder, s, dl,
                                                            "session", **include) for s in subjects))
    return store(cache_path(args, "armeni2022"), len(subjects) * 10 * PNPL_CAP, parts)


# ------------------------------------------------------------------ THINGS-MEG (ds004212)

def things_run(root, sub, ses, run):
    base = f"sub-{sub}/ses-{ses:02d}/meg/sub-{sub}_ses-{ses:02d}_task-main_run-{run:02d}"
    ev = pd.read_csv(openneuro("ds004212", base + "_events.tsv", root), sep="\t")
    ev = ev[ev.trial_type == "test"]
    raw = mne.io.read_raw_ctf(openneuro_dir("ds004212", base + "_meg.ds", root))
    X, sel, _ = epoch(raw, ev.onset.values, 0.0, 0.8)
    labels = ev.things_category_nr.astype(int).astype(str).values[sel]
    return X, [dict(label=l, subject=sub, session=str(ses), run=str(run)) for l in labels]


def load_things(args, root):
    subs, sess, runs = (["BIGMEG1"], [1, 2], [1]) if args.quick else (
        [f"BIGMEG{i}" for i in range(1, 5)], range(1, 13), range(1, 11))
    parts = guarded("THINGS-MEG", (lambda a=a, b=b, c=c: things_run(root, a, b, c) for a in subs for b in sess for c in runs))
    return store(cache_path(args, "things_meg"), len(subs) * len(sess) * len(runs) * 20, parts)


# ------------------------------------------------------------------ emotion videos (ds007640)

EMO_TASKS = {1: "HAHV", 2: "HALV", 3: "LAHV", 4: "LALV"}
EMO_WIN = 4.0


def emotion_session(root, s, k):
    task = EMO_TASKS[k]
    raw = mne.io.read_raw_fif(openneuro("ds007640", f"sub-{s:02d}/ses-{k:02d}/meg/sub-{s:02d}_ses-{k:02d}_task-{task}_meg.fif", root))
    ev = mne.find_events(raw, stim_channel="Stimulus", min_duration=0.002)
    fs, t = raw.info["sfreq"], (ev[:, 0] - raw.first_samp) / raw.info["sfreq"]
    starts, ends = t[ev[:, 2] == 112], t[ev[:, 2] == 113]
    Xs, rows = [], []
    for clip, a in enumerate(starts):
        b = ends[ends > a][0] if (ends > a).any() else raw.times[-1]
        seg = raw.copy().crop(a, b)
        X, _, _ = epoch(seg, np.arange(0, b - a - EMO_WIN, EMO_WIN), 0.0, EMO_WIN - 1 / fs, band=(1.0, 45.0))
        Xs.append(X)
        rows += [dict(label=task, subject=f"{s:02d}", session=str(k), run=str(clip))] * len(X)
    return np.concatenate(Xs), rows


def load_emotion(args, root):
    pairs = [(1, 1)] if args.quick else [(s, k) for s in range(1, 24) for k in EMO_TASKS]
    parts = guarded("Emotion-ds007640", (lambda s=s, k=k: emotion_session(root, s, k) for s, k in pairs))
    return store(cache_path(args, "emotion_ds007640"), len(pairs) * 400, parts)


# ------------------------------------------------------------------ LibriBrain (pnpl)

def libribrain_split(root, kind, quick):
    """Train / test pnpl datasets for one track (official sessions; test standardized with train statistics)."""
    from pnpl.datasets import LibriBrain
    from pnpl.datasets.libribrain2025.constants import RUN_KEYS, TEST_RUN_KEYS, VALIDATION_RUN_KEYS
    from pnpl.tasks import PhonemeClassification, SpeechDetection
    held = {tuple(k) for k in VALIDATION_RUN_KEYS} | {tuple(k) for k in TEST_RUN_KEYS}
    train_keys = [tuple(k) for k in RUN_KEYS if tuple(k) not in held][:1 if quick else None]
    task = (lambda: SpeechDetection(tmin=0.0, tmax=0.5)) if kind == "speech" else (lambda: PhonemeClassification(tmin=0.0, tmax=0.5))
    tr = LibriBrain(data_path=root, task=task(), include_run_keys=train_keys)
    te = LibriBrain(data_path=root, task=task(), include_run_keys=[tuple(k) for k in TEST_RUN_KEYS],
                    channel_means=tr.channel_means, channel_stds=tr.channel_stds)
    return tr, te


def libribrain_parts(ds, part, kind, cap, chunk=1024):
    """Windows of a pnpl dataset (250 Hz, standardized) resampled to 50 Hz, with their labels."""
    idx = np.arange(len(ds))
    if cap and len(idx) > cap:
        idx = np.sort(np.random.default_rng(0).choice(idx, cap, replace=False))
    for a in range(0, len(idx), chunk):
        sub = idx[a:a + chunk]
        X = resample_poly(np.stack([ds[int(i)][0].numpy() for i in sub]), 1, 5, axis=-1)
        if kind == "speech":
            labels = ["speech" if ds.samples[i][5][len(ds.samples[i][5]) // 2] else "silence" for i in sub]
        else:
            labels = [ds.samples[i][5].split("_")[0] for i in sub]
        yield X.astype(np.float32), [dict(label=l, subject="0", session="0", run=part) for l in labels]


def load_libribrain(args, root, kind):
    tr, te = libribrain_split(root, kind, args.quick)
    cap = (3000, 1000) if args.quick else (None, None)
    n = min(len(tr), cap[0] or len(tr)) + min(len(te), cap[1] or len(te))

    def parts():
        yield from libribrain_parts(tr, "train", kind, cap[0])
        yield from libribrain_parts(te, "test", kind, cap[1])
    return store(cache_path(args, f"libribrain_{kind}"), n, parts())


def average_groups(X, y, meta, size=100):
    """Competition-style phoneme samples: consecutive windows of the same phoneme, within each split, averaged in
    groups of `size` (incomplete groups dropped)."""
    Xs, ys, runs = [], [], []
    for part in ("train", "test"):
        for label in np.unique(y):
            idx = np.flatnonzero((meta.run.values == part) & (y == label))
            for g in range(len(idx) // size):
                Xs.append(np.asarray(X[idx[g * size:(g + 1) * size]], dtype=np.float32).mean(0))
                ys.append(label)
                runs.append(part)
    if not Xs or "test" not in runs or "train" not in runs:
        raise RuntimeError(f"no complete groups of {size} in both splits")
    return np.stack(Xs), np.array(ys), pd.DataFrame(dict(subject="0", session="0", run=runs))


def classical_subset(X, y, meta, max_train):
    """All test windows plus a random subset of training windows (classical models only)."""
    tr, te = np.flatnonzero(meta.run.values == "train"), np.flatnonzero(meta.run.values == "test")
    if len(tr) > max_train:
        tr = np.sort(np.random.default_rng(0).choice(tr, max_train, replace=False))
    keep = np.r_[tr, te]
    return chunked(lambda x: time_bins(x, 5), Rows(X, keep)), y[keep], meta.iloc[keep].reset_index(drop=True)


def run_libribrain(results, args, root):
    hooks = {"speech": lambda yt, yp: {"f1_speech": f1_score(yt, yp, pos_label="speech")}, "phoneme": None}
    for kind, dname in (("speech", "LibriBrain-Speech"), ("phoneme", "LibriBrain-Phoneme")):
        if not wanted(args, dname, "LibriBrain", "LibriBrain-Phoneme-avg100"):
            continue
        data = attempt(dname, load_libribrain, args, root, kind)
        if data is None:
            continue
        X, table = data
        y, meta = split_table(table)
        if wanted(args, dname, "LibriBrain"):
            F, yf, mf = classical_subset(X, y, meta, LIBRI_CLASSICAL_MAX)
            _safe(evaluate, PHASE, results, dname, "standard", "PCA+LR",
                  classical(PIPELINES["PCA+LR"][1]()), F, yf, mf, args.seeds, needs_seed=False, fold_hook=hooks[kind])
            bench(results, args, dname, X, y, meta, ["standard"], 50, models=("ResNet1D",), epochs=20,
                  hook=hooks[kind], batch_size=256)
        if kind == "phoneme" and wanted(args, "LibriBrain-Phoneme-avg100", "LibriBrain"):
            avg = attempt("LibriBrain-Phoneme-avg100", average_groups, X, y, meta)
            if avg is not None:
                bench(results, args, "LibriBrain-Phoneme-avg100", *avg, ["standard"], 50, models=("PCA+LR", "ResNet1D"),
                      epochs=50)


# ------------------------------------------------------------------ resting-state, subject-level (Cam-CAN, OMEGA)

REST_BANDS = ((1, 4), (4, 8), (8, 13), (13, 30), (30, 45))


def rest_features(path, seconds=300):
    """Log band power per MEG channel over the first `seconds` of a resting recording (Welch)."""
    raw = mne.io.read_raw(path)
    raw.crop(0, min(seconds, raw.times[-1]))
    psd = raw.compute_psd(fmin=1, fmax=45, picks=mne.pick_types(raw.info, meg=True, ref_meg=False, exclude=()))
    P, f = psd.get_data(), psd.freqs
    return np.log(np.concatenate([P[:, (f >= a) & (f < b)].mean(1) for a, b in REST_BANDS]) + 1e-40)


def subject_of(path):
    m = re.search(r"sub-([A-Za-z0-9]+)", path)
    return m.group(1) if m else None


def rest_table(args, name, files, targets):
    """Features for one recording per subject that has a target; cached as .npz."""
    path = cache_path(args, name) + ".npz"
    if os.path.exists(path):
        d = np.load(path, allow_pickle=True)
        return d["F"], d["y"], d["subjects"]
    seen, F, y, subs = set(), [], [], []
    for f in sorted(files):
        s = subject_of(f)
        if s is None or s in seen or s not in targets:
            continue
        try:
            F.append(rest_features(f))
        except Exception as e:
            log_error(PHASE, f"{name}: {f}: {type(e).__name__}: {e}")
            continue
        seen.add(s)
        y.append(targets[s])
        subs.append(s)
        if args.quick and len(subs) >= 10:
            break
    n = pd.Series([len(x) for x in F]).mode()[0]  # drop subjects with another channel count
    keep = [i for i, x in enumerate(F) if len(x) == n]
    F, y, subs = np.stack([F[i] for i in keep]), np.array([y[i] for i in keep]), np.array([subs[i] for i in keep])
    os.makedirs(os.path.dirname(path), exist_ok=True)
    np.savez(path, F=F, y=y, subjects=subs)
    return F, y, subs


def participants(folder, column, alt_file=None, alt_id=None, alt_col=None):
    """{subject: value} from a BIDS participants.tsv column (case-insensitive), else from an alternative csv."""
    for p in glob.glob(os.path.join(folder, "**", "participants.tsv"), recursive=True):
        t = pd.read_csv(p, sep="\t")
        cols = {c.lower(): c for c in t.columns}
        if column in cols:
            return {str(i).replace("sub-", ""): v for i, v in zip(t[cols["participant_id"]], t[cols[column]]) if pd.notna(v)}
    if alt_file:
        for p in glob.glob(os.path.join(folder, "**", alt_file), recursive=True):
            t = pd.read_csv(p)
            return {str(i): v for i, v in zip(t[alt_id], t[alt_col]) if pd.notna(v)}
    raise FileNotFoundError(f"no participants.tsv with a '{column}' column under {folder}")


def run_camcan(results, args, folder):
    def load():
        ages = participants(folder, "age", "standard_data.csv", "CCID", "Age")
        files = [f for f in glob.glob(os.path.join(folder, "**", "*task-rest*_meg.fif"), recursive=True)]
        return rest_table(args, "camcan", files, {k: float(v) for k, v in ages.items()})
    data = attempt("CamCAN", load)
    if data is None:
        return
    F, y, subs = data
    meta = pd.DataFrame(dict(subject=subs, session="0", run="0"))
    ridge = lambda seed: make_pipeline(StandardScaler(), RidgeCV(alphas=np.logspace(-3, 5, 17)))
    _safe(evaluate_custom, PHASE, results, "CamCAN", "cross_subject", "BandPower+Ridge", ridge, F, y.astype(float),
          meta, args.seeds, scorer=regression_scores, needs_seed=False)


def run_omega(results, args, folder):
    def load():
        groups = participants(folder, "group")
        files = glob.glob(os.path.join(folder, "**", "*task-rest*_meg.ds"), recursive=True) + \
            glob.glob(os.path.join(folder, "**", "*task-rest*_meg.fif"), recursive=True)
        return rest_table(args, "omega", files, {k: str(v) for k, v in groups.items()})
    data = attempt("OMEGA", load)
    if data is None:
        return
    F, y, subs = data
    meta = pd.DataFrame(dict(subject=subs, session="0", run="0"))
    _safe(evaluate, PHASE, results, "OMEGA", "cross_subject", "BandPower+LR",
          classical(make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, class_weight="balanced"))),
          F, y, meta, args.seeds, needs_seed=False)


# ------------------------------------------------------------------ MOUS (gated)

MOUS_TARGET = {2: "sentence", 6: "sentence", 4: "word_list", 8: "word_list"}  # Schoffelen et al. 2019, Table 7


def mous_subject(ds_path, task):
    ev = pd.read_csv(ds_path.replace("_meg.ds", "_events.tsv"), sep="\t")
    ev = ev[(ev["type"].astype(str) == "UPPT001")]
    ev = ev.assign(value=pd.to_numeric(ev.value, errors="coerce"))
    ev = ev[ev.value.isin(list(MOUS_TARGET))]
    delay = 0.036 if task == "visual" else 0.0  # fixed visual delay; the auditory delay varies (~60 ms), not corrected
    raw = mne.io.read_raw_ctf(ds_path)
    X, sel, _ = epoch(raw, pd.to_numeric(ev.onset).values + delay, 0.0, 0.8)
    s = subject_of(ds_path)
    return X, [dict(label=MOUS_TARGET[int(v)], subject=s, session="0", run="0") for v in ev.value.values[sel]]


def run_mous(results, args, folder):
    for task in ("visual", "auditory"):
        dname = f"MOUS-{task}"
        if not wanted(args, dname, "MOUS"):
            continue

        def load(task=task):
            files = sorted(glob.glob(os.path.join(folder, "**", f"sub-*_task-{task}_meg.ds"), recursive=True))
            files = files[:2] if args.quick else files
            parts = guarded(dname, (lambda f=f: mous_subject(f, task) for f in files))
            return store(cache_path(args, f"mous_{task}"), len(files) * 260, parts)
        data = attempt(dname, load)
        if data is not None:
            X, table = data
            bench(results, args, dname, X, *split_table(table), ["cross_subject"], SF)


# ------------------------------------------------------------------ HCP MEG (gated)

HCP_TASKS = ("Restin", "Wrkmem", "StoryM", "Motort")


def hcp_run(pdf):
    d = os.path.dirname(pdf)
    run = os.path.basename(os.path.dirname(d))  # e.g. "3-Restin"
    subject = pdf.split(os.sep + "unprocessed")[0].split(os.sep)[-1]
    raw = mne.io.read_raw_bti(pdf, config_fname=os.path.join(d, "config"), head_shape_fname=None)
    raw.crop(10, min(130, raw.times[-1]))
    X, _, _ = epoch(raw, np.arange(0, raw.times[-1] - 2, 2.0), 0.0, 2.0 - 1 / raw.info["sfreq"], band=(1.0, 40.0))
    return X, [dict(label=run.split("-", 1)[1], subject=subject, session="0", run=run)] * len(X)


def run_hcp(results, args, folder):
    def load():
        pdfs = [p for p in sorted(glob.glob(os.path.join(folder, "**", "unprocessed", "MEG", "*", "4D", "c,rfDC"), recursive=True))
                if os.path.basename(os.path.dirname(os.path.dirname(p))).split("-", 1)[-1] in HCP_TASKS]
        if args.quick:
            subs = sorted({p.split(os.sep + "unprocessed")[0] for p in pdfs})[:2]
            pdfs = [p for p in pdfs if p.split(os.sep + "unprocessed")[0] in subs]
        parts = guarded("HCP-MEG", (lambda p=p: hcp_run(p) for p in pdfs))
        return store(cache_path(args, "hcp_meg"), len(pdfs) * 60, parts)
    data = attempt("HCP-MEG", load)
    if data is not None:
        X, table = data
        bench(results, args, "HCP-MEG", X, *split_table(table), ["cross_subject"], SF, models=("BandPower+LR", "EEGNet"))


# ------------------------------------------------------------------ Brain2Qwerty / DECOMEG (local copy)

def b2q_timeline(events, timeline):
    from neuralset.events import Event
    e = events[events.timeline == timeline]
    meg = e[e.type == "Meg"].iloc[0]
    raw = Event.from_dict(meg.to_dict()).read()
    keys = e[(e.type == "Keystroke") & e.text.astype(str).str.fullmatch(r"[a-zñ ]")]
    sentences = e[e.type == "Sentence"].drop_duplicates("trial_id").set_index("trial_id").text
    X, sel, _ = epoch(raw, keys.start.values - meg.start, -0.5, 0.2)
    keys = keys.iloc[sel]
    folds = [str(zlib.crc32(str(sentences.get(t, t)).encode()) % 5) for t in keys.trial_id]
    return X, [dict(label="space" if c == " " else c, subject=str(s), session=str(timeline), run=f)
               for c, s, f in zip(keys.text, keys.subject, folds)]


def run_b2q(results, args, folder):
    def load():
        try:
            import studies  # noqa: F401  (brain2qwerty repo: registers Pinet2024Meg with neuralset)
            from neuralset.events import Study
        except ImportError as e:
            raise RuntimeError("needs `pip install neuralset neuralfetch` and the brain2qwerty repo on PYTHONPATH "
                               f"(github.com/facebookresearch/brain2qwerty) ({e})")
        events = Study(name="Pinet2024Meg", path=folder).build()
        timelines = events.timeline.unique()[:2 if args.quick else None]
        parts = guarded("Brain2Qwerty", (lambda t=t: b2q_timeline(events, t) for t in timelines))
        return store(cache_path(args, "brain2qwerty"), int((events.type == "Keystroke").sum()), parts)
    data = attempt("Brain2Qwerty", load)
    if data is not None:
        X, table = data
        bench(results, args, "Brain2Qwerty", X, *split_table(table), ["leave_one_run_out"], SF)


# ------------------------------------------------------------------ runner

def run(results, args):
    root = os.path.join(args.data_dir, "meg")
    os.makedirs(root, exist_ok=True)

    small = [("MNE-sample", load_sample, ["within_session:5"], ("PCA+LR", "XdawnCov+TS+LR", "EEGNet")),
             ("MNE-somato", load_somato, ["leave_one_run_out"], ("PCA+LR", "Cov+TS+LR", "EEGNet")),
             ("MNE-bst-auditory", load_bst_auditory, ["leave_one_run_out"], ("PCA+LR", "XdawnCov+TS+LR", "EEGNet"))]
    for name, fn, protocols, models in small:
        if not wanted(args, name, "MNE"):
            continue
        if args.quick and name == "MNE-bst-auditory" and name not in (args.datasets or []):
            print(f"\n[{PHASE}] {name}: skipped in --quick (1.6 GB download); name it in --datasets to run it")
            continue
        if name == "MNE-bst-auditory" and not getattr(args, "accept_licenses", False):
            print(f"\n[{PHASE}] {name}: skipped (needs the Brainstorm licence; rerun with --accept-licenses)")
            continue
        data = attempt(name, fn, root, True) if name == "MNE-bst-auditory" else attempt(name, fn, root)
        if data is not None:
            bench(results, args, name, *data, protocols, SF, models=models)

    if wanted(args, "WakemanHenson"):
        data = attempt("WakemanHenson", load_wh, args, root)
        if data is not None:
            X, table = data
            protocols = ["cross_subject"] if args.quick else ["leave_one_run_out", "cross_subject"]  # quick: 1 run each
            bench(results, args, "WakemanHenson", X, *split_table(table), protocols, SF)

    if wanted(args, "BCICIV-3"):
        data = attempt("BCICIV-3", load_bci3, os.path.join(root, "bciciv3"))
        if data is not None:
            bench(results, args, "BCICIV-3", *data, ["standard"], 400,
                  models=("PCA+LR", "Cov+TS+LR", "EEGNet", "ShallowConvNet"))

    if wanted(args, "MEG-MASC"):
        data = attempt("MEG-MASC", load_masc, args, os.path.join(root, "meg_masc"))
        if data is not None:
            X, table = data
            bench(results, args, "MEG-MASC", X, *split_table(table), ["leave_one_run_out"], 50)

    if wanted(args, "THINGS-MEG"):
        data = attempt("THINGS-MEG", load_things, args, root)
        if data is not None:
            X, table = data
            bench(results, args, "THINGS-MEG", X, *split_table(table), ["cross_session"], SF)

    if wanted(args, "LibriBrain", "LibriBrain-Speech", "LibriBrain-Phoneme", "LibriBrain-Phoneme-avg100"):
        run_libribrain(results, args, os.path.join(root, "libribrain"))

    if wanted(args, "Emotion-ds007640"):
        data = attempt("Emotion-ds007640", load_emotion, args, root)
        if data is not None:
            X, table = data
            bench(results, args, "Emotion-ds007640", X, *split_table(table), ["cross_subject"], 1024 / 10,
                  models=("BandPower+LR", "EEGNet"))

    if wanted(args, "Armeni2022") and (folder := gated(args, "armeni", "Armeni2022")):
        data = attempt("Armeni2022", load_armeni, args, folder)
        if data is not None:
            X, table = data
            bench(results, args, "Armeni2022", X, *split_table(table), ["leave_one_run_out"], 50)
    if wanted(args, "CamCAN") and (folder := gated(args, "camcan", "CamCAN")):
        run_camcan(results, args, folder)
    if wanted(args, "MOUS", "MOUS-visual", "MOUS-auditory") and (folder := gated(args, "mous", "MOUS")):
        run_mous(results, args, folder)
    if wanted(args, "HCP-MEG") and (folder := gated(args, "hcp_meg", "HCP-MEG")):
        run_hcp(results, args, folder)
    if wanted(args, "OMEGA") and (folder := gated(args, "omega", "OMEGA")):
        run_omega(results, args, folder)
    if wanted(args, "Brain2Qwerty") and (folder := gated(args, "brain2qwerty", "Brain2Qwerty")):
        run_b2q(results, args, folder)
