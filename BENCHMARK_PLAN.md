# Benchmark plan

A plan for running baselines and state-of-the-art models on the open datasets catalogued in this repo, and comparing the results honestly with published state-of-the-art (SOTA) numbers.

Order of work: **EEG and EMG first** (they have the most datasets and published results), then the other data types, most of which already have public leaderboards to plug into.

## 1. Goals

1. **Reproduce.** On each dataset, re-run the published SOTA and strong baselines using the dataset's own standard protocol, and check whether the published numbers hold.
2. **Compare fairly.** Re-evaluate every model under one shared, leakage-free protocol per data type, so results become comparable across papers and datasets.
3. **Publish.** One results table per dataset, one leaderboard per data type, and a short report of which SOTA claims reproduced and which didn't.

Not a goal: inventing new models. That comes after there is a trustworthy baseline to beat.

## 2. Principles

- **Reuse, don't rebuild.** MOABB already benchmarks BCI EEG pipelines; Braindecode provides the standard deep EEG models; most foundation models and leaderboards ship their own data loaders and scorers. This repo adds configs, glue scripts and results, not a new framework.
- **Same protocol, same metric, or no comparison.** A number goes next to a published SOTA only when the split, class set, input and metric match. Everything else is labelled "not directly comparable", as in the `DATASETS.md` files.
- **Leakage-free by default** (checklist in §7).
- **Report variance.** At least 3 seeds per model, results per subject, and mean ± std. No cherry-picked best runs.
- **Everything versioned.** Dataset version, preprocessing config, code commit and seed are saved with every result.

## 3. Datasets, by phase

Full specifications and the published results for every dataset are in each data type's `DATASETS.md`. "Access" notes what you need before downloading.

### Phase 1: EEG motor imagery and execution

| Dataset | Task | Standard protocol | Main metric | Access |
|---|---|---|---|---|
| BCI Competition IV 2a | 4-class MI, 9 subjects | Train session T, test session E | Accuracy, kappa | Open (via MOABB) |
| BCI Competition IV 2b | 2-class MI, 9 subjects | Sessions 1–3 train, 4–5 test | Accuracy, kappa | Open (via MOABB) |
| High-Gamma Dataset | 4-class motor execution, 14 subjects | Fixed train/test per subject | Accuracy | Open |
| PhysioNet Motor Movement/Imagery | ME + MI, 109 subjects | Cross-subject (no single standard) | Accuracy | Open |
| Lee 2019 (OpenBMI), MI part | 2-class MI, 54 subjects | Session 1 → session 2; cross-subject | Accuracy | Open |
| Cho 2017 | 2-class MI, 52 subjects | Within-subject CV | Accuracy | Open |
| BCI Competition III IVa, IIIa | MI, 5 and 3 subjects | Competition splits | Accuracy, kappa | Open |

### Phase 2: EMG gestures, typing and pose

| Dataset | Task | Standard protocol | Main metric | Access |
|---|---|---|---|---|
| Ninapro DB5 | 52+ gestures, Myo armband, 10 subjects | Repetition split (see the three DB5 tables) | Accuracy | Ninapro site (license not stated) |
| Ninapro DB1, DB2 | 52 / 49 gestures, 27 / 40 subjects | Repetitions 2, 5 test | Accuracy | CC0 (Dryad copy) |
| Ninapro DB3 | Amputees, 11 subjects | Repetitions 2, 5 test | Accuracy | CC0 (Dryad copy) |
| CapgMyo DB-a/b/c | HD-EMG, 8–12 gestures | Du et al. 2017 protocols | Accuracy | figshare copy CC0 |
| GRABMyo | 16 gestures, 43 subjects, 3 days | Cross-day | Accuracy | CC BY 4.0 |
| Hyser | HD-EMG, 34 gestures + finger force, 20 subjects | Within-session leave-one-out | Accuracy, force error | ODC-By 1.0 |
| EMG-EPN-612 | 5 gestures, 612 users | Official train/test users | Accuracy | CC BY 4.0 |
| putEMG | 7 gestures, 44 subjects | Per-subject 3-fold over trials | Accuracy | CC BY-NC 4.0 |
| emg2qwerty | Typing, 108 users | 8 held-out test users | Character error rate | CC BY-NC-SA 4.0 |
| emg2pose | Hand pose, 193 users | Held-out users and stages | Angle / landmark error | CC BY-NC-SA 4.0 |
| Meta Generic Neuromotor Interface | Gestures, handwriting, wrist | Repo splits | Task-specific | CC BY-NC 4.0 |

### Phase 3: Other EEG BCI paradigms

| Dataset | Task | Main metric |
|---|---|---|
| Tsinghua SSVEP Benchmark, BETA, Nakanishi 2015 | 40 / 40 / 12-target SSVEP | Accuracy and ITR at fixed data lengths |
| Lee 2019 ERP + SSVEP parts | Speller, 4-target SSVEP | Accuracy |
| BNCI2014-009, Brain Invaders 2013a, BCI III P300 | P300 | AUC / character accuracy |
| Kaggle BCI Challenge (ErrP) | Error potentials, 16 train / 10 test subjects | AUC |
| WAY-EEG-GAL (Grasp-and-Lift) | 6 movement events | Mean AUC |
| Thinking Out Loud, Kara One | Imagined speech | Accuracy (no strong standard yet) |

### Phase 4: Large-scale EEG and EEG foundation models

| Dataset | Task | Main metric | Access |
|---|---|---|---|
| TUAB | Normal vs abnormal | Balanced accuracy, AUROC, AUPR | Free TUH request form |
| TUEV | 6 event classes | Balanced accuracy, weighted F1, kappa | Same |
| TUSZ | Seizure detection | Event sensitivity and false alarms/24 h (state the scoring method) | Same |
| CHB-MIT, Siena | Seizure detection | Sensitivity, false positives/h (patient-specific vs cross-patient kept apart) | Open |
| SEED, SEED-IV, SEED-V | Emotion | Accuracy, subject-dependent vs subject-independent | Application + license |
| DEAP, DREAMER | Emotion | Accuracy (only trial-disjoint splits count) | EULA / request |
| HMS (Kaggle 2024) | Harmful brain activity | KL divergence | Kaggle rules |
| HBN-EEG | NeurIPS 2025 EEG Foundation Challenge tasks | Challenge metrics | CC BY-SA 4.0 |

Bonn is used only as a sanity check: its segments are not clinically realistic (see its block in `eeg/DATASETS.md`).

### Phase 5: The other data types (plug into existing scorers)

| Data type | Datasets with a standard scorer or leaderboard |
|---|---|
| EOG / sleep | Sleep-EDF-20 and -78 (subject-wise CV), SEED-VIG (cross-subject only), EEGdenoiseNet |
| ECG | PTB-XL (Strodthoff benchmark, folds 1–8/9/10), MIT-BIH inter-patient (DS1→DS2), CinC 2017/2020/2021, CPSC 2018, CODE-test, Apnea-ECG |
| fNIRS | Shin 2017 (MI, MA), Shin 2018, Bak 2019, fNIRS2MW |
| MEG | MOUS / MEG-MASC speech decoding, LibriBrain tracks, THINGS-MEG retrieval, Cam-CAN brain age |
| ECoG / sEEG | BCI IV dataset 4 (finger flexion), Brain Treebank / Neuroprobe, Kaggle seizure sets, Mayo/FNUSA |
| Spikes / LFP | Neural Latents Benchmark, FALCON, Brain-to-Text '24/'25 |

For these, the job is mostly running the official baselines and scorer, then adding one or two models of your own.

## 4. Two evaluation tracks

**Track A: Reproduce the paper.** Use exactly the dataset's standard protocol and metric, as recorded in its `DATASETS.md` table. Compare with every published row in the same table.

**Track B: Unified protocol.** One protocol per data type, applied to every dataset and model:

| Data type | Unified protocol |
|---|---|
| EEG (BCI) | (1) Within-subject, cross-session. (2) Cross-subject, leave-one-subject-out or a fixed held-out subject set. Preprocessing: band-pass, resample to a common rate, channel set fixed per dataset. Normalization fitted on training data only. |
| EEG (clinical) | Official train/eval split; validation subjects drawn from training subjects; one channel montage per comparison, stated in the table. |
| EMG | (1) Within-subject, held-out repetitions. (2) Cross-subject, held-out users. (3) Cross-day where available. Windows never span train and test repetitions. |
| Others | The official benchmark split (Phase 5 scorers already enforce it). |

Track B is where the honest comparison happens. Most papers report Track A only, and the gap between the two is often the most interesting result.

## 5. Model ladder

Every dataset gets the same ladder, from cheapest to most expensive. Stop climbing when the results stop changing what you'd conclude.

| Level | EEG | EMG |
|---|---|---|
| 1. Chance and trivial | Permutation chance level; majority class | Same |
| 2. Classical | CSP + LDA, FBCSP, Riemannian MDM and tangent space + LR (MOABB pipelines); xDAWN for P300; CCA / FBCCA / TRCA for SSVEP | Hudgins features (MAV, WL, ZC, SSC) + LDA / SVM / random forest (LibEMG) |
| 3. Compact deep | ShallowConvNet, DeepConvNet, EEGNet, EEG-TCNet (Braindecode) | 1D CNN on raw windows; the papers' own CNNs |
| 4. Strong deep | ATCNet, EEG Conformer, TCFormer (official code) | Transformers; emg2qwerty / emg2pose reference models |
| 5. Foundation models | LaBraM, CBraMod, EEGPT, BIOT: linear probe and full fine-tune | TinyMyo / BioFoundation; Meta's generic models where released |

Hyperparameters: each model's published defaults, plus a small tuning budget on a validation split carved from training data. The same budget for every model.

## 6. Infrastructure

Keep it small:

```
benchmarks/
├── configs/          # one YAML per (dataset, protocol, model)
├── sota.csv          # published results, machine-readable
├── results/          # one CSV row per (dataset, protocol, subject, seed, model)
├── run.py            # thin wrapper: load config → MOABB / Braindecode / official repo → write CSV
└── report.ipynb      # tables, gap to SOTA, statistics, figures
```

**`sota.csv`** is built in Phase 0 from the `DATASETS.md` result tables. Columns: `dataset, version, protocol, split, metric, value, std, paper, year, source_url, via, flags`. The `flags` column carries known problems already recorded in the tables: test-set model selection (EEG Conformer, FingerFlex), pretraining overlap with the test set, best-of-N runs, post-deadline leaderboard entries.

**`results/*.csv`** columns: `dataset, version, protocol, subject, seed, model, metric, value, train_time_s, gpu, git_commit, config_hash`.

Tools to reuse rather than reimplement: MOABB (datasets, evaluations, pipelines), Braindecode (models, training), pyRiemann, LibEMG, the official repositories of each SOTA model, and the official scorers (nlb_tools, the FALCON challenge package, the PTB-XL benchmarking repo, the PhysioNet challenge scoring code).

## 7. Leakage and validity checklist

Every result must pass this before it goes in a table:

- [ ] Train and test split by subject, session or repetition, as the protocol says. Never random windows from the same recording.
- [ ] Every fitted step (filters with learned parameters, ICA, CSP, normalization, feature scaling) fitted on training data only.
- [ ] Model selection and early stopping on a validation split carved from training data, never on the test set.
- [ ] Foundation models: pretraining data checked for overlap with the test subjects.
- [ ] At least 3 seeds; per-subject results saved.
- [ ] Chance level computed by permutation for small test sets.
- [ ] Dataset version recorded (for example PTB-XL v1.0.1 vs v1.0.3, TUSZ version).

## 8. Comparing with SOTA

For each (dataset, protocol, metric), compare your result with the best comparable row in `sota.csv`:

| Status | Rule |
|---|---|
| **Reproduced** | Your mean is within the published std, or within 1 point if no std is given |
| **Below** | Lower, with a bootstrap 95% confidence interval that excludes the published value |
| **Above** | Higher, with the interval excluding the published value. Re-check the leakage checklist before believing it |
| **Not comparable** | Protocol, class set, input or metric differs |
| **Flagged SOTA** | The published number has a known problem (from the `flags` column); report it, but rank against the best unflagged result |

**Statistics.**
- Two models on one dataset: paired Wilcoxon signed-rank test over subjects (or over seeds when there is one test set).
- Many models across many datasets: Friedman test with a critical-difference diagram (Demšar 2006), so the ranking doesn't depend on one dataset.
- Always report the per-subject spread. BCI performance varies widely between people, and the mean hides that.

## 9. Timeline

| Weeks | Phase | Output |
|---|---|---|
| 1–2 | **0. Setup** | `benchmarks/` folder, `sota.csv` for EEG and EMG, one end-to-end run (CSP+LDA on BCI IV 2a) |
| 3–6 | **1. EEG motor imagery** | Ladder levels 1–4 on 7 datasets, Tracks A and B; first reproduction report |
| 7–10 | **2. EMG** | Ladder levels 1–4 on Ninapro, CapgMyo, GRABMyo, Hyser, EPN-612, putEMG; emg2qwerty/emg2pose reference models |
| 11–13 | **3. Other EEG paradigms** | SSVEP, P300, ErrP, Grasp-and-Lift |
| 14–20 | **4. Large-scale EEG + foundation models** | TUAB, TUEV, TUSZ, CHB-MIT, SEED; level 5 on EEG and EMG |
| 21–30 | **5. Other data types** | Official baselines + one model each on the Phase 5 benchmarks |
| Ongoing | **6. Publish** | Leaderboard pages, blog post per phase, preprint on reproducibility, pipelines contributed back to MOABB |

Start TUH, SEED and DEAP access requests in week 1, since approval can take a while.

## 10. Compute

- **Classical pipelines** run on a laptop CPU.
- **Compact deep models** (EEGNet and similar) need one consumer GPU; per-subject training on small BCI datasets is short.
- **Foundation-model fine-tuning, TUH-scale data, emg2qwerty and emg2pose** need a single modern GPU with plenty of memory, or cloud hours. Budget these explicitly before Phase 4.
- Log training time and hardware with every result; efficiency is part of the comparison.

## 11. Deliverables

1. `benchmarks/results/` with every run, reproducible from configs.
2. One results table per dataset: Track A next to published SOTA, Track B for all models.
3. A leaderboard per data type (Track B), with a critical-difference diagram.
4. A reproduction report: for each SOTA claim, reproduced / below / above / not comparable, with the reason.
5. Posts and a preprint. "Which BCI results reproduce?" is a useful contribution in its own right.

## 12. Risks

| Risk | Mitigation |
|---|---|
| Dataset access is slow (TUH, SEED, DEAP, MOUS) | Request in week 1; start with open datasets |
| SOTA code is missing or broken | Note it in the reproduction report; re-implement only if the paper is detailed enough |
| Published SOTA used test-set selection | Already flagged in the tables; rank against the best unflagged result |
| Compute runs out | Climb the ladder only as far as needed; run foundation models on a subset of datasets first |
| Leaderboards change (NLB, FALCON, Neuroprobe, LibriBrain) | Record the date with every leaderboard number |
| Licences restrict sharing (CC BY-NC, DUAs) | Publish code, configs and scores only, never the data |
