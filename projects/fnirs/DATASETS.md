# fNIRS Datasets and Benchmark Results

This page has specifications for the main public fNIRS datasets (including hybrid EEG+fNIRS sets) and the published results on each. Every number links to the paper or official page where it was read. If a source did not report a value, the cell says "not reported". If I could not read the value in a source myself, it is left out or marked *not verified*. Sources were read on 2026-10-11.

Two original papers could not be read because they are paywalled: Shin et al. 2017 (*IEEE TNSRE*, the MI/MA hybrid dataset) and Wang et al. 2022 (fNIRS-T, *IEEE JBHI*). Their specs and numbers are given only as reported in later open-access papers, and each one is marked "per X" or "via X".

## Overview

| Dataset | Subjects | Channels | Sampling rate | Task / classes | Size on disk | License |
|---|---|---|---|---|---|---|
| Shin 2017 hybrid (A: MI, B: MA) | 29 | 36 fNIRS (14 src × 16 det) + 30 EEG | 12.5 Hz fNIRS (10 Hz as released) | L vs R hand MI; MA vs rest | not reported | GNU GPL (per download page) |
| Shin 2018 hybrid (n-back, DSR, WG) | 26 | 36 fNIRS (16 src × 16 det) + 30 EEG + EOG | 10.4 Hz fNIRS | 0/2/3-back; DSR; WG vs rest | ~6.41 GB | CC BY 4.0 |
| Herff 2014 n-back | 10 | 8 (4 src × 4 det, forehead) | 25 Hz | 1/2/3-back + relax | not reported | not reported |
| Bak 2019 UFFT | 30 | 20 (8 src × 8 det, over C3/C4) | 13.3 Hz (per later papers) | R finger / L finger / foot tapping | 244.7 MB (zip) | CC BY 4.0 |
| Tufts fNIRS2MW | 68 eligible (87 recorded) | 2 locations × HbO/HbR × intensity/phase (D = 8) | 5.2 Hz | 0/1/2/3-back | not reported | CC BY 4.0 |
| MNE-NIRS finger tapping (BIDS-NIRS-Tapping) | 5 | 28 pairs incl. 8 short | 7.8125 Hz | L tap / R tap / control | 43.8 MB (zip) | "other-open" (Zenodo) |
| Luke 2021 auditory (MNE-NIRS `block_speech_noise`; FRESH Dataset I) | 17 | 24 long + 8 short | 5.2 Hz | speech / noise / silence | 93.4 MB (OSF zip) | not stated on OSF; CC0 on OpenNeuro copy |
| FRESH Dataset II (motor) | 10 | 64 long + 4 short | 8.9 Hz | L/R finger tapping, 2 s and 3 s | 0.24 GB (OpenNeuro) | CC BY 4.0 (OSF); CC0 (OpenNeuro) |
| Ning 2024 spatial attention (ds004830) | 11 analysed (12 on OpenNeuro) | 30 long + 6 short | 50 Hz | attend left / center / right | 1.32 GB | CC0 |
| Kernel Flow2 reliability (ds006545) | 49 | thousands of TD-fNIRS channels (35 modules) | 3.76 Hz | rest, Go/No-Go, passive auditory | 50.15 GB | CC0 |
| WashU HD-DOT sets (ds007463, ds007473, ds007816, ds008798) | 5–13 per set | HD-DOT (high-density) | not verified | localizers, movies, stroke rest | 2.45–138.18 GB | CC0 |

Sources are in each dataset's block below. OpenNeuro sizes and subject counts come from the OpenNeuro GraphQL API (latest snapshot, read 2026-10-11).

---

## Part 1: Dataset specifications

### Shin et al. 2017: open-access hybrid EEG+NIRS (dataset A motor imagery, dataset B mental arithmetic)
| Field | Value |
|---|---|
| Year & paper | 2017 (online 2016); Shin, von Lühmann, Blankertz, Kim, Jeong, Hwang, Müller, *IEEE TNSRE* 25(10):1735–1745 ([DOI](https://doi.org/10.1109/TNSRE.2016.2628057); paywalled, abstract via [Korea Univ. repository](https://scholar.korea.ac.kr/handle/2021.sw.korea/82149?mode=full)). Specs below as described by [FGANet](https://doi.org/10.1109/TNSRE.2022.3149899), [Qiu et al. 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9388144/) and [BenchNIRS](https://pmc.ncbi.nlm.nih.gov/articles/PMC10790918/) |
| Subjects | 29: 14 male, 15 female; 28 right-handed, 1 left-handed; age 28.5 ± 3.7 (per FGANet) |
| Device, wavelengths | NIRx NIRScout, continuous wave (CW); 760 and 850 nm (per Qiu et al. and BenchNIRS) |
| Sources / detectors / channels | 14 sources, 16 detectors, 36 channels, 30 mm source–detector distance. Layout per Qiu et al.: 9 frontal channels (around Fp1, Fp2, Fpz), 12 around C3, 12 around C4, 3 around Oz. Short channels: none reported |
| Sampling rate | fNIRS 12.5 Hz, downsampled to 10 Hz by the data provider; EEG 1000 Hz, downsampled to 200 Hz (per FGANet) |
| Other modalities | EEG, 30 channels (BrainAmp) on the same cap. The abstract says the set "includes motion artifacts and physiological data"; exact EOG/ECG/respiration channels *not verified* |
| Tasks / classes, trials, timing | A: left vs right hand kinesthetic motor imagery (opening and closing the hand). B: mental arithmetic (three-digit minus one-digit, repeated) vs baseline rest. 30 trials per class. Trial = 2 s instruction, 10 s task, 15–17 s rest (per FGANet) |
| Sessions | 6 sessions alternating MI (1, 3, 5) and MA (2, 4, 6), each with 60 s pre-rest, 20 trials, 60 s post-rest (per Qiu et al.). A separate motion-artifact recording is also part of the release (per [Shin et al. 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC5810421/)) |
| Size | not reported |
| Format | MATLAB, BBCI-toolbox structures; loading needs the BBCI toolbox ([fNIRS-T repo](https://github.com/wzhlearning/fNIRS-Transformer)). BenchNIRS notes that the fNIRS part is released as light intensity, so the user has to apply the modified Beer–Lambert law |
| Access & license | [doc.ml.tu-berlin.de/hBCI](https://doc.ml.tu-berlin.de/hBCI/), download after accepting the GNU license (link to gpl.txt) |
| Standard evaluation protocol | No official split. Common choices: per subject, 3 s windows with a 1 s step and 5-fold CV, but in two different forms: accuracy computed separately for each window position (FGANet, −2 to 10 s, 10 positions; Sun et al. 2020, −10 to 25 s, 33 positions), or all 10 windows of a trial (−2 to 10 s) pooled with folds split by trial (fNIRSNet); or LOSO |
| Known issues | The original paper's protocol could not be checked. [fNIRSNet](https://doi.org/10.1109/TNSRE.2023.3330911) points out that the original analysis classifies segments from the same time point in every trial, which does not test generalisation across time segments. BenchNIRS describes the optodes as "on the PFC", which contradicts the frontal + motor + occipital layout given by Qiu et al. |

### Shin et al. 2018: simultaneous EEG+NIRS during cognitive tasks (n-back, DSR, word generation)
| Field | Value |
|---|---|
| Year & paper | 2018; Shin, von Lühmann, Kim, Mehnert, Hwang, Müller, *Scientific Data* 5:180003 ([PMC5810421](https://pmc.ncbi.nlm.nih.gov/articles/PMC5810421/)) |
| Subjects | 26 right-handed: 9 male, 17 female; age 26.1 ± 3.5 (17–33) |
| Device, wavelengths | NIRx NIRScout (CW). Wavelengths are not given in the paper; 760 and 850 nm per [BenchNIRS](https://pmc.ncbi.nlm.nih.gov/articles/PMC10790918/) |
| Sources / detectors / channels | 16 sources, 16 detectors, 36 channels, 30 mm. Frontal 16 channels (around AFz, AF3, AF4, AF7, AF8), motor 4 around C3 + 4 around C4, parietal 4 around P3 + 4 around P4, occipital 4 around POz. Short channels: none reported |
| Sampling rate | NIRS 10.4 Hz (downsampled to 10 Hz in the paper's analysis); EEG 1000 Hz |
| Other modalities | EEG, 30 active electrodes (BrainAmp, 10-5 system); EOG, 2 vertical + 2 horizontal, at 1000 Hz |
| Tasks / classes, trials, timing | A n-back (0, 2, 3-back): 9 series, each 2 s instruction + 40 s task + 20 s rest, one digit every 2 s; 180 stimulus trials per n-back level. B discrimination/selection response (DSR, O vs X): same block structure, 180 trials. C word generation (WG) vs baseline (BL): 10 WG + 10 BL per session, 2 s instruction + 10 s task + 13–15 s rest; 30 trials per class |
| Sessions | 3 per task, all on one day (about 3.5 h), recorded in the order A → C → B |
| Size | About 6.41 GB (EEG + NIRS, MATLAB format); per-subject NIRS files about 29 MB, EEG about 223 MB ([DepositOnce](https://doi.org/10.14279/depositonce-5830.2)) |
| Format | MATLAB BBCI structures (`cnt`, `mrk`, `mnt`) plus the vendor's raw files |
| Access & license | [DepositOnce](https://doi.org/10.14279/depositonce-5830.2), CC BY 4.0; also [doc.ml.tu-berlin.de/simultaneous_EEG_NIRS](http://doc.ml.tu-berlin.de/simultaneous_EEG_NIRS/) |
| Standard evaluation protocol | Paper baseline: NIRS classified only for WG vs BL. Features are mean and slope of HbR and HbO in 5 s windows (1 s step), shrinkage LDA, 10×5-fold CV, per subject. ERP classification for A and B is EEG only (10×10-fold) |
| Known issues | Rest periods are too short for the hemodynamics to return to baseline after 40 s blocks (the authors say so). The 1.5 s inter-stimulus interval in A and B is not suitable for event-related NIRS. Fatigue over a 3.5 h session. Task performance during WG was not assessed |

### Herff et al. 2014: n-back workload (prefrontal)
| Field | Value |
|---|---|
| Year & paper | 2014 (epub Jan 2014); Herff, Heger, Fortmann, Hennrich, Putze, Schultz, *Front. Hum. Neurosci.* 7:935 ([PMC3893598](https://pmc.ncbi.nlm.nih.gov/articles/PMC3893598/)) |
| Subjects | 10: 4 female; mean age 22; 8 right-handed, 2 left-handed |
| Device, wavelengths | Artinis OxyMon Mark III (CW); 765 and 856 nm |
| Sources / detectors / channels | 4 transmitters, 4 receivers on the forehead, 3.5 cm apart → 8 channels (HbO + HbR). Short channels: none reported |
| Sampling rate | 25 Hz |
| Other modalities | not reported |
| Tasks / classes, trials, timing | 1-, 2-, 3-back, 10 trials each (3 ± 1 targets per trial), plus relax. Per [BenchNIRS](https://pmc.ncbi.nlm.nih.gov/articles/PMC10790918/): 5 s instruction, 44 s n-back (a letter every 2 s), 15 s rest |
| Sessions | 1 |
| Size / format | not reported |
| Access & license | Link given by BenchNIRS: `csl.uni-bremen.de/CorpusData/download.php?crps=fNIRS` (did not respond when checked on 2026-10-11); license not reported |
| Standard evaluation protocol | Per subject, 10-fold CV, LDA on HbO/HbR slope features with mutual-information feature selection inside the training folds |
| Known issues | Only 10 subjects and 8 channels; relax trials are 10 s long while n-back trials are 44 s |

### Bak et al. 2019: unilateral finger- and foot-tapping (UFFT)
| Field | Value |
|---|---|
| Year & paper | 2019; Bak, Park, Shin, Jeong, *Electronics* 8(12):1486 ([DOI](https://doi.org/10.3390/electronics8121486); read via [Wayback copy](http://web.archive.org/web/20230731121639/https://www.mdpi.com/2079-9292/8/12/1486/htm)) |
| Subjects | 30: 17 male; 29 right-handed; age 23.4 ± 2.5 |
| Device, wavelengths | Shimadzu LIGHTNIRS, three-wavelength CW; wavelengths not reported |
| Sources / detectors / channels | 8 sources, 8 detectors; 4 + 4 around C3 and 4 + 4 around C4 → 20 channels (10 per hemisphere). 30 mm distance per [BenchNIRS](https://pmc.ncbi.nlm.nih.gov/articles/PMC10790918/). Short channels: none reported |
| Sampling rate | Not stated in the paper text; 13.3 Hz per [BenchNIRS](https://pmc.ncbi.nlm.nih.gov/articles/PMC10790918/) and [fNIRSNet](https://doi.org/10.1109/TNSRE.2023.3330911) |
| Other modalities | not reported |
| Tasks / classes, trials, timing | Right-hand finger tapping, left-hand finger tapping (thumb to each finger, 2 Hz), foot tapping (1 Hz); 25 trials per class. Trial = 2 s introduction, 10 s task, 17–19 s break (about 30 s between triggers) |
| Sessions | 3 sessions in one visit |
| Size | 244.7 MB zip ([figshare](https://doi.org/10.6084/m9.figshare.9783755.v1)) |
| Format | MATLAB BBCI structures: `cntHb` (ΔHbO/HbR), `mrk`, `mnt`; per-channel SNR stored |
| Access & license | [figshare](https://doi.org/10.6084/m9.figshare.9783755.v1), CC BY 4.0; tutorials at [github.com/JaeyoungShin/fNIRS-dataset](https://github.com/JaeyoungShin/fNIRS-dataset) |
| Standard evaluation protocol | Paper baseline: per subject, leave-one-trial-out CV, linear SVM on mean ΔHbO/ΔHbR in 0–5, 5–10, 10–15 s (120 features) |
| Known issues | This is overt movement (motor execution), not imagery. Low-SNR channels were not removed. The paper's text labels classes "RFT/LFT" while defining RHT/LHT. The [Tufts paper](https://datasets-benchmarks-proceedings.neurips.cc/paper_files/paper/2021/file/bd686fd640be98efaae0091fa301e613-Paper-round2.pdf) (Table 1) lists this set as 10 Hz with optodes "attached to forehead", which contradicts the C3/C4 placement in the original paper |

### Tufts fNIRS2MW (fNIRS to Mental Workload)
| Field | Value |
|---|---|
| Year & paper | 2021; Huang, Wang, Blaney, Slaughter, McKeon, Zhou, Jacob, Hughes, NeurIPS Datasets & Benchmarks ([paper](https://datasets-benchmarks-proceedings.neurips.cc/paper_files/paper/2021/file/bd686fd640be98efaae0091fa301e613-Paper-round2.pdf)) |
| Subjects | 87 completed; 68 eligible after exclusions. Eligible cohort: 26 M, 39 F, 2 other, 1 declined; age 18–44 (mean 21.71); 64 right-handed; race reported (32 Asian, 27 White, …) |
| Device, wavelengths | ISS Imagent, **frequency-domain (FD)**, 110 MHz modulation; 690 and 830 nm; dual-slope probe design |
| Sources / detectors / channels | Two custom probes (left and right forehead) on a headband; D = 8 per timestep = 2 locations × {ΔHbO, ΔHbR} × {intensity, phase}. The dual-slope design suppresses superficial signals; there are no separate short channels |
| Sampling rate | 5.2 Hz |
| Other modalities | None; demographics, n-back performance, NASA-TLX, logs |
| Tasks / classes, trials, timing | n-back with n ∈ {0, 1, 2, 3}; 16 blocks of 40 trials (80 s per block), 10–30 s rest between blocks. The benchmark task is binary 0-back vs 2-back |
| Sessions | 1 per subject (over 21 min of task data) |
| Size | not reported |
| Format | CSV; raw, band-pass-filtered (0.001–0.2 Hz), and pre-windowed versions (2, 5, 10, 20, 30, 40 s windows, 0.6 s stride) ([dataset page](https://tufts-hci-lab.github.io/code_and_datasets/fNIRS2MW.html)) |
| Access & license | [Dataset page](https://tufts-hci-lab.github.io/code_and_datasets/fNIRS2MW.html) (Box), CC BY 4.0; code MIT ([repo](https://github.com/tufts-ml/fNIRS-mental-workload-classifiers)) |
| Standard evaluation protocol | Three paradigms with fixed splits: subject-specific, generic (17 buckets of 4 test subjects, a development pool of up to 64 other subjects, split 75/25 train/validation by subject), and generic + fine-tuning. Each 80 s block goes wholly to train, validation or test, so overlapping windows never cross splits |
| Known issues | Forehead only. One session, so no cross-session test. 19 subjects were excluded (5 behavioural, 5 for different sensor settings, 9 for abnormal oxygen dynamics); their data are still released |

### MNE-NIRS finger tapping (BIDS-NIRS-Tapping)
| Field | Value |
|---|---|
| Year & paper | 2021; Luke & McAlpine, "fNIRS Finger Tapping Data in BIDS Format" ([Zenodo](https://doi.org/10.5281/zenodo.5529797), [repo](https://github.com/rob-luke/BIDS-NIRS-Tapping)); used by MNE-NIRS as `fnirs_motor_group` ([datasets page](https://mne.tools/mne-nirs/dev/auto_examples/general/plot_05_datasets.html)). MNE-Python's `fnirs_motor` is a single participant of the same experiment ([tutorial](https://mne.tools/stable/auto_tutorials/preprocessing/70_fnirs_processing.html)) |
| Subjects | 5: ages 34, 32, 26, 20, 53; 2 M, 3 F (`participants.tsv`) |
| Device, wavelengths | NIRx (CW amplitude); 760 and 850 nm (`channels.tsv`); model not stated |
| Sources / detectors / channels | 8 sources, 16 detectors; 56 channels = 28 source–detector pairs × 2 wavelengths (sub-01 sidecar). Standard NIRx motor montage plus 8 short channels ([MNE-NIRS example](https://mne.tools/mne-nirs/stable/auto_examples/general/plot_11_hrf_measured.html)) |
| Sampling rate | 7.8125 Hz |
| Other modalities | none |
| Tasks / classes, trials, timing | Left-thumb tapping, right-thumb tapping, control; 30 per condition, 5 s each, auditory cue; inter-stimulus interval 20–35 s ([experiment repo](https://github.com/rob-luke/experiment-fNIRS-tapping)) |
| Sessions | 1 (sub-01 recording about 2974 s) |
| Size | 43.8 MB zip (Zenodo) |
| Format | BIDS 1.8.0 with SNIRF |
| Access & license | Zenodo, license recorded as "other-open" |
| Standard evaluation protocol | none (tutorial dataset for GLM and averaging) |
| Known issues | 5 subjects; the repo warns that fNIRS-BIDS was still a work in progress when it was built |

### Luke et al. 2021: passive auditory block design (MNE-NIRS `block_speech_noise`; FRESH Dataset I)
| Field | Value |
|---|---|
| Year & paper | 2021; Luke, Larson, Shader, Innes-Brown, Van Yper, Lee, Sowman, McAlpine, *Neurophotonics* 8(2):025008 ([PMC8140612](https://pmc.ncbi.nlm.nih.gov/articles/PMC8140612/)) |
| Subjects | 17, age 22–40, no hearing concerns; sex not reported |
| Device, wavelengths | NIRx NIRScoutX with APD detectors (CW); 760 and 850 nm per [FRESH](https://pmc.ncbi.nlm.nih.gov/articles/PMC12322209/) |
| Sources / detectors / channels | 12 sources, 12 detectors + 8 short detectors; covers left IFG, left and right STG, occipital. FRESH counts 24 long channels + 8 short channels |
| Sampling rate | 5.2 Hz |
| Other modalities | none reported |
| Tasks / classes, trials, timing | Speech (three sentences, 5.25 s), noise (5 s), silence (5 s); 20 trials each (60 total); 10–20 s silent interval; about 25 min; 7 subjects watched a silent subtitled film |
| Sessions | 1 |
| Size | 93.4 MB zip ([OSF f6tdk](https://osf.io/f6tdk/)) |
| Format | BIDS (SNIRF in the FRESH copy) |
| Access & license | OSF (license not set on the project); FRESH copy on [OSF b4wck](https://osf.io/b4wck) (CC BY 4.0) and [OpenNeuro ds005964](https://openneuro.org/datasets/ds005964) (CC0) |
| Standard evaluation protocol | Group and individual GLM / averaging (not a classification benchmark) |
| Known issues | The MNE-NIRS API docstring says "18 participants", while the paper and the MNE-NIRS example page say 17 |

### FRESH (fNIRS Reproducibility Study Hub) datasets
| Field | Value |
|---|---|
| Year & paper | 2025; Yücel et al., "fNIRS reproducibility varies with data quality, analysis pipelines, and researcher experience", *Commun. Biol.* 8:1149 ([PMC12322209](https://pmc.ncbi.nlm.nih.gov/articles/PMC12322209/)) |
| Dataset I (auditory) | The Luke et al. 2021 data above (17 adults) |
| Dataset II (motor): subjects | 10 healthy right-handed adults, age 20–35 (a subset published before) |
| Dataset II: device, wavelengths | NIRx NIRScout (CW), 760 and 850 nm |
| Dataset II: channels | 14 sources, 32 detectors over motor cortex; 64 pairs at about 3 cm + 4 short pairs at 0.8 cm; optode positions digitised per subject (Polhemus Fastrak) |
| Dataset II: sampling rate | 8.9 Hz |
| Dataset II: tasks | Right- and left-hand finger tapping lasting 2 s (30 repetitions) and 3 s (25 repetitions); rest 10–20 s; 4 runs |
| Other modalities | not reported |
| Size | Dataset II 0.24 GB, Dataset I 0.07 GB ([OpenNeuro ds005963](https://openneuro.org/datasets/ds005963), [ds005964](https://openneuro.org/datasets/ds005964)) |
| Format | SNIRF (validated with pysnirf2 0.7.4), BIDS |
| Access & license | [OSF b4wck](https://osf.io/b4wck), CC BY 4.0; OpenNeuro copies CC0 |
| Standard evaluation protocol | Hypothesis testing: 7 group-level hypotheses (Dataset I) and individual-level hypotheses (Dataset II), analysed independently by 38 teams |
| Known issues | Built to measure analysis variability, not as a decoding benchmark |

### Ning et al. 2024: spatial attention during complex scene analysis (OpenNeuro ds004830)
| Field | Value |
|---|---|
| Year & paper | 2024; Ning, Duwadi, Yücel, von Lühmann, Boas, Sen, *Front. Hum. Neurosci.* ([PMC10991699](https://pmc.ncbi.nlm.nih.gov/articles/PMC10991699/)) |
| Subjects | 16 listed in the paper's Table 1, 11 included after quality/behaviour exclusions; [OpenNeuro snapshot 2.0.0](https://openneuro.org/datasets/ds004830) lists 12 |
| Device, wavelengths | TechEn CW6 (CW); 690 and 830 nm |
| Channels | 12 sources, 17 long detectors (30 mm), 6 short detectors (8 mm) → 30 long channels (one subject: 34); dorsal frontoparietal network |
| Sampling rate | 50 Hz |
| Tasks / classes | Attend to the speaker at left (−45°), center, or right (45°) in a 3-talker audiovisual scene; 30 trials per condition (90 per subject) |
| Size / format / license | 1.32 GB; BIDS/SNIRF; CC0 |
| Standard evaluation protocol | Per subject, shrinkage LDA on HbT HRF area, 10 × 5-fold nested CV; the short-channel GLM is fitted inside each training fold to avoid leakage |
| Known issues | Large between-subject variation in accuracy |

### Kernel Flow2 test-retest dataset (OpenNeuro ds006545)
| Field | Value |
|---|---|
| Year & paper | 2024; Dubois et al., "Reliability of brain metrics derived from a time-domain functional near-infrared spectroscopy system", *Sci. Rep.* 14:17500 ([PMC11289386](https://pmc.ncbi.nlm.nih.gov/articles/PMC11289386/)) |
| Subjects | 49 healthy participants, repeated measures across time points and headsets |
| Device, wavelengths | Kernel Flow2, **time-domain (TD)**; 690 and 905 nm |
| Channels | 35 modules × (3 sources, 6 detectors); within- and between-module channels give thousands of channels, source–detector distances 8–60 mm |
| Sampling rate | 3.76 Hz effective |
| Tasks | Resting state (7 min video), Go/No-Go, passive auditory (20 s story vs 20 s noise blocks) |
| Size / format / license | [OpenNeuro ds006545](https://openneuro.org/datasets/ds006545): 50.15 GB, CC0, task listed as "audio". The paper itself says data were "available … on reasonable request"; whether the release includes the rest and Go/No-Go recordings is *not verified* |
| Standard evaluation protocol | Test-retest reliability (ICC), not classification |

### WashU HD-DOT datasets on OpenNeuro (Culver lab)
All CC0, SNIRF, read from OpenNeuro dataset descriptions:
- [ds007463](https://openneuro.org/datasets/ds007463): very-high-density DOT + fMRI validation, 8 participants, 74.37 GB (Fogarty et al., *Imaging Neuroscience* 2025).
- [ds007473](https://openneuro.org/datasets/ds007473): HD-DOT audiovisual movie viewing, 5 participants, 38.96 GB (Tripathy et al., *HBM* 2024; *Neurophotonics* 2025 decoding paper).
- [ds007816](https://openneuro.org/datasets/ds007816): HD-DOT + fMRI semantic encoding of natural movies, 6 participants, 138.18 GB.
- [ds008798](https://openneuro.org/datasets/ds008798): bedside HD-DOT resting state in 13 stroke patients, 2.45 GB (Bergonzi et al., *Neurophotonics* 2026).

Device specifics (wavelengths, sampling rate, optode counts) for these were not verified.

**Other OpenNeuro fNIRS-BIDS sets, in brief** (API, 2026-10-11; all CC0; specs not verified beyond the README):
- [ds004514](https://openneuro.org/datasets/ds004514): simultaneous EEG (BioSemi 64 ch) + fNIRS, semantic decoding of imagined animals/tools, 12 participants, 25.93 GB.
- [ds007554](https://openneuro.org/datasets/ds007554): EEG + fNIRS + ECG + EMG, motor imagery, mental arithmetic, n-back and more, 30 participants, 3 sessions, 4.52 GB.
- [ds007738](https://openneuro.org/datasets/ds007738): whole-head cocktail-party attention, 38 participants, 56 sources, 144 detectors, 1134 channels at about 8.99 Hz, with eye tracking, 38.8 GB.
- [ds006377](https://openneuro.org/datasets/ds006377) "InclusionStudy": 115 participants, resting + ball squeeze, 1.48 GB.
- [ds008192](https://openneuro.org/datasets/ds008192) "InterGenSynch": 122 participants, 2.79 GB.
- [ds007420](https://openneuro.org/datasets/ds007420): multi-distance fNIRS, ball squeezing + induced motion artifacts, 12 participants.
- [ds006459](https://openneuro.org/datasets/ds006459) / [ds006460](https://openneuro.org/datasets/ds006460): sparse vs high-density word-colour Stroop, 17 participants each.
- [ds005929](https://openneuro.org/datasets/ds005929) "Motion-Yucel2014": 7 participants, motion-artifact data.

---

## Part 2: Results

Within each table, rows use the same protocol and metric unless a row is marked otherwise. "Re-run in X" means the authors of paper X re-implemented the method under their own protocol. "Via X" means the number was read in X's comparison table, not in the original paper. All accuracies are mean over subjects (± SD over subjects unless stated).

### Shin 2017 dataset B (mental arithmetic vs rest), fNIRS only: per subject, 3 s windows (1 s step), 5-fold CV split by trial
| Paper | Year | Method | Input | Protocol | Metric | Result |
|---|---|---|---|---|---|---|
| Sun et al. 1D-CNN, re-run in [fNIRSNet Table II](https://doi.org/10.1109/TNSRE.2023.3330911) | 2020 | 1D-CNN | HbO + HbR | 10 segments per trial (−2 to 10 s), 48/12 trials per fold | Accuracy | 64.53 ± 13.03% |
| Lyu et al. CNN, re-run in [fNIRSNet](https://doi.org/10.1109/TNSRE.2023.3330911) | 2021 | CNN | HbO + HbR | same | Accuracy | 64.18 ± 13.12% |
| Lyu et al. LSTM, re-run in [fNIRSNet](https://doi.org/10.1109/TNSRE.2023.3330911) | 2021 | LSTM | HbO + HbR | same | Accuracy | 57.36 ± 11.94% |
| Wang et al. fNIRS-T, re-run in [fNIRSNet](https://doi.org/10.1109/TNSRE.2023.3330911) | 2022 | Transformer (hyperparameters adapted to 3 s input) | HbO + HbR | same | Accuracy | 65.17 ± 13.67% |
| [Wang, Fang, Zhang (fNIRSNet)](https://doi.org/10.1109/TNSRE.2023.3330911) | 2023 | 498-parameter CNN with 1 × S "delayed hemodynamic response" kernels | HbO + HbR | same | Accuracy | 70.76 ± 15.60% |

### Shin 2017 dataset B (MA), fNIRS only: subject-independent, LOSO, 3 s windows
| Paper | Year | Method | Input | Protocol | Metric | Result |
|---|---|---|---|---|---|---|
| Sun et al. 1D-CNN, re-run in [fNIRSNet](https://doi.org/10.1109/TNSRE.2023.3330911) | 2020 | 1D-CNN | HbO + HbR | LOSO, 29 folds | Accuracy | 57.18 ± 6.05% |
| Lyu et al. CNN / LSTM, re-run in [fNIRSNet](https://doi.org/10.1109/TNSRE.2023.3330911) | 2021 | CNN / LSTM | HbO + HbR | same | Accuracy | 56.05 ± 7.13% / 56.01 ± 6.37% |
| Wang et al. fNIRS-T, re-run in [fNIRSNet](https://doi.org/10.1109/TNSRE.2023.3330911) | 2022 | Transformer | HbO + HbR | same | Accuracy | 56.91 ± 6.14% |
| [fNIRSNet](https://doi.org/10.1109/TNSRE.2023.3330911) | 2023 | fNIRSNet (F1 = 16, F2 = 32) | HbO + HbR | same | Accuracy | 65.26 ± 6.65% |

### Shin 2017 MA and Shin 2018 WG, fNIRS only: whole-trial input (MA samples 80–320, WG 80–300, i.e. about 22–24 s at 10 Hz). Not directly comparable with the 3 s tables above
From the [vision fNIRS framework paper](https://ieeexplore.ieee.org/document/9828508) (Wang et al., *IEEE TNSRE* 2022), Tables IV and V. It says "5 × 5-fold cross-validation (KFold-CV)" without stating whether folds are within one subject or pooled across subjects; the ±1–2 SDs suggest SD over folds. All baselines were re-run by these authors.

| Paper | Year | Method | Input | Protocol | Metric | MA | WG |
|---|---|---|---|---|---|---|---|
| fNIRS-T, re-run in [vision paper](https://ieeexplore.ieee.org/document/9828508) | 2022 | Transformer | HbO + HbR | 5 × 5-fold | Accuracy | 76.59 ± 1.86% | 72.36 ± 2.04% |
| fNIRS-PreT, re-run in [vision paper](https://ieeexplore.ieee.org/document/9828508) | 2022 | Transformer with learned preprocessing | HbO + HbR | 5 × 5-fold | Accuracy | 78.53 ± 1.83% | 72.14 ± 1.48% |
| [Vision framework](https://ieeexplore.ieee.org/document/9828508) | 2022 | Gramian-angular images + PVTv2-B0 / MLP-Mixer (best per dataset) | HbO + HbR | 5 × 5-fold | Accuracy | 78.68 ± 1.59% (PVTv2-B0) | 73.92 ± 1.45% (MLP-Mixer) |
| fNIRS-T, re-run in [vision paper](https://ieeexplore.ieee.org/document/9828508) | 2022 | Transformer | HbO + HbR | **LOSO** | Accuracy | 78.16 ± 7.59% | 76.15 ± 7.81% |
| fNIRS-PreT, re-run in [vision paper](https://ieeexplore.ieee.org/document/9828508) | 2022 | Transformer | HbO + HbR | **LOSO** | Accuracy | 80.57 ± 7.53% | 76.35 ± 7.38% |
| [Vision framework](https://ieeexplore.ieee.org/document/9828508) | 2022 | GADF + ResNet-18 (MA) / PVTv2-B0 (WG) | HbO + HbR | **LOSO** | Accuracy | 81.44 ± 8.16% | 76.99 ± 5.70% |

The same fNIRS-T LOSO on MA scores 78.16% with whole-trial input here and 56.91% with 3 s windows in fNIRSNet. The windows here also include post-task rest samples.

### Shin 2017 datasets A (MI) and B (MA), hybrid EEG + fNIRS: per subject, 3 s windows, 5-fold CV
FGANet's "mean" accuracy averages the 10 window positions in a trial (−2–1 s … 7–10 s); its "max" is the best window position. Sun et al. and the Shin et al. figure they quote are the best window position (comparable to "max"), but Sun et al. slide the window over −10 to 25 s (33 positions, numbered by left edge), so their "best" is picked from a wider range than FGANet's. These per-position numbers are not comparable with the pooled-window fNIRSNet table above.

| Paper | Year | Method | Input | Protocol | Metric | MA | MI |
|---|---|---|---|---|---|---|---|
| Shin et al., via [Sun et al. Fig. 7](https://doi.org/10.1109/ACCESS.2020.2994226) | 2017 | Shrinkage-LDA meta-classifier (original baseline) | EEG + HbO + HbR | original paper's protocol, best window (*not verified*) | Accuracy | 88.10% | 74.20% |
| Shin et al., re-run in [FGANet Table V](https://doi.org/10.1109/TNSRE.2022.3149899) | 2017 | as above, re-implemented | EEG + fNIRS | mean / max over windows | Accuracy | 75.60 ± 6.69% / 84.29 ± 9.07% | 60.91 ± 9.07% / 63.85 ± 10.83% |
| [Sun et al.](https://doi.org/10.1109/ACCESS.2020.2994226) | 2020 | 1D-CNN branches + pth-order polynomial (tensor) fusion | EEG + HbO + HbR | best window (MA: 8, MI: 1) | Accuracy | 90.19% | 77.53% |
| [Sun et al.](https://doi.org/10.1109/ACCESS.2020.2994226) | 2020 | 1D-CNN, single modality | HbO only / HbR only | best window | Accuracy | 86.28% / 84.42% | 67.01% / 69.31% |
| Sun et al. pth-PF, re-run in [FGANet](https://doi.org/10.1109/TNSRE.2022.3149899) | 2020 | as above | EEG + fNIRS | mean / max | Accuracy | 87.24 ± 6.14% / 91.67 ± 6.09% | 75.90 ± 8.89% / 77.36 ± 10.88% |
| [Kwak, Song, Kim (FGANet)](https://doi.org/10.1109/TNSRE.2022.3149899) | 2022 | FSNet (fNIRS-only branch) | HbO + HbR | mean / max | Accuracy | 82.34 ± 8.11% / 86.95 ± 9.19% | 67.80 ± 8.23% / 68.68 ± 9.00% |
| [FGANet](https://doi.org/10.1109/TNSRE.2022.3149899) | 2022 | ESNet (EEG-only branch) | EEG | mean / max | Accuracy | 89.14 ± 7.73% / 92.07 ± 8.42% | 76.50 ± 9.63% / 77.47 ± 10.71% |
| [FGANet](https://doi.org/10.1109/TNSRE.2022.3149899) | 2022 | fNIRS-guided attention, early fusion + weighted prediction | EEG + fNIRS | mean / max | Accuracy | 91.96 ± 5.82% / 95.46 ± 5.12% | 78.59 ± 8.86% / 80.23 ± 9.63% |

Other papers quote different values for the original Shin et al. hybrid baseline: [Qiu et al. 2022 Table 3](https://pmc.ncbi.nlm.nih.gov/articles/PMC9388144/) gives 75.9% (MI) and 86.2% (MA). I could not read the original to resolve this.

### Shin 2017 MI / MA, hybrid: not directly comparable (high leakage risk)
| Paper | Year | Method | Input | Protocol | Metric | Result (MI / MA) |
|---|---|---|---|---|---|---|
| [Qiu et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC9388144/) | 2022 | Multi-domain features + stacked RF/LR, decision fusion | EEG + fNIRS | One 80/20 split of feature vectors after feature selection; 8-fold inside the 80% | Accuracy | 96.74 ± 1.96% / 98.42 ± 1.52% |
| [Qiu et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC9388144/) | 2022 | Random forest, hybrid fNIRS features | HbO + HbR | same | Accuracy | 92.19 ± 2.95% / 94.88 ± 2.35% |

The text does not make clear whether the feature selection saw the 20% test portion, so I treat these rows as likely optimistic. The same paper's Table 2 lists identical "Shin et al." fNIRS numbers for MI and MA, which looks like a copying error.

### Shin 2018 dataset C (word generation vs baseline): original baseline, per subject, sliding 5 s window, 10 × 5-fold CV, shrinkage LDA
| Paper | Year | Method | Input | Protocol | Metric | Result |
|---|---|---|---|---|---|---|
| [Shin et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC5810421/) | 2018 | CSP log-variance + sLDA | EEG | peak at t = 10 s | Accuracy | 76.9% |
| [Shin et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC5810421/) | 2018 | Mean + slope features, sLDA | HbO + HbR | peak at t = 14 s | Accuracy | 74.3% |
| [Shin et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC5810421/) | 2018 | Meta-classifier on LDA outputs | EEG + HbO + HbR | peak at t = 11 s | Accuracy | 80.7% |

These are peak values of an accuracy-over-time curve, which means the best window was picked after seeing test results. For datasets A and B the paper reports only EEG ERP classification (10 × 10-fold sLDA): 76.9 ± 8.0% for 2-back and 76.0 ± 7.9% for 3-back (Table 5 labels these "versus 0-back"; the text describes target vs non-target), and 86.8 ± 5.9% for O vs X; NIRS was not classified for these.

### BenchNIRS (Benerradi et al. 2023): nested CV, 10 s epochs, five open datasets, accuracy
[Benerradi et al., *Front. Neuroergon.*](https://pmc.ncbi.nlm.nih.gov/articles/PMC10790918/). "Generalised" = outer group 5-fold by subject (test subjects unseen), inner group 3-fold for hyperparameters. "Personalised" = the same per subject with stratified 5/3-fold. Channels averaged by region of interest; TDDR + 0.01–0.5 Hz band-pass; HbO + HbR; fNIRS only. SD (in brackets) is over outer folds for generalised and over participants for personalised.

| Dataset (classes) | Chance | Generalised LDA | Generalised best other | Personalised LDA | Personalised best other |
|---|---|---|---|---|---|
| Herff 2014 n-back (1/2/3) | 0.333 | 0.407 (0.049) | kNN 0.377 | 0.353 (0.099) | ANN 0.373 |
| Shin 2018 n-back (0/2/3) | 0.333 | 0.389 (0.026) | CNN 0.393 | 0.360 (0.103) | LSTM 0.356 |
| Shin 2018 WG vs BL | 0.500 | 0.596 (0.026) | CNN 0.587 | 0.588 (0.090) | SVC / ANN 0.562 |
| Shin 2017 MA vs BL | 0.500 | 0.591 (0.035) | CNN 0.602 | 0.633 (0.107) | LSTM 0.608 |
| Bak 2019 UFFT (3 classes) | 0.333 | 0.518 (0.068) | LSTM 0.511 | 0.513 (0.140) | LSTM 0.446 |

With a 2 s non-overlapping sliding window (generalised, LDA): Herff 0.385, Shin 2018 n-back 0.360, WG 0.568, Shin 2017 MA 0.564, Bak 0.427 (same paper, Table 4).

### Bak 2019 UFFT (3 classes): original baseline
| Paper | Year | Method | Input | Protocol | Metric | Result |
|---|---|---|---|---|---|---|
| [Bak et al.](https://doi.org/10.3390/electronics8121486) | 2019 | Linear SVM, mean ΔHbO/R in 3 windows (0–15 s) | HbO + HbR | Per subject, leave-one-trial-out | Accuracy | 70.4 ± 18.4% (ternary); binary 83.4 ± 17.0% (R vs L hand), 77.4 ± 14.6% (R hand vs foot), 80.6 ± 14.3% (L hand vs foot) |

### Bak 2019 UFFT: per subject, 3 s windows (0–10 s, 8 per trial), 5-fold CV split by trial
| Paper | Year | Method | Input | Protocol | Metric | Result |
|---|---|---|---|---|---|---|
| Sun et al. 1D-CNN, re-run in [fNIRSNet Table II](https://doi.org/10.1109/TNSRE.2023.3330911) | 2020 | 1D-CNN | HbO + HbR | as above | Accuracy | 57.76 ± 17.85% |
| Lyu et al. CNN, re-run in [fNIRSNet](https://doi.org/10.1109/TNSRE.2023.3330911) | 2021 | CNN | HbO + HbR | same | Accuracy | 60.57 ± 17.64% |
| Lyu et al. LSTM, re-run in [fNIRSNet](https://doi.org/10.1109/TNSRE.2023.3330911) | 2021 | LSTM | HbO + HbR | same | Accuracy | 46.14 ± 14.07% |
| fNIRS-T, re-run in [fNIRSNet](https://doi.org/10.1109/TNSRE.2023.3330911) | 2022 | Transformer | HbO + HbR | same | Accuracy | 61.26 ± 18.54% |
| [fNIRSNet](https://doi.org/10.1109/TNSRE.2023.3330911) | 2023 | fNIRSNet | HbO + HbR | same | Accuracy | 68.67 ± 19.85% (71.79% with a 7 s window, Fig. 8) |

### Bak 2019 UFFT: subject-independent LOSO, 3 s windows
| Paper | Year | Method | Input | Protocol | Metric | Result |
|---|---|---|---|---|---|---|
| Sun et al. 1D-CNN, re-run in [fNIRSNet](https://doi.org/10.1109/TNSRE.2023.3330911) | 2020 | 1D-CNN | HbO + HbR | LOSO | Accuracy | 53.36 ± 12.15% |
| Lyu et al. CNN / LSTM, re-run in [fNIRSNet](https://doi.org/10.1109/TNSRE.2023.3330911) | 2021 | CNN / LSTM | HbO + HbR | LOSO | Accuracy | 57.42 ± 13.36% / 57.49 ± 13.43% |
| fNIRS-T, re-run in [fNIRSNet](https://doi.org/10.1109/TNSRE.2023.3330911) | 2022 | Transformer | HbO + HbR | LOSO | Accuracy | 56.40 ± 13.03% |
| [fNIRSNet](https://doi.org/10.1109/TNSRE.2023.3330911) | 2023 | fNIRSNet | HbO + HbR | LOSO | Accuracy | 64.43 ± 15.75% |

### Bak 2019 UFFT: whole-trial input (samples 20–320). Not directly comparable with the 3 s tables
| Paper | Year | Method | Input | Protocol | Metric | Result |
|---|---|---|---|---|---|---|
| fNIRS-T, re-run in [vision paper Table IV](https://ieeexplore.ieee.org/document/9828508) | 2022 | Transformer | HbO + HbR | 5 × 5-fold (see note above) | Accuracy | 75.49 ± 2.07% |
| fNIRS-T, re-run in [vision paper Table V](https://ieeexplore.ieee.org/document/9828508) | 2022 | Transformer | HbO + HbR | LOSO | Accuracy | 78.22 ± 16.69% |
| [Vision framework](https://ieeexplore.ieee.org/document/9828508) | 2022 | GADF + ResMLP (best visual model) | HbO + HbR | 5 × 5-fold | Accuracy | 74.36 ± 1.90% |

### Herff 2014 n-back: original baseline, per subject, 10-fold CV, LDA on slope features
| Paper | Year | Method | Input | Protocol | Metric | Result |
|---|---|---|---|---|---|---|
| [Herff et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC3893598/) | 2014 | LDA, MI feature selection in training folds | HbO + HbR slopes | 25 s window: 1 vs 2 / 1 vs 3 / 2 vs 3 / 1-2-3 | Accuracy | 58.5% / 78.0% / 61.0% / 50.3% |
| [Herff et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC3893598/) | 2014 | same | same | 15 s window: same four tasks | Accuracy | 58.5% / 63.5% / 56.3% / 44.0% |
| [Herff et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC3893598/) | 2014 | same | same | vs relax (10 s): 1-back / 2-back / 3-back / 4-class | Accuracy | 71.5 ± 17.7% / 80.3 ± 10.5% / 80.5 ± 13.8% / 44.5 ± 10.0% |

### Tufts fNIRS2MW: 0-back vs 2-back, official splits, 30 s windows, accuracy averaged over test subjects
| Paper | Year | Method | Input | Protocol | Metric | Result |
|---|---|---|---|---|---|---|
| [Huang et al.](https://datasets-benchmarks-proceedings.neurips.cc/paper_files/paper/2021/file/bd686fd640be98efaae0091fa301e613-Paper-round2.pdf) | 2021 | Random forest (mean, SD, slope, intercept per channel) | HbO + HbR, intensity + phase | Generic, pool of 16 other subjects | Accuracy | 66.9% |
| [Huang et al.](https://datasets-benchmarks-proceedings.neurips.cc/paper_files/paper/2021/file/bd686fd640be98efaae0091fa301e613-Paper-round2.pdf) | 2021 | Random forest | same | Generic, pool of 64 other subjects | Accuracy | 72.2% |

Subject-specific, fine-tuned, LR, DeepConvNet and EEGNet results appear only in figures (Fig. 3, B.1), so they are not copied here. In text, the authors state that generic models beat subject-specific and fine-tuned models on average, and that LR with 30 s windows reaches a mean of 62% in the window-length study.

### Ning 2024 spatial attention (ds004830): per subject, shrinkage LDA, 10 × 5-fold nested CV, 5 s window
| Paper | Year | Method | Input | Protocol | Metric | Result |
|---|---|---|---|---|---|---|
| [Ning et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC10991699/) | 2024 | Shrinkage LDA, HbT HRF area; short-channel GLM fitted in training folds | HbT | 2 classes (L vs R) / 3 classes | CV accuracy | about 73% / about 45% (11 included subjects; per-subject values in the paper's Table 1) |

### FRESH: analysis agreement (not a decoding metric)
| Paper | Year | Setting | Metric | Result |
|---|---|---|---|---|
| [Yücel et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC12322209/) | 2025 | 38 teams, same two datasets, own pipelines | Teams agreeing on group-level results | "nearly 80%" |
| [Yücel et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC12322209/) | 2025 | Dataset II, individual-level H1–H3 | Mean ± SD agreement with expected outcome | 0.44 ± 0.26, 0.51 ± 0.19, 0.54 ± 0.17 |

---

## How to read these numbers

- **Trial/epoch leakage is the main pitfall.** A 10 s trial cut into overlapping 3 s windows (1 s step) gives 8–10 highly autocorrelated samples. If windows from the same trial land in both train and test, accuracy is inflated. Split by trial, block, session or subject, never by window. fNIRSNet explicitly splits folds by trial ([fNIRSNet §III-C](https://doi.org/10.1109/TNSRE.2023.3330911)). Tufts assigns each 80 s block to a single split. Herff et al. note that with 10 trials per class and 10 folds they "never use any data shortly before or after the testing data" because of fNIRS autocorrelation ([PMC3893598](https://pmc.ncbi.nlm.nih.gov/articles/PMC3893598/)).
- **Preprocessing can leak too.** Short-channel or GLM regression, z-scoring, feature selection and channel pruning fitted on all trials leak test information. Ning et al. fit the short-channel GLM inside each training fold for this reason ([PMC10991699](https://pmc.ncbi.nlm.nih.gov/articles/PMC10991699/)). BenchNIRS lists hyperparameter tuning on the test set and overlapping sliding windows across sets as common errors ([PMC10790918](https://pmc.ncbi.nlm.nih.gov/articles/PMC10790918/)).
- **"Max over windows" is selected on test data.** FGANet's "max" columns, Sun et al.'s "best time window", and Shin 2018's peak-of-curve values all choose the window after seeing test accuracy. Compare the "mean" columns, or numbers from a window fixed in advance.
- **Window length and position change the task.** On MA, the same fNIRS-T LOSO is 56.91% with 3 s windows ([fNIRSNet](https://doi.org/10.1109/TNSRE.2023.3330911)) and 78.16% with a whole-trial window that also includes post-task rest ([vision paper](https://ieeexplore.ieee.org/document/9828508)). Tufts finds about 30 s windows work best for workload. Windows that reach into the rest period use the delayed hemodynamic response, which a real-time BCI cannot wait for.
- **Subject-specific vs cross-subject.** Under nested, subject-held-out evaluation, BenchNIRS's LDA reaches only 0.389–0.596 across the five tasks, on datasets where per-subject papers report 70–90%. On Tufts, generic models trained on 64 other subjects beat subject-specific ones on average.
- **Re-runs are not the original numbers.** Most deep-model rows on Shin 2017 and Bak 2019 come from one group's re-implementations (fNIRSNet, vision paper). Baselines re-run by a method's authors are often weaker than in the original papers.
- **Input choices differ.** Some rows use HbO + HbR, some HbT, Tufts adds FD phase, and BenchNIRS averages channels by region. Hybrid rows add EEG, and in FGANet most of the MA gain over fNIRS-only comes from the EEG branch (ESNet 89.14% vs FSNet 82.34% mean).
- **Dataset quirks.** Shin 2018 n-back/DSR blocks have rests too short for the signal to return to baseline. Bak 2019 is overt movement, not imagery. Kernel and FRESH sets were released for reliability and reproducibility, not decoding, so they have no standard split.
