"""External benchmarks (phase 14): wrappers around the official pipelines of emg2qwerty, emg2pose and the
Meta Generic Neuromotor Interface (GNI). Nothing is reimplemented: each repo's own train / test entry points run
with their own configs, and the numbers they print are parsed into results rows.

| Dataset | Obtained | Protocol(s) | Models | Tested here |
|---|---|---|---|---|
| emg2qwerty (108 users, 2 x 16 ch) | `--path emg2qwerty=` or auto (one 308 GB tar.gz, streamed and unpacked; needs ~310 GB free). No small subset exists, so `--quick` skips it unless the data is already there | `generic` (train on 100 users, test each of the 8 held-out users), `personalized_finetuned`, `personalized_randominit` (one model per held-out user); folds = user0..user7 | TDSConvCTC (greedy), TDSConvCTC+LM (6-gram beam); retrained and the released checkpoints (`(released)`) | partial: data URL (HEAD) and tar layout (first member) checked; full wrapper run end to end (venv, released checkpoints, greedy + LM test, personalized random-init training, CER parsing) on synthetic HDF5 sessions for user0. Generic and fine-tuned training not run (needs the 100 training users) |
| emg2pose (193 users) | `--path emg2pose=` or auto: quick = official 647 MB mini dataset; full = 463 GB tar (streamed, needs ~470 GB free) | regression task, `heldout_user`, `heldout_stage`, `heldout_user_stage` (the repo's `generalization` column) | vemg2pose, NeuroPose (official `regression_*` experiments); retrained and released checkpoints | yes, mini dataset (one validation user; its files stand in for the test split in `--quick`, so `heldout_stage` is not applicable there) |
| GNI_discrete_gestures, GNI_handwriting, GNI_wrist (100 users each, 80/10/10) | `--path GNI_<task>=` or auto through the repo's download script: quick = `--small-subset` (3 users, 1.1 / 2.0 / 1.3 GB); full = 33 / 75 / 49 GB | `standard` (official subject-wise split; quick: the repo's `<task>_mini_split`) | DiscreteGesturesNet (metric `cler`), HandwritingConformer (`cer`), WristNet (`mae`, deg/s); retrained and released checkpoints | discrete gestures: yes (small subset); handwriting / wrist: same code path, data URLs checked only |

How it runs
- Each repo is fetched as the GitHub source archive of a pinned commit (no git needed) into
  `data_dir/external/<name>/repo-<sha>`, and gets its own virtual environment (`.../<name>/venv`) made with `uv`
  (auto-installed with pip if missing), because all three pin versions that conflict with ours
  (Python 3.10, torch 2.3, numpy 1.x, pytorch-lightning 1.8 / 2.2). The pins mirror each repo's environment.yml,
  minus dev tools. `uv` downloads the needed Python itself.
- Every official run is a subprocess (`python -m <pkg>.train ... hydra.run.dir=<run folder>`) with its full
  output in `<run folder>/run.log`; a finished run leaves `<run folder>/ok` and is not repeated, so a stopped
  benchmark resumes at run level. GPU: `trainer.accelerator` is set to the GPU when torch sees CUDA, else CPU.
- `--quick`: smallest official configuration: the mini / small-subset data and splits, 1 epoch (emg2qwerty: user0
  only, 5 train and 5 val batches per epoch).
- Checkpoint selection is the official one: best validation metric (emg2qwerty val CER, emg2pose val loss, GNI
  val metric); the test set is not used for it. Training follows the official max-epoch settings.
- Seeds: retrained models run once per `--seeds` value (passed as the repo's `seed=`); released checkpoints run once
  (seed 0).
- Units: CER and GNI CLER as fractions; emg2pose `angle_error` in degrees (the repo's radians x 180/pi),
  `landmark_error` / `fingertip_error` in mm; GNI wrist `mae` in degrees per second.
- emg2pose is evaluated with the official `test_analysis` (one number per generalization type). Upstream bug: it reads
  `self.data_dir` before setting it; the wrapper sets it on the class, and keeps only the files present on disk.
- Path values in Hydra overrides are quoted, because Lightning checkpoint names contain `=`.
- Licences: emg2qwerty and emg2pose CC BY-NC-SA 4.0, GNI CC BY-NC 4.0; all are plain downloads with no terms to accept.
"""
import glob
import math
import os
import re
import shutil
import subprocess
import sys
import tarfile
import time
import urllib.request
from datetime import datetime, timezone

import pandas as pd
import torch

from common import NotApplicable, _safe, download, git_commit, log_error
from ecg import wanted

PHASE = "phase14"
GPU = torch.cuda.is_available()
S3 = "https://fb-ctrl-oss.s3.amazonaws.com"

# name: (GitHub repo, pinned commit, Python, pip pins from the repo's environment.yml, extra editable sub-packages)
REPOS = {
    "emg2qwerty": ("facebookresearch/emg2qwerty", "3200d91eeb952cbed1f278e47d0cc56928334fd1", "3.10", [
        "torch==2.3.0", "torchaudio==2.3.0", "pytorch-lightning==1.8.6", "torchmetrics==0.11.4", "lightning-bolts==0.7.0",
        "hydra-core==1.3.2", "hydra-submitit-launcher==1.2.0", "omegaconf==2.3.0", "h5py==3.11.0", "numpy==1.24.4",
        "pandas==2.0.3", "scipy==1.10.1", "python-levenshtein==0.25.1", "unidecode==1.3.8", "setuptools<70",
        "kenlm @ https://github.com/kpu/kenlm/archive/4cb443e60b7bf2c0ddf3c745378f76cb59e254e5.zip"], []),
    "emg2pose": ("facebookresearch/emg2pose", "5f6f62b1a0a08426adffe55900842e75a8adb38c", "3.10", [
        "torch==2.3.1", "pytorch-lightning==2.2.2", "numpy==1.26.4", "scipy==1.13.1", "h5py==3.11.0", "pandas==2.2.2",
        "hydra-core==1.3.2", "unidecode==1.3.8", "pyyaml==6.0.1", "tqdm", "joblib==1.4.2", "plotly==5.24.1",
        "matplotlib==3.9.2", "pillow==11.0.0", "opencv-python-headless==4.10.0.84", "setuptools<70"],
        ["emg2pose/UmeTrack"]),
    "gni": ("facebookresearch/generic-neuromotor-interface", "b6bf250e2be5a67b23488104335373cdb87a15c9", "3.12", [
        "torch==2.4.1", "pytorch-lightning==1.8.6", "numpy==1.26.4", "scipy==1.14.1", "h5py==3.12.1", "pandas==2.2.2",
        "hydra-core==1.3.2", "levenshtein==0.26.1", "python-levenshtein==0.26.1", "numba==0.60.0", "tables==3.10.2",
        "unidecode==1.3.8", "pyyaml==6.0.2", "click==8.1.8", "requests", "tqdm", "setuptools<70"], []),
}


# ------------------------------------------------------------------ shared plumbing

def untar_url(url, dest, need_free=True):
    """Stream a (gzipped) tar from url into dest without keeping the archive. Skips if already done."""
    flag = os.path.join(dest, ".untar_" + re.sub(r"\W", "_", url.rsplit("/", 1)[-1]))
    if os.path.exists(flag):
        return dest
    os.makedirs(dest, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "bci-roadmap-benchmarks"})
    with urllib.request.urlopen(req, timeout=120) as r:
        size, free = int(r.headers.get("Content-Length") or 0), shutil.disk_usage(dest).free
        if need_free and size and free < 1.05 * size:
            raise RuntimeError(f"{url} is {size / 1e9:.0f} GB but only {free / 1e9:.0f} GB are free in {dest}; "
                               "download it elsewhere and pass --path")
        if size > 5e9:
            print(f"      streaming {size / 1e9:.0f} GB from {url} (not resumable: an interrupted unpack restarts)")
        # ponytail: one sequential stream, no resume; fine below a few GB, a 300+ GB tar may prefer a manual download
        with tarfile.open(fileobj=r, mode="r|*") as t:
            t.extractall(dest, filter="data")
    open(flag, "w").close()
    return dest


def setup(root, name):
    """Fetch the repo at its pinned commit and build its own venv. Returns (repo_dir, python)."""
    repo, sha, pyver, pins, extra = REPOS[name]
    base = os.path.join(root, name)
    src = os.path.join(base, f"repo-{sha[:8]}")
    if not os.path.isdir(src):
        tmp = untar_url(f"https://github.com/{repo}/archive/{sha}.tar.gz", os.path.join(base, "src_tmp"))
        os.replace(glob.glob(os.path.join(tmp, "*-" + sha))[0], src)
        shutil.rmtree(tmp)
    venv, py = os.path.join(base, "venv"), os.path.join(base, "venv", "bin", "python")
    if not os.path.exists(os.path.join(venv, ".ok")):
        uv = shutil.which("uv")
        if not uv:
            subprocess.run([sys.executable, "-m", "pip", "install", "-q", "uv"], check=True)
            uv = os.path.join(os.path.dirname(sys.executable), "uv")
        print(f"      building the {name} environment (Python {pyver}) in {venv}")
        subprocess.run([uv, "venv", "-q", "--clear", "--python", pyver, venv], check=True)
        subprocess.run([uv, "pip", "install", "-q", "--python", py, *pins], check=True)
        subprocess.run([uv, "pip", "install", "-q", "--python", py, "--no-deps", "-e", src,
                        *[a for e in extra for a in ("-e", os.path.join(src, e))]], check=True)
        open(os.path.join(venv, ".ok"), "w").close()
    return src, py


FAILED = {}  # run folder -> error, so a failed shared run (e.g. the generic model) is not retried by every unit


def run_job(cmd, cwd, out):
    """Run one official command, logging to out/run.log. Finished runs (out/ok) are reused. Returns the log text."""
    log, ok = os.path.join(out, "run.log"), os.path.join(out, "ok")
    if out in FAILED:
        raise RuntimeError(FAILED[out])
    if not os.path.exists(ok):
        os.makedirs(out, exist_ok=True)
        print("      $ " + " ".join("<inline launcher>" if "\n" in c else c for c in cmd))
        with open(log, "w") as f:
            code = subprocess.run(cmd, cwd=cwd, stdout=f, stderr=subprocess.STDOUT,
                                  env={**os.environ, "PYTHONUNBUFFERED": "1", "HYDRA_FULL_ERROR": "1"}).returncode
        if code:
            tail = open(log).read().strip().replace("\n", " | ")
            FAILED[out] = f"exit {code}; see {log}; tail: {tail[-600:]}"
            raise RuntimeError(FAILED[out])
        open(ok, "w").close()
    return open(log).read()


def parse_metrics(text, key="test_metrics"):
    """Numbers in the last `'test_metrics': [{...}]` block that the official train scripts pprint at the end."""
    i = text.rfind(f"'{key}'")
    if i < 0:
        raise RuntimeError(f"no '{key}' in the run log")
    block = text[i:text.index("]", i)]
    return {k: float(v) for k, v in re.findall(r"'([^']+)':\s*([-+0-9.eE]+|nan|inf)", block)}


def best_ckpt(out):
    """The best checkpoint that Lightning's ModelCheckpoint (save_top_k=1) wrote under a run folder."""
    found = [p for p in glob.glob(os.path.join(out, "**", "*.ckpt"), recursive=True) if not p.endswith("last.ckpt")]
    if len(found) != 1:
        raise RuntimeError(f"expected one best checkpoint in {out}, found {len(found)}")
    return found[0]


def unit(phase, results, dataset, protocol, model, seed, args, fn):
    """Run fn() -> {fold: {metric: value}} for one (dataset, protocol, model, seed) and store its rows."""
    if args.models and model.split(" (")[0] not in args.models:
        return
    if results.is_done(dataset, protocol, model, seed):
        print(f"  = {dataset} | {protocol} | {model} | seed {seed}: done, skipping")
        return
    t0 = time.time()
    folds = fn()
    now, commit = datetime.now(timezone.utc).isoformat(timespec="seconds"), git_commit()
    rows = [dict(phase=phase, dataset=dataset, protocol=protocol, model=model, seed=seed, fold=fold, metric=m,
                 value=float(v), n_train=None, n_test=None, train_s=round(time.time() - t0, 1),
                 device="cuda" if GPU else "cpu", commit=commit, time=now)
            for fold, ms in folds.items() for m, v in ms.items()]
    results.add(rows)
    print(f"  + {dataset} | {protocol} | {model} | seed {seed}: " +
          ", ".join(f"{r['fold']} {r['metric']} {r['value']:.4f}" for r in rows[:6]) + (" ..." if len(rows) > 6 else ""))


def runs_for(args):
    """(seed, released?) pairs: the released checkpoints once, then one retraining per seed."""
    return [(0, True)] + [(s, False) for s in args.seeds]


# ------------------------------------------------------------------ emg2qwerty

QWERTY_DATA = f"{S3}/emg2qwerty/emg2qwerty-data-2021-08.tar.gz"
QWERTY_PROTOCOLS = {"generic": "generic.ckpt", "personalized_finetuned": "personalized-finetuned/{u}.ckpt",
                    "personalized_randominit": "personalized-randominit/{u}.ckpt"}
QWERTY_DECODERS = {"TDSConvCTC": "ctc_greedy", "TDSConvCTC+LM": "ctc_beam"}


def qwerty_released(root, rel):
    """Released checkpoints live in Git LFS; fetch them from GitHub's media endpoint (no git-lfs needed)."""
    repo, sha = REPOS["emg2qwerty"][:2]
    return download(f"https://media.githubusercontent.com/media/{repo}/{sha}/models/{rel}",
                    os.path.join(root, "emg2qwerty", "released", rel), quiet=True)


def qwerty_commands(py, data, seed, quick):
    """Common arguments of every emg2qwerty.train call (README: Training / Testing)."""
    base = [py, "-m", "emg2qwerty.train", f"dataset.root='{data}'", f"trainer.accelerator={'gpu' if GPU else 'cpu'}",
            "trainer.devices=1", f"seed={seed}"]
    return base + (["trainer.max_epochs=1", "++trainer.limit_train_batches=5", "++trainer.limit_val_batches=5"]
                   if quick else [])


def run_emg2qwerty(results, args, root):
    data = args.paths.get("emg2qwerty") or os.path.join(root, "emg2qwerty", "data", "emg2qwerty-data-2021-08")
    if not os.path.exists(os.path.join(data, "metadata.csv")):
        if args.quick:
            print("  - emg2qwerty: skipped in --quick (no small subset; the only download is a 308 GB tar.gz). "
                  "Pass --path emg2qwerty=FOLDER to run it on existing data.")
            return
        untar_url(QWERTY_DATA, os.path.join(root, "emg2qwerty", "data"))
    repo, py = setup(root, "emg2qwerty")
    users = ["user0"] if args.quick else [f"user{i}" for i in range(8)]
    runs = os.path.join(root, "emg2qwerty", "quick_runs" if args.quick else "runs")

    def job(tag, *extra, seed=0):
        out = os.path.join(runs, tag)
        return out, run_job(qwerty_commands(py, data, seed, args.quick) + [*extra, f"hydra.run.dir='{out}'"], repo, out)

    def ckpt(protocol, u, seed, released):
        if released:
            return qwerty_released(root, QWERTY_PROTOCOLS[protocol].format(u=u))
        if protocol != "personalized_randominit":
            generic = best_ckpt(job(f"s{seed}/generic/train", "user=generic", seed=seed)[0])
            if protocol == "generic":
                return generic
        init = [f"checkpoint='{generic}'"] if protocol == "personalized_finetuned" else []
        return best_ckpt(job(f"s{seed}/{protocol}/{u}/train", f"user={u}", *init, seed=seed)[0])

    def test(protocol, decoder, seed, released):
        tag = "released" if released else f"s{seed}"
        return {u: {"cer": parse_metrics(job(f"{tag}/{protocol}/{u}/test_{decoder}", f"user={u}",
                                             f"checkpoint='{ckpt(protocol, u, seed, released)}'", "train=False",
                                             f"decoder={decoder}", seed=seed)[1])["test/CER"] / 100}
                for u in users}

    for seed, released in runs_for(args):
        for protocol in QWERTY_PROTOCOLS:
            for model, decoder in QWERTY_DECODERS.items():
                name = model + (" (released)" if released else "")
                _safe(unit, PHASE, results, "emg2qwerty", protocol, name, seed, args,
                      lambda: test(protocol, decoder, seed, released))


# ------------------------------------------------------------------ emg2pose

POSE_EXPERIMENTS = {"vemg2pose": "regression_vemg2pose", "NeuroPose": "regression_neuropose"}
POSE_SPLITS = {"heldout_user": "user", "heldout_stage": "stage", "heldout_user_stage": "user_stage"}
# Official test_analysis CLI, with its data_dir bug patched and the corpus limited to files on disk.
# argv: data folder, quick flag, then hydra arguments. The mini dataset holds only validation-split files (one user),
# so --quick lets them stand in for the test split: a smoke test of the code path, not a result.
POSE_EVAL = """import os, sys
import emg2pose.test_analysis as t
E, data, quick = t.EMG2PoseEvaluation, sys.argv.pop(1), sys.argv.pop(1) == "quick"
E.data_dir = data  # upstream: get_corpus_df() reads self.data_dir before __post_init__ sets it
read = t.pd.read_csv
t.pd.read_csv = lambda *a, **k: (lambda d: d.assign(split=d.split.replace("val", "test")) if quick and "split" in d else d)(read(*a, **k))
corpus = E.get_corpus_df
E.get_corpus_df = lambda self: (lambda d: d[[os.path.exists(os.path.join(data, f + ".hdf5")) for f in d.filename]])(corpus(self))
t.cli()
"""


def run_emg2pose(results, args, root):
    base = os.path.join(root, "emg2pose")
    data = args.paths.get("emg2pose")
    if not data:
        name = "emg2pose_dataset_mini" if args.quick else "emg2pose_dataset"
        untar_url(f"{S3}/emg2pose/{name}.tar", os.path.join(base, "data"))
        data = os.path.join(base, "data", name)
    repo, py = setup(root, "emg2pose")
    released_dir = os.path.join(untar_url(f"{S3}/emg2pose/emg2pose_model_checkpoints.tar.gz", base),
                                "emg2pose_model_checkpoints")
    runs = os.path.join(base, "quick_runs" if args.quick else "runs")
    acc = f"++trainer.accelerator={'gpu' if GPU else 'cpu'}"

    def evaluate_all(model, seed, released):
        """Official test_analysis over the test split; one row per generalization type."""
        exp, tag = POSE_EXPERIMENTS[model], "released" if released else f"s{seed}"
        if released:
            ck = os.path.join(released_dir, f"{exp}.ckpt")
        else:
            out = os.path.join(runs, f"{tag}/{model}/train")
            run_job([py, "-m", "emg2pose.train", "train=True", "eval=False", f"experiment={exp}", f"data_location='{data}'",
                     f"seed={seed}", acc, f"hydra.run.dir='{out}'"] +
                    (["trainer.max_epochs=1", "data_split=mini_split"] if args.quick else []), repo, out)
            ck = best_ckpt(out)
        out = os.path.join(runs, f"{tag}/{model}/test")
        run_job([py, "-c", POSE_EVAL, data, "quick" if args.quick else "full", f"--config-path={repo}/config",
                 f"data_location='{data}'", f"experiment={exp}", f"checkpoint='{ck}'", acc,
                 f"hydra.run.dir='{out}'"], repo, out)
        return pd.read_csv(os.path.join(out, "results.csv"))

    def scores(model, protocol, seed, released):
        df = evaluate_all(model, seed, released)  # cached after the first protocol
        r = df[df.generalization == POSE_SPLITS[protocol]]
        if r.empty:
            raise NotApplicable(f"no test files of generalization '{POSE_SPLITS[protocol]}' on disk")
        r = r.iloc[0]
        return {"all": {"angle_error": math.degrees(r.test_mae), "landmark_error": r.test_landmark_distance,
                        "fingertip_error": r.test_fingertip_distance}}

    for seed, released in runs_for(args):
        for model in POSE_EXPERIMENTS:
            for protocol in POSE_SPLITS:
                _safe(unit, PHASE, results, "emg2pose", protocol, model + (" (released)" if released else ""), seed,
                      args, lambda: scores(model, protocol, seed, released))


# ------------------------------------------------------------------ Generic Neuromotor Interface

GNI_TASKS = {  # task: (model name, official test metric, our metric, scale)
    "discrete_gestures": ("DiscreteGesturesNet", "test_cler", "cler", 1.0),
    "handwriting": ("HandwritingConformer", "test/CER", "cer", 0.01),
    "wrist": ("WristNet", "test_mae_deg_per_sec", "mae", 1.0),
}
# Evaluate a released checkpoint the way the repo's integration test does (train.evaluate_from_checkpoint).
GNI_EVAL = """import glob, sys
from omegaconf import OmegaConf
from generic_neuromotor_interface.train import evaluate_from_checkpoint
model_dir, data, split, acc = sys.argv[1:5]
c = OmegaConf.load(model_dir + '/model_config.yaml')
c.data_location = c.data_module.data_location = data
c.trainer.accelerator = acc
if split != 'official':
    c.data_module.data_split = OmegaConf.load(split)
r = evaluate_from_checkpoint(c, glob.glob(model_dir + '/*.ckpt')[0], evaluate_validation_set=False)
print({'test_metrics': r['test_metrics']})
"""


def run_gni(results, args, root, task):
    dataset = f"GNI_{task}"
    model, key, metric, scale = GNI_TASKS[task]
    base = os.path.join(root, "gni")
    repo, py = setup(root, "gni")
    data = args.paths.get(dataset)
    if not data:
        data = os.path.join(base, "data_small" if args.quick else "data_full")
        run_job([py, "-m", "generic_neuromotor_interface.scripts.download_data", "--task", task, "--output-dir", data]
                + (["--small-subset"] if args.quick else []), repo, os.path.join(base, "logs", f"download_{task}_{args.quick}"))
    models = os.path.join(base, "models")
    run_job([py, "-m", "generic_neuromotor_interface.scripts.download_models", "--task", task, "--output-dir", models],
            repo, os.path.join(base, "logs", f"download_model_{task}"))
    model_dir = os.path.dirname(glob.glob(os.path.join(models, "**", task, "model_config.yaml"), recursive=True)[0])
    runs = os.path.join(base, "quick_runs" if args.quick else "runs", task)
    acc = "gpu" if GPU else "cpu"
    split = os.path.join(repo, "config", "data_module", "data_split", f"{task}_mini_split.yaml")

    def scores(seed, released):
        if released:
            out = os.path.join(runs, "released")
            text = run_job([py, "-c", GNI_EVAL, model_dir, data, split if args.quick else "official", acc], repo, out)
        else:
            out = os.path.join(runs, f"s{seed}")
            text = run_job([py, "-m", "generic_neuromotor_interface.train", f"--config-name={task}",
                            f"data_location='{data}'", f"seed={seed}", f"trainer.accelerator={acc}",
                            f"hydra.run.dir='{out}'"] +
                           ([f"data_module/data_split={task}_mini_split", "trainer.max_epochs=1"] if args.quick else []),
                           repo, out)
        return {"test": {metric: parse_metrics(text)[key] * scale}}

    for seed, released in runs_for(args):
        _safe(unit, PHASE, results, dataset, "standard", model + (" (released)" if released else ""), seed, args,
              lambda: scores(seed, released))


# ------------------------------------------------------------------ runner

def run(results, args):
    root = os.path.join(args.data_dir, "external")
    jobs = [("emg2qwerty", run_emg2qwerty, ()), ("emg2pose", run_emg2pose, ())]
    jobs += [(f"GNI_{t}", run_gni, (t,)) for t in GNI_TASKS]
    for name, fn, extra in jobs:
        if not wanted(args, name, *(["GNI"] if name.startswith("GNI") else [])):
            continue
        print(f"\n[{PHASE}] {name}")
        try:
            fn(results, args, root, *extra)
        except Exception as e:
            log_error(PHASE, f"{name}: could not set up ({type(e).__name__}: {e})")
