"""fNIRS benchmarks (phase 10): hybrid EEG+fNIRS, workload, motor, auditory and attention datasets.

Source of truth for protocols and published numbers: projects/fnirs/DATASETS.md.

Every recording goes through the same MNE pipeline: light intensity -> optical density -> modified Beer-Lambert law
(partial pathlength factor 6) -> HbO/HbR, short channels (< 1.5 cm) dropped, 0.01-0.5 Hz band-pass, resampled to
10 Hz when faster. Sets released as HbO/HbR (Bak 2019, Tufts) skip the first two steps. Each trial is baseline
corrected with the 2 s before its onset (unsupervised, per trial). Input variants are kept as separate dataset names,
because the published numbers differ a lot between them (DATASETS.md, "How to read these numbers"):
`(3s windows)` = 3-s windows with a 1-s step pooled over a trial (fNIRSNet protocol), `(10s epochs)` etc. = one
sample per trial over a fixed interval chosen in advance (never a test-selected "best window").

Protocols (no trial/window leakage):
- `leave_one_run_out`: per subject, 5-fold CV over trials. The `run` column holds each trial's fold (stratified,
  fixed seed), so all windows of a trial are in the same fold. Tufts: 4 folds over whole 80-s blocks.
- `cross_subject`: leave-one-subject-out when <= 20 subjects, else GroupKFold(5) by subject. Tufts: subject = the
  official test bucket, so this is the 17-bucket "generic" paradigm.
- `cross_session` (ds007554, Kernel), `heldout_session:left3s,right3s` (FRESH II: train on the 2-s tapping runs,
  test on the 3-s runs).

Models: `MeanSlope+sLDA` (mean and slope of every HbO/HbR channel in ~5-s segments, shrinkage LDA: the original
Shin et al. baseline), `ResNet1D` (common.resnet1d on the HbO/HbR time series; braindecode EEGNet does not fit
30-sample inputs at 10 Hz).

| Dataset (name in results) | How it is obtained | Protocol(s) | Models | Tested here |
|---|---|---|---|---|
| Shin 2017 A motor imagery / B mental arithmetic (`Shin2017A-MI`, `Shin2017B-MA`, each `(3s windows)` and `(10s epochs)`) | auto-download from doc.ml.tu-berlin.de/hBCI (GNU GPL click-through; NIRS zip 0.8 GB, raw intensity) | per subject, cross-subject | sLDA, ResNet1D | yes, quick (2 subjects) |
| Shin 2017 hybrid EEG+fNIRS (`Shin2017A-MI hybrid (3s windows)`, `Shin2017B-MA hybrid (3s windows)`) | same site, EEG zips (1.1 GB per 5 subjects); EEG log band power (4-8, 8-13, 13-30 Hz) at 10 Hz stacked with HbO/HbR | per subject, cross-subject | sLDA, ResNet1D | yes, quick (2 subjects) |
| Shin 2018 n-back 0/2/3 and word generation vs baseline (`Shin2018-nback (40s blocks)`, `Shin2018-WG (10s epochs)`) | auto-download, NIRx raw files per subject (61 MB each) | per subject, cross-subject | sLDA, ResNet1D | yes, quick (2 subjects) |
| Shin 2018 DSR | not run: the NIRS markers only carry block onsets (no class contrast for fNIRS); O vs X is an EEG ERP task | - | - | no |
| Herff 2014 n-back | not run: the download needs e-mail registration and the file format could not be checked | - | - | no |
| Bak 2019 UFFT (`Bak2019-UFFT (3s windows)`, `(10s epochs)`) | auto-download, figshare (245 MB) | per subject, cross-subject | sLDA, ResNet1D | yes, quick (2 subjects) |
| Tufts fNIRS2MW 0- vs 2-back (`Tufts-fNIRS2MW 0v2 (30s windows)`) | auto-download of the band-pass-filtered whole-session CSVs from the public Box folder, or `--path tufts=FOLDER` with `sub_*.csv` | per subject (4 block folds), generic (17 official buckets) | sLDA, ResNet1D | yes, quick (2 subjects from 2 buckets) |
| MNE-NIRS finger tapping (`MNE-NIRS-Tapping (15s epochs)`) | official package, `mne_nirs.datasets.fnirs_motor_group` | per subject, cross-subject | sLDA, ResNet1D | yes, quick |
| Luke 2021 auditory = FRESH Dataset I (`Luke2021-Auditory (15s epochs)`) | auto-download, OpenNeuro ds005964 (same data as MNE-NIRS `block_speech_noise`) | per subject, cross-subject | sLDA, ResNet1D | yes, quick |
| FRESH Dataset II motor (`FRESH-II-Motor L-R (15s epochs)`) | auto-download, OpenNeuro ds005963 | train 2-s runs, test 3-s runs; cross-subject | sLDA, ResNet1D | yes, quick |
| Ning 2024 spatial attention (`Ning2024 (15s epochs)` 3 classes, `Ning2024 L-R (15s epochs)`) | auto-download, OpenNeuro ds004830 (50 Hz, resampled to 10 Hz) | per subject, cross-subject | sLDA, ResNet1D | partial (1 run of 1 subject) |
| Rybar semantic imagery animals vs tools (`ds004514 animal-tool (15s epochs)`) | auto-download, OpenNeuro ds004514 (fNIRS part only) | per subject, cross-subject | sLDA, ResNet1D | yes, quick |
| ds007554 task identity MA / n-back / MI (`ds007554 task (30s windows)`) | auto-download, OpenNeuro ds007554 (one 3-min recording per task and session; windows of a recording stay together) | cross-session, cross-subject | sLDA, ResNet1D | yes, quick |
| ds007738 covert attention left vs right (`ds007738 covert L-R (15s epochs)`) | auto-download, OpenNeuro ds007738 (127 MB per run; uses the `include` column) | per subject, cross-subject | sLDA, ResNet1D | partial (1 subject) |
| Stroop congruent vs incongruent blocks, sparse / high-density (`ds006459 Stroop`, `ds006460 Stroop`, 15s epochs) | auto-download, OpenNeuro | per subject, cross-subject | sLDA, ResNet1D | yes, quick |
| Kernel Flow2 auditory story vs noise (`Kernel-Flow2 story-noise (20s epochs)`) | auto, OpenNeuro ds006545, streamed with HTTP range reads (only the TD-moment data, not the 400 MB of aux per file); moment-0 counts used as CW intensity, channels 15-45 mm averaged per module | per subject, cross-session, cross-subject | sLDA, ResNet1D | partial (1 subject, 2 sessions) |
| WashU HD-DOT motor localizer left vs right hand (`HD-DOT MOT L-R (15s epochs)`) | auto, OpenNeuro ds007473, streamed like Kernel; channels 15-45 mm averaged per source optode (~250 HbO/HbR channels) | per subject, cross-subject | sLDA, ResNet1D | partial (1 run) |
| WashU ds007463, ds007816 (74-138 GB, localizers/movies), ds008798 (stroke rest), ds006377 / ds007420 (event codes undocumented), ds008192 (hyperscanning, no classes), ds005929 (motion artifacts) | not run: no usable classification task or labels | - | - | no |

Extra packages: mne-nirs (for the tapping set), h5py (Kernel / HD-DOT streaming).
"""
import glob
import io
import json
import os
import re
import urllib.parse
import urllib.request
import zipfile

import mne
import numpy as np
import pandas as pd
import scipy.io as sio
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from common import _safe, classical, deep, download, evaluate, log_error, resnet1d
from ecg import HttpFile, wanted
from eog import use

PHASE = "phase10"
FS = 10.0  # target rate for everything sampled faster
OPENNEURO = "https://s3.amazonaws.com/openneuro.org/"
DEEP = dict(lr=1e-3, weight_decay=1e-4, batch_size=64)


def attempt(name, fn, *a):
    print(f"\n[{PHASE}] {name}")
    try:
        return fn(*a)
    except Exception as e:
        log_error(PHASE, f"{name}: could not load ({type(e).__name__}: {e})")


# ------------------------------------------------------------------ preprocessing (MNE)

def cw_raw(I, wls, fs, src=None, det=None):
    """Intensity array (2 * n_pairs, T), ordered pair by pair (wl1, wl2), as an MNE raw.

    Without positions, every pair gets a 30-mm source-detector distance (the distance reported for Shin 2017/2018).
    """
    n = len(I) // 2
    names = [f"S{i + 1}_D{i + 1} {int(w)}" for i in range(n) for w in wls]
    info = mne.create_info(names, fs, "fnirs_cw_amplitude")
    for k, ch in enumerate(info["chs"]):
        s = np.zeros(3) if src is None else src[k // 2]
        d = np.array([0.03, 0, 0]) if det is None else det[k // 2]
        ch["loc"][:3], ch["loc"][3:6], ch["loc"][6:9], ch["loc"][9] = (s + d) / 2, s, d, wls[k % 2]
    return mne.io.RawArray(np.asarray(I, dtype=np.float64), info, verbose=False)


def hb_raw(x, n_hbo, fs):
    """HbO/HbR array (2n, T): first n rows HbO, next n HbR."""
    names = [f"S{i + 1}_D{i + 1} {k}" for k in ("hbo", "hbr") for i in range(n_hbo)]
    return mne.io.RawArray(np.asarray(x, dtype=np.float64), mne.create_info(names, fs, ["hbo"] * n_hbo + ["hbr"] * n_hbo),
                           verbose=False)


def to_hb(raw, dmin=0.015, dmax=0.045):
    """Intensity -> OD -> MBLL -> HbO/HbR (uM), band-pass 0.01-0.5 Hz, <= 10 Hz. Returns (x, fs, channel names)."""
    raw.load_data(verbose=False)
    if "fnirs_cw_amplitude" in raw.get_channel_types():
        raw.pick("fnirs_cw_amplitude")
        raw._data = np.maximum(raw._data, 1e-12)  # zero/negative intensities would give inf OD
        raw = mne.preprocessing.nirs.optical_density(raw, verbose=False)
        d = mne.preprocessing.nirs.source_detector_distances(raw.info)
        if np.nanmedian(d) < 0.01:  # positions stored in cm but labelled mm (seen in ds007554): rescale
            for ch in raw.info["chs"]:
                ch["loc"][:9] *= 10
            d = d * 10
        raw.pick(np.flatnonzero((d >= dmin) & (d <= dmax)))
        raw = mne.preprocessing.nirs.beer_lambert_law(raw, ppf=6.0)
    raw.pick(["hbo", "hbr"])
    raw.filter(0.01, min(0.5, raw.info["sfreq"] / 2 - 0.1), verbose=False)
    if raw.info["sfreq"] > FS + 0.5:
        raw.resample(FS, verbose=False)
    return np.nan_to_num(raw.get_data() * 1e6).astype(np.float32), raw.info["sfreq"], raw.ch_names


def rec(x, fs, ch, events, subject, session="0", run="0"):
    """One continuous recording. events: list of (onset_s, label, trial_id)."""
    return dict(x=x, fs=fs, ch=list(ch), events=events, subject=str(subject), session=str(session), run=str(run))


# ------------------------------------------------------------------ epochs, windows, folds

def epochs(recs, tmin, tmax, win=None, step=1.0, base=2.0):
    """Cut every event into [tmin, tmax] (optionally into win-s windows with a step), baseline corrected.

    Channels are the ones common to all recordings (montages can differ by a few channels between subjects).
    """
    common = [c for c in recs[0]["ch"] if all(c in set(r["ch"]) for r in recs[1:])]
    X, y, meta = [], [], []
    for r in recs:
        x, fs = r["x"][[r["ch"].index(c) for c in common]], r["fs"]
        n = int(round((tmax - tmin) * fs))
        w = int(round(win * fs)) if win else n
        starts = range(0, n - w + 1, max(1, int(round(step * fs)))) if win else [0]
        for on, lab, tr in r["events"]:
            a, b = int(round((on + tmin) * fs)), int(round(on * fs))
            if a < 0 or a + n > x.shape[1]:
                continue
            seg = x[:, a:a + n]
            if base and b - int(base * fs) >= 0:
                seg = seg - x[:, b - int(base * fs):b].mean(1, keepdims=True)
            for s in starts:
                X.append(seg[:, s:s + w])
                y.append(lab)
                meta.append(dict(subject=r["subject"], session=r["session"], run=r["run"], trial=f"{r['session']}/{r['run']}/{tr}"))
    if not X:
        raise ValueError("no epochs")
    return np.stack(X).astype(np.float32), np.asarray(y), pd.DataFrame(meta)


def per_subject(meta, y, k=5):
    """Meta for `leave_one_run_out`: per subject, trials dealt into k stratified folds (fixed seed); all windows of
    a trial share its fold, so overlapping windows never straddle train and test."""
    m = meta.copy()
    key = m.subject + "|" + m.trial
    trials = pd.DataFrame({"key": key, "subj": m.subject, "y": y}).drop_duplicates("key")
    rng, fold = np.random.RandomState(0), {}
    for _, g in trials.groupby(["subj", "y"]):
        off = rng.randint(k)
        for i, kk in enumerate(rng.permutation(g.key.values)):
            fold[kk] = f"f{(i + off) % k}"
    m["session"], m["run"] = "0", key.map(fold)
    return m


class MeanSlope(BaseEstimator, TransformerMixin):
    """Mean and least-squares slope of every channel in `seg` equal time segments."""

    def __init__(self, seg=1):
        self.seg = seg

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X, out = np.asarray(X, dtype=np.float32), []
        for s in np.array_split(np.arange(X.shape[-1]), self.seg):
            x, t = X[..., s], np.arange(len(s)) - (len(s) - 1) / 2
            out += [x.mean(-1), (x * t).sum(-1) / max((t ** 2).sum(), 1e-9)]
        return np.concatenate(out, 1)


def run_models(results, args, dname, X, y, protocols, seconds):
    """protocols: list of (protocol, meta). Mean/slope over ~5-s segments of the input."""
    print(f"  {dname}: {len(y)} samples, {X.shape[1]} channels x {X.shape[2]} samples, classes {sorted(set(y))}")
    seg = max(1, min(int(seconds // 5), 4000 // (2 * X.shape[1])))  # ponytail: fewer segments for 1000+ channels (LDA cost ~ d^3)
    for protocol, meta in protocols:
        if use(args, "MeanSlope+sLDA"):
            pipe = make_pipeline(MeanSlope(seg), StandardScaler(), LDA(solver="lsqr", shrinkage="auto"))
            _safe(evaluate, PHASE, results, dname, protocol, "MeanSlope+sLDA", classical(pipe), X, y, meta, args.seeds,
                  needs_seed=False)
        if use(args, "ResNet1D"):
            make = deep(resnet1d, epochs=min(args.epochs, 60), **DEEP)
            _safe(evaluate, PHASE, results, dname, protocol, "ResNet1D", make, X, y, meta, args.seeds)


def standard_runs(results, args, dname, recs, tmin, tmax, win=None, extra=()):
    try:
        X, y, meta = epochs(recs, tmin, tmax, win)
    except Exception as e:
        return log_error(PHASE, f"{dname}: could not build epochs ({type(e).__name__}: {e})")
    protocols = [("leave_one_run_out", per_subject(meta, y)), ("cross_subject", meta), *[(p, meta) for p in extra]]
    run_models(results, args, dname, X, y, protocols, win or (tmax - tmin))


# ------------------------------------------------------------------ Shin 2017 (hBCI, TU Berlin)

HBCI = "https://doc.ml.tu-berlin.de/hBCI/"
EEG_ZIPS = ["01-05", "06-10", "11-15", "16-20", "21-25", "26-29"]


def members(zpath, prefix, dest):
    """Extract only the zip members under prefix."""
    with zipfile.ZipFile(zpath) as z:
        names = [n for n in z.namelist() if n.startswith(prefix)]
        if not all(os.path.exists(os.path.join(dest, n)) for n in names):
            z.extractall(dest, names)
    return os.path.join(dest, prefix)


def mat(path, key):
    return sio.loadmat(path, squeeze_me=True, struct_as_record=False)[key]


def eeg_env(x, fs, bands=((4, 8), (8, 13), (13, 30))):
    """Log band power envelopes (1-Hz smoothed) of EEG channels, decimated to 10 Hz."""
    out = []
    for lo, hi in bands:
        p = mne.filter.filter_data(x, fs, lo, hi, verbose=False) ** 2
        p = mne.filter.filter_data(p, fs, None, 1.0, verbose=False)
        out.append(np.log(np.maximum(p[:, ::int(fs // FS)], 1e-6)))
    return np.concatenate(out)


def load_shin2017(root, subjects, task, hybrid):
    """task 'MI' (LMI vs RMI, sessions 1/3/5) or 'MA' (MA vs BL, sessions 2/4/6). Intensity -> MNE -> HbO/HbR."""
    print("  Shin 2017 data are GNU GPL licensed (doc.ml.tu-berlin.de/hBCI); downloading means accepting it.")
    nz = download(HBCI + "NIRS/NIRS_01-29.zip", os.path.join(root, "NIRS_01-29.zip"))
    recs = []
    for s in subjects:
        d = members(nz, f"subject {s:02d}/", os.path.join(root, "nirs"))
        cnt, mrk = mat(os.path.join(d, "cnt.mat"), "cnt"), mat(os.path.join(d, "mrk.mat"), "mrk")
        if hybrid:
            grp = EEG_ZIPS[(s - 1) // 5]
            ez = download(HBCI + f"EEG/EEG_{grp}.zip", os.path.join(root, f"EEG_{grp}.zip"))
            ed = members(ez, f"subject {s:02d}/with occular artifact/", os.path.join(root, "eeg"))
            ecnt, emrk = mat(os.path.join(ed, "cnt.mat"), "cnt"), mat(os.path.join(ed, "mrk.mat"), "mrk")
        for i in range(0 if task == "MI" else 1, 6, 2):
            c, m = cnt[i], mrk[i]
            low = [j for j, n in enumerate(c.clab) if n.endswith("lowWL")]
            high = [list(c.clab).index(c.clab[j].replace("lowWL", "highWL")) for j in low]
            I = np.asarray(c.x, dtype=np.float64).T[np.ravel(list(zip(low, high)))]
            x, fs, ch = to_hb(cw_raw(I, list(c.wavelengths), float(c.fs)))
            onsets = np.asarray(m.time) / 1000.0
            labels = np.asarray(m.className)[np.argmax(np.asarray(m.y), 0)]
            if hybrid:
                ec, em = ecnt[i], emrk[i]
                assert (np.argmax(np.asarray(em.y), 0) == np.argmax(np.asarray(m.y), 0)).all(), "EEG/NIRS trial order differs"
                keep = [j for j, n in enumerate(ec.clab) if "EOG" not in n]
                env = eeg_env(np.asarray(ec.x, dtype=np.float64).T[keep], float(ec.fs))
                shift = int(round(np.median(onsets - np.asarray(em.time) / 1000.0) * FS))  # NIRS time = EEG time + shift
                al = np.zeros((len(env), x.shape[1]), dtype=np.float32)
                a, b = max(0, shift), min(x.shape[1], env.shape[1] + shift)
                al[:, a:b] = env[:, a - shift:b - shift]
                x, ch = np.vstack([x, al]), ch + [f"eeg{j}" for j in range(len(env))]
            recs.append(rec(x, fs, ch, [(o, lab, t) for t, (o, lab) in enumerate(zip(onsets, labels))], s, i // 2, "0"))
    return recs


def run_shin2017(results, args, root):
    subjects = [1, 2] if args.quick else range(1, 30)
    for task, name in (("MI", "Shin2017A-MI"), ("MA", "Shin2017B-MA")):
        if not wanted(args, "Shin2017", name):
            continue
        recs = attempt(f"{name} (fNIRS)", load_shin2017, root, subjects, task, False)
        if recs:
            standard_runs(results, args, f"{name} (3s windows)", recs, -2, 10, win=3)  # 10 windows: -2..1 ... 7..10 s
            standard_runs(results, args, f"{name} (10s epochs)", recs, 0, 10)
        recs = attempt(f"{name} (EEG + fNIRS)", load_shin2017, root, subjects, task, True)
        if recs:
            standard_runs(results, args, f"{name} hybrid (3s windows)", recs, -2, 10, win=3)


# ------------------------------------------------------------------ Shin 2018 (n-back, DSR, WG), NIRx raw files

SHIN18 = "http://doc.ml.tu-berlin.de/simultaneous_EEG_NIRS/NIRS/VP{:03d}.zip"
SHIN18_CODES = {"nback": {7: "0-back", 8: "2-back", 9: "3-back"}, "wg": {1: "WG", 2: "BL"}}


def nirx_session(folder):
    """One NIRx session folder -> (intensity (2*36, T) pair by pair, wavelengths, fs, events [(t, code)])."""
    hdr = open(glob.glob(os.path.join(folder, "*.hdr"))[0], encoding="latin-1").read()
    block = lambda key: re.search(key + r'="#\s*\n(.*?)#"', hdr, re.S).group(1)
    fs = float(re.search(r"SamplingRate=([\d.]+)", hdr).group(1))
    wls = [float(w) for w in re.search(r'Wavelengths="([^"]+)"', hdr).group(1).split()]
    n_det = int(re.search(r"Detectors=(\d+)", hdr).group(1))
    src, det = np.nonzero(np.loadtxt(io.StringIO(block("S-D-Mask"))))
    ev = np.loadtxt(io.StringIO(block("Events")), ndmin=2)
    cols = src * n_det + det  # S-D-Key order: 1-1, 1-2, ..., 1-n_det, 2-1, ...
    w1, w2 = (np.loadtxt(glob.glob(os.path.join(folder, f"*.wl{k}"))[0])[:, cols].T for k in (1, 2))
    return np.stack([w1, w2], 1).reshape(-1, w1.shape[1]), wls, fs, [(t, int(c)) for t, c, *_ in ev]


def load_shin2018(root, subjects, task):
    recs = []
    for s in subjects:
        z = download(SHIN18.format(s), os.path.join(root, f"VP{s:03d}.zip"))
        d = os.path.join(root, f"VP{s:03d}")
        if not os.path.isdir(d):
            zipfile.ZipFile(z).extractall(d)
        sess = 0
        for f in sorted(glob.glob(os.path.join(d, "**", "*.hdr"), recursive=True)):
            I, wls, fs, ev = nirx_session(os.path.dirname(f))
            codes = SHIN18_CODES[task]
            if sum(c in codes for _, c in ev) < len(ev) / 2:  # another task's session (told apart by its marker codes)
                continue
            ev = [(t, codes[c]) for t, c in ev if c in codes]
            x, fs, ch = to_hb(cw_raw(I, wls, fs))
            recs.append(rec(x, fs, ch, [(t, lab, i) for i, (t, lab) in enumerate(ev)], s, sess))
            sess += 1
    return recs


def run_shin2018(results, args, root):
    subjects = [1, 2] if args.quick else range(1, 27)
    if wanted(args, "Shin2018", "Shin2018-nback"):
        recs = attempt("Shin2018 n-back", load_shin2018, root, subjects, "nback")
        if recs:
            standard_runs(results, args, "Shin2018-nback (40s blocks)", recs, 0, 40)
    if wanted(args, "Shin2018", "Shin2018-WG"):
        recs = attempt("Shin2018 word generation", load_shin2018, root, subjects, "wg")
        if recs:
            standard_runs(results, args, "Shin2018-WG (10s epochs)", recs, 0, 10)


# ------------------------------------------------------------------ Bak 2019 UFFT

BAK = "https://ndownloader.figshare.com/files/18069143"


def load_bak(root, subjects):
    z = download(BAK, os.path.join(root, "fNIRS data.zip"))
    recs = []
    for s in subjects:
        f = members(z, f"fNIRS {s:02d}.mat", root)
        m = sio.loadmat(f, squeeze_me=True, struct_as_record=False)
        x = np.stack([m[f"ch{i}"] for i in range(1, 41)])  # ch1-20 HbO, ch21-40 HbR (nfo.clab)
        x, fs, ch = to_hb(hb_raw(x, 20, float(m["nfo"].fs)))
        mk = m["mrk"]
        labels = np.asarray(mk.className)[np.asarray(mk.event.desc).astype(int) - 1]
        recs.append(rec(x, fs, ch, [(t / 1000.0, lab, i) for i, (t, lab) in enumerate(zip(mk.time, labels))], s))
    return recs


def run_bak(results, args, root):
    if not wanted(args, "Bak2019", "Bak2019-UFFT"):
        return
    recs = attempt("Bak 2019 UFFT", load_bak, root, [1, 2] if args.quick else range(1, 31))
    if recs:
        standard_runs(results, args, "Bak2019-UFFT (3s windows)", recs, 0, 10, win=3)  # 8 windows: 0..3 ... 7..10 s
        standard_runs(results, args, "Bak2019-UFFT (10s epochs)", recs, 0, 10)


# ------------------------------------------------------------------ Tufts fNIRS2MW

TUFTS_SHARE, TUFTS_FOLDER = "bj0iml74am3wnuittzmjggjemxxgz2cp", "144901078723"  # band_pass_filtered/whole_data
TUFTS_PLAN = "https://raw.githubusercontent.com/tufts-ml/fNIRS-mental-workload-classifiers/main/partition_plan.txt"


def tufts_plan(root):
    """Eligible subjects and the 17 official test buckets of the 64-subject generic paradigm."""
    t = open(download(TUFTS_PLAN, os.path.join(root, "partition_plan.txt"), quiet=True)).read()
    eligible = [int(s) for s in t.split("All eligible subjects:")[1].split("1.")[0].split()]
    buckets = [[int(v) for v in re.findall(r"\d+", b)] for b in re.findall(r"test_subjects = \[([^\]]+)\]", t)[:17]]
    return eligible, {s: f"bucket{i + 1:02d}" for i, b in enumerate(buckets) for s in b}


def tufts_fetch(root, subjects):
    """Per-subject CSVs from the public Box folder (file ids read from the folder pages)."""
    ids, page = {}, 1
    while True:
        url = f"https://tufts.box.com/s/{TUFTS_SHARE}/folder/{TUFTS_FOLDER}?page={page}"
        html = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read().decode()
        found = dict((n, i) for i, n in re.findall(r'"typedID":"f_(\d+)".{0,400}?"name":"(sub_\d+\.csv)"', html))
        if not found or set(found) <= set(ids):
            break
        ids.update(found)
        page += 1
    for s in subjects:
        n = f"sub_{s}.csv"
        if n in ids:
            download(f"https://tufts.app.box.com/index.php?rm=box_download_shared_file&shared_name={TUFTS_SHARE}"
                     f"&file_id=f_{ids[n]}", os.path.join(root, n), quiet=True)
    return root


def load_tufts(root, folder, quick, win=150, step=15):
    """0-back vs 2-back, 30-s windows (150 samples at 5.2 Hz), 3-s step, inside each 80-s block; block = trial."""
    eligible, bucket = tufts_plan(root)
    subjects = [next(s for s in eligible if bucket.get(s) == b) for b in ("bucket01", "bucket02")] if quick else eligible
    folder = folder or tufts_fetch(os.path.join(root, "whole_data"), subjects)
    X, y, meta = [], [], []
    for s in subjects:
        f = os.path.join(folder, f"sub_{s}.csv")
        if not os.path.exists(f):
            continue
        d = pd.read_csv(f)
        lab = d.pop("label").values
        x = d.values.T.astype(np.float32)
        blocks = np.r_[0, np.cumsum(np.diff(lab) != 0)]
        for b in np.unique(blocks):
            idx = np.flatnonzero(blocks == b)
            if lab[idx[0]] not in (0, 2):
                continue
            for a in range(idx[0], idx[-1] - win + 2, step):
                X.append(x[:, a:a + win])
                y.append(f"{lab[idx[0]]}-back")
                meta.append(dict(subject=str(s), session="0", run="0", trial=str(b), bucket=bucket.get(s, "none")))
    return np.stack(X), np.asarray(y), pd.DataFrame(meta)


def run_tufts(results, args, root):
    if not wanted(args, "Tufts", "Tufts-fNIRS2MW"):
        return
    d = attempt("Tufts fNIRS2MW", load_tufts, root, args.paths.get("tufts"), args.quick)
    if d:
        X, y, meta = d
        protocols = [("leave_one_run_out", per_subject(meta, y, k=4)), ("cross_subject", meta.assign(subject=meta.bucket))]
        run_models(results, args, "Tufts-fNIRS2MW 0v2 (30s windows)", X, y, protocols, 30)


# ------------------------------------------------------------------ BIDS / SNIRF sets (OpenNeuro, MNE-NIRS)

def s3_keys(ds, root):
    """All file keys of an OpenNeuro dataset (public S3 listing), cached."""
    cache = os.path.join(root, f"{ds}_files.json")
    if os.path.exists(cache):
        return json.load(open(cache))
    keys, tok = [], None
    while True:
        q = {"list-type": "2", "prefix": ds + "/", **({"continuation-token": tok} if tok else {})}
        t = urllib.request.urlopen(OPENNEURO + "?" + urllib.parse.urlencode(q), timeout=120).read().decode()
        keys += re.findall(r"<Key>([^<]+)</Key>", t)
        m = re.search(r"<NextContinuationToken>([^<]+)<", t)
        if not m:
            break
        tok = m.group(1)
    os.makedirs(root, exist_ok=True)
    json.dump(keys, open(cache, "w"))
    return keys


def openneuro(ds, root, task, n_subjects=None, per_subject_max=None):
    """SNIRF keys of one task (regex on the file name), limited to the first n subjects / files per subject."""
    keys = [k for k in s3_keys(ds, root) if k.endswith("_nirs.snirf") and re.search(task, os.path.basename(k))]
    subs = sorted({k.split("/")[1] for k in keys})[:n_subjects]
    out = []
    for s in subs:
        out += sorted(k for k in keys if k.split("/")[1] == s)[:per_subject_max]
    return out


def local(ds, root, key):
    for k in (key, key.replace("_nirs.snirf", "_events.tsv")):
        download(OPENNEURO + urllib.parse.quote(k), os.path.join(root, k), quiet=True)
    return os.path.join(root, key)


def entities(path):
    return dict(re.findall(r"(sub|ses|run|task)-([A-Za-z0-9]+)", os.path.basename(path)))


def bids_events(path, fs, n, label):
    """Events from the BIDS events.tsv: label(trial_type, entities) -> class or None."""
    ev = pd.read_csv(path.replace("_nirs.snirf", "_events.tsv"), sep="\t")
    if "include" in ev:
        ev = ev[ev.include.astype(str) == "1"]
    on = ev.onset.astype(float).values
    if len(on) and on.max() > n / fs:  # some sets (WashU) store onsets in samples
        on = on / fs
    ent = entities(path)
    return [(o, label(str(t), ent), i) for i, (o, t) in enumerate(zip(on, ev.trial_type)) if label(str(t), ent)]


def load_bids(paths, label, task_windows=None):
    """SNIRF + events.tsv -> recordings. task_windows=(label_of_task, seconds): one class per recording, cut into
    consecutive windows that all share one trial id (the whole recording stays in one fold)."""
    recs = []
    for p in paths:
        ent = entities(p)
        x, fs, ch = to_hb(mne.io.read_raw_snirf(p, verbose="error"))
        if task_windows:
            lab, sec = task_windows
            events = [(t, lab[ent["task"]], 0) for t in np.arange(0, x.shape[1] / fs - sec, sec)]
        else:
            events = bids_events(p, fs, x.shape[1], label)
        recs.append(rec(x, fs, ch, events, ent["sub"], ent.get("ses", "0"), ent.get("run", ent.get("task", "0"))))
    return recs


def first_word(table):
    """Map trial_type by its first matching key (case-insensitive substring)."""
    return lambda t, ent: next((v for k, v in table.items() if k in t.lower()), None)


# name, OpenNeuro id, task regex, label function, (tmin, tmax), extra protocols, quick subjects, files/subject (quick)
BIDS_SETS = [
    ("Luke2021-Auditory (15s epochs)", "ds005964", "FRESHAUDIO", first_word({"speech": "speech", "noise": "noise", "control": "silence"}), (0, 15), [], 2, None),
    ("FRESH-II-Motor L-R (15s epochs)", "ds005963", "FRESHMOTOR", lambda t, e: e["ses"][:-2] if t == "motor" else None, (0, 15), ["heldout_session:left3s,right3s"], 2, None),
    ("Ning2024 (15s epochs)", "ds004830", "task-overt", first_word({"left": "left", "right": "right", "center": "center"}), (0, 15), [], 1, 1),
    ("ds004514 animal-tool (15s epochs)", "ds004514", "task-nirs", first_word({"animal_image": "animal", "tool_image": "tool"}), (0, 15), [], 2, None),
    ("ds007738 covert L-R (15s epochs)", "ds007738", "task-covert", first_word({"left": "left", "right": "right"}), (0, 15), [], 1, 1),
    ("ds006459 Stroop (15s epochs)", "ds006459", "WordStroop", first_word({"incongruent": "incongruent", "congruent": "congruent"}), (0, 15), [], 2, None),
    ("ds006460 Stroop (15s epochs)", "ds006460", "WordStroop", first_word({"incongruent": "incongruent", "congruent": "congruent"}), (0, 15), [], 2, None),
]
DS7554_TASKS = {"mentalarithmetic": "MA", "nback": "nback", "motorimagery": "MI"}


def run_bids(results, args, root):
    for name, ds, task, label, (tmin, tmax), extra, nq, fq in BIDS_SETS:
        if not wanted(args, name, ds, name.split(" ")[0]):
            continue
        paths = attempt(name, lambda: [local(ds, root, k) for k in openneuro(ds, root, task, nq if args.quick else None,
                                                                                fq if args.quick else None)])
        recs = paths and attempt(f"{name}: preprocessing", load_bids, paths, label)
        if recs:
            standard_runs(results, args, name, recs, tmin, tmax, extra=extra)
            if name.startswith("Ning2024"):  # the published 2-class contrast (left vs right) on the same epochs
                lr = [dict(r, events=[e for e in r["events"] if e[1] != "center"]) for r in recs]
                standard_runs(results, args, "Ning2024 L-R (15s epochs)", lr, tmin, tmax)

    name = "ds007554 task (30s windows)"
    if wanted(args, name, "ds007554"):
        pat = "task-(" + "|".join(DS7554_TASKS) + ")_"
        paths = attempt(name, lambda: [local("ds007554", root, k) for k in openneuro("ds007554", root, pat, 2 if args.quick else None)])
        recs = paths and attempt(f"{name}: preprocessing", load_bids, paths, None, (DS7554_TASKS, 30))
        d = recs and attempt(f"{name}: windows", epochs, recs, 0, 30, None, 1.0, 0)
        if d:
            X, y, meta = d
            run_models(results, args, name, X, y, [("cross_session", meta), ("cross_subject", meta)], 30)

    name = "MNE-NIRS-Tapping (15s epochs)"
    if wanted(args, name, "MNE-NIRS-Tapping"):
        def tapping():
            from mne_nirs.datasets import fnirs_motor_group
            base = str(fnirs_motor_group.data_path(path=os.path.join(root, "mne_nirs")))
            paths = sorted(glob.glob(os.path.join(base, "sub-*", "**", "*_nirs.snirf"), recursive=True))
            return load_bids(paths[:2] if args.quick else paths,
                             first_word({"left": "left", "right": "right", "control": "control"}))
        recs = attempt(name, tapping)
        if recs:
            standard_runs(results, args, name, recs, 0, 15)


# ------------------------------------------------------------------ streamed SNIRF (Kernel Flow2, WashU HD-DOT)

def streamed(key, root, select, dmin=0.015, dmax=0.045, group=None):
    """Read one large SNIRF over HTTP range requests (only the data block), keep the CW-like channels chosen by
    select(channels.tsv) at dmin-dmax, run the MNE pipeline, optionally average channels by group(source label).
    Result cached as a small .npz."""
    import h5py
    cache = os.path.join(root, os.path.basename(key).replace(".snirf", "_grouped.npz" if group else ".npz"))
    if not os.path.exists(cache):
        url = OPENNEURO + key
        chans = pd.read_csv(url.replace("_nirs.snirf", "_channels.tsv"), sep="\t")
        with h5py.File(HttpFile(url), "r") as f:
            p, d = f["nirs/probe"], f["nirs/data1"]
            unit = f["nirs/metaDataTags/LengthUnit"][()].decode() if "LengthUnit" in f["nirs/metaDataTags"] else "mm"
            scale = {"mm": 1e-3, "cm": 1e-2}.get(unit, 1.0)
            pos = {}
            for kind in ("source", "detector"):
                xyz = p[f"{kind}Pos3D"][()] * scale
                labels = [v.decode() for v in p[f"{kind}Labels"][()]] if f"{kind}Labels" in p else []
                pos[kind] = lambda v, xyz=xyz, labels=labels: xyz[labels.index(v) if v in labels else int(v) - 1]
            sel = chans.index[select(chans)].values
            pairs = chans.loc[sel].groupby(["source", "detector"], sort=False)
            cols, src, det, groups = [], [], [], []
            wls = sorted(chans.loc[sel, "wavelength_nominal"].astype(float).unique())
            for (s, dd), g in pairs:
                g = g.sort_values("wavelength_nominal")
                sp, dp = pos["source"](str(s)), pos["detector"](str(dd))
                if len(g) == 2 and dmin <= np.linalg.norm(sp - dp) <= dmax:
                    cols += list(g.index)
                    src.append(sp)
                    det.append(dp)
                    groups.append(group(str(s)) if group else None)
            ts, t = d["dataTimeSeries"], d["time"][()]
            I = np.concatenate([ts[i:i + 512][:, cols] for i in range(0, ts.shape[0], 512)]).T
            fs = 1.0 / np.median(np.diff(t)) if t.ndim and len(t) > 1 else float(t)
        x, fs, ch = to_hb(cw_raw(I, wls, fs, np.array(src), np.array(det)))
        if group:  # mean HbO / HbR per group (e.g. Kernel module) keeps the channel count small
            rows = {}
            for j, c in enumerate(ch):  # names are 'S{i}_D{i} hbo' with i = kept pair index + 1
                pid, kind = c.split(" ")
                rows.setdefault(f"{groups[int(pid.split('_')[0][1:]) - 1]} {kind}", []).append(j)
            ch = sorted(rows)
            x = np.stack([x[rows[c]].mean(0) for c in ch])
        os.makedirs(root, exist_ok=True)
        np.savez(cache, x=x, fs=fs, ch=np.array(ch))
    z = np.load(cache)
    return z["x"], float(z["fs"]), list(z["ch"])


def load_streamed(keys, root, select, label, group=None):
    recs = []
    for k in keys:
        x, fs, ch = streamed(k, root, select, group=group)
        ev_path = os.path.join(root, k.replace("_nirs.snirf", "_events.tsv"))
        download(OPENNEURO + k.replace("_nirs.snirf", "_events.tsv"), ev_path, quiet=True)
        ent = entities(k)
        recs.append(rec(x, fs, ch, bids_events(ev_path.replace("_events.tsv", "_nirs.snirf"), fs, x.shape[1], label),
                        ent["sub"], ent.get("ses", "0"), ent.get("run", ent.get("task", "0"))))
    return recs


def run_streamed(results, args, root):
    name = "Kernel-Flow2 story-noise (20s epochs)"
    if wanted(args, name, "Kernel-Flow2", "ds006545"):
        recs = attempt(name, lambda: load_streamed(
            openneuro("ds006545", root, "task-audio", 1 if args.quick else None), root,
            lambda c: c.name.str.endswith("-sum"),  # TD moment 0 (photon count) per wavelength = CW-like intensity
            first_word({"story": "story", "noise": "noise"}), group=lambda s: s[:4]))  # 'M012S01' -> module 'M012'
        if recs:
            standard_runs(results, args, name, recs, 0, 20, extra=["cross_session"])

    name = "HD-DOT MOT L-R (15s epochs)"
    if wanted(args, name, "HD-DOT", "ds007473"):
        recs = attempt(name, lambda: load_streamed(
            openneuro("ds007473", root, "task-MOT", 1 if args.quick else None, 1 if args.quick else None), root,
            lambda c: c.type.str.upper() == "NIRSCWAMPLITUDE", first_word({"left": "left", "right": "right"}),
            group=lambda s: f"S{s}"))  # mean over each source's 15-45 mm channels: ~3600 -> ~250 Hb channels
        if recs:
            standard_runs(results, args, name, recs, 0, 15)


# ------------------------------------------------------------------ runner

def run(results, args):
    root = os.path.join(args.data_dir, "fnirs")
    if wanted(args, "Herff2014"):
        print(f"\n[{PHASE}] Herff 2014 n-back: not run (download needs e-mail registration at csl.uni-bremen.de; "
              "file format not checked)")
    for fn, sub in [(run_shin2017, "shin2017"), (run_shin2018, "shin2018"), (run_bak, "bak2019"), (run_tufts, "tufts"),
                    (run_bids, "bids"), (run_streamed, "streamed")]:
        try:
            fn(results, args, os.path.join(root, sub))
        except Exception as e:  # anything outside the per-model guards must not stop the phase
            log_error(PHASE, f"{fn.__name__}: {type(e).__name__}: {e}")
