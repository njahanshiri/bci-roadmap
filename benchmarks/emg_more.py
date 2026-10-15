"""More EMG benchmarks (phase 7): Ninapro DB1/DB2/DB3/DB7, CapgMyo, CSL-HDEMG, Hyser PR, EMG-EPN-612, putEMG.

Ninapro DB5 and GRABMyo run in emg.py; this module reuses its features, windowing and models.
Protocols follow projects/emg-eog-ecg/emg/DATASETS.md.

| Dataset | Obtained | Protocol(s) | Models | Tested here |
|---|---|---|---|---|
| NinaproDB1 (10 ch RMS, 100 Hz, 52 + rest) | auto (ninapro.hevs.ch, 20 MB/subject) | `heldout_run:2,5,7`, `cross_subject` | Hudgins+LDA/RF, ResNet1D | yes, 2 subjects |
| NinaproDB2 (12 ch, 2 kHz, 49 + rest) | auto (470 MB/subject) | `heldout_run:2,5`, `cross_subject` (classical) | Hudgins+LDA/RF, ResNet1D | yes, 2 subjects, exercise B only |
| NinaproDB3 (amputees, up to 49 + rest) | auto (250 MB/subject) | `heldout_run:2,5`, `cross_subject` (classical) | Hudgins+LDA/RF, ResNet1D | yes, 2 subjects, exercise B only |
| NinaproDB7 (subjects 1-20, 40 + rest) | auto (1.5 GB/subject) | `leave_one_run_out` (6 folds over repetitions) | Hudgins+LDA/RF, ResNet1D | yes, 1 subject, exercise 1 only |
| NinaproDB7-amputee (subjects 21-22) | auto | `leave_one_run_out` | Hudgins+LDA/RF, ResNet1D | same code path as DB7, not run |
| CapgMyo-DBa (128 ch, 8 gestures) | auto (figshare CC0 copy, 78 MB/subject) | `heldout_run:2,4,6,8,10` (odd trials train), `cross_subject` (LOSO) | Hudgins+LDA/RF, ResNet1D, GridCNN | yes, 2 subjects |
| CapgMyo-DBb / CapgMyo-DBc | `--path capgmyo_dbb=` / `capgmyo_dbc=` (official site, link not reachable) | odd/even trials, `heldout_session:2` (DB-b), `cross_subject` | as DB-a | no (same loader as DB-a) |
| CSL-HDEMG (168 ch, 27 gestures) | `--path csl_hdemg=` (registration at uni-bremen.de) | `leave_one_run_out` (leave one trial out per session) | Hudgins+LDA/RF, ResNet1D, GridCNN | no (format from the authors' description, unverified) |
| HyserPR-dynamic / HyserPR-maintenance (256 ch) | auto (PhysioNet, preprocessed PR files only, ~19 GB) | `leave_one_run_out` (classical: leave one sample out; GridCNN: folds over repetitions), `heldout_session:2`, `cross_subject` | trial-level Hudgins+LDA/RF; GridCNN on 250 ms windows | partial: 2 subjects x 2 sessions x 2 gestures |
| EMG-EPN-612 (8 ch Myo, 5 + relax) | auto (Zenodo zip, 5.5 GB) | `cross_subject_fixed:1-306:1001-1306` (306 training users -> 306 testing users) | Hudgins+LDA/RF, ResNet1D | yes, 2 + 2 users (range reads) |
| putEMG (24 ch, 7 + idle) | auto (official cloud, HDF5, 46 MB/record) | `leave_one_run_out` (3 trajectories per subject and day), `heldout_session:2`, `cross_subject` | Hudgins+LDA/RF, GridCNN | yes, 1 subject, 2 days |

Notes
- Quick runs read only the needed members of the Ninapro and EPN zips over HTTP range requests, and keep at most
  1000 evenly spaced windows per subject (or record).
- Windows are cached per subject as .npy files and reopened as memmaps (data_dir/emg_more/<dataset>/cache*).
- GridCNN: per-frame 2D CNN over the electrode grid on 10 RMS frames per window, logits averaged over frames.
  Channels are reshaped to the grid in file order.
- Hyser classical models use one feature vector per sample (first 0.25 s dropped) and leave-one-sample-out within
  a session, as in Jiang et al. 2021; Hyser GridCNN uses windows and folds over gesture repetitions.
  Hyser and putEMG keep only features and RMS frames on disk (raw windows would need 20-90 GB), so ResNet1D does not run on them.
- CapgMyo-DBb: assumes the official numbering where file subjects 2k-1 and 2k are sessions 1 and 2 of person k.
"""
import glob
import io
import json
import os
import re
import urllib.request
import warnings
import zipfile
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd
import scipy.io as sio
import torch
from scipy.signal import butter, filtfilt, iirnotch, sosfiltfilt

from common import _safe, classical, deep, download, evaluate, log_error, resnet1d, unzip
from emg import EMG_DEEP_TRAIN, emg_classical, features, hudgins, windows

PHASE = "phase7"


# ------------------------------------------------------------------ storage helpers

class _HTTPFile(io.RawIOBase):
    """Seekable read-only file over HTTP range requests, so zipfile can read single members."""

    def __init__(self, url):
        super().__init__()
        self.url, self.pos = url, 0
        with self._get(0, 0) as r:
            self.size = int(r.headers["Content-Range"].split("/")[1])

    def _get(self, a, b):
        req = urllib.request.Request(self.url, headers={"User-Agent": "bci-roadmap-benchmarks", "Range": f"bytes={a}-{b}"})
        return urllib.request.urlopen(req, timeout=120)

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
        with self._get(self.pos, self.pos + n - 1) as r:
            data = r.read()
        b[:len(data)] = data
        self.pos += len(data)
        return len(data)


def open_zip(url, dst, remote):
    """Remote (quick runs): read members over HTTP. Otherwise download the zip once and read it locally."""
    if remote and not os.path.exists(dst):
        return zipfile.ZipFile(io.BufferedReader(_HTTPFile(url), 1 << 20))
    return zipfile.ZipFile(download(url, dst))


class Stack:
    """Row-wise concatenation of per-part memmaps; supports len, shape, slices and index arrays."""

    def __init__(self, parts):
        self.parts = parts
        self.off = np.cumsum([0] + [len(p) for p in parts])
        self.shape = (int(self.off[-1]),) + parts[0].shape[1:]

    def __len__(self):
        return self.shape[0]

    def __getitem__(self, idx):
        idx = np.arange(len(self))[idx]
        p = np.searchsorted(self.off, idx, "right") - 1
        if np.ndim(idx) == 0:
            return np.asarray(self.parts[p][idx - self.off[p]])
        out = np.empty((len(idx),) + self.shape[1:], np.float32)
        for k in np.unique(p):
            m = p == k
            out[m] = self.parts[k][idx[m] - self.off[k]]
        return out


def cached(path, fn):
    """fn() -> (arrays, y, meta), computed once; arrays are saved as .npy and reopened as memmaps."""
    if not os.path.exists(path + ".csv"):
        arrays, y, meta = fn()
        for i, a in enumerate(arrays):
            np.save(f"{path}.{i}.npy", np.ascontiguousarray(a, dtype=np.float32))
        meta.assign(y=y).to_csv(path + ".csv", index=False)  # written last: marks the part complete
    m = pd.read_csv(path + ".csv", dtype=str, keep_default_na=False)
    arrays = [np.load(f, mmap_mode="r") for f in sorted(glob.glob(path + ".*.npy"))]
    return arrays, m.pop("y").values, m


def load_parts(root, quick, items, quick_max=1000):
    """items: (part name, fn) pairs, e.g. one per subject. A failing part is logged and skipped.

    Quick runs keep at most quick_max evenly spaced windows per part."""
    cache = os.path.join(root, "cache_quick" if quick else "cache")
    os.makedirs(cache, exist_ok=True)
    parts = []
    for name, fn in items:
        try:
            arrays, y, meta = cached(os.path.join(cache, name), fn)
        except Exception as e:
            log_error(PHASE, f"{cache} {name}: {type(e).__name__}: {e}")
            continue
        if quick and len(y) > quick_max:
            keep = np.linspace(0, len(y) - 1, quick_max).astype(int)
            arrays, y, meta = [a[keep] for a in arrays], y[keep], meta.iloc[keep]
        if len(y):
            parts.append((arrays, y, meta))
    if not parts:
        raise RuntimeError("no data loaded")
    arrays = [Stack([p[0][i] for p in parts]) for i in range(len(parts[0][0]))]
    return arrays, np.concatenate([p[1] for p in parts]), pd.concat([p[2] for p in parts], ignore_index=True)


# ------------------------------------------------------------------ models

def rms_frames(X, n=10, chunk=4096):
    """Windows (n_win, ch, time) -> RMS over n equal frames (n_win, ch, n): the GridCNN input."""
    out = []
    for i in range(0, len(X), chunk):
        x = np.asarray(X[i:i + chunk], np.float32)
        t = x.shape[-1] // n * n
        out.append(np.sqrt((x[..., :t].reshape(*x.shape[:2], n, -1) ** 2).mean(-1)))
    return np.concatenate(out)


class GridCNN(torch.nn.Module):
    """Per-frame 2D CNN over the electrode grid, logits averaged over frames.

    A small take on the instantaneous HD-EMG image idea of Geng et al. (2016), on RMS frames.
    grid = (planes, rows, cols); channels are reshaped to it in file order.
    """

    def __init__(self, grid, n_outputs, width=32):
        super().__init__()
        self.grid = grid
        nn = torch.nn
        conv = lambda i, o: [nn.Conv2d(i, o, 3, padding=1), nn.BatchNorm2d(o), nn.ReLU()]  # noqa: E731
        self.net = nn.Sequential(*conv(grid[0], width), *conv(width, width), nn.Flatten(), nn.Dropout(0.5),
                                 nn.Linear(width * grid[1] * grid[2], 128), nn.ReLU(), nn.Linear(128, n_outputs))

    def forward(self, x):  # (batch, channels, frames)
        b, _, f = x.shape
        return self.net(x.transpose(1, 2).reshape(b * f, *self.grid)).view(b, f, -1).mean(1)


def bench(results, args, dataset, protocols, y, meta, F=None, X=None, R=None, grid=None, deep_on=None):
    """Hudgins+LDA/RF on features F, ResNet1D on raw windows X, GridCNN on RMS frames R.

    deep_on: protocols the deep models run on (default: all); big datasets skip deep cross-subject (memory).
    """
    make = lambda build: deep(build, epochs=min(args.epochs, 100), batch_size=256, **EMG_DEEP_TRAIN)  # noqa: E731
    deep_models = [("ResNet1D", X, resnet1d),
                   ("GridCNN", R, lambda n_chans, n_times, n_outputs: GridCNN(grid, n_outputs))]
    for protocol in protocols:
        if F is not None:
            for mname, pipe in emg_classical().items():
                _safe(evaluate, PHASE, results, dataset, protocol, mname, classical(pipe), F, y, meta, args.seeds,
                      needs_seed=False)
        if deep_on is not None and protocol not in deep_on:
            continue
        for mname, Xd, build in deep_models:
            if Xd is not None and (not args.models or mname in args.models):
                _safe(evaluate, PHASE, results, dataset, protocol, mname, make(build), Xd, y, meta, args.seeds)


# ------------------------------------------------------------------ Ninapro DB1, DB2, DB3, DB7

NP = "https://ninapro.hevs.ch/files/"
# url, member regex, {exercise: movements}, channels, sampling rate
NINAPRO = {
    "NinaproDB1": (NP + "DB1/Preprocessed/s{n}.zip", r"S{n}_A1_E{e}\.mat$", {1: 12, 2: 17, 3: 23}, 10, 100),
    "NinaproDB2": (NP + "DB2_Preproc/DB2_s{n}.zip", r"S{n}_E{e}_A1\.mat$", {1: 17, 2: 23, 3: 9}, 12, 2000),
    "NinaproDB3": (NP + "db3_Preproc/s{n}_0.zip", r"S{n}_E{e}_A1\.mat$", {1: 17, 2: 23, 3: 9}, 12, 2000),
    "NinaproDB7": (NP + "DB7_Preproc/Subject_{n}.zip", r"S{n}_E{e}_A1\.mat$", {1: 17, 2: 23}, 12, 2000),
}


def ninapro_subject(spec, n, root, quick):
    """All exercises of one subject (quick: first exercise), 200-ms windows with 100-ms step."""
    url, member, exercises, n_ch, fs = spec
    url = url.format(n=n)
    z = open_zip(url, os.path.join(root, os.path.basename(url)), remote=quick)
    out, offset = [], 0
    for e, n_mov in list(exercises.items())[:1 if quick else None]:
        name = next(f for f in z.namelist() if re.search(r"(^|/)" + member.format(n=n, e=e), f))
        m = sio.loadmat(io.BytesIO(z.read(name)), variable_names=["emg", "restimulus", "rerepetition"])
        lab = m["restimulus"].ravel().astype(int)
        if lab.max() <= n_mov:  # numbered per exercise: shift to global movement ids
            lab = np.where(lab > 0, lab + offset, 0)
        offset += n_mov
        # rest samples carry repetition 0; give them the repetition of the movement they follow (as in emg.py)
        rep = pd.Series(m["rerepetition"].ravel().astype(float)).replace(0, np.nan).ffill().bfill().astype(int).values
        emg = m["emg"].astype(np.float32)
        emg = np.pad(emg, ((0, 0), (0, n_ch - emg.shape[1])))  # DB3 subjects 7-8 have 10 electrodes
        out.append(windows(emg, lab, rep, int(0.2 * fs), int(0.1 * fs)))
    X, y, r = (np.concatenate(a) for a in zip(*out))
    return (X,), y.astype(str), pd.DataFrame(dict(subject=str(n), session="0", run=r.astype(str)))


def run_ninapro(results, args, name, subjects, protocols, deep_on=None):
    spec = NINAPRO[name.replace("-amputee", "")]
    root = os.path.join(args.data_dir, "emg_more", name.split("-")[0].lower())
    os.makedirs(root, exist_ok=True)
    (X,), y, meta = load_parts(root, args.quick,
                               [(f"s{n}", lambda n=n: ninapro_subject(spec, n, root, args.quick)) for n in subjects])
    bench(results, args, name, protocols, y, meta, F=features(X), X=X, deep_on=deep_on)


# ------------------------------------------------------------------ CapgMyo and CSL-HDEMG (HD-EMG grids)

CAPG_DBA_API = "https://api.figshare.com/v2/articles/7210397"


def capg_subject(files, db):
    """Files 'SSS-GGG-TTT.mat' (subject, gesture, trial) with 'data' (1000 x 128); 150-ms windows, 50-ms step."""
    X, meta, y = [], [], []
    for f in files:
        s, g, t = map(int, re.search(r"(\d{3})-(\d{3})-(\d{3})\.mat$", f).groups())
        sig = sio.loadmat(f, variable_names=["data"])["data"].astype(np.float32)
        z = np.zeros(len(sig), int)
        w = windows(sig, z, z, 150, 50)[0]
        person, sess = ((s + 1) // 2, 2 - s % 2) if db == "b" else (s, 1)
        X.append(w)
        y += [str(g)] * len(w)
        meta += [dict(subject=str(person), session=str(sess), run=str(t))] * len(w)
    return (np.concatenate(X),), np.asarray(y), pd.DataFrame(meta)


def run_capgmyo(results, args, db, folder):
    name = f"CapgMyo-DB{db}"
    root = os.path.join(args.data_dir, "emg_more", "capgmyo", f"db{db}")
    if folder is None:  # DB-a: figshare copy, one zip per subject
        want = {1, 2} if args.quick else set(range(1, 19))
        for f in json.load(urllib.request.urlopen(CAPG_DBA_API, timeout=60))["files"]:
            n = int(re.search(r"s(\d+)\.zip", f["name"]).group(1))
            d = os.path.join(root, f"s{n}")
            if n in want and not glob.glob(os.path.join(d, "*.mat")):
                unzip(download(f["download_url"], os.path.join(root, f["name"])), d)
        folder = root
    files = sorted(glob.glob(os.path.join(folder, "**", "*.mat"), recursive=True))
    by_subject = {}
    for f in files:
        if re.search(r"\d{3}-\d{3}-\d{3}\.mat$", f):
            by_subject.setdefault(int(os.path.basename(f)[:3]), []).append(f)
    subjects = sorted(by_subject)[:(4 if db == "b" else 2) if args.quick else None]  # DB-b: 2 files per person
    (X,), y, meta = load_parts(root, args.quick,
                               [(f"s{s}", lambda s=s: capg_subject(by_subject[s], db)) for s in subjects])
    protocols = ["heldout_run:2,4,6,8,10"] + (["heldout_session:2"] if db == "b" else []) + ["cross_subject"]
    bench(results, args, name, protocols, y, meta, F=features(X), X=X, R=rms_frames(X), grid=(1, 8, 16))


def csl_subject(files):
    """CSL-HDEMG .mat per gesture and session, holding one array per trial (192 electrodes x time, 2048 Hz).

    Every 8th of the 192 electrode rows is dropped, leaving the 7 x 24 bipolar grid. 150-ms windows, 75-ms step.
    """
    X, y, meta = [], [], []
    for f in files:
        sess, g = re.search(r"session(\d+)[/\\]gest(\d+)\.mat$", f, re.I).groups()
        mat = sio.loadmat(f)
        cell = next(v for k, v in mat.items() if not k.startswith("__"))
        for t, trial in enumerate(cell.flat, 1):
            a = np.asarray(trial, np.float32)
            a = a if a.shape[0] in (192, 168) else a.T
            if a.shape[0] == 192:
                a = np.delete(a, np.s_[7::8], 0)
            z = np.zeros(a.shape[1], int)
            w = windows(a.T, z, z, 307, 154)[0]
            X.append(w)
            y += [g] * len(w)
            meta += [dict(subject=re.search(r"subject(\d+)", f, re.I).group(1), session=sess, run=str(t))] * len(w)
    return (np.concatenate(X),), np.asarray(y), pd.DataFrame(meta)


def run_csl(results, args, folder):
    files = [f for f in glob.glob(os.path.join(folder, "**", "*.mat"), recursive=True)
             if re.search(r"subject\d+[/\\]session\d+[/\\]gest\d+\.mat$", f, re.I)]
    if not files:
        raise FileNotFoundError(f"no subject*/session*/gest*.mat files under {folder}")
    by_subject = {}
    for f in sorted(files):
        by_subject.setdefault(re.search(r"subject(\d+)", f, re.I).group(1), []).append(f)
    subjects = sorted(by_subject)[:2 if args.quick else None]
    root = os.path.join(args.data_dir, "emg_more", "csl_hdemg")
    (X,), y, meta = load_parts(root, args.quick,
                               [(f"s{s}", lambda s=s: csl_subject(by_subject[s])) for s in subjects])
    bench(results, args, "CSL-HDEMG", ["leave_one_run_out"], y, meta, F=features(X), X=X, R=rms_frames(X),
          grid=(1, 7, 24))


# ------------------------------------------------------------------ Hyser PR (PhysioNet)

HYSER = "https://physionet.org/files/hd-semg/2.0.0/pr_dataset/subject{s:02d}_session{k}/"


def hyser_part(root, s, k, task, gestures, level):
    """One subject, session and task. level 'trial': one Hudgins vector per sample (first 0.25 s dropped),
    run = sample number, so leave_one_run_out is the paper's leave-one-sample-out.
    level 'window': RMS frames of 250-ms windows with 125-ms step, run = repetition of the gesture,
    so windows of one sample are never split between train and test."""
    import wfdb
    base, d = HYSER.format(s=s, k=k), os.path.join(root, f"subject{s:02d}_session{k}")
    labels = np.atleast_1d(np.loadtxt(download(base + f"label_{task}.txt", os.path.join(d, f"label_{task}.txt")),
                                      delimiter=",", dtype=int))
    idx = [i for i, g in enumerate(labels, 1) if g in gestures]
    names = [f"{task}_preprocess_sample{i}" for i in idx]
    with ThreadPoolExecutor(8) as ex:  # PhysioNet is slow per connection
        list(ex.map(lambda f: download(base + f, os.path.join(d, f), quiet=True),
                    [n + e for n in names for e in (".hea", ".dat")]))
    A, y, meta, reps = [], [], [], {}
    for i, n in zip(idx, names):
        g = labels[i - 1]
        reps[g] = reps.get(g, 0) + 1  # repetition number of this sample within its gesture
        sig = wfdb.rdrecord(os.path.join(d, n)).p_signal[512:].astype(np.float32)
        if level == "trial":
            a = hudgins(sig.T[None])
        else:
            z = np.zeros(len(sig), int)
            a = rms_frames(windows(sig, z, z, 512, 256)[0])
        A.append(a)
        y += [str(g)] * len(a)
        meta += [dict(subject=str(s), session=str(k), run=str(i if level == "trial" else reps[g]))] * len(a)
    return (np.concatenate(A),), np.asarray(y), pd.DataFrame(meta)


def run_hyser(results, args, task):
    root = os.path.join(args.data_dir, "emg_more", "hyser")
    subjects, gestures = ([1, 2], {1, 2}) if args.quick else (range(1, 21), set(range(1, 35)))
    name, protocols = f"HyserPR-{task}", ["leave_one_run_out", "heldout_session:2", "cross_subject"]
    for level in ("trial", "window"):
        (A,), y, meta = load_parts(root, args.quick, [
            (f"{task}_{level}_s{s}_{k}", lambda s=s, k=k: hyser_part(root, s, k, task, gestures, level))
            for s in subjects for k in (1, 2)])
        if level == "trial":
            with warnings.catch_warnings():  # single-sample test folds: kappa / F1 warnings on every fold
                warnings.simplefilter("ignore")
                bench(results, args, name, protocols, y, meta, F=A)
        else:
            bench(results, args, name, protocols, y, meta, R=A, grid=(4, 8, 8))


# ------------------------------------------------------------------ EMG-EPN-612 (Zenodo)

EPN_URL = "https://zenodo.org/records/4421500/files/EMG-EPN612%20Dataset.zip"


def epn_user(z, member, subject):
    """All labelled recordings of one user (testing users' 'testingSamples' are unlabelled), cropped/padded to 5 s."""
    d = json.loads(z.read(member))
    samples = [s for part in ("trainingSamples", "testingSamples") for s in d[part].values() if "gestureName" in s]
    X = np.zeros((len(samples), 8, 1000), np.float32)
    for i, s in enumerate(samples):
        e = np.asarray([s["emg"][f"ch{c}"] for c in range(1, 9)], np.float32)[:, :1000]
        X[i, :, :e.shape[1]] = e
    meta = pd.DataFrame(dict(subject=str(subject), session="0", run="0"), index=range(len(samples)))
    return (X,), np.asarray([s["gestureName"] for s in samples]), meta


def run_epn(results, args):
    root = os.path.join(args.data_dir, "emg_more", "emg_epn612")
    os.makedirs(root, exist_ok=True)
    z = open_zip(EPN_URL, os.path.join(root, "EMG-EPN612.zip"), remote=args.quick)
    users = [1, 2] if args.quick else range(1, 307)
    items = [(f"{g}_user{u}", lambda g=g, u=u: epn_user(z, f"EMG-EPN612 Dataset/{g}JSON/user{u}/user{u}.json",
                                                        u + (1000 if g == "testing" else 0)))
             for g in ("training", "testing") for u in users]
    (X,), y, meta = load_parts(root, args.quick, items)
    # official split: training users are subjects 1-306, testing users 1001-1306
    bench(results, args, "EMG-EPN-612", ["cross_subject_fixed:1-306:1001-1306"], y, meta, F=features(X), X=X)


# ------------------------------------------------------------------ putEMG

PUT_URL = "https://chmura.put.poznan.pl/s/45NY5snj0U4tgQz/download?path=/{dir}&files={name}"
PUT_FS = 5120


def put_record(path, subject, session, trajectory):
    """One trajectory: 20-700 Hz band-pass + 50 Hz notch, 488-ms windows with 244-ms step (as in the paper).

    Windows must lie inside one TRAJ_GT label (drops transitions); relax (-1) is dropped. Returns
    Hudgins features and RMS frames (raw windows are not kept)."""
    d = pd.read_hdf(path)
    sig = d[[f"EMG_{i}" for i in range(1, 25)]].to_numpy(np.float64)
    sig = sosfiltfilt(butter(4, [20, 700], "bandpass", fs=PUT_FS, output="sos"), sig, axis=0)
    sig = filtfilt(*iirnotch(50, 30, fs=PUT_FS), sig, axis=0).astype(np.float32)
    lab = d["TRAJ_GT"].to_numpy().astype(int)
    X, y, _ = windows(sig, lab, np.zeros(len(lab), int), 5000, 2500)
    X, y = X[y >= 0], y[y >= 0]
    meta = pd.DataFrame(dict(subject=subject, session=session, run=trajectory), index=range(len(y)))
    return (features(X), rms_frames(X)), y.astype(str), meta


def run_putemg(results, args):
    root = os.path.join(args.data_dir, "emg_more", "putemg")
    recs = open(download(PUT_URL.format(dir="", name="records.txt"), os.path.join(root, "records.txt"))).read().split()
    recs = [r for r in recs if r.startswith("emg_gestures-")]
    subjects = sorted({r.split("-")[1] for r in recs})[:1 if args.quick else None]
    items = []
    for s in subjects:
        mine = [r for r in recs if r.split("-")[1] == s]
        dates = sorted({r.split("-", 3)[3][:10] for r in mine})
        for r in mine:
            path = os.path.join(root, r + ".hdf5")
            sess, traj = str(dates.index(r.split("-", 3)[3][:10]) + 1), r.split("-")[2]
            items.append((r, lambda r=r, path=path, s=s, sess=sess, traj=traj: put_record(
                download(PUT_URL.format(dir="Data-HDF5", name=r + ".hdf5"), path), s, sess, traj)))
    (F, R), y, meta = load_parts(root, args.quick, items)
    bench(results, args, "putEMG", ["leave_one_run_out", "heldout_session:2", "cross_subject"], y, meta, F=F, R=R,
          grid=(1, 3, 8))


# ------------------------------------------------------------------ runner

def run(results, args):
    quick = args.quick
    gated = {"CapgMyo-DBb": "capgmyo_dbb", "CapgMyo-DBc": "capgmyo_dbc", "CSL-HDEMG": "csl_hdemg"}
    jobs = [
        ("NinaproDB1", lambda: run_ninapro(results, args, "NinaproDB1", [1, 2] if quick else range(1, 28),
                                           ["heldout_run:2,5,7", "cross_subject"])),
        ("NinaproDB2", lambda: run_ninapro(results, args, "NinaproDB2", [1, 2] if quick else range(1, 41),
                                           ["heldout_run:2,5", "cross_subject"], deep_on=["heldout_run:2,5"])),
        ("NinaproDB3", lambda: run_ninapro(results, args, "NinaproDB3", [1, 2] if quick else range(1, 12),
                                           ["heldout_run:2,5", "cross_subject"], deep_on=["heldout_run:2,5"])),
        ("NinaproDB7", lambda: run_ninapro(results, args, "NinaproDB7", [1] if quick else range(1, 21),
                                           ["leave_one_run_out"])),
        ("NinaproDB7-amputee", lambda: run_ninapro(results, args, "NinaproDB7-amputee", [21] if quick else [21, 22],
                                                   ["leave_one_run_out"])),
        ("CapgMyo-DBa", lambda: run_capgmyo(results, args, "a", None)),
        ("CapgMyo-DBb", lambda: run_capgmyo(results, args, "b", args.paths["capgmyo_dbb"])),
        ("CapgMyo-DBc", lambda: run_capgmyo(results, args, "c", args.paths["capgmyo_dbc"])),
        ("CSL-HDEMG", lambda: run_csl(results, args, args.paths["csl_hdemg"])),
        ("HyserPR-dynamic", lambda: run_hyser(results, args, "dynamic")),
        ("HyserPR-maintenance", lambda: run_hyser(results, args, "maintenance")),
        ("EMG-EPN-612", lambda: run_epn(results, args)),
        ("putEMG", lambda: run_putemg(results, args)),
    ]
    paths = getattr(args, "paths", None) or {}
    for name, job in jobs:
        if args.datasets and name not in args.datasets:
            continue
        print(f"\n[{PHASE}] {name}")
        if name in gated and gated[name] not in paths:
            print(f"  - {name}: access-gated, skipped (pass --path {gated[name]}=FOLDER)")
            continue
        try:
            job()
        except Exception as e:
            log_error(PHASE, f"{name}: {type(e).__name__}: {e}")
