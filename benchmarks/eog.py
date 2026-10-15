"""EOG benchmarks (phase 8): sleep staging, EOG artifact removal, activity recognition, vigilance, emotion.

Source of truth for protocols and published numbers: projects/emg-eog-ecg/eog/DATASETS.md.
Sleep-EDF-20 runs in other.py (phase 5); its epoching (wake trimmed to 30 min around sleep, N3+N4 merged,
30-s epochs at 100 Hz) and models are reused here for every sleep set.

| Dataset (name in results) | How it is obtained | Protocol(s) | Models | Tested here |
|---|---|---|---|---|
| Sleep-EDF-78 (`SleepEDF-78 (EEG / EOG / EEG+EOG)`) | auto-download, PhysioNet S3 mirror through MNE | `cross_subject` = 10-fold subject-wise CV (subjects dealt into 10 groups) | BandPower+RF, SleepStagerChambon2018, DeepSleepNet, AttnSleep | yes, quick (2 subjects, 300 epochs per night) |
| ISRUC-Sleep (`ISRUC (...)`) | `--path isruc=FOLDER`: the site now serves the data only through MEGA folders, so download by hand; any cohort, raw `.rec`/`.edf` with `<name>_1.txt` (scorer 1) next to it | `cross_subject` (LOSO for cohort III, GroupKFold 5 for cohort I) | as Sleep-EDF | partial: synthetic EDF + hypnogram in the same layout |
| EEGdenoiseNet, EOG task (`EEGdenoiseNet-EOG`) | auto-download, GitHub (32 MB) | `standard` = 3,400 EEG/EOG pairs, 80/10/10 (validation part unused), mixed at 10 SNRs from -7 to 2 dB; RRMSE_t, RRMSE_s, CC | Ridge (linear filter), CNNDenoiser | yes, quick (200 pairs) |
| Klados & Bamidis 2016 (`Klados2016`) | auto-download, Mendeley v4 (55 MB) | `cross_subject` over 27 groups of two consecutive datasets (subject ids are not published; pairing is an assumption); 2-s windows per channel, input = contaminated channel + VEOG + HEOG | EOG-regression (per window, no training), Ridge, CNNDenoiser | yes, quick (4 datasets) |
| Bulling EOG activity (`BullingEOG`) | auto-download, DaRUS (21 MB) | `cross_subject` = leave-one-person-out; 30-s windows, 5-s step, 5 activities + NULL (distraction samples dropped); macro precision / recall | EOGFeat+SVM, ResNet1D | yes, quick (2 participants, non-overlapping windows) |
| ALS locked-in EEG+EOG | not run | - | - | no: yes/no labels exist, but the trial trigger codes are defined only in a figure, files ship as 3.3-3.9 GB RAR archives, and file-to-session matching needs the paper's manual tables |
| SHHS (`SHHS (...)`) | `--path shhs=FOLDER` (NSRR): `shhs1-*.edf` + `shhs1-*-nsrr.xml` anywhere below | `standard` = 70/30 split by subject (hash of the record id); EEG C4-A1, EOG(L) | as Sleep-EDF | partial: synthetic EDF + NSRR XML |
| MASS (`MASS (...)`) | `--path mass=FOLDER`: `* PSG.edf` + `* Base.edf` | `cross_subject` = 20-fold subject-wise CV; only recordings scored in 30-s epochs (SS1, SS3, SS5) | as Sleep-EDF | partial: synthetic EDF + EDF+ annotations |
| SEED-VIG (`SEED-VIG-within`, `SEED-VIG-cross`) | `--path seed_vig=FOLDER`: `perclos_labels/*.mat` (`perclos`) + `EOG_Feature/*.mat` (same file name; a key containing `icaminus` if present, else the first array with one row per sample) | within: 5-fold over contiguous time blocks of each experiment; cross: leave-one-experiment-out; PCC and RMSE | Ridge, SVR, MLP | partial: synthetic .mat files in the assumed layout |
| DEAP EOG (`DEAP-EOG (valence)`, `DEAP-EOG (arousal)`) | `--path deap=FOLDER`: `data_preprocessed_python/s*.dat` | `cross_subject` (GroupKFold 5); hEOG + vEOG, 60 s after the 3-s baseline; rating > 5 = high | EOGFeat+SVM, ResNet1D | partial: synthetic .dat files |
| JINS MEME driving | `--path jins_driving=` accepted, not run | - | - | no: the DataPort files were not uploaded when DATASETS.md was audited, so no file layout to code against |

Large sleep sets are written once to float16 memmaps under `<data-dir>/eog/` and read lazily (SHHS-1 with
two channels needs about 70 GB of disk). Regression and denoising tasks write rows through evaluate_reg(),
the regression twin of common.evaluate(); RRMSE and RMSE are lower-is-better.
"""
import glob
import os
import pickle
import time
import urllib.request
import json
import xml.etree.ElementTree as ET
import zlib
from datetime import datetime, timezone

import mne
import numpy as np
import pandas as pd
import scipy.io as sio
import torch
from scipy.signal import welch
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import Ridge
from sklearn.metrics import precision_score, recall_score
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC, SVR

import other
from common import (NotApplicable, _safe, classical, deep, download, evaluate, git_commit, log_error, resnet1d,
                    set_seed, splits)
from ecg import Rows, attempt, cached, wanted
from eeg import braindecode_builder
from emg import windows

PHASE = "phase8"
SLEEP_EDF_S3 = "https://physionet-open.s3.amazonaws.com/sleep-edfx/1.0.0/sleep-cassette"
SLEEP_CH = ["EEG Fpz-Cz", "EOG horizontal"]  # other.sleep_epochs picks these; other sets are renamed to them
DEEP_EPOCHS = 50


# ------------------------------------------------------------------ shared helpers

def evaluate_reg(phase, results, dataset, protocol, model_name, make_model, X, Y, meta, seeds, scorer,
                 folds=None, needs_seed=True):
    """common.evaluate() for regression / denoising: same rows, metrics from scorer(Y_true, Y_pred)."""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    folds = folds if folds is not None else list(splits(meta, Y, protocol))
    if not folds:
        raise NotApplicable("no folds")
    for seed in (seeds if needs_seed else seeds[:1]):
        if results.is_done(dataset, protocol, model_name, seed):
            print(f"  = {dataset} | {protocol} | {model_name} | seed {seed}: done, skipping")
            continue
        rows, t_unit = [], time.time()
        for fold, tr, te in folds:
            set_seed(seed)
            est = make_model(seed)
            t0 = time.time()
            est.fit(X[tr], Y[tr])
            train_s = time.time() - t0
            for metric, value in scorer(Y[te], np.asarray(est.predict(X[te]))).items():
                rows.append(dict(phase=phase, dataset=dataset, protocol=protocol, model=model_name, seed=seed,
                                 fold=fold, metric=metric, value=float(value), n_train=len(tr), n_test=len(te),
                                 train_s=round(train_s, 2), device=device, commit=git_commit(),
                                 time=datetime.now(timezone.utc).isoformat(timespec="seconds")))
        results.add(rows)
        first = rows[0]["metric"]
        print(f"  + {dataset} | {protocol} | {model_name} | seed {seed}: {len(folds)} folds, mean {first} "
              f"{np.mean([r['value'] for r in rows if r['metric'] == first]):.4f}, {time.time() - t_unit:.0f}s")


def eog_features(X, fs, chunk=2048):
    """Per channel: log std, log mean |derivative|, log Welch power in five low-frequency bands."""
    out = []
    for i in range(0, len(X), chunk):
        x = np.asarray(X[i:i + chunk], dtype=np.float32)
        f, p = welch(x, fs=fs, nperseg=min(x.shape[-1], int(4 * fs)), axis=-1)
        bands = [p[..., (f >= a) & (f < b)].mean(-1) for a, b in [(0, 0.5), (0.5, 2), (2, 4), (4, 8), (8, 16)]]
        feats = [x.std(-1), np.abs(np.diff(x, axis=-1)).mean(-1), *bands]
        out.append(np.log(np.concatenate(feats, axis=1) + 1e-8))
    return np.concatenate(out)


def svm():
    return make_pipeline(StandardScaler(), SVC(C=1.0, kernel="rbf", class_weight="balanced"))


def pr_hook(y, p):
    return dict(precision=precision_score(y, p, average="macro", zero_division=0),
                recall=recall_score(y, p, average="macro", zero_division=0))


def use(args, model):
    return not args.models or model in args.models


def groups_of(subjects, k):
    """Deal sorted subjects into k groups, so cross_subject (LOSO over groups) becomes k-fold subject-wise CV."""
    order = {s: f"g{i % k:02d}" for i, s in enumerate(sorted(set(subjects)))}
    return np.array([order[s] for s in subjects])


# ------------------------------------------------------------------ sleep staging

def pick(names, prefixes):
    for p in prefixes:
        if p in names:
            return p
    for p in prefixes:
        for n in names:
            if n.startswith(p):
                return n
    raise ValueError(f"none of {prefixes} in {names}")


def sleep_record(raw, ann, eeg, eog):
    """Pick one EEG and one EOG channel, rename them to the Sleep-EDF names, resample to 100 Hz, epoch."""
    e, o = pick(raw.ch_names, eeg), pick(raw.ch_names, eog)
    raw.pick([e, o]).load_data()
    raw.rename_channels({e: SLEEP_CH[0], o: SLEEP_CH[1]})
    if raw.info["sfreq"] != 100:
        raw.resample(100)
    X, y, _ = other.sleep_epochs(raw, ann)
    return X, y


def stage_annotations(onsets, durations, codes):
    """Annotations with Sleep-EDF stage names from numeric stage codes (0 W, 1-4 N1-N4, 5 REM)."""
    names = {0: "Sleep stage W", 1: "Sleep stage 1", 2: "Sleep stage 2", 3: "Sleep stage 3",
             4: "Sleep stage 4", 5: "Sleep stage R"}
    keep = [i for i, c in enumerate(codes) if c in names]
    return mne.Annotations([onsets[i] for i in keep], [durations[i] for i in keep], [names[codes[i]] for i in keep])


def load_sleep(path, records, max_epochs=None):
    """records: (subject, session, loader) with loader() -> (X, y). Cached as a float16 memmap."""
    def rows():
        for subj, sess, load in records:
            try:
                X, y = load()
            except Exception as e:
                log_error(PHASE, f"{path}: record {subj}/{sess} skipped ({type(e).__name__}: {e})")
                continue
            for x, lab in list(zip(X, y))[:max_epochs]:
                yield x, dict(subject=subj, session=sess, label=lab)
    X, t = cached(path, len(records) * (max_epochs or 2000), (2, 3000), rows())
    if not len(t):
        raise RuntimeError("no record could be loaded")
    meta = pd.DataFrame(dict(subject=t.subject.astype(str), session=t.session.astype(str), run="0"))
    return X, t.label.values.astype(str), meta


class Pick(torch.nn.Module):
    def __init__(self, idx, net):
        super().__init__()
        self.idx, self.net = idx, net

    def forward(self, x):
        return self.net(x[:, self.idx])


def picked(build, idx):
    return lambda n_chans, n_times, n_outputs: Pick(idx, build(len(idx), n_times, n_outputs))


def run_sleep_models(results, args, dname, X, y, meta, protocol):
    """Every Sleep-EDF input (EEG, EOG, EEG+EOG) with BandPower+RF and the other.py sleep stagers."""
    F = np.concatenate([other.band_powers(np.asarray(X[i:i + 4096], dtype=np.float32)) for i in range(0, len(X), 4096)])
    for inp, chans in other.INPUTS.items():
        name, idx = f"{dname} ({inp})", [SLEEP_CH.index(c) for c in chans]
        cols = [b * len(SLEEP_CH) + c for b in range(5) for c in idx]  # band_powers is band-major
        rf = RandomForestClassifier(n_estimators=300, n_jobs=-1, random_state=0)
        _safe(evaluate, PHASE, results, name, protocol, "BandPower+RF", classical(rf), F[:, cols], y, meta,
              args.seeds, needs_seed=False)
        for mname, train in other.SLEEP_DEEP.items():
            if mname == "AttnSleep" and len(idx) > 1:  # braindecode's AttnSleep has a single-channel input layer
                print(f"  - {name} | {protocol} | AttnSleep: not applicable (single-channel model)")
            elif use(args, mname):
                make = deep(picked(braindecode_builder(mname, 100), idx), epochs=min(args.epochs, DEEP_EPOCHS),
                            batch_size=128, **train)
                _safe(evaluate, PHASE, results, name, protocol, mname, make, Rows(X), y, meta, args.seeds)


def sleep_edf78(root, quick):
    from mne.datasets.sleep_physionet.age import fetch_data
    subjects = [0, 1] if quick else list(range(83))  # 39, 68, 69, 78, 79 do not exist -> 78 subjects
    files = fetch_data(subjects=subjects, recording=[1, 2], on_missing="ignore", base_url=SLEEP_EDF_S3)

    def loader(psg, hyp):
        return lambda: sleep_record(mne.io.read_raw_edf(psg, verbose=False), mne.read_annotations(hyp),
                                    [SLEEP_CH[0]], [SLEEP_CH[1]])
    recs = [(os.path.basename(p)[3:5], os.path.basename(p)[5], loader(p, h)) for p, h in files]
    X, y, meta = load_sleep(os.path.join(root, f"sleepedf78_{'quick' if quick else 'full'}"), recs,
                            300 if quick else None)
    meta["subject"] = groups_of(meta.subject.values, 10)
    return X, y, meta


def isruc(folder, root, quick):
    """Raw ISRUC recordings (.rec is EDF) with scorer-1 hypnograms <name>_1.txt in the same folder."""
    sigs = sorted(f for f in glob.glob(os.path.join(folder, "**", "*"), recursive=True)
                  if f.lower().endswith((".rec", ".edf")) and os.path.exists(os.path.splitext(f)[0] + "_1.txt"))
    sigs = sigs[:2] if quick else sigs

    def loader(f):
        def load():
            if f.lower().endswith(".rec"):  # MNE wants an .edf name
                link = os.path.join(root, "isruc_links", os.path.relpath(f, folder).replace(os.sep, "_")[:-4] + ".edf")
                os.makedirs(os.path.dirname(link), exist_ok=True)
                if not os.path.exists(link):
                    os.symlink(os.path.abspath(f), link)
            raw = mne.io.read_raw_edf(link if f.lower().endswith(".rec") else f, verbose=False)
            codes = [int(s) for s in open(os.path.splitext(f)[0] + "_1.txt").read().split()]
            ann = stage_annotations([30.0 * i for i in range(len(codes))], [30.0] * len(codes), codes)
            return sleep_record(raw, ann, ["C4-A1", "C4-M1", "C4"], ["LOC-A2", "E1-M2", "LOC", "E1"])
        return load
    recs = [(os.path.splitext(os.path.relpath(f, folder))[0].split(os.sep)[0], "0", loader(f)) for f in sigs]
    return load_sleep(os.path.join(root, f"isruc_{'quick' if quick else 'full'}"), recs, 300 if quick else None)


def nsrr_stages(xml):
    onsets, durs, codes = [], [], []
    for ev in ET.parse(xml).getroot().iter("ScoredEvent"):
        if "Stages" in (ev.findtext("EventType") or ""):
            onsets.append(float(ev.findtext("Start")))
            durs.append(float(ev.findtext("Duration")))
            codes.append(int(ev.findtext("EventConcept").split("|")[-1]))
    return stage_annotations(onsets, durs, codes)


def shhs(folder, root, quick):
    xmls = {os.path.basename(x)[:-len("-nsrr.xml")]: x
            for x in glob.glob(os.path.join(folder, "**", "shhs1-*-nsrr.xml"), recursive=True)}
    edfs = [e for e in sorted(glob.glob(os.path.join(folder, "**", "shhs1-*.edf"), recursive=True))
            if os.path.basename(e)[:-4] in xmls]
    edfs = edfs[:4] if quick else edfs

    def loader(e):
        return lambda: sleep_record(mne.io.read_raw_edf(e, verbose=False), nsrr_stages(xmls[os.path.basename(e)[:-4]]),
                                    ["EEG"], ["EOG(L)"])
    recs = [(os.path.basename(e)[6:-4], "0", loader(e)) for e in edfs]
    X, y, meta = load_sleep(os.path.join(root, f"shhs_{'quick' if quick else 'full'}"), recs, 300 if quick else None)
    # 70/30 split by subject (XSleepNet protocol); encoded in run so the `standard` protocol applies
    meta["run"] = ["test" if zlib.crc32(s.encode()) % 10 < 3 else "train" for s in meta.subject]
    if quick:
        meta["run"] = np.where(meta.subject == meta.subject.iloc[0], "test", "train")
    meta["subject"], meta["session"] = "all", "0"
    return X, y, meta


def mass(folder, root, quick):
    psgs = sorted(glob.glob(os.path.join(folder, "**", "* PSG.edf"), recursive=True))
    psgs = [p for p in psgs if os.path.exists(p.replace(" PSG.edf", " Base.edf"))]
    psgs = psgs[:2] if quick else psgs

    def loader(p):
        def load():
            ann = mne.read_annotations(p.replace(" PSG.edf", " Base.edf"))
            stage = np.array([d.startswith("Sleep stage") for d in ann.description])
            if not stage.any() or abs(np.median(ann.duration[stage]) - 30) > 0.5:
                raise NotApplicable("not scored in 30-s epochs (SS2/SS4 use 20 s)")
            return sleep_record(mne.io.read_raw_edf(p, verbose=False), ann, ["EEG C4"],
                                ["EOG Left Horiz", "EOG Right Horiz", "EOG"])
        return load
    recs = [(os.path.basename(p).split(" ")[0], "0", loader(p)) for p in psgs]
    X, y, meta = load_sleep(os.path.join(root, f"mass_{'quick' if quick else 'full'}"), recs, 300 if quick else None)
    meta["subject"] = groups_of(meta.subject.values, 20)
    return X, y, meta


# ------------------------------------------------------------------ artifact removal

def rrmse(a, b):
    return np.sqrt(((a - b) ** 2).mean(-1)) / np.sqrt((b ** 2).mean(-1))


def denoise_scores(Y, P):
    """EEGdenoiseNet metrics, averaged over segments: RRMSE temporal, RRMSE spectral (Welch PSD), correlation."""
    pp, py = welch(P, nperseg=min(256, Y.shape[-1]), axis=-1)[1], welch(Y, nperseg=min(256, Y.shape[-1]), axis=-1)[1]
    yc, pc = Y - Y.mean(-1, keepdims=True), P - P.mean(-1, keepdims=True)
    cc = (yc * pc).sum(-1) / np.sqrt((yc ** 2).sum(-1) * (pc ** 2).sum(-1) + 1e-12)
    return dict(rrmse_t=rrmse(P, Y).mean(), rrmse_s=rrmse(pp, py).mean(), cc=cc.mean())


class Denoiser(torch.nn.Module):
    """Four dilated 1D conv layers (64 filters, kernel 7, dilation 1-8) and a 1x1 output: noisy (+refs) -> clean."""

    def __init__(self, n_chans, width=64):
        super().__init__()
        layers, c = [], n_chans
        for d in (1, 2, 4, 8):
            layers += [torch.nn.Conv1d(c, width, 7, padding=3 * d, dilation=d), torch.nn.BatchNorm1d(width),
                       torch.nn.ReLU()]
            c = width
        self.net = torch.nn.Sequential(*layers, torch.nn.Conv1d(width, 1, 1))

    def forward(self, x):
        return self.net(x)[:, 0]


class TorchRegressor:
    """Fixed-epoch AdamW + cosine MSE trainer (no early stopping, last epoch evaluated)."""

    def __init__(self, build, epochs, lr=1e-3, batch_size=128):
        self.build, self.epochs, self.lr, self.batch_size = build, epochs, lr, batch_size
        self.dev = "cuda" if torch.cuda.is_available() else "cpu"

    def fit(self, X, Y):
        self.net = self.build(X.shape[1]).to(self.dev)
        opt = torch.optim.AdamW(self.net.parameters(), lr=self.lr)
        sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=max(1, self.epochs))
        data = torch.utils.data.TensorDataset(torch.as_tensor(X, dtype=torch.float32), torch.as_tensor(Y, dtype=torch.float32))
        loader = torch.utils.data.DataLoader(data, batch_size=self.batch_size, shuffle=True)
        self.net.train()
        for _ in range(self.epochs):
            for xb, yb in loader:
                opt.zero_grad(set_to_none=True)
                loss = torch.nn.functional.mse_loss(self.net(xb.to(self.dev)), yb.to(self.dev))
                loss.backward()
                opt.step()
            sched.step()
        return self

    @torch.no_grad()
    def predict(self, X):
        self.net.eval()
        X = torch.as_tensor(X, dtype=torch.float32)
        return torch.cat([self.net(X[i:i + 1024].to(self.dev)).cpu() for i in range(0, len(X), 1024)]).numpy()


class Flat:
    """sklearn regressor on flattened (n, channels, time) input."""

    def __init__(self, est):
        self.est = est

    def fit(self, X, Y):
        self.est.fit(X.reshape(len(X), -1), Y)
        return self

    def predict(self, X):
        return self.est.predict(X.reshape(len(X), -1))


class EOGRegression:
    """Classic EOG regression per window: least-squares fit of VEOG, HEOG and offset to the contaminated
    channel, then subtraction. Uses only the test window itself (fit() learns nothing)."""

    def fit(self, X, Y):
        return self

    def predict(self, X):
        A = np.concatenate([X[:, 1:], np.ones_like(X[:, :1])], 1).transpose(0, 2, 1)  # (n, time, VEOG/HEOG/1)
        beta = np.stack([np.linalg.lstsq(a, c, rcond=None)[0] for a, c in zip(A, X[:, 0])])
        return X[:, 0] - np.einsum("ntk,nk->nt", A[..., :2], beta[:, :2])


def run_denoise(results, args, dname, X, Y, meta, protocol, with_regression=False):
    models = {"Ridge": lambda seed: Flat(Ridge(alpha=1.0))}
    if with_regression:
        models = {"EOG-regression": lambda seed: EOGRegression(), **models}
    if use(args, "CNNDenoiser"):
        ep = min(args.epochs, DEEP_EPOCHS)
        models["CNNDenoiser"] = lambda seed: TorchRegressor(Denoiser, epochs=ep)
    for mname, make in models.items():
        _safe(evaluate_reg, PHASE, results, dname, protocol, mname, make, X, Y, meta, args.seeds, denoise_scores,
              needs_seed=mname == "CNNDenoiser")


DN_URL = "https://raw.githubusercontent.com/ncclabsustech/EEGdenoiseNet/master/data/{}"


def eegdenoisenet(root, quick):
    """EOG task: 3,400 EEG + 3,400 EOG segments (2 s, 256 Hz), 80/10/10, each pair mixed at SNR -7..2 dB."""
    eeg = np.load(download(DN_URL.format("EEG_all_epochs.npy"), os.path.join(root, "EEG_all_epochs.npy")))
    eog = np.load(download(DN_URL.format("EOG_all_epochs.npy"), os.path.join(root, "EOG_all_epochs.npy")))
    rng = np.random.default_rng(0)
    n = 200 if quick else len(eog)
    eeg, eog = eeg[rng.permutation(len(eeg))[:n]], eog[rng.permutation(len(eog))[:n]]
    part = np.where(np.arange(n) < 0.8 * n, "train", np.where(np.arange(n) < 0.9 * n, "val", "test"))
    rms = lambda a: np.sqrt((a ** 2).mean(-1, keepdims=True))  # noqa: E731
    X, Y, run = [], [], []
    for snr in np.linspace(-7, 2, 10):
        noisy = eeg + eog * rms(eeg) / (rms(eog) * 10 ** (snr / 20))
        s = noisy.std(-1, keepdims=True)
        X.append(noisy / s)
        Y.append(eeg / s)
        run.append(part)
    run = np.concatenate(run)
    keep = run != "val"  # no model selection here, so the validation part is not used
    X, Y = np.concatenate(X)[keep, None].astype(np.float32), np.concatenate(Y)[keep].astype(np.float32)
    return X, Y, pd.DataFrame(dict(subject="all", session="0", run=run[keep]))


KLADOS_URL = "https://data.mendeley.com/public-files/datasets/wb6yvr725d/files/{}/file_downloaded"
KLADOS_FILES = {"Pure_Data.mat": "b2ba223a-3c10-4c55-9810-62abc4a05a56",
                "Contaminated_Data.mat": "4715578f-bc5a-4d44-ad84-1edc5880a078",
                "VEOG.mat": "2222a5a6-b275-451b-8ce5-75d4b677aa5c",
                "HEOG.mat": "3c971ecd-5370-4bca-8899-47e4a3a1cd8c"}  # version 4: plain .mat (v1-3 ship a RAR)


def klados(root, quick, win=400):
    m = {f: sio.loadmat(download(KLADOS_URL.format(i), os.path.join(root, f), quiet=True)) for f, i in KLADOS_FILES.items()}
    X, Y, groups = [], [], []
    for k in range(1, 5 if quick else 55):
        pure, con = m["Pure_Data.mat"][f"sim{k}_resampled"], m["Contaminated_Data.mat"][f"sim{k}_con"]
        v, h = m["VEOG.mat"][f"veog_{k}"][0], m["HEOG.mat"][f"heog_{k}"][0]
        for s in range(0, con.shape[1] - win + 1, win):
            for ch in range(con.shape[0]):
                x = np.stack([con[ch, s:s + win], v[s:s + win], h[s:s + win]])
                sd = x[0].std() + 1e-8
                X.append(x / sd)
                Y.append(pure[ch, s:s + win] / sd)
                groups.append(f"pair{(k - 1) // 2:02d}")  # ponytail: assumes consecutive datasets share a subject
    meta = pd.DataFrame(dict(subject=groups, session="0", run="0"))
    return np.asarray(X, np.float32), np.asarray(Y, np.float32), meta


# ------------------------------------------------------------------ classification and regression with EOG

DARUS = "https://darus.uni-stuttgart.de/api/"


def bulling(root, quick, fs=128):
    """5 office activities + NULL, 30-s windows with a 5-s step inside constant-label stretches."""
    req = urllib.request.Request(DARUS + "datasets/:persistentId/?persistentId=doi:10.18419/DARUS-3135",
                                 headers={"User-Agent": "bci-roadmap-benchmarks"})
    files = {f["dataFile"]["filename"]: f["dataFile"]["id"]
             for f in json.load(urllib.request.urlopen(req, timeout=60))["data"]["latestVersion"]["files"]}
    names = sorted(n for n in files if n.endswith(".mat") and (not quick or n[11] in "12"))
    classes = {1: "NULL", 2: "read", 3: "browse", 4: "write", 5: "video", 6: "copy"}  # 7, 8: distractions, dropped
    Xs, ys, metas = [], [], []
    for n in names:
        d = sio.loadmat(download(f"{DARUS}access/datafile/{files[n]}", os.path.join(root, n), quiet=True))["data"]
        X, y, _ = windows(d[:, 2:4].astype(np.float32), d[:, 4], np.zeros(len(d), int), 30 * fs, (30 if quick else 5) * fs)
        keep = np.isin(y, list(classes))
        X = X[keep] - np.median(X[keep], axis=-1, keepdims=True)  # remove the amplifier offset per window
        Xs.append(X)
        ys.append([classes[c] for c in y[keep]])
        part, run = n[len("participant"):-4].split("_")
        metas.append(pd.DataFrame(dict(subject=part, session=run, run="0"), index=range(len(X))))
    return np.concatenate(Xs), np.concatenate(ys), pd.concat(metas, ignore_index=True)


def deap(folder, quick):
    """Preprocessed DEAP (128 Hz): hEOG and vEOG (channels 33, 34), 60 s after the 3-s baseline."""
    files = sorted(glob.glob(os.path.join(folder, "**", "s[0-9][0-9].dat"), recursive=True))[:2 if quick else None]
    if not files:
        raise FileNotFoundError("no sNN.dat files (data_preprocessed_python) below the folder")
    X, lab, meta = [], [], []
    for f in files:
        d = pickle.load(open(f, "rb"), encoding="latin1")
        X.append(d["data"][:, 32:34, 3 * 128:].astype(np.float32))
        lab.append(d["labels"][:, :2])
        meta += [dict(subject=os.path.basename(f)[1:3], session="0", run="0")] * len(d["labels"])
    return np.concatenate(X), np.concatenate(lab), pd.DataFrame(meta)


def run_classify(results, args, dname, X, y, meta, protocol, fs, hook=None):
    F = eog_features(X, fs)
    _safe(evaluate, PHASE, results, dname, protocol, "EOGFeat+SVM", classical(svm()), F, y, meta, args.seeds,
          needs_seed=False, fold_hook=hook)
    if use(args, "ResNet1D"):
        make = deep(resnet1d, epochs=min(args.epochs, DEEP_EPOCHS), batch_size=64, lr=1e-3, weight_decay=1e-4)
        _safe(evaluate, PHASE, results, dname, protocol, "ResNet1D", make, X, y, meta, args.seeds, fold_hook=hook)


def seed_vig(folder):
    """Per experiment: PERCLOS labels and the 36 forehead-EOG features (layout described in the docstring)."""
    labs = sorted(glob.glob(os.path.join(folder, "**", "perclos_labels", "*.mat"), recursive=True))
    if not labs:
        raise FileNotFoundError("no perclos_labels/*.mat below the folder")
    X, y, meta = [], [], []
    for lab in labs:
        p = sio.loadmat(lab)["perclos"].ravel()
        feat = glob.glob(os.path.join(folder, "**", "EOG_Feature", os.path.basename(lab)), recursive=True)
        m = sio.loadmat(feat[0])
        keys = [k for k in m if not k.startswith("__") and getattr(m[k], "ndim", 0) >= 2 and m[k].shape[0] == len(p)]
        k = next((k for k in keys if "icaminus" in k.lower()), keys[0])
        X.append(m[k].reshape(len(p), -1).astype(np.float32))
        y.append(p)
        block = np.arange(len(p)) * 5 // len(p)  # five contiguous time blocks
        meta.append(pd.DataFrame(dict(subject=os.path.basename(lab)[:-4], session=block.astype(str), run="0")))
    return np.concatenate(X), np.concatenate(y).astype(np.float32), pd.concat(meta, ignore_index=True)


def vig_scores(y, p):
    return dict(pcc=np.corrcoef(y, p)[0, 1] if y.std() > 0 and p.std() > 0 else np.nan,
                rmse=np.sqrt(((y - p) ** 2).mean()))


def run_seed_vig(results, args, X, y, meta):
    models = {"Ridge": make_pipeline(StandardScaler(), Ridge(alpha=1.0)),
              "SVR": make_pipeline(StandardScaler(), SVR(C=1.0, epsilon=0.01))}
    within = list(splits(meta, y, "cross_session"))  # session = time block -> 5-fold over blocks per experiment
    groups = meta.subject.values
    cross = [(f"test={groups[te][0]}", tr, te) for tr, te in LeaveOneGroupOut().split(X, y, groups)]
    for dname, protocol, folds in [("SEED-VIG-within", "within_subject_5fold", within),
                                   ("SEED-VIG-cross", "cross_subject", cross)]:
        for mname, pipe in models.items():
            _safe(evaluate_reg, PHASE, results, dname, protocol, mname, classical(pipe), X, y, meta, args.seeds,
                  vig_scores, folds=folds, needs_seed=False)
        if use(args, "MLP"):
            mlp = lambda seed: make_pipeline(StandardScaler(), MLPRegressor(hidden_layer_sizes=(64, 64), max_iter=300, random_state=seed))  # noqa: E731
            _safe(evaluate_reg, PHASE, results, dname, protocol, "MLP", mlp, X, y, meta, args.seeds, vig_scores,
                  folds=folds)


# ------------------------------------------------------------------ runner

def gated(args, key, name):
    folder = args.paths.get(key)
    if not folder:
        print(f"\n[{PHASE}] {name}: skipped (access-gated; pass --path {key}=FOLDER)")
    return folder


def run(results, args):
    root = os.path.join(args.data_dir, "eog")
    os.makedirs(root, exist_ok=True)

    if wanted(args, "SleepEDF-78"):
        d = attempt("Sleep-EDF-78", sleep_edf78, root, args.quick)
        if d:
            run_sleep_models(results, args, "SleepEDF-78", *d, "cross_subject")

    if wanted(args, "ISRUC") and gated(args, "isruc", "ISRUC-Sleep (manual download from the MEGA links on sleeptight.isr.uc.pt)"):
        d = attempt("ISRUC-Sleep", isruc, args.paths["isruc"], root, args.quick)
        if d:
            run_sleep_models(results, args, "ISRUC", *d, "cross_subject")

    if wanted(args, "EEGdenoiseNet-EOG", "EEGdenoiseNet"):
        d = attempt("EEGdenoiseNet (EOG)", eegdenoisenet, os.path.join(root, "eegdenoisenet"), args.quick)
        if d:
            run_denoise(results, args, "EEGdenoiseNet-EOG", *d, "standard")

    if wanted(args, "Klados2016"):
        d = attempt("Klados & Bamidis 2016", klados, os.path.join(root, "klados"), args.quick)
        if d:
            run_denoise(results, args, "Klados2016", *d, "cross_subject", with_regression=True)

    if wanted(args, "BullingEOG"):
        d = attempt("Bulling EOG activity", bulling, os.path.join(root, "bulling"), args.quick)
        if d:
            run_classify(results, args, "BullingEOG", *d, "cross_subject", 128, hook=pr_hook)

    if wanted(args, "ALS-LIS"):
        print(f"\n[{PHASE}] ALS locked-in EEG+EOG: not run (trial trigger codes are defined only in a figure; "
              "3.3-3.9 GB RAR archives; manual file-to-session tables)")

    if wanted(args, "SHHS") and gated(args, "shhs", "SHHS"):
        d = attempt("SHHS", shhs, args.paths["shhs"], os.path.join(root, "shhs"), args.quick)
        if d:
            run_sleep_models(results, args, "SHHS", *d, "standard")

    if wanted(args, "MASS") and gated(args, "mass", "MASS"):
        d = attempt("MASS", mass, args.paths["mass"], os.path.join(root, "mass"), args.quick)
        if d:
            run_sleep_models(results, args, "MASS", *d, "cross_subject")

    if wanted(args, "SEED-VIG") and gated(args, "seed_vig", "SEED-VIG"):
        d = attempt("SEED-VIG", seed_vig, args.paths["seed_vig"])
        if d:
            run_seed_vig(results, args, *d)

    if wanted(args, "DEAP-EOG") and gated(args, "deap", "DEAP (EOG)"):
        d = attempt("DEAP (EOG)", deap, args.paths["deap"], args.quick)
        if d:
            X, lab, meta = d
            for j, dim in enumerate(["valence", "arousal"]):
                y = np.where(lab[:, j] > 5, "high", "low")
                run_classify(results, args, f"DEAP-EOG ({dim})", X, y, meta, "cross_subject", 128)

    if wanted(args, "JINS-MEME") and gated(args, "jins_driving", "JINS MEME driving"):
        print(f"[{PHASE}] JINS MEME driving: not run (no published file layout to code against yet)")
