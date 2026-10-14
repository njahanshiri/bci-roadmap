# Benchmarks

Scripts that run baselines and state-of-the-art models on open BCI and biosignal datasets, then compare the results with published numbers. This implements the plan in [../BENCHMARK_PLAN.md](../BENCHMARK_PLAN.md).

## Run everything

```bash
./benchmarks/run_all.sh --quick   # 1. smoke test: 2 subjects, 2 epochs, 1 seed (small downloads)
./benchmarks/run_all.sh           # 2. full run on the GPU
```

`run_all.sh` creates `benchmarks/.venv`, installs [requirements.txt](requirements.txt), checks for a GPU, runs all five phases in order with [main.py](main.py), writes a log to `results/`, and finishes with the comparison report.

- **Resumable:** results are saved after every (dataset, protocol, model, seed) unit. Stop and rerun the same command, and finished units are skipped.
- **Errors don't stop the run:** a failing dataset or model is logged to `results/errors.log` and the run moves on.
- **Options** (passed through to `main.py`):

| Option | Default | Meaning |
|---|---|---|
| `--phases 1 2 …` | all | Which phases to run |
| `--datasets …` / `--models …` | all | Restrict to some dataset or model names |
| `--seeds 0 1 2` | 0 1 2 | Seeds for deep models (classical models run once) |
| `--epochs` | 300 | Epochs for EEG deep models (EMG, sleep and ECG models are capped lower) |
| `--foundation-epochs` | 50 | Fine-tuning epochs for LaBraM, CBraMod, EEGPT |
| `--batch-size` | 64 | Batch size for EEG deep models |
| `--data-dir` | `~/bci_data` | Where datasets are downloaded |
| `--tuab-path` | none | Local TUAB v3.0.1 folder; TUAB is skipped without it (needs TUH access) |
| `--tuab-windows` | 12 | 10-s windows kept per TUAB recording (memory) |

Set `TORCH_INDEX_URL` before the first run if you need a specific CUDA build of PyTorch.

## What runs

| Phase | Datasets | Protocols | Models |
|---|---|---|---|
| 1. EEG motor imagery | BCI IV 2a, BCI IV 2b, High-Gamma, PhysioNet MI, Lee 2019 MI, Cho 2017 | `standard` (official train/test), `cross_subject`, plus `cross_session` (Lee), `within_session:5` (Cho), fixed subject split (PhysioNet) | CSP+LDA, TS+LR, MDM; EEGNet, ShallowConvNet, DeepConvNet, EEG-TCNet, ATCNet, EEGConformer, TCFormer |
| 2. EMG | Ninapro DB5 (41 classes, both Myos), GRABMyo (28 ch, 3 days) | DB5: repetitions 2, 5 held out; cross-subject. GRABMyo: trials 6–7 held out; day 3 held out; cross-subject (classical only) | Hudgins features + LDA / random forest; ResNet1D |
| 3. EEG SSVEP and P300 | Nakanishi 2015, Tsinghua Benchmark (Wang 2016), Lee 2019 SSVEP; BNCI2014-009, Brain Invaders 2013a, Lee 2019 ERP | within-session k-fold; `standard` (Lee) | CCA, TRCA, EEGNet (SSVEP); XDAWN+LDA, XDAWNCov+MDM, XDAWNCov+TS+SVM, EEGNet, EEGInceptionERP (P300) |
| 4. EEG foundation models | BCI IV 2a, 2b, PhysioNet MI; TUAB if `--tuab-path` | as in phase 1; TUAB official train/eval | LaBraM, CBraMod, EEGPT, fine-tuned from their pretrained weights |
| 5. Other data types | Sleep-EDF-20 (EEG, EOG, EEG+EOG), PTB-XL (5 superclasses) | 20-fold subject-wise CV; PTB-XL folds 1–8 train, 10 test | Band power + RF, SleepStagerChambon2018, DeepSleepNet, AttnSleep; ResNet1D, DeepConvNet, ShallowConvNet |

Datasets download automatically on first use: EEG through MOABB, Ninapro DB5 from the Ninapro site, GRABMyo (9.8 GB zip) and PTB-XL (1.8 GB zip) from PhysioNet, Sleep-EDF through MNE. Several MOABB datasets (High-Gamma, Lee 2019, Cho 2017, Wang 2016) are large, so put `--data-dir` on a big disk.

## Outputs

| File | Contents |
|---|---|
| `results/benchmark.csv` | One row per (dataset, protocol, model, seed, fold, metric), with training time, device and git commit |
| `results/benchmark_summary.md` | Per-dataset tables (mean ± std over seeds) and the comparison with published results |
| `results/benchmark_summary.csv` | The comparison table as CSV |
| `results/errors.log` | Anything that failed, with the reason |

Regenerate the report at any time with `python benchmarks/report.py results/benchmark.csv results/benchmark_summary.md`.

## How results are compared

[sota.csv](sota.csv) holds 75 published results, all taken from the audited `DATASETS.md` files in `projects/`. A published number is compared only when the dataset, protocol and metric match. The report marks each comparison as **within CI**, **above SOTA** or **below SOTA**, using a 95% bootstrap confidence interval over folds (usually subjects). The `sota_flags` column carries known caveats, for example a paper that selected its best epoch on the test set, used data augmentation, or reported a linear probe.

## Design choices (and their limits)

- **No test-set influence.** Deep models train for a fixed number of epochs and the last epoch is evaluated. No early stopping, no checkpoint selection, no per-subject tuning. Some published numbers did select on the test set; those rows are flagged.
- **Fitted only on training data.** Per-channel standardization statistics come from the training set of each fold.
- **One setting per model,** taken from braindecode and paper defaults, with no hyperparameter search. Published numbers often used tuned settings or augmentation, so a gap below SOTA is expected for some models.
- **Known protocol differences** (also in `sota_flags`):
  - Nakanishi 2015 uses stratified 15-fold CV, because MOABB metadata has no block labels (the paper uses leave-one-block-out).
  - Sleep models classify single 30-s epochs; the published leaders are sequence models.
  - TUAB uses 21 referential channels and only the first `--tuab-windows` windows per recording after the first minute; published results use all windows.
  - High-Gamma is filtered at 4–120 Hz at 250 Hz (paper: 4–125 Hz).
- **Not included yet:** TUSZ, TUEV, CHB-MIT, SEED, DEAP (access requests or seizure-scoring tools needed), emg2qwerty and emg2pose (use their official repos), MEG, ECoG and spikes benchmarks (use their official leaderboards: LibriBrain, Neuroprobe, NLB, FALCON).
