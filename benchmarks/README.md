# Benchmarks

Scripts that run baselines and state-of-the-art models on the open datasets catalogued in this repo (EEG, EMG, EOG, ECG, fNIRS, MEG, ECoG/sEEG, spikes/LFP), then compare the results with 789 published numbers. This implements the plan in [../BENCHMARK_PLAN.md](../BENCHMARK_PLAN.md).

## Run everything

```bash
./benchmarks/run_all.sh --quick   # 1. smoke test: a few subjects, 2 epochs, 1 seed
./benchmarks/run_all.sh           # 2. full run on the GPU (read "Disk and time" first)
```

`run_all.sh` creates `benchmarks/.venv`, installs [requirements.txt](requirements.txt) and [requirements-nodeps.txt](requirements-nodeps.txt), checks for a GPU, runs phases 1–14 in order with [main.py](main.py), logs to `results/`, and finishes with the comparison report.

- **Resumable:** results are saved after every (dataset, protocol, model, seed) unit. Rerun the same command and finished units are skipped.
- **Errors don't stop the run:** a failing dataset, model or whole phase is logged to `results/errors.log` and the run moves on.
- **Pick what to run:** `--phases 1 2 9`, `--datasets BNCI2014_001 PTB-XL`, `--models EEGNet ResNet1D`.

| Option | Default | Meaning |
|---|---|---|
| `--phases …` | 1–14 | Which phases to run |
| `--datasets …` / `--models …` | all | Restrict to some dataset or model names |
| `--seeds …` | 0 1 2 | Seeds for deep models (classical models run once) |
| `--epochs` | 300 | Epochs for EEG deep models (other modules cap this lower) |
| `--foundation-epochs` | 50 | Fine-tuning epochs for LaBraM, CBraMod, EEGPT |
| `--batch-size` | 64 | Batch size for EEG deep models |
| `--data-dir` | `~/bci_data` | Where datasets are downloaded and cached |
| `--path NAME=FOLDER` | none | Local folder for an access-gated dataset (repeatable) |
| `--tuab-path`, `--tuab-windows` | none, 12 | TUAB folder; 10-s windows kept per recording |
| `--accept-licenses` | off | Accept dataset licences that require explicit consent (currently: Brainstorm auditory) |

Set `TORCH_INDEX_URL` before the first run if you need a specific CUDA build of PyTorch.

## Phases

| Phase | Module | Data type | Datasets |
|---|---|---|---|
| 1 | [eeg.py](eeg.py) | EEG motor imagery | BCI IV 2a, 2b, High-Gamma, PhysioNet MI, Lee 2019 MI, Cho 2017 |
| 2 | [emg.py](emg.py) | EMG | Ninapro DB5, GRABMyo |
| 3 | [eeg.py](eeg.py) | EEG SSVEP, P300 | Nakanishi 2015, Tsinghua Benchmark, Lee 2019 SSVEP; BNCI2014-009, BI2013a, Lee 2019 ERP |
| 4 | [eeg.py](eeg.py) | EEG foundation models | LaBraM, CBraMod, EEGPT on BCI IV 2a/2b and PhysioNet MI; TUAB (gated) |
| 5 | [other.py](other.py) | Sleep, ECG | Sleep-EDF-20 (EEG, EOG, EEG+EOG), PTB-XL superdiagnostic |
| 6 | [eeg_more.py](eeg_more.py) | More EEG | BETA, BCI III IVa/IIIa, CHB-MIT, Siena, Bonn (sanity), HBN-EEG challenge, KU Leuven AAD, Thinking Out Loud, Kara One, WAY-EEG-GAL; gated: TUSZ, TUEV, TUAR, SEED/-IV/-V, DEAP, DREAMER, EEGEyeNet, Kaggle ErrP, Kaggle HMS |
| 7 | [emg_more.py](emg_more.py) | More EMG | Ninapro DB1, DB2, DB3, DB7, CapgMyo DB-a, Hyser, EMG-EPN-612, putEMG; gated: CapgMyo DB-b/DB-c, CSL-HDEMG |
| 8 | [eog.py](eog.py) | EOG | Sleep-EDF-78, EEGdenoiseNet, Klados 2016, Bulling activity; gated: ISRUC, SHHS, MASS, SEED-VIG, DEAP EOG |
| 9 | [ecg.py](ecg.py) | ECG | MIT-BIH (inter- and intra-patient), INCART, PTB, PTB-XL (5 more tasks), CinC 2017, CinC 2021 collection, CODE-15% → CODE-test, Chagas 2025, Apnea-ECG, WESAD; gated: MIMIC-IV-ECG, Harvard-Emory |
| 10 | [fnirs.py](fnirs.py) | fNIRS | Shin 2017 A/B (fNIRS and hybrid), Shin 2018, Bak 2019, Tufts fNIRS2MW, MNE-NIRS tapping, FRESH I/II, Ning 2024, Kernel Flow2, WashU HD-DOT, OpenNeuro fNIRS sets |
| 11 | [meg.py](meg.py) | MEG | MNE sample/somato, Brainstorm auditory (licence), Wakeman & Henson, BCI IV ds3, MEG-MASC, THINGS-MEG, LibriBrain, emotion videos; gated: Cam-CAN, MOUS, HCP, OMEGA, Armeni, Brain2Qwerty |
| 12 | [ecog.py](ecog.py) | ECoG / sEEG | BCI IV ds4, Miller finger flexion, Brain Treebank (Neuroprobe), Berezutskaya, Podcast, Chen 2024, Verwoert, Mayo/FNUSA, HUP, SWEC-ETHZ, Bellier; gated: Kaggle seizure sets, RAM |
| 13 | [spikes.py](spikes.py) | Spikes / LFP | Neural Latents Benchmark (7 sets), FALCON (5 tasks), O'Doherty, Churchland maze, Allen, IBL, Steinmetz; gated: Brain-to-Text '24/'25, Willett handwriting, CRCNS |
| 14 | [external.py](external.py) | Official pipelines | emg2qwerty, emg2pose, Meta Generic Neuromotor Interface (each in its own environment, at a pinned commit) |

Each module's docstring has the full coverage table: how every dataset is obtained, its protocols, models, and what was tested.

## Access-gated datasets

These need registration, a data-use agreement or a login. Request access, download them yourself, then pass the folder:

```bash
./benchmarks/run_all.sh --path seed=/data/SEED --path tusz=/data/tuh/tusz --tuab-path /data/tuh/tuab
```

| Data type | `--path` keys |
|---|---|
| EEG | `tuab` (or `--tuab-path`), `tusz`, `tuev`, `tuar`, `seed`, `seed_iv`, `seed_v`, `deap`, `dreamer`, `eegeyenet`, `kaggle_errp`, `kaggle_hms` |
| EMG | `capgmyo_dbb`, `capgmyo_dbc`, `csl_hdemg`; optional local copies: `emg2qwerty`, `emg2pose`, `GNI_discrete_gestures`, `GNI_handwriting`, `GNI_wrist` |
| EOG / sleep | `isruc`, `shhs`, `mass`, `seed_vig`, `deap`, `jins_driving` |
| ECG | `mimic_iv_ecg`, `heedb` |
| fNIRS | optional local copy: `tufts` |
| MEG | `camcan`, `mous`, `hcp_meg`, `omega`, `armeni`, `brain2qwerty` |
| ECoG / sEEG | `kaggle_aes2014`, `kaggle_upenn_mayo`, `kaggle_melbourne`, `ram`; optional: `braintreebank` |
| Spikes | `b2t24`, `b2t25`, `handwriting`, `crcns_pvc-8`, `crcns_pvc-11` |

Without a folder, these datasets are skipped with a printed message.

## Disk and time

A full run downloads well over 1 TB and takes days on one GPU. Some of the largest automatic downloads:

| Dataset | Size |
|---|---|
| emg2pose (phase 14) | 463 GB |
| emg2qwerty (phase 14) | 308 GB (only with enough free disk) |
| THINGS-MEG (phase 11) | about 255 GB |
| Meta Generic Neuromotor Interface (phase 14) | 33 + 75 + 49 GB |
| CODE-15% (phase 9) | about 46 GB |
| ds007738 fNIRS (phase 10) | about 38 GB |
| LibriBrain phoneme cache (phase 11) | about 34 GB |
| Hyser (phase 7) | about 19 GB |
| Kernel Flow2, streamed (phase 10) | about 11 GB |
| GRABMyo (phase 2) | 9.8 GB |

Put `--data-dir` on a large disk, and consider running phases or datasets in groups (for example `--phases 1 2 3 5`, then the rest).

## Outputs

| File | Contents |
|---|---|
| `results/benchmark.csv` | One row per (dataset, protocol, model, seed, fold, metric), with training time, device and git commit |
| `results/benchmark_summary.md` | Per-dataset tables (mean ± std over seeds) and the comparison with published results |
| `results/benchmark_summary.csv` | The comparison table as CSV |
| `results/errors.log` | Anything that failed, with the reason |

Regenerate the report any time: `python benchmarks/report.py results/benchmark.csv results/benchmark_summary.md`.

## How results are compared

[sota.csv](sota.csv) and [sota/](sota/) hold 789 published results, all taken from the audited `DATASETS.md` files in `projects/`. A published number is compared only when the dataset, protocol and metric match. Each comparison is marked **within CI**, **better than SOTA** or **worse than SOTA**, using a 95% bootstrap confidence interval over folds; for error metrics (RMSE, MAE, CER, WER, angle error, …) lower is better. The `sota_flags` column lists known caveats: test-set model selection, augmentation, linear probing, hidden test sets we can't access (we use public validation or cross-validation instead), different window lengths, and so on. Read it before drawing conclusions.

## Design choices and limits

- **No test-set influence:** deep models train for a fixed number of epochs and the last epoch is evaluated (the official pipelines in phase 14 use their own validation-based selection). No early stopping on test data and no per-subject tuning.
- **Fitted only on training data:** standardization statistics come from each fold's training set.
- **One setting per model,** from braindecode and paper defaults, with no hyperparameter search. A gap below published numbers is expected for some models.
- **Hidden test sets:** many challenges (PhysioNet/CinC, NLB, FALCON, Brain-to-Text, LibriBrain, Kaggle) keep their test labels private. We evaluate on public validation splits or cross-validation and flag those comparisons.
- **What was tested before release:** phases 6–14 each ran end to end in quick mode on CPU; phases 1–5 were tested piece by piece (all phase-1 models on BCI IV 2a/2b, P300 and SSVEP pipelines, Ninapro DB5, GRABMyo windowing, Sleep-EDF epoching, foundation-model weight loading, the report). Open datasets were tested on real data (small subsets). Most gated datasets were tested only on synthetic files in their documented formats, because we had no access. Full-size runs and GPU runs were not done here.
- **Not included:** THINGS-EEG (a fair baseline needs an image model), the ALS locked-in EEG/EOG set and JINS MEME (no usable labels or files), Herff 2014 fNIRS (e-mail registration), GPFA for NLB (needs `elephant`).
