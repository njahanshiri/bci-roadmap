# EEG datasets and benchmark results

EEG has more public datasets than any other brain signal, so this file is split into two parts:

- [Part A: BCI paradigm datasets](#part-a-bci-paradigm-datasets): motor imagery, P300/ERP, SSVEP, error potentials, continuous movement, imagined speech.
- [Part B: Clinical, sleep, affective and large-scale datasets](#part-b-clinical-sleep-affective-and-large-scale-datasets): TUH corpus, seizures, harmful brain activity, emotion, foundation-model pretraining.

Each part has an overview table, full dataset specifications, tables of published results, and notes on how to read the numbers. Results only share a table when they use the same protocol and metric.

---

## Part A: BCI paradigm datasets

This part covers public EEG datasets recorded for brain-computer interface (BCI) paradigms: motor imagery and execution (MI/ME), P300 / event-related potentials (ERP), steady-state visual evoked potentials (SSVEP), error potentials, continuous movement decoding and imagined speech. Every number links to the page or paper where it was read (checked 2026-10-11). "not reported" means the source does not give the value. A number tagged "via X" was read in X's comparison table or text, not in the original paper.

### A.1 Overview

| Dataset | Subjects | Channels | Hz | Paradigm / classes | Sessions | Size | License |
|---|---|---|---|---|---|---|---|
| BCI Competition IV 2a (BNCI2014-001) | 9 | 22 EEG + 3 EOG | 250 | MI, 4 (left hand, right hand, feet, tongue) | 2 (different days) | not reported | CC BY-ND 4.0 (BNCI Horizon copy) |
| BCI Competition IV 2b (BNCI2014-004) | 9 | 3 bipolar EEG + 3 EOG | 250 | MI, 2 (left vs right hand) | 5 | not reported | CC BY-ND 4.0 (BNCI Horizon copy) |
| BCI Competition III IVa | 5 | 118 | 1000 (100 Hz version provided) | MI; 3 cued, 2 scored (right hand vs right foot) | 4 (no feedback) | not reported | Competition terms (cite the data paper) |
| BCI Competition III IIIa | 3 | 60 | 250 | MI, 4 (left hand, right hand, foot, tongue) | not reported | not reported | Competition terms |
| BCI Competition III II (P300 speller) | 2 | 64 | 240 | P300 6×6 speller (36 characters) | 5 per subject | not reported | Competition terms |
| High-Gamma Dataset (Schirrmeister 2017) | 14 in public release (20 in arXiv paper) | 128 (44 motor channels used) | 500 public (5 kHz recorded) | Motor **execution**, 4 (left hand, right hand, feet, rest) | 1 (13 runs) | not reported | CC BY 4.0 |
| PhysioNet EEG Motor Movement/Imagery | 109 | 64 | 160 | ME + MI: left/right fist, both fists/both feet, rest | 1 (14 runs) | 3.4 GB (1.9 GB zip) | ODC-By 1.0 |
| Lee 2019 / OpenBMI | 54 | 62 EEG + EMG (both arms) | 1000 | MI 2 classes; ERP 36-symbol speller; SSVEP 4 targets | 2 (different days) | ~209 GB | Article CC BY 4.0; data license *not verified* |
| Cho 2017 (GigaDB MI) | 52 | 64 EEG + 4 EMG | 512 | MI, 2 (left vs right hand) | 1 | not reported | Article CC BY 4.0; data license *not verified* |
| BNCI2014-009 (covert/overt P300) | 10 | 16 | 256 | P300 speller (overt) + GeoSpell (covert), 36 characters | 3 (description also says 4) | not reported | CC BY-NC-ND 4.0 |
| Brain Invaders 2013a (bi2013a) | 24 | 16 | 512 | P300 game, 36 symbols in 12 groups; target vs non-target | 8 (subjects 1–7) or 1 (8–24) | 9.74 GB (Zenodo, .mat + .csv) | CC BY (Zenodo) |
| Tsinghua SSVEP Benchmark (Wang 2017) | 35 | 64 | 250 (1000 recorded) | SSVEP, 40 targets, 8–15.8 Hz | 6 blocks | not reported | *not verified* |
| BETA (Liu 2020) | 70 | 64 | 250 (1000 recorded) | SSVEP, 40 targets, 8–15.8 Hz | 4 blocks | 5.28 GB (figshare) | CC BY 4.0 (figshare) |
| Nakanishi 2015 (12-class SSVEP) | 10 | 8 | 256 (2048 recorded) | SSVEP, 12 targets, 9.25–14.75 Hz | 15 blocks | not reported | not stated |
| Kaggle BCI Challenge @ NER 2015 (ErrP) | 26 (16 train / 10 test) | 56 EEG + EOG | 200 released (600 recorded) | Feedback error potential: correct vs incorrect | 5 | not reported | Kaggle competition rules |
| Kaggle Grasp-and-Lift / WAY-EEG-GAL | 12 | 32 | 500 | 6 grasp-and-lift events (frame-wise detection) | 10 series | ~15 GB (MATLAB release) | CC BY 4.0 (data paper); Kaggle copy under competition rules |
| Thinking Out Loud (Nieto 2022) | 10 | 128 EEG + 8 EXG | 1024 raw (256 processed) | Inner / pronounced / visualized speech, 4 Spanish words | 3 (one day) | 19.6 GB (OpenNeuro) | CC0 |
| Kara One (Zhao & Rudzicz 2015) | 12 recruited (14 files released) | 64-channel cap + 4 EOG | 1000 | Imagined and spoken speech, 11 prompts | 1 | 24 GB | Free for academic non-profit use |

Sources are in each dataset block below. MOABB, which wraps most of these datasets, is described at the end of A.2.

---

### A.2 Dataset specifications

#### BCI Competition IV 2a
| Field | Value |
|---|---|
| Year & paper | 2008; Brunner, Leeb, Müller-Putz, Schlögl, Pfurtscheller, Graz data set A ([description PDF](https://www.bbci.de/competition/iv/desc_2a.pdf)) |
| Subjects | 9; healthy/age/sex not reported in the description |
| Device & electrodes | 22 Ag/AgCl electrodes, 3.5 cm inter-electrode distance |
| Channels & montage | 22 EEG (10-20 system), monopolar, left mastoid reference, right mastoid ground; 3 monopolar EOG channels (must not be used for classification) |
| Sampling rate | 250 Hz |
| Resolution | not reported (amplifier sensitivity 100 µV for EEG, 1 mV for EOG) |
| Filters | Band-pass 0.5–100 Hz, 50 Hz notch on |
| Paradigm & timing | Cue-based MI: left hand, right hand, both feet, tongue. Fixation cross + tone at t = 0 s, arrow cue at t = 2 s for 1.25 s, imagery until t = 6 s; no feedback. 6 runs × 48 trials (12 per class) = 288 trials per session (72 per class) |
| Sessions | 2 sessions on different days; each starts with ~5 min of EOG calibration (eyes open, closed, eye movements) |
| Size / format | Size not reported; GDF, one file per subject and session (A0xT / A0xE) |
| Access & license | [bbci.de](https://www.bbci.de/competition/iv/) (agree to cite the data paper); [BNCI Horizon](http://bnci-horizon-2020.eu/database/data-sets) copy as 001-2014 under CC BY-ND 4.0 |
| Standard protocol | Session T (training) → session E (evaluation). Competition metric: Cohen's kappa of a causal, continuous classifier output (best time point) |
| Known issues | Expert-marked artifact trials (event 1023); EOG block shorter for A04T; runs separated by NaNs; many deep-learning papers pick the best epoch on session E (see A.4) |

#### BCI Competition IV 2b
| Field | Value |
|---|---|
| Year & paper | 2008; Leeb, Brunner, Müller-Putz, Schlögl, Pfurtscheller, Graz data set B ([description PDF](https://www.bbci.de/competition/iv/desc_2b.pdf)); study first published as ref. [1] of the description (Leeb et al. 2007) |
| Subjects | 9, right-handed, normal or corrected vision, paid; age/sex not reported |
| Device & electrodes | not reported |
| Channels & montage | 3 bipolar channels around C3, Cz, C4 (positions differ slightly per subject); Fz ground; 3 monopolar EOG (left mastoid reference) |
| Sampling rate | 250 Hz |
| Resolution | not reported (dynamic range ±100 µV screening, ±50 µV feedback; ±1 mV EOG) |
| Filters | Band-pass 0.5–100 Hz, 50 Hz notch |
| Paradigm & timing | Left vs right hand MI. Screening sessions: cue 1.25 s, imagery 4 s, 6 runs × 20 trials = 120 trials per session. Feedback ("smiley") sessions: cue from 3 to 7.5 s, 4 runs × 20 trials per class |
| Sessions | 5: 01T, 02T (no feedback, within two weeks), 03T, 04E, 05E (feedback) |
| Size / format | Size not reported; GDF |
| Access & license | [bbci.de](https://www.bbci.de/competition/iv/); [BNCI Horizon](http://bnci-horizon-2020.eu/database/data-sets) 004-2014, CC BY-ND 4.0 |
| Standard protocol | Sessions 1–3 train, sessions 4–5 test; metric kappa |
| Known issues | No EOG calibration block in B0102T and B0504E; only 3 channels, so spatial-filter methods have little room; electrode positions vary per subject |

#### BCI Competition III IVa (Berlin)
| Field | Value |
|---|---|
| Year & paper | 2005; Fraunhofer FIRST / Charité ([description](https://www.bbci.de/competition/iii/desc_IVa.html)); background setup in Dornhege et al. 2004 IEEE TBME |
| Subjects | 5 healthy (aa, al, av, aw, ay); age/sex not reported |
| Device & electrodes | BrainAmp amplifiers, 128-channel Ag/AgCl cap (ECI) |
| Channels & montage | 118 EEG, extended 10/20; no EOG listed |
| Sampling rate | 1000 Hz; a 100 Hz version (every 10th sample) is also provided |
| Resolution | 16-bit, 0.1 µV |
| Filters | Band-pass 0.05–200 Hz |
| Paradigm & timing | Visual cue for 3.5 s: left hand, right hand, right foot; only right hand vs foot used in the competition. Rest 1.75–2.25 s. 280 cues per subject |
| Sessions | 4 initial sessions without feedback |
| Size / format | Size not reported; MATLAB .mat or zipped ASCII |
| Access & license | [bbci.de/competition/iii](https://www.bbci.de/competition/iii/) (agree to cite the data paper) |
| Standard protocol | Fixed per-subject labelled/unlabelled split, designed for "small training sets": train/test trials aa 168/112, al 224/56, av 84/196, aw 56/224, ay 28/252; metric accuracy |
| Known issues | Very unequal training sizes across subjects; one stimulus type may induce target-correlated eye movements |

#### BCI Competition III IIIa (Graz)
| Field | Value |
|---|---|
| Year & paper | 2005; Schlögl (Graz) ([description PDF](https://www.bbci.de/competition/iii/desc_IIIa.pdf)) |
| Subjects | 3 (K3, K6, L1), "ranging from quite good to fair performance"; demographics not reported |
| Device & electrodes | 64-channel Neuroscan amplifier |
| Channels & montage | 60 EEG; left mastoid reference, right mastoid ground |
| Sampling rate | 250 Hz |
| Resolution | not reported |
| Filters | 1–50 Hz, notch on |
| Paradigm & timing | Cue at t = 3 s (arrow for 1 s), imagery until t = 7 s; 4 classes; at least 6 runs × 40 trials; 60 trials per class (summary line) |
| Sessions | not reported |
| Size / format | Size not reported; GDF |
| Access & license | [bbci.de/competition/iii](https://www.bbci.de/competition/iii/) |
| Standard protocol | Labelled vs NaN-labelled trials in one file; metric kappa from continuous outputs |
| Known issues | Only 3 subjects; artifact trials marked visually |

#### BCI Competition III II (Wadsworth P300 speller)
| Field | Value |
|---|---|
| Year & paper | 2005; Krusienski & Schalk, Wadsworth Center ([description PDF](https://www.bbci.de/competition/iii/desc_II.pdf)) |
| Subjects | 2 (A and B); demographics not reported |
| Device & electrodes | BCI2000 P3 Speller; amplifier not reported |
| Channels & montage | 64 EEG |
| Sampling rate | 240 Hz |
| Resolution | not reported (single-precision floats) |
| Filters | Band-pass 0.1–60 Hz |
| Paradigm & timing | 6×6 character matrix; each row/column flashed 100 ms, then 75 ms blank (5.7 Hz); 15 repetitions of 12 flashes per character; 2.5 s blank between characters |
| Sessions | 5 per subject |
| Size / format | Size not reported; MATLAB (train 85 characters, test 100 characters per subject) |
| Access & license | [bbci.de/competition/iii](https://www.bbci.de/competition/iii/) |
| Standard protocol | Predict the 100 test characters; accuracy with all 15 repetitions and with the first 5 |
| Known issues | Only 2 subjects; character epochs scrambled so test words cannot be guessed |

#### High-Gamma Dataset (HGD, Schirrmeister 2017)
| Field | Value |
|---|---|
| Year & paper | 2017; Schirrmeister et al., *Human Brain Mapping* ([doi](https://doi.org/10.1002/hbm.23730), [arXiv](https://arxiv.org/abs/1703.05051)) |
| Subjects | arXiv version: 20 healthy (9 female, 4 left-handed, age 27.5 ± 3.2). Public release and [MOABB loader](https://github.com/NeuroTechX/moabb/blob/develop/moabb/datasets/schirrmeister2017.py): 14 subjects (6 female, 2 left-handed, age 27.2 ± 3.6) |
| Device & electrodes | NeurOne amplifiers (24-bit), 128-channel WaveGuard caps, shielded cabin |
| Channels & montage | 128; papers use the 44 sensors over motor cortex |
| Sampling rate | Recorded at 5 kHz; 500 Hz in the public release ([MOABB](https://github.com/NeuroTechX/moabb/blob/develop/moabb/datasets/schirrmeister2017.py)); resampled to 250 Hz in the paper |
| Resolution | 24-bit |
| Filters | not reported for the release |
| Paradigm & timing | Executed movements: left-hand finger tapping, right-hand finger tapping, toe clenching, rest; 4 s trials, 3–4 s inter-trial interval; 80 trials per run, 13 runs, ~1000 trials per subject |
| Sessions | 1 (13 runs) |
| Size / format | Size not reported; EDF (and earlier HDF5 .mat) on [GIN](https://gin.g-node.org/robintibor/high-gamma-dataset) |
| Access & license | CC BY 4.0 ([LICENSE.txt](https://github.com/robintibor/high-gamma-dataset/blob/master/LICENSE.txt)); also via Braindecode and MOABB |
| Standard protocol | ~880 training trials (all runs but the last two) vs ~160 test trials (last 2 runs) |
| Known issues | Executed, not imagined, movements; subject 14 lost meaningful signal on about half the sensors in the test set ([README](https://github.com/robintibor/high-gamma-dataset)); subject count differs between arXiv paper and release |

#### PhysioNet EEG Motor Movement/Imagery (EEGMMIDB)
| Field | Value |
|---|---|
| Year & paper | 2009; Schalk, PhysioNet ([page](https://physionet.org/content/eegmmidb/1.0.0/), doi 10.13026/C28G6P); BCI2000, Schalk et al. 2004 IEEE TBME |
| Subjects | 109 subject folders (S001–S109); demographics not reported |
| Device & electrodes | BCI2000 system; amplifier not reported |
| Channels & montage | 64, 10-10 system (excluding Nz, F9, F10, FT9, FT10, A1, A2, TP9, TP10, P9, P10) |
| Sampling rate | 160 Hz (subject 88 was recorded at 128 Hz, per the [MOABB loader](https://github.com/NeuroTechX/moabb/blob/develop/moabb/datasets/physionet_mi.py)) |
| Resolution | not reported |
| Filters | not reported |
| Paradigm & timing | 14 runs: 1-min eyes-open and eyes-closed baselines, then 3 × 4 two-minute tasks (real/imagined left/right fist; real/imagined both fists/both feet). Events T0 rest, T1/T2 with run-dependent meaning. Trial length not reported on the page |
| Sessions | 1 |
| Size / format | 3.4 GB uncompressed, 1.9 GB zip; EDF+ |
| Access & license | Open access, Open Data Commons Attribution v1.0 |
| Standard protocol | None official; papers use their own subject splits (e.g., CBraMod: subjects 1–70 train, 71–89 validation, 90–109 test) |
| Known issues | T1/T2 meaning depends on the run number; few trials per class per subject; subject 88 sampling rate |

#### Lee 2019 / OpenBMI (MI, ERP, SSVEP)
| Field | Value |
|---|---|
| Year & paper | 2019; Lee et al., *GigaScience* ([PMC6501944](https://pmc.ncbi.nlm.nih.gov/articles/PMC6501944/)); data on GigaDB (doi 10.5524/100542) |
| Subjects | 54 healthy, age 24–35, 25 female; 38 BCI-naive |
| Device & electrodes | BrainAmp (Brain Products), 62 Ag/AgCl electrodes |
| Channels & montage | 62 EEG, nasion reference, AFz ground; one EMG electrode on each arm's flexor digitorum profundus (olecranon reference) |
| Sampling rate | 1000 Hz (paper's analyses downsample to 100 Hz) |
| Resolution | not reported |
| Filters | not reported for recording |
| Paradigm & timing | **ERP**: 6×6 row-column speller with random-set presentation and face stimuli; 80 ms flash, 135 ms ISI; 5 sequences per character; 1,980 training and 2,160 test epochs. **MI**: left/right hand grasping, 3 s fixation, 4 s imagery, 6 ± 1.5 s blank; 100 training + 100 test trials. **SSVEP**: 4 targets at 5.45, 6.67, 8.57, 12 Hz; 4 s stimulus, 6 s ISI; 100 training + 100 test trials |
| Sessions | 2 on different days; each paradigm has an offline training phase and an online test phase |
| Size / format | ~209 GB in 433 files; MATLAB .mat |
| Access & license | Article CC BY 4.0; dataset license on GigaDB *not verified* (gigadb.org did not render) |
| Standard protocol | Per session: offline (training) phase → online (test) phase; MI also reported with 10 × 10-fold CV (CSP-cv) |
| Known issues | Large MI performance spread (53.7% of subjects labelled "MI illiterate" at a 70% threshold); paradigms recorded in fixed order (ERP, MI, SSVEP) |

#### Cho 2017 (GigaDB MI)
| Field | Value |
|---|---|
| Year & paper | 2017; Cho et al., *GigaScience* ([PMC5493744](https://pmc.ncbi.nlm.nih.gov/articles/PMC5493744/)); data GigaDB (doi 10.5524/100295) |
| Subjects | 52 healthy, 19 female, age 24.8 ± 3.86; 50 right-handed, 2 both-handed |
| Device & electrodes | Biosemi ActiveTwo, 64 Ag/AgCl active electrodes; BCI2000 3.0.2 |
| Channels & montage | 64 EEG (10-10) + 4 EMG (flexor digitorum profundus and extensor digitorum, both arms); 3D electrode positions digitized |
| Sampling rate | 512 Hz |
| Resolution | not reported |
| Filters | not reported |
| Paradigm & timing | Left vs right hand MI (kinesthetic finger-to-thumb sequence): 2 s fixation, 3 s cue/imagery, 4.1–4.8 s break; 100 or 120 trials per class; plus 20 real-movement trials per class and 6 types of noise/rest recordings |
| Sessions | 1 (5–6 MI runs) |
| Size / format | Size not reported; MATLAB .mat; questionnaire .xlsx |
| Access & license | Article CC BY 4.0; dataset license *not verified* |
| Standard protocol | Paper: CSP + FLDA, 7/10 of trials train and 3/10 test, repeated 120 times |
| Known issues | Subjects s29 and s34 flagged as EMG-contaminated and excluded by the authors; bad-trial indices supplied; 14 of 52 subjects below the chance limit |

#### BNCI2014-009 (covert and overt ERP speller)
| Field | Value |
|---|---|
| Year & paper | 2014; Aricò et al., *J. Neural Eng.* 11:035008 (ref. [5] of the [description PDF](http://bnci-horizon-2020.eu/database/data-sets/009-2014/description.pdf)) |
| Subjects | 10 healthy, all female, age 26.8 ± 5.6, experienced with P300 BCIs |
| Device & electrodes | g.USBamp (g.tec), 16 Ag/AgCl electrodes on an Electro-Cap |
| Channels & montage | Fz, FCz, Cz, CPz, Pz, Oz, F3, F4, C3, C4, CP3, CP4, P3, P4, PO7, PO8; linked-earlobe reference, right mastoid ground |
| Sampling rate | 256 Hz |
| Resolution | not reported |
| Filters | High-pass 0.1 Hz, low-pass 20 Hz |
| Paradigm & timing | P300 Speller (overt attention, 6×6 matrix) and GeoSpell (covert attention, 6 characters on a hexagon); 2 s target prompt; 8 sequences = 16 target flashes per trial; 125 ms flash + 125 ms ISI (250 ms SOA) |
| Sessions | "3 recording sessions" and "4 recording sessions" both appear in the description; 3 runs per interface per session |
| Size / format | Size not reported; .mat files A01S/A01G … A10S/A10G |
| Access & license | [BNCI Horizon](http://bnci-horizon-2020.eu/database/data-sets), CC BY-NC-ND 4.0 |
| Standard protocol | None official; MOABB uses within-session 5-fold CV on target vs non-target epochs |
| Known issues | Session count inconsistent in the description; all-female sample |

#### Brain Invaders 2013a (bi2013a)
| Field | Value |
|---|---|
| Year & paper | Recorded 2013; Vaineau et al. technical report 2019 ([arXiv:1904.09111](https://arxiv.org/abs/1904.09111)); data on [Zenodo](https://doi.org/10.5281/zenodo.1494163) |
| Subjects | 24 (12 female), age 25.96 ± 4.46; 7 of them (4 female) also did the longitudinal study |
| Device & electrodes | g.USBamp + g.GAMMAcap, 16 wet Ag/AgCl electrodes; OpenViBE |
| Channels & montage | FP1, FP2, F5, AFZ, F6, T7, CZ, T8, P7, P3, PZ, P4, P8, O1, OZ, O2; left earlobe reference, FZ ground |
| Sampling rate | 512 Hz |
| Resolution | not reported |
| Filters | None applied during acquisition |
| Paradigm & timing | Brain Invaders P300 game: 36 symbols in 12 flash groups; a repetition is 12 flashes (2 target, 10 non-target). Training phase: 80 target + 400 non-target flashes. Online phase length varies with performance. Adaptive (calibration-free Riemannian) vs non-adaptive runs |
| Sessions | Subjects 1–7: 8 sessions on different days; subjects 8–24: 1 session; 2 runs per session |
| Size / format | 9.74 GB, 73 files on Zenodo (.mat and .csv, plus meta.yml) |
| Access & license | CC BY (Zenodo record) |
| Standard protocol | Balanced accuracy recommended in the report (1:5 class imbalance); MOABB uses ROC-AUC |
| Known issues | Online-phase trial count depends on game performance; the adaptive condition was initialized with grand averages from another Brain Invaders database |

#### Tsinghua SSVEP Benchmark (Wang 2017)
| Field | Value |
|---|---|
| Year & paper | 2017; Wang, Chen, Gao, Gao, *IEEE TNSRE* (doi 10.1109/TNSRE.2016.2627556; paper not read, specs from the official [Readme.txt](http://bci.med.tsinghua.edu.cn/upload/yijun/Readme.txt)) |
| Subjects | 35 healthy, 17 female, age 17–34 (mean 22); 8 experienced (S01–S08), 27 naive |
| Device & electrodes | Neuroscan Synamps2 |
| Channels & montage | 64, 10-20 system; vertex reference, ground between Fz and FPz |
| Sampling rate | 1000 Hz recorded, epochs downsampled to 250 Hz |
| Resolution | not reported (stored as double) |
| Filters | Amplifier passband 0.15–200 Hz, 50 Hz notch |
| Paradigm & timing | 40-target speller, 8–15.8 Hz in 0.2 Hz steps (joint frequency-phase modulation); 0.5 s cue, 5 s flicker, 0.5 s blank. Epochs: 0.5 s pre to 5.5 s post onset, `data` = [64 × 1500 × 40 × 6] |
| Sessions | 6 blocks of 40 trials (one per target) |
| Size / format | Size not reported; one .mat per subject (.7z) |
| Access & license | [Download page](http://bci.med.tsinghua.edu.cn/download.html); license *not verified* |
| Standard protocol | Leave-one-block-out (train on 5 blocks, test on 1); accuracy and ITR vs data length, with a 0.5 or 0.55 s gaze-shift time |
| Known issues | Recorded in a shielded room, so higher SNR than BETA; MOABB's `Wang2016` loader exposes 34 subjects (`range(1, 35)`) ([source](https://github.com/NeuroTechX/moabb/blob/develop/moabb/datasets/ssvep_wang.py)) |

#### BETA (Liu 2020)
| Field | Value |
|---|---|
| Year & paper | 2020; Liu, Huang, Wang, Chen, Gao, *Front. Neurosci.* ([PMC7324867](https://pmc.ncbi.nlm.nih.gov/articles/PMC7324867/)) |
| Subjects | 70 healthy (42 male, 28 female), age 25.14 ± 7.97 (9–64); all from the BCI 2018 Olympics SSVEP track, none naive |
| Device & electrodes | Neuroscan SynAmps2 |
| Channels & montage | 64, 10-10, Cz reference |
| Sampling rate | 1000 Hz recorded, 250 Hz released |
| Resolution | not reported |
| Filters | Hardware 0.15–200 Hz, 50 Hz notch; released epochs band-passed 3–100 Hz |
| Paradigm & timing | 40-target QWERTY speller, 8–15.8 Hz; 0.5 s cue, flicker ≥2 s (S1–S15) or ≥3 s (S16–S70), 0.5 s rest |
| Sessions | 4 blocks × 40 trials, online with FBCCA feedback, outside a shielded room |
| Size / format | 5.28 GB on [figshare](https://figshare.com/articles/The_BETA_database/12264401) (72 files); one .mat per subject |
| Access & license | CC BY 4.0 (figshare) |
| Standard protocol | Leave-one-block-out over 4 blocks; ITR with 0.55 s gaze shift (paper) |
| Known issues | Two trial lengths (2 s vs 3 s); lower SNR than the Benchmark by design |

#### Nakanishi 2015 (12-class SSVEP)
| Field | Value |
|---|---|
| Year & paper | 2015; Nakanishi et al., *PLoS One* ([PMC4610694](https://pmc.ncbi.nlm.nih.gov/articles/PMC4610694/)) |
| Subjects | 10 healthy (9 male, 1 female), mean age 28 |
| Device & electrodes | BioSemi ActiveTwo, 8 Ag/AgCl electrodes over occipital area |
| Channels & montage | 8, referenced to CMS near Cz |
| Sampling rate | 2048 Hz recorded; epochs downsampled to 256 Hz |
| Resolution | not reported |
| Filters | Analysis epochs band-passed 6–80 Hz (zero-phase IIR) |
| Paradigm & timing | 12 targets as a phone keypad, 9.25–14.75 Hz in 0.5 Hz steps, phase step 0.5π; 1 s cue, 4 s flicker |
| Sessions | 15 blocks × 12 trials (simulated online) |
| Size / format | Size not reported; data at ftp://sccn.ucsd.edu/pub/cca_ssvep |
| Access & license | Data license not stated (article CC BY) |
| Standard protocol | Leave-one-block-out (14 train, 1 test); ITR with 1 s gaze shift |
| Known issues | Earlier MOABB versions exposed only subjects 1–9 ([source](https://github.com/NeuroTechX/moabb/blob/develop/moabb/datasets/ssvep_nakanishi.py)) |

#### Kaggle BCI Challenge @ NER 2015 (feedback error potentials)
| Field | Value |
|---|---|
| Year & paper | Competition Nov 2014 – Feb 2015, sponsored by INRIA (dates/sponsor *unverified*: Kaggle pages did not render) ([Kaggle](https://www.kaggle.com/c/inria-bci-challenge)); data description from the Kaggle data/description pages and [EEGNet](https://arxiv.org/abs/1611.08024) |
| Subjects | 26 healthy (13 male), age 28.8 ± 5.4 (20–37), all BCI-naive (demographics *unverified*); 16 train, 10 test |
| Device & electrodes | 56 passive Ag/AgCl sensors (VSM-CTF compatible) |
| Channels & montage | 56 EEG, extended 10-20, nose reference, shoulder ground (reference/ground *unverified*); plus an EOG derivation |
| Sampling rate | 600 Hz recorded; released at 200 Hz |
| Resolution | not reported |
| Filters | not reported |
| Paradigm & timing | P300 speller copy-spelling; after each selection the chosen item is shown; label = feedback correct vs incorrect. Fast (4 flashes per item) and slow (8 flashes) modes (*unverified*) |
| Sessions | 5 per subject: 60 feedbacks in sessions 1–4, 100 in session 5 (340 per subject) |
| Size / format | Size not reported; CSV per subject and session |
| Access & license | Kaggle, "Subject to Competition Rules" |
| Standard protocol | Cross-subject: train on 16 subjects, test on 10 unseen subjects; metric ROC-AUC over all test feedbacks pooled |
| Known issues | Timing leak in session 5 reveals the online error detector's output; submitting only per-subject class-balance estimates scored 0.746 private AUC ([winner write-up](https://github.com/alexandrebarachant/bci-challenge-ner-2015)) |

#### Kaggle Grasp-and-Lift EEG Detection / WAY-EEG-GAL
| Field | Value |
|---|---|
| Year & paper | 2014 data paper: Luciw, Jarocka, Edin, *Sci. Data* 1:140047 ([PMC4365902](https://pmc.ncbi.nlm.nih.gov/articles/PMC4365902/)); Kaggle competition Jun–Aug 2015 (dates *unverified*) ([Kaggle](https://www.kaggle.com/c/grasp-and-lift-eeg-detection)) |
| Subjects | 12 right-handed, 8 female, age 19–35 |
| Device & electrodes | BrainAmp + ActiCap (32 electrodes); 5 EMG; force, position and kinematic sensors |
| Channels & montage | 32 EEG |
| Sampling rate | Amplifier sampled at 5 kHz, stored at 500 Hz; EMG 4 kHz |
| Resolution | not reported |
| Filters | Hardware 0.016–1000 Hz; anti-alias low-pass for 500 Hz |
| Paradigm & timing | Reach, grasp, lift, hold, replace an object with unpredictable weight (165/330/660 g) and surface (sandpaper/suede/silk). Kaggle task: 6 events (HandStart, FirstDigitTouch, BothStartLoadPhase, LiftOff, Replace, BothReleased), each labelled ±150 ms around the event |
| Sessions | 10 series per subject (~30 trials each), 3,936 trials in total |
| Size / format | ~15 GB MATLAB structures (figshare); Kaggle copy as CSV |
| Access & license | Data paper: CC BY 4.0. Kaggle copy: competition rules |
| Standard protocol | Kaggle: series 1–8 train, series 9–10 test; mean column-wise AUC; no future samples may be used |
| Known issues | Labels are windows around events, not movement intention; strong temporal structure between events lets sequence models exploit event order |

#### Thinking Out Loud (inner speech)
| Field | Value |
|---|---|
| Year & paper | 2022; Nieto et al., *Sci. Data* ([PMC8844234](https://pmc.ncbi.nlm.nih.gov/articles/PMC8844234/)); [OpenNeuro ds003626](https://openneuro.org/datasets/ds003626) |
| Subjects | 10 healthy right-handed, 4 female, mean age 34 (sd 10) |
| Device & electrodes | BioSemi ActiveTwo |
| Channels & montage | 128 EEG + 8 external: EXG1–2 earlobe references, EXG3–6 horizontal/vertical EOG, EXG7–8 used for mouth-EMG control |
| Sampling rate | 1024 Hz raw; processed data decimated to 256 Hz (the text says "254 Hz" once) |
| Resolution | 24-bit |
| Filters | Acquisition: 208 Hz low-pass only. Processed: 0.5–100 Hz band-pass, 50 Hz notch, ICA |
| Paradigm & timing | Spanish words "arriba", "abajo", "derecha", "izquierda" (up, down, right, left) in 3 conditions: pronounced, inner speech, visualized; 4.5 s epochs |
| Sessions | 3 consecutive sessions in one day; 200 trials in sessions 1 and 2, session 3 varies |
| Size / format | 19.6 GB (snapshot 2.1.2); BIDS, .bdf raw, .fif epochs |
| Access & license | CC0 (OpenNeuro) |
| Standard protocol | None defined in the data paper |
| Known issues | 115 trials (2.5%) flagged for mouth EMG; sub-03 swapped condition runs in sessions 1 and 3 |

#### Kara One (imagined and spoken phonemes)
| Field | Value |
|---|---|
| Year & paper | 2015; Zhao & Rudzicz, ICASSP 2015 ([paper PDF](http://www.cs.toronto.edu/~complingweb/data/karaOne/ZhaoRudzicz15.pdf), [dataset page](http://www.cs.toronto.edu/~complingweb/data/karaOne/karaOne.html)) |
| Subjects | Paper: 12 recruited (4 female, 8 male), mean age 27.4; data from 4 discarded. Dataset page: 14 participant archives |
| Device & electrodes | 64-channel Neuroscan Quick-cap, SynAmps RT; Kinect face tracking and audio |
| Channels & montage | 64-channel cap (62 EEG channels used in the analyses) + 4 EOG electrodes |
| Sampling rate | 1 kHz |
| Resolution | not reported |
| Filters | Analysis: 1–50 Hz, ocular artifact removal, small Laplacian |
| Paradigm & timing | 7 phonemic/syllabic prompts (/iy/, /uw/, /piy/, /tiy/, /diy/, /m/, /n/) + 4 words (pat, pot, knew, gnaw); per trial 5 s rest, stimulus, 5 s imagined speech, then spoken; 12 repetitions, 132 trials |
| Sessions | 1 (30–40 min) |
| Size / format | 24 GB, one .tar.bz2 per participant |
| Access & license | Free for academic (non-profit) use, cite the paper |
| Standard protocol | Paper: subject-independent leave-one-subject-out; binary phonological tasks (C/V, ±Nasal, ±Bilabial, ±/iy/, ±/uw/) |
| Known issues | Participant count differs between paper (12 recruited, 4 discarded) and release (14 files); some reported binary accuracies are far below 50% (see A.3) |

#### MOABB (aggregator)
[MOABB](https://pypi.org/project/moabb/) (Mother of All BCI Benchmarks; v1.7.2 on PyPI, BSD-3-Clause) is a Python library that downloads public BCI datasets through one API, applies a paradigm (MI, P300, SSVEP, c-VEP) and runs standard evaluations (within-session, cross-session, cross-subject). Its develop-branch summary tables list 106 imagery, 69 P300, 18 SSVEP and 8 c-VEP dataset rows ([summary CSVs](https://github.com/NeuroTechX/moabb/tree/develop/moabb/datasets)). The 2024 benchmark paper ([Chevallier et al., arXiv:2404.15319](https://arxiv.org/abs/2404.15319)) re-implements 30 pipelines (11 raw-signal, 13 Riemannian, 6 deep learning) on 36 datasets (14 MI, 15 P300, 7 SSVEP). Its main evaluation is **within-session 5-fold stratified CV over shuffled trials**, which the authors call an upper bound compared with online use. Metric: ROC-AUC for 2-class tasks, accuracy for more classes. MOABB names used below: BNCI2014-001 = IV 2a, BNCI2014-004 = IV 2b, Schirrmeister2017 = HGD, Wang2016 = Tsinghua Benchmark, BrainInvaders2013a = bi2013a.

---

### A.3 Published results

Within a table, rows share protocol and metric unless marked. "Own" = number reported by the method's authors; "rerun" = method re-implemented by the citing paper.

#### BCI IV 2a: competition (session E), kappa
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| Ang et al. (1st), [results](https://www.bbci.de/competition/iv/results/) | 2008 | Filter Bank CSP + Naive Bayes Parzen window | T → E, causal | Kappa | 0.57 |
| Liu Guangquan et al. (2nd), [results](https://www.bbci.de/competition/iv/results/) | 2008 | CSP 8–30 Hz + LDA/Bayes | T → E | Kappa | 0.52 |
| Wei Song et al. (3rd), [results](https://www.bbci.de/competition/iv/results/) | 2008 | CSP + SVM ensemble | T → E | Kappa | 0.31 |

#### BCI IV 2a: within-subject, session T → session E, 4 classes, accuracy (numbers as reported by each paper's own pipeline)
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Schirrmeister et al.](https://arxiv.org/abs/1703.05051) | 2017 | FBCSP / Deep ConvNet / Shallow ConvNet | T → E, 0.5–4 s, 0–38 Hz | Accuracy | 68.0% / 70.9% / 73.7% (FBCSP + reported differences +2.9 and +5.7, Table 2) |
| [Ingolfsson et al. (EEG-TCNet)](https://arxiv.org/abs/2006.00622) | 2020 | EEG-TCNet, fixed hyperparameters | T → E | Accuracy / kappa | 77.35% / 0.70 |
| [Ingolfsson et al.](https://arxiv.org/abs/2006.00622) | 2020 | EEGNet / Shallow ConvNet (rerun) | T → E | Accuracy | 72.40% / 74.31% |
| [Ingolfsson et al.](https://arxiv.org/abs/2006.00622) | 2020 | EEG-TCNet, per-subject hyperparameters | T → E; **not directly comparable** (hyperparameters tuned per subject) | Accuracy / kappa | 83.84% / 0.78 |
| [Song et al. (EEG Conformer)](https://ieeexplore.ieee.org/document/9991178) | 2023 | EEG Conformer, with S&R augmentation | T → E | Accuracy / kappa | 78.66% / 0.7155 |
| [Song et al.](https://ieeexplore.ieee.org/document/9991178) | 2023 | FBCSP / ConvNet / EEGNet (in-paper comparison) | T → E | Accuracy | 67.75% / 72.53% / 74.50% |

#### BCI IV 2a: within-subject T → E, re-implementations in a single pipeline
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [ATCNet repo README](https://github.com/Altaheri/EEG-ATCNet) | 2023 | ATCNet / EEG-TCNet / EEGNet / ShallowConvNet / DeepConvNet | `main_TrainValTest.py` (validation split from training session), 500 epochs | Accuracy | 81.10% / 65.36% / 68.67% / 67.48% / 42.78% |
| [Altaheri et al. (TCFormer)](https://www.nature.com/articles/s41598-025-16219-7), [README](https://github.com/Altaheri/TCFormer) | 2025 | EEGNet (rerun) | T → E, last-epoch checkpoint, 5 runs; −aug / +aug | Accuracy | 70.39% / 72.62% |
| same | 2025 | ShallowNet (rerun) | same | Accuracy | 60.50% / 65.72% |
| same | 2025 | EEG-TCNet (rerun) | same | Accuracy | 75.62% / 78.82% |
| same | 2025 | EEG Conformer (rerun) | same | Accuracy | 70.70% / 75.39% |
| same | 2025 | ATCNet (rerun) | same | Accuracy | 83.40% / 83.78% |
| same | 2025 | TCFormer | same | Accuracy | 83.06% / 84.79% |

The ATCNet paper's own headline number (IEEE TII 2023) is paywalled and was not read; the README notes that the paper's original `main_TrainTest.py` evaluation "does not align with current best practices".

#### BCI IV 2a: cross-subject (leave one subject out)
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [TCFormer](https://www.nature.com/articles/s41598-025-16219-7), [README](https://github.com/Altaheri/TCFormer) | 2025 | EEGNet / ShallowNet / EEG-TCNet / EEG Conformer (rerun) | LOSO, −aug | Accuracy | 52.01% / 48.83% / 55.09% / 45.44% |
| same | 2025 | ATCNet (rerun) / TCFormer | LOSO, −aug / +aug | Accuracy | 60.05% / 59.66%; 62.44% / 63.00% |

Foundation models, LOSO with **linear probing** ([EEGPT, NeurIPS 2024, Table 4](https://papers.neurips.cc/paper_files/paper/2024/file/4540d267eeec4e5dbd9dae9448f0b739-Paper-Conference.pdf)). Different metric (balanced accuracy) and frozen encoders, so not directly comparable with the table above:

| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| BENDR, in [EEGPT](https://papers.neurips.cc/paper_files/paper/2024/file/4540d267eeec4e5dbd9dae9448f0b739-Paper-Conference.pdf) | 2024 | Pretrained transformer (full fine-tuning per EEGPT text) | LOSO | Balanced acc. / kappa | 0.4899 / 0.3199 |
| BIOT, in EEGPT | 2024 | Pretrained, linear probe | LOSO | Balanced acc. / kappa | 0.4590 / 0.2787 |
| LaBraM, in EEGPT | 2024 | Pretrained, linear probe | LOSO | Balanced acc. / kappa | 0.5613 / 0.4151 |
| [EEGPT](https://papers.neurips.cc/paper_files/paper/2024/file/4540d267eeec4e5dbd9dae9448f0b739-Paper-Conference.pdf) | 2024 | 10M-param pretrained transformer, linear probe | LOSO | Balanced acc. / kappa | 0.5846 / 0.4462 |

#### BCI IV 2a (BNCI2014-001): MOABB within-session 5-fold CV. Not comparable with T → E
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Chevallier et al. (MOABB benchmark), Table D1](https://arxiv.org/abs/2404.15319) | 2024 | CSP+LDA / FBCSP+SVM / MDM / FgMDM | Within-session, "all labels" (Table 1 lists the dataset as "3(4)" classes, so tongue inclusion is unclear) | Accuracy | 65.99% / 66.53% / 61.60% / 70.14% |
| same | 2024 | TS+LR / TS+SVM / TS+EL / ACM+TS+SVM | same | Accuracy | 71.97% / 70.76% / 72.38% / 77.82% |
| same | 2024 | ShallowConvNet / EEGNet-8,2 / EEG-TCNet / DeepConvNet | same | Accuracy | 72.47% / 60.46% / 41.65% / 35.29% |
| same, Table D2 | 2024 | CSP+LDA / MDM / TS+LR / ACM+TS+SVM / ShallowConvNet / EEGNet-8,2 | Within-session, left vs right hand | ROC-AUC | 82.34 / 81.69 / 87.41 / 91.71 / 86.17 / 77.15 |

#### BCI IV 2b: competition (sessions 4–5), kappa
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| Chin et al. (1st), [results](https://www.bbci.de/competition/iv/results/) | 2008 | FBCSP + Naive Bayes Parzen window | Sessions 1–3 → 4–5 | Kappa | 0.60 |
| Huang Gan et al. (2nd), [results](https://www.bbci.de/competition/iv/results/) | 2008 | CSSD + LDA | same | Kappa | 0.58 |
| Coyle et al. (3rd), [results](https://www.bbci.de/competition/iv/results/) | 2008 | NTSPP + CSP + LDA/SVM | same | Kappa | 0.46 |

#### BCI IV 2b: within-subject, sessions 1–3 → 4–5, accuracy
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Song et al. (EEG Conformer)](https://ieeexplore.ieee.org/document/9991178) | 2023 | FBCSP / ConvNet / EEGNet (in-paper) | own pipeline | Accuracy | 80.00% / 79.37% / 80.48% |
| [Song et al.](https://ieeexplore.ieee.org/document/9991178) | 2023 | EEG Conformer | own pipeline | Accuracy / kappa | 84.63% / 0.6926 |
| [TCFormer](https://www.nature.com/articles/s41598-025-16219-7), [README](https://github.com/Altaheri/TCFormer) | 2025 | EEGNet / EEG-TCNet / EEG Conformer / ATCNet (rerun) | unified pipeline, last epoch; −aug / +aug | Accuracy | 82.80/83.65; 85.54/86.74; 79.46/81.89; 86.25/86.26 |
| same | 2025 | TCFormer | same | Accuracy | 87.11% / 87.71% |

Cross-subject 2b: TCFormer LOSO (−aug/+aug) EEGNet 77.67/77.89, EEG Conformer 73.44/75.25, ATCNet 80.29/80.94, TCFormer 79.73/81.34 ([README](https://github.com/Altaheri/TCFormer)). EEGPT LOSO linear probe, balanced accuracy / kappa: BENDR 0.7067/0.4131, BIOT 0.6409/0.2817, LaBraM 0.6851/0.3703, EEGPT 0.7212/0.4426 ([EEGPT Table 4](https://papers.neurips.cc/paper_files/paper/2024/file/4540d267eeec4e5dbd9dae9448f0b739-Paper-Conference.pdf)). MOABB within-session ROC-AUC (BNCI2014-004, [Table D2](https://arxiv.org/abs/2404.15319)): CSP+LDA 80.10, FBCSP+SVM 80.39, MDM 77.66, TS+LR 80.09, ACM+TS+SVM 82.67, ShallowConvNet 72.36, EEGNet-8,2 69.50.

#### BCI Competition III IVa: competition, accuracy on unlabelled trials (right hand vs foot)
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| Yijun Wang et al. (1st), [results](https://www.bbci.de/competition/iii/results/) | 2005 | CSP + AR + readiness-potential features, LDA, self-training on test | Official split | Accuracy | 94.17% |
| Yuanqing Li et al. (2nd), [results](https://www.bbci.de/competition/iii/results/) | 2005 | CSP (mu/beta) + extended EM | Official split | Accuracy | 85.12% |
| Liu Yang et al. (3rd), [results](https://www.bbci.de/competition/iii/results/) | 2005 | CSP + wavelet correlation features | Official split | Accuracy | 83.45% |

Per subject for the winner: aa 95.5%, al 100%, av 80.6%, aw 100%, ay 97.6% (ay has only 28 training trials).

#### BCI Competition III IIIa: competition, kappa
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| Cuntai Guan et al. (1st), [results](https://www.bbci.de/competition/iii/results/) | 2005 | Fisher-ratio band selection + multiclass CSP + SVM | Official split | Kappa | 0.7926 |
| Gao Xiaorong et al. (2nd), [results](https://www.bbci.de/competition/iii/results/) | 2005 | Laplacian + CSP (one-vs-rest) + SVM/kNN/LDA bagging | same | Kappa | 0.6872 |
| Jeremy Hill et al. (3rd), [results](https://www.bbci.de/competition/iii/results/) | 2005 | ICA + spectra + PCA + SVM | same | Kappa | 0.6272 |

#### BCI Competition III II (P300 speller): character accuracy on 100 test characters per subject
| Paper | Year | Method | Protocol | Metric | Result (15 / 5 repetitions) |
|---|---|---|---|---|---|
| Rakotomamonjy & Guigue (1st), [results](https://www.bbci.de/competition/iii/results/) | 2005 | not described on the page | Official split | Character accuracy | 96.5% / 73.5% |
| Li Yandong et al. (2nd), [results](https://www.bbci.de/competition/iii/results/) | 2005 | not described on the page | same | Character accuracy | 90.5% / 55.0% |
| Zhou Zongtan et al. (3rd), [results](https://www.bbci.de/competition/iii/results/) | 2005 | not described on the page | same | Character accuracy | 90.0% / 59.5% |

Chance is 2.8% (1/36). The results page only links a text description of each method, which I did not read.

#### High-Gamma Dataset: within-subject, last 2 runs as test, 4 classes, accuracy
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Schirrmeister et al.](https://arxiv.org/abs/1703.05051) | 2017 | FBCSP / Deep ConvNet / Shallow ConvNet | 0–125 Hz (arXiv: 20 subjects) | Accuracy | 91.2% / 92.5% / 89.3% (FBCSP + reported differences) |
| [Schirrmeister et al.](https://arxiv.org/abs/1703.05051) | 2017 | FBCSP / Deep / Shallow | 4–125 Hz | Accuracy | 90.9% / 91.4% / 93.9% |
| [HGD README reproduction](https://github.com/robintibor/high-gamma-dataset) | — | Deep / Shallow (braindecode `example.py`, 3 seeds) | README column "Lowpass [Hz]" = 0 / 4 (the paper's 0–f_end and 4–f_end bands) | Accuracy | Deep 92.3% / 92.2%; Shallow 88.9% / 94.6% |
| [ATCNet README](https://github.com/Altaheri/EEG-ATCNet) | 2023 | ATCNet / EEG-TCNet / EEGNet / Shallow / Deep | Train-Val-Test script | Accuracy | 92.05% / 87.80% / 88.25% / 87.00% / 87.53% |
| [TCFormer](https://www.nature.com/articles/s41598-025-16219-7), [README](https://github.com/Altaheri/TCFormer) | 2025 | EEGNet / EEG Conformer / ATCNet / TCFormer | unified pipeline, 3 runs, −aug / +aug | Accuracy | 85.59/85.94; 93.60/94.67; 93.65/95.08; 95.62/96.27 |

Cross-subject HGD (TCFormer, LOSO, −aug): EEGNet 57.95%, ShallowNet 72.47%, EEG Conformer 69.21%, ATCNet 67.42%, TCFormer 71.90% with a deeper N = 5 encoder (72.83% with augmentation) ([README](https://github.com/Altaheri/TCFormer)). MOABB within-session 5-fold CV, 14 subjects, all classes ([Table D1](https://arxiv.org/abs/2404.15319)): CSP+LDA 72.97%, FBCSP+SVM 75.94%, MDM 52.03%, TS+EL 85.53%, ShallowConvNet 85.13%, EEGNet-8,2 76.99%, DeepConvNet 56.78%.

#### PhysioNet MI: cross-subject, 4 classes (left fist, right fist, both fists, both feet)
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| EEGNet, in [CBraMod Table 3](https://arxiv.org/abs/2412.07236) | 2025 | CNN | Subjects 1–70 / 71–89 / 90–109; 4 s windows at 200 Hz | Balanced acc. / kappa | 0.5814 / 0.4468 |
| EEG Conformer, in CBraMod | 2025 | CNN-transformer | same | Balanced acc. / kappa | 0.6049 / 0.4736 |
| BIOT, in CBraMod | 2025 | Pretrained transformer | same | Balanced acc. / kappa | 0.6153 / 0.4875 |
| LaBraM-Base, in CBraMod | 2025 | Pretrained transformer | same | Balanced acc. / kappa | 0.6173 / 0.4912 |
| [Wang et al. (CBraMod, ICLR 2025)](https://arxiv.org/abs/2412.07236) | 2025 | Criss-cross pretrained transformer, fine-tuned | same | Balanced acc. / kappa | 0.6417 / 0.5222 |

Not directly comparable: MOABB within-session 5-fold CV ([Table D1](https://arxiv.org/abs/2404.15319), all labels): CSP+LDA 47.73%, FBCSP+SVM 45.49%, MDM 42.96%, TS+SVM 58.46%, TS+EL 59.93%, ShallowConvNet 41.87%, EEGNet-8,2 29.04%; left vs right ROC-AUC ([Table D2](https://arxiv.org/abs/2404.15319)): CSP+LDA 65.75, TS+SVM 68.18, FgMDM 68.46, ShallowConvNet 65.19. CSP + FLDA on 109 subjects, 60.42%, via [Cho et al. 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5493744/) (their ref. [20], protocol not stated).

#### Lee 2019 / OpenBMI: dataset paper baselines (offline training phase → online test phase, per session)
| Paper | Year | Method | Protocol | Metric | Result (session 1 / session 2) |
|---|---|---|---|---|---|
| [Lee et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC6501944/) | 2019 | MI: CSP / CSSP / FBCSP / BSSFO (+LDA) | Train phase → test phase | Accuracy | 67.2/68.5; 69.6/69.6; 68.8/70.5; 67.9/71.1% |
| [Lee et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC6501944/) | 2019 | MI: CSP-cv | **Not comparable**: 10 × 10-fold CV over train + test trials | Accuracy | 70.1 / 72.2% |
| [Lee et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC6501944/) | 2019 | ERP: mean-amplitude features + LDA, 5 sequences | Train phase → online test | Accuracy / ITR | 96.5/96.9%; 21.1/21.2 bits/min |
| [Lee et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC6501944/) | 2019 | SSVEP: multi-channel CCA, 4 s epochs, 10 occipital channels | All trials (training-free) | Accuracy | 94.9 / 95.4% |

MOABB within-session ([Tables D2, D4, D5](https://arxiv.org/abs/2404.15319)): Lee2019-MI ROC-AUC CSP+LDA 76.88, TS+EL 84.74, ShallowConvNet 75.83, EEGNet-8,2 65.67; Lee2019-ERP ROC-AUC XDAWN+LDA 96.45, XDAWNCov+MDM 97.70, XDAWNCov+TS+SVM 98.41; Lee2019-SSVEP accuracy (1 s trials) CCA 23.86%, TRCA 64.01%, MDM 75.38%, TS+LR 89.44%.

#### Cho 2017: within-subject left vs right MI
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Cho et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC5493744/) | 2017 | CSP (2 filters per class) + FLDA, 8–30 Hz, 0.5–2.5 s | 7/10 train, 3/10 test, 120 repeats; 50 subjects | Accuracy | 67.46 ± 13.17% |
| [MOABB, Table D2](https://arxiv.org/abs/2404.15319) | 2024 | CSP+LDA / MDM / TS+EL / ACM+TS+SVM / ShallowConvNet / EEGNet-8,2 | Within-session 5-fold CV | ROC-AUC | 71.38 / 63.39 / 76.23 / 73.56 / 73.84 / 66.79 |

#### P300 datasets: MOABB within-session 5-fold CV, target vs non-target, ROC-AUC ([Table D4](https://arxiv.org/abs/2404.15319))
| Pipeline | BNCI2014-009 | BrainInvaders2013a | Lee2019-ERP |
|---|---|---|---|
| XDAWN+LDA | 64.03 | 76.74 | 96.45 |
| ERPCov+MDM | 81.16 | 80.59 | 74.43 |
| ERPCov(svdn4)+MDM | 84.52 | 82.07 | 82.47 |
| XDAWNCov+MDM | 92.04 | 90.97 | 97.70 |
| XDAWNCov+TS+SVM | 93.43 | 92.71 | 98.41 |

All rows: Chevallier et al. 2024. These are epoch-level AUCs, not character accuracy; the bi2013a report recommends balanced accuracy instead.

#### Tsinghua SSVEP Benchmark: 40 targets, leave-one-block-out, accuracy and ITR
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| CCA, via [BETA paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC7324867/) (from Chen 2015 / Wang 2017) | 2017 | Training-free CCA | 0.55 s gaze shift | Peak ITR | 90.16 ± 6.81 bits/min at 1.6 s |
| FBCCA, via [BETA paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC7324867/) | 2017 | Filter-bank CCA (training-free) | 0.55 s gaze shift | Peak ITR | 117.96 ± 7.78 bits/min at 1.2 s |
| m-Extended CCA, via [BETA paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC7324867/) | 2017 | Individual-template CCA | 0.55 s gaze shift | Peak ITR | 190.41 ± 7.90 bits/min at 0.8 s |
| [Guney et al. (DNN)](https://arxiv.org/abs/2011.08562) | 2021 | CNN over sub-bands, channels, time; global then per-subject training | **0.5 s** gaze shift; 9 channels; 0.4 s data | Accuracy / ITR | 79.89 ± 2.81%; 244.45 bits/min |
| [Guney et al.](https://arxiv.org/abs/2011.08562) | 2021 | same, 64 channels | 0.5 s gaze shift; 0.4 s data | Accuracy / ITR | 84.54 ± 2.08%; 265.23 bits/min |

The DNN's first training stage uses other subjects' data, and its ITR uses a 0.5 s rather than 0.55 s gaze shift, so it is not strictly comparable with the "via BETA" rows. MOABB within-session accuracy on `Wang2016` (5 s trials, 34 subjects, [Table D5](https://arxiv.org/abs/2404.15319)): CCA 2.48%, TRCA 2.79%, MDM 54.77%, TS+LR 67.52%. CCA and TRCA there sit at chance (1/40 = 2.5%), far below the published CCA results, so treat them as pipeline/configuration failures, not dataset ceilings.

#### BETA: 40 targets, leave-one-block-out (4 blocks)
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Liu et al. (BETA)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7324867/) | 2020 | CCA / FBCCA (training-free) | 0.55 s gaze shift | Peak ITR | 72.54 ± 4.54 at 1.8 s; 98.79 ± 4.49 bits/min at 1.4 s |
| [Liu et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC7324867/) | 2020 | Extended CCA / m-Extended CCA | same | Peak ITR | 119.17 ± 6.67 at 1 s; 130.58 ± 7.53 bits/min at 0.8 s |
| [Liu et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC7324867/) | 2020 | TRCA (ensemble, filter bank) / msTRCA | same | Peak ITR | 139.58 ± 8.52 at 0.6 s; 145.26 ± 8.15 bits/min at 0.6 s |
| [Guney et al. (DNN)](https://arxiv.org/abs/2011.08562) | 2021 | DNN, 9 channels | **0.5 s** gaze shift; 0.4 s data | Accuracy / ITR | 67.52 ± 2.17%; 188.45 bits/min |
| [Guney et al.](https://arxiv.org/abs/2011.08562) | 2021 | DNN, 64 channels | 0.5 s gaze shift; 0.4 s data | Accuracy / ITR | 69.54 ± 2.07%; 196.59 bits/min |

#### Nakanishi 2015 (12 targets): leave-one-block-out (14 train / 1 test)
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Nakanishi et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC4610694/) | 2015 | Standard CCA / MsetCCA / IT-CCA / CCA + IT-CCA combination | 1 s data, 8 channels | Accuracy | 55.00% / 73.61% / 81.17% / 92.78% |
| [Nakanishi et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC4610694/) | 2015 | Standard CCA / combination method | Peak over 0.5–4 s, 1 s gaze shift | Peak ITR | 50.40 ± 21.03 (2 s) / 91.68 ± 20.32 bits/min (1 s) |
| [MOABB, Table D5](https://arxiv.org/abs/2404.15319) | 2024 | CCA / TRCA / MDM / TS+LR | **Not comparable**: within-session 5-fold CV, 4.15 s trials | Accuracy | 8.15% / 83.21% / 78.77% / 87.22% |

#### Kaggle BCI Challenge (ErrP): 10 unseen test subjects
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Barachant, Cycon, Gouy-Pailler (1st)](https://github.com/alexandrebarachant/bci-challenge-ner-2015) | 2015 | XDAWN covariances + Riemannian electrode selection + tangent space + meta-features, Elastic Net, 500 bagged models; uses the session-5 leak | Kaggle private LB | Pooled AUC | 0.87224 |
| [same](https://github.com/alexandrebarachant/bci-challenge-ner-2015) | 2015 | same, no leak ("online compatible") | Kaggle private LB | Pooled AUC | 0.84585 |
| [same](https://github.com/alexandrebarachant/bci-challenge-ner-2015) | 2015 | same, no leak | Subject-wise 4-fold CV on training subjects | Mean per-subject AUC | 0.7696 |

EEGPT (4-fold CV with 10 test subjects, linear probe) reports balanced accuracy / AUROC: BENDR 0.5672/0.6030, BIOT 0.5118/0.5495, LaBraM 0.5439/0.5693, EEGPT 0.5837/0.6621 ([Table 4](https://papers.neurips.cc/paper_files/paper/2024/file/4540d267eeec4e5dbd9dae9448f0b739-Paper-Conference.pdf)). These are not comparable with the pooled-AUC leaderboard.

#### Kaggle Grasp-and-Lift: series 9–10 test, mean column-wise AUC
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Barachant & Cycon (1st), "YOLO"](https://github.com/alexandrebarachant/Grasp-and-lift-EEG-challenge) | 2015 | 3-level ensemble (covariance/Riemannian, ERP and filter-bank features; CNN, RNN, XGBoost), average of 18 level-3 models | Kaggle private LB | Mean AUC | 0.98109 |
| [same, "Safe1"](https://github.com/alexandrebarachant/Grasp-and-lift-EEG-challenge) | 2015 | Single level-3 model | Kaggle private LB | Mean AUC | 0.98095 |
| [same, level-1 "FBL_Sc"](https://github.com/alexandrebarachant/Grasp-and-lift-EEG-challenge) | 2015 | Single level-1 model on filter-bank low-pass (FBL) features | Kaggle private LB | Mean AUC | 0.92297 |

#### Kara One: subject-independent leave-one-subject-out, SVM-quad, EEG-only features
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Zhao & Rudzicz](http://www.cs.toronto.edu/~complingweb/data/karaOne/ZhaoRudzicz15.pdf) | 2015 | SVM (quadratic kernel), 5 features | C/V / ±Nasal / ±Bilabial / ±/iy/ / ±/uw/ (binary) | Accuracy | 18.08% / 63.50% / 56.64% / 59.60% / 79.16% |

The authors state that a deep-belief network reached 80–91% on ±/uw/ and C/V (figure only, no table). An 18% binary accuracy is far below chance and suggests a label or class-balance problem; treat these as unreliable. No classification baseline is given in the Thinking Out Loud data paper.

---

### A.4 How to read these numbers

- **The split decides the number more than the model.** EEG-TCNet on BCI IV 2a scores 77.35% in its own paper (session T → E), 75.62% when rerun by TCFormer, 55.09% leave-one-subject-out, and 41.65% under MOABB within-session CV ([EEG-TCNet](https://arxiv.org/abs/2006.00622), [TCFormer](https://github.com/Altaheri/TCFormer), [MOABB](https://arxiv.org/abs/2404.15319)). Only compare rows inside one table.
- **Test-set model selection inflates deep-learning results on 2a/2b.** The released EEG Conformer code tracks the best test-session accuracy across epochs ([conformer.py](https://github.com/eeyhsong/EEG-Conformer/blob/main/conformer.py), `bestAcc`), and the ATCNet authors now say their original evaluation does not follow best practice ([README](https://github.com/Altaheri/EEG-ATCNet)). When TCFormer reran EEG Conformer with the last-epoch checkpoint, it got 70.70% (75.39% with augmentation) instead of the 78.66% in the original paper. Prefer results that use a validation split or a fixed number of epochs.
- **Within-session shuffled CV is an upper bound.** MOABB's main protocol shuffles trials within one session ([Chevallier et al.](https://arxiv.org/abs/2404.15319)), so neighbouring trials leak slow drifts into training. Deep models with MOABB's default settings and only one session of data do poorly there (DeepConvNet 35.29% on BNCI2014-001), which reflects data size and configuration, not the architecture's ceiling.
- **Kappa, accuracy, balanced accuracy and AUC are not interchangeable.** Competition IV uses kappa (κ = (p_o − p_e)/(1 − p_e); with 4 balanced classes p_e = 0.25), MOABB uses ROC-AUC for 2-class tasks, and foundation-model papers often report balanced accuracy. P300 results are either epoch-level AUC (MOABB) or character accuracy after N repetitions (Competition III II, Lee 2019); these measure different things.
- **SSVEP ITR depends on data length and gaze-shift time.** Papers report the peak ITR at the best data length: 0.4 s for the DNN, 0.8–1.8 s for CCA variants. They also add 0.5 s, 0.55 s or 1 s of gaze shift. The same accuracy gives a much higher ITR at shorter windows, so always read accuracy, window length and gaze time together.
- **Pooled AUC can be gamed.** In the Kaggle ERN challenge the metric pooled all test subjects. Submitting only per-subject class-balance estimates (from a timing leak) scored 0.746 ([winner write-up](https://github.com/alexandrebarachant/bci-challenge-ner-2015)). The same team's leak-free model scored 0.846 on the private leaderboard, while its per-subject AUC in cross-validation on training subjects was 0.770.
- **Subject counts differ between papers and loaders.** HGD has 20 subjects in the arXiv paper but 14 in the public release. MOABB loads 34 of the 35 Benchmark subjects. Earlier MOABB versions loaded 9 of 10 Nakanishi subjects. PhysioNet subject 88 is at 128 Hz. EEGPT's Table 1 lists 10 subjects for BCI IV 2a and 2b, which have 9. Check which subjects a result used.
- **Foundation-model results need two extra checks.** First, was the evaluation dataset in the pretraining corpus? EEGPT pretrains on PhysioNet MI, HGD and the Tsinghua Benchmark, so its numbers on those sets would not be held-out. Second, was the model linear-probed (frozen) or fully fine-tuned? EEGPT's comparison mixes BENDR (fine-tuned) with linear-probed BIOT and LaBraM.
- **Small test sets make leaderboards noisy.** The Competition IV organizers warn that on a fixed 100-trial binary test set, the best and worst of 15 equally good methods are expected to differ by more than 10% by chance ([results page](https://www.bbci.de/competition/iv/results/)). Competition III IIIa has 3 subjects and III II has 2. Treat single-digit gaps there as ties.
- **Executed vs imagined movement.** HGD and the movement runs of PhysioNet and Grasp-and-Lift are executed movements. They also carry EMG and movement artifacts, so their accuracies do not transfer to motor imagery.


---

## Part B: Clinical, sleep, affective and large-scale datasets

This part covers clinical EEG (TUH corpus and subsets, seizure and harmful-activity datasets), sleep (brief, with pointers), affective, and large-scale or foundation-model datasets. Every number links to the page or paper where I read it. If a source did not give a value, the cell says "not reported". A number tagged "via X" was read in paper X's table, not in the original paper. I did not estimate anything. Sources were checked on 2026-10-11.

### B.1 Overview

| Dataset | Subjects / recordings | Channels | Hz | Task / labels | Size | Access |
|---|---|---|---|---|---|---|
| TUH EEG Corpus (TUEG) v2.0.2 | 14,987 patients; 26,846 sessions; 70,831 EDF files | Over 40 channel configurations; 95% include a 10-20 subset | 250–1024 | Unlabeled clinical EEG (reports searchable on request only) | 1,643 GB | Free; signed request form, then rsync |
| TUAB (abnormal) v3.0.1 | 2,329 unique subjects; 2,993 recordings (one per session) | 10-20 (AR reference) | varies (see block) | Normal / abnormal per recording | 60 GB | As TUEG |
| TUEV (events) v2.0.1 | 518 files (359 train, 159 eval) | 22-channel TCP bipolar montage for labels | varies | 6 event classes per channel | not reported | As TUEG |
| TUAR (artifacts) v3.0.1 | 213 patients; 259 sessions; 310 files | TCP montage (AR / LE / AR-A) | varies | 5 artifact types, every channel | not reported | As TUEG |
| TUSZ (seizure) v2.0.6 | 675 patients; 1,643 sessions; 8,140 files | TCP montage (AR / LE) | varies | Seizure start/stop, channel, type | 81.4 GB | As TUEG |
| CHB-MIT Scalp EEG | 22 subjects (23 cases + chb24); 664 EDF files | 23 (24 or 26 in a few files), bipolar | 256 | 198 seizure onsets/offsets | 42.6 GB | Open, ODC-By 1.0 |
| Siena Scalp EEG | 14 patients | 10-20 EEG + 1–2 EKG | 512 | 47 seizures | 20.3 GB | Open, CC BY 4.0 |
| Bonn (Andrzejak 2001) | 5 sets × 100 single-channel segments | 1 | 173.61 | 5 sets: healthy eyes open/closed, interictal ×2, ictal | about 3 MB (5 ZIPs) | Free download, cite the paper |
| HMS Harmful Brain Activity (Kaggle 2024) | 1,950 patients, 106,800 labeled segments (train); 1,532 patients (hidden test) | 10-20 EEG + EKG | 200 | Expert-vote distribution over 6 classes | not reported | Kaggle account and competition rules |
| Sleep-EDF Expanded | 78 (SC) + 22 (ST); 197 recordings | EEG Fpz-Cz, Pz-Oz (+ EOG, EMG) | 100 | Sleep stages (R&K) | 8.1 GB | Open, ODC-By |
| SHHS | 5,804 (NSRR) | EEG C3-A2, C4-A1 (+ EOG, ECG, …) | 125 (EEG, SHHS1) | Sleep stages, events | not reported | NSRR data-use agreement |
| DEAP | 32 | 32 EEG + 8 peripheral | 512 raw / 128 preprocessed | Valence, arousal, dominance, liking (1–9) | not reported | Signed EULA, academic only |
| SEED | 15 × 3 sessions | 62 | 1000 raw / 200 preprocessed | Positive / neutral / negative | not reported | License agreement + application |
| SEED-IV | 15 × 3 sessions × 24 trials | 62 | 200 (preprocessed) | Happy / sad / fear / neutral | not reported | License agreement + application |
| SEED-V | 16 × 3 sessions × 15 trials | 62 | 200 (preprocessed) | Happy / sad / neutral / disgust / fear | not reported | License agreement + application |
| DREAMER | 23 | 14 (Emotiv EPOC) | 128 | Valence / arousal / dominance (1–5) | not reported | Zenodo, restricted (request) |
| HBN-EEG | Over 3,000 participants aged 5–21; 11 public releases | 128 (EGI HydroCel) | 500 raw; 100 in the challenge copy | 6 tasks; 4 CBCL psychopathology factors | "multi-terabyte" | CC BY-SA 4.0 (releases 1–11) |
| THINGS-EEG (Gifford 2022) | 10 participants × 82,160 trials | 64 (EASYCAP) | 1000 | 16,740 image conditions | not reported | OSF (license not read) |
| EEGEyeNet | 356 | 128 | 500 | Gaze direction / position | 47+ h | CC BY 4.0 |
| KU Leuven auditory attention (AAD) | 16 | 64 (BioSemi) | 8192 raw / 128 distributed | Attended speaker in a two-talker scene | not reported | Zenodo, CC BY-NC-SA 4.0 |

Sources are in each block below. Sleep-EDF, SHHS, DEAP and EEGEyeNet are covered in full in the [EOG datasets file](../emg-eog-ecg/eog/DATASETS.md); their rows above are copied from there.

---

### B.2 Dataset specifications

#### TUH EEG Corpus (TUEG)
| Field | Value |
|---|---|
| Year & paper | Obeid & Picone 2016, *Front. Neurosci.* 10:196 ([PMC4865520](https://pmc.ncbi.nlm.nih.gov/articles/PMC4865520/)); the current README asks to cite the 2018 book-chapter version ([v2.0.2 README](https://isip.piconepress.com/projects/nedc/data/tuh_eeg/tuh_eeg/v2.0.2/AAREADME.txt)) |
| Subjects / recordings | v2.0.2: 14,987 patients, 26,846 sessions, 70,831 EDF files, 1.79 sessions per patient; total 97,467,928 s (27,074 h) ([README](https://isip.piconepress.com/projects/nedc/data/tuh_eeg/tuh_eeg/v2.0.2/AAREADME.txt)). Recorded at Temple University Hospital 2002–2017 ([TUH page](https://isip.piconepress.com/projects/nedc/html/tuh_eeg/)). The 2016 release had 16,986 sessions from 10,874 subjects, 51% female, age under 1 to over 90 ([PMC4865520](https://pmc.ncbi.nlm.nih.gov/articles/PMC4865520/)) |
| Device & montage | Clinical Nicolet systems; files converted from NicVue to EDF ([PMC4865520](https://pmc.ncbi.nlm.nih.gov/articles/PMC4865520/)). Over 40 channel configurations; 95% of the data includes a 10-20 subset |
| Channels | Most common EEG-only count per file was 31 (as few as 20) in the 2016 release ([PMC4865520](https://pmc.ncbi.nlm.nih.gov/articles/PMC4865520/)) |
| Sampling rate | 250–1024 Hz (v2.0.2 README). In 2016: 87% at 250 Hz, 8.3% at 256 Hz, 3.8% at 400 Hz, 1% at 512 Hz |
| Resolution | not reported |
| Labels | None on TUEG itself. Physician reports were paired with each session; they are no longer distributed, but NEDC will run user-supplied keyword scripts over them ([TUH page](https://isip.piconepress.com/projects/nedc/html/tuh_eeg/)) |
| Size / format | 1,643 GB of EDF |
| Access & license | Free, but you must send a signed request form; data comes by rsync with ssh keys (since January 2026) or on a mailed 8 TB drive ([TUH page](https://isip.piconepress.com/projects/nedc/html/tuh_eeg/)) |
| Standard protocol | None for TUEG. It is the pretraining corpus of EEG foundation models such as [CBraMod](https://arxiv.org/html/2412.07236); [LaBraM](https://arxiv.org/html/2405.18765) pretrains on the TUAR, TUEP, TUSZ and TUSL subsets instead of the full TUEG |
| Known issues | All subsets (TUAB, TUEV, TUAR, TUSZ, TUEP, TUSL) are drawn from TUEG and are linked back to it ([TUH page](https://isip.piconepress.com/projects/nedc/html/tuh_eeg/)), so pretraining on TUEG can include the downstream test recordings. Session dates are shifted and "usually within 6 months" of the real date (README) |

#### TUAB, TUH Abnormal EEG Corpus
| Field | Value |
|---|---|
| Year & paper | Lopez 2017 MS thesis (cited by the [v3.0.1 README](https://isip.piconepress.com/projects/nedc/data/tuh_eeg/tuh_eeg_abnormal/v3.0.1/AAREADME.txt)); v3.0.1 released 2024-02-07 (headers only changed) |
| Subjects / recordings | 2,993 recordings (eval 276, train 2,717); subject entries 253 eval + 2,130 train, of which 2,076 unique in train because 54 subjects appear as both normal and abnormal. Normal / abnormal recordings: 1,521 / 1,472. Eval subjects 105 abnormal / 148 normal ([README](https://isip.piconepress.com/projects/nedc/data/tuh_eeg/tuh_eeg_abnormal/v3.0.1/AAREADME.txt)). Ages 7 days to 96 years ([Gemein 2020](https://arxiv.org/html/2002.05115)) |
| Device & montage | TUH clinical systems; one configuration in this corpus, `01_tcp_ar` (averaged reference) |
| Channels | not reported in README. Papers use 21 electrodes ([Gemein](https://arxiv.org/html/2002.05115)) or 16 bipolar channels ([BIOT](https://arxiv.org/html/2305.10351)); [LaBraM](https://arxiv.org/html/2405.18765) describes it as 23-channel |
| Sampling rate | not reported in README. LaBraM says 256 Hz; [CBraMod](https://arxiv.org/html/2412.07236) says 250 Hz. Papers resample to 200 Hz (BIOT, LaBraM, CBraMod) or 100 Hz (Gemein) |
| Resolution | not reported |
| Labels | One normal/abnormal label per recording. For v3.0.0 the data was manually reviewed against the EEG reports: positive agreement for 276/276 eval files and 2,700/2,727 train files (README; the train total in that table differs from 2,717 elsewhere in the README). The v2.0.0 README reported 97–100% inter-rater agreement; [Gemein et al.](https://arxiv.org/html/2002.05115) note the review was done by medical students who knew the diagnoses, and that published neurologist agreement on normal/abnormal is 86–88% |
| Duration / size | 1,142.00 h (eval 102.94 h, train 1,038.06 h); every file over 15 min; 59,995 MB of EDF |
| Format | EDF; path encodes train/eval and normal/abnormal |
| Access & license | As TUEG (signed form) |
| Standard protocol | Official train / eval split, no subject overlap. Two incompatible reporting styles: (a) **recording-level accuracy** on the 276 eval recordings ([Gemein 2020](https://arxiv.org/html/2002.05115)); (b) **10-s segment-level** balanced accuracy / AUROC on 409,455 segments, 16 bipolar channels at 200 Hz, training patients split 80/20 into train/val, eval set as test ([BIOT](https://arxiv.org/html/2305.10351), reused by LaBraM, EEGPT, CBraMod; LaBraM's released preprocessing [code](https://github.com/935963004/LaBraM/blob/main/dataset_maker/make_TUAB.py) keeps 23 referential channels instead of 16 bipolar, and EEGPT and SeizureTransformer also describe 23 channels) |
| Known issues | Pathology correlates with age, and the train and eval sets differ systematically ([Gemein](https://arxiv.org/html/2002.05115)). v1.1.1 had duplicates across train and eval, removed in v2.0.0 (Gemein appendix). Segment-level and recording-level numbers are not comparable |

#### TUEV, TUH EEG Events Corpus
| Field | Value |
|---|---|
| Year & paper | Harati et al. 2015, IEEE SPMB ([v2.0.1 README](https://isip.piconepress.com/projects/nedc/data/tuh_eeg/tuh_eeg_events/v2.0.1/AAREADME.txt)) |
| Subjects / recordings | Train 359 files, eval 159 files; subject counts not reported. Files containing each class, eval / train: SPSW 9 / 27, GPED 28 / 51, PLED 33 / 48, ARTF 46 / 164, EYEM 35 / 46, BCKG 89 / 211 |
| Device & montage | AR and LE recordings, all convertible to the 22-channel ACNS TCP bipolar montage used for the labels |
| Channels | 22 TCP channels in the label files; papers use 16 bipolar channels ([BIOT](https://arxiv.org/html/2305.10351)) |
| Sampling rate | not reported in README; LaBraM says 256 Hz, CBraMod says 250 Hz; resampled to 200 Hz |
| Resolution | not reported |
| Labels | Per channel, in seconds: spike/sharp wave (SPSW), GPED, PLED, eye movement (EYEM), artifact (ARTF), background (BCKG). BCKG is a catch-all. Annotator identity and agreement not reported in the README |
| Duration / size | not reported; papers cut 112,491 five-second samples ([LaBraM](https://arxiv.org/html/2405.18765)) |
| Format | EDF + `.rec` / `.lab` label files + `.htk` features |
| Access & license | As TUEG |
| Standard protocol | Official train / eval split; train patients split 80/20 into train/val; metrics balanced accuracy, Cohen's κ, weighted F1 ([BIOT](https://arxiv.org/html/2305.10351)) |
| Known issues | Strong class imbalance (only 9 eval files contain SPSW). Eval file names carry the class (`bckg_032_a_.edf`), so file names must not be used as features. TUEV is inside TUEG, which most foundation models pretrain on ([CBraMod](https://arxiv.org/html/2412.07236) re-ran pretraining without it to check) |

#### TUAR, TUH EEG Artifact Corpus
| Field | Value |
|---|---|
| Year & paper | Buckwalter et al. 2021, IEEE SPMB ([v3.0.1 README](https://isip.piconepress.com/projects/nedc/data/tuh_eeg/tuh_eeg_artifact/v3.0.1/AAREADME.txt)) |
| Subjects / recordings | 213 patients, 259 sessions, 310 files; 42 files also have seizures |
| Device & montage | Three configurations: `01_tcp_ar`, `02_tcp_le`, `03_tcp_ar_a`; labels on TCP bipolar channels |
| Sampling rate / resolution | not reported |
| Labels | Every event on every channel (upgrade from v1.0.0, which labeled only examples): eye movement, chewing, shivering, muscle, electrode (pop / static / lead), plus combinations; unlabeled = background. 160,073 non-background events; musc 31.89%, eyem 24.09%, elec 20.70% are the largest classes. Agreement not reported in README |
| Duration / size | 359,936 s (99.98 h); size not reported |
| Format | EDF + CSV (`channel,start,stop,label,confidence`); separate `*_seiz.csv` seizure files |
| Access & license | As TUEG |
| Standard protocol | None official (no train/eval split in the release) |
| Known issues | Many overlapping multi-label events (for example `eyem_musc`), so single-label setups need a merge rule |

#### TUSZ, TUH EEG Seizure Corpus
| Field | Value |
|---|---|
| Year & paper | Shah et al. 2018, *Front. Neuroinform.* 12:83 ([PMC6246677](https://pmc.ncbi.nlm.nih.gov/articles/PMC6246677/)); current release v2.0.6, re-annotated in v2.0.5 (2026-03-10) with a subject-metadata spreadsheet ([README](https://isip.piconepress.com/projects/nedc/data/tuh_eeg/tuh_eeg_seizure/v2.0.6/AAREADME.txt)) |
| Subjects / recordings | v2.0.6: patients 579 train / 53 dev / 43 eval; sessions 1,175 / 342 / 126; files 5,057 / 2,203 / 880. Patients with seizures 171 / 37 / 30. The 2018 paper describes v1.2.0: 315 subjects, 822 sessions, 280 with seizures, eval 50 patients (56% female) |
| Device & montage | AR and LE recordings, all convertible to the 22-channel TCP montage |
| Channels | 22 TCP channels for labels; [SzCORE](https://arxiv.org/html/2402.13005) lists 17–128 channels per file across TUH |
| Sampling rate | not reported in README; 250–1000 Hz per [SzCORE](https://arxiv.org/html/2402.13005) |
| Resolution | not reported |
| Labels | Seizure start/stop, channel and seizure type (`.csv`), plus term-based seizure/background (`.csv_bi`). Sessions were preselected by report keyword search, Persyst and a deep-learning detector; annotation by trained undergraduates, a portion checked against neurologists with "high inter-rater agreement" (no number given in the paper) ([PMC6246677](https://pmc.ncbi.nlm.nih.gov/articles/PMC6246677/)) |
| Duration / size | Seizure events 1,812 train / 492 dev / 360 eval. Total duration 3,278,444 s train (≈910.7 h), 1,567,972 s dev (≈435.5 h), 462,818 s eval (≈128.6 h); 81.4 GB. Files are capped at 1,800 s since v2.0.5 |
| Format | EDF + CSV |
| Access & license | As TUEG |
| Standard protocol | Train on `train`, tune on `dev`, report once on blind `eval` ("you should never optimize parameters on this set", README). The Neureka 2020 challenge used v1.5.x ([TABS slides](https://isip.piconepress.com/conferences/ieee_spmb/2020/papers/l02_01_slides.pdf)). Metrics: sensitivity and false alarms per 24 h with a named scoring method (OVLP, TAES, EPCH, DPAL, or SzCORE event / sample scoring) |
| Known issues | Versions change annotations and file splits (v2.0.1, v2.0.3, v2.0.5, v2.0.6), so results on different versions are not directly comparable. The 2018 eval set was built so about 34% of files contain seizures, far more than routine EEG ([PMC6246677](https://pmc.ncbi.nlm.nih.gov/articles/PMC6246677/)) |

#### CHB-MIT Scalp EEG Database
| Field | Value |
|---|---|
| Year & paper | Shoeb 2009 PhD thesis; Shoeb & Guttag 2010, ICML ([PDF](https://icml.cc/Conferences/2010/papers/493.pdf)); data on [PhysioNet](https://physionet.org/content/chbmit/1.0.0/) |
| Subjects / recordings | 22 pediatric subjects with intractable seizures, monitored after anti-seizure medication withdrawal at Children's Hospital Boston: 5 males aged 3–22, 17 females aged 1.5–19. 23 cases (chb21 is chb01 recorded 1.5 years later); chb24 added in 2010 without demographics. 664 EDF files, 129 with seizures ([PhysioNet](https://physionet.org/content/chbmit/1.0.0/)) |
| Device & montage | 10-20 electrode positions; bipolar montage that can change between files (listed in each `chbNN-summary.txt`) |
| Channels | Most files 23 EEG signals (24 or 26 in a few); up to 5 dummy "-" channels; ECG in 36 chb04 files, VNS in 18 chb09 files |
| Sampling rate | 256 Hz |
| Resolution | 16-bit |
| Labels | Seizure onset and offset times, 198 seizures in total (182 in the original 23 cases). Annotator and agreement not reported on PhysioNet |
| Duration / size | Mostly 1 h files (2 h for chb10, 4 h for chb04/06/07/09/23); 42.6 GB. [SzCORE](https://arxiv.org/html/2402.13005) counts 982 h and 686 files (differs from PhysioNet's 664) |
| Format | EDF + `.seizure` annotation files + per-case summary text |
| Access & license | Open, Open Data Commons Attribution v1.0 |
| Standard protocol | No official split. Three common setups: (1) **patient-specific**: per patient, leave one seizure record out ([Shoeb & Guttag](https://icml.cc/Conferences/2010/papers/493.pdf)); (2) **cross-patient, event-based**: subject-independent CV within the dataset ([SzCORE](https://arxiv.org/html/2402.13005)); (3) **cross-patient, 10-s segments**: patients 1–19 train, 20–21 validation, 22–23 test, then swap validation and test and average, 16 bipolar channels at 200 Hz ([BIOT](https://arxiv.org/html/2305.10351); CBraMod uses the same split) |
| Known issues | chb01 and chb21 are the same person, so leave-one-case-out leaks a patient. Gaps between files (usually ≤10 s, sometimes much longer). Only bipolar channels, which cannot be converted to a referential montage ([SzCORE](https://arxiv.org/html/2402.13005)). Segment-level seizure prevalence is about 0.6% in the BIOT training split ([BIOT](https://arxiv.org/html/2305.10351)), so accuracy is meaningless; use balanced accuracy, AUC-PR, or event metrics |

#### Siena Scalp EEG Database
| Field | Value |
|---|---|
| Year & paper | Detti, Vatti & Zabalo Manrique de Lara 2020, *Processes*; data v1.0.0 on [PhysioNet](https://physionet.org/content/siena-scalp-eeg/1.0.0/) |
| Subjects / recordings | 14 epilepsy patients at the University of Siena: 9 males aged 25–71, 5 females aged 20–58. 1–5 EDF files per patient (41 files per [SzCORE](https://arxiv.org/html/2402.13005)) |
| Device & montage | Video-EEG with EB Neuro and Natus Quantum LTM amplifiers, reusable silver/gold cup electrodes, 10-20 system |
| Channels | EEG plus 1 or 2 EKG; 35–45 channels per file per [SzCORE](https://arxiv.org/html/2402.13005) |
| Sampling rate | 512 Hz |
| Resolution | not reported |
| Labels | Seizure start/end in a per-patient text file; epilepsy diagnosis and ILAE seizure classification by an expert clinician. Agreement not reported |
| Duration / size | 47 seizures in about 128 h; 20.3 GB uncompressed |
| Format | EDF |
| Access & license | Open, CC BY 4.0 |
| Standard protocol | None official; used with subject-independent CV and as training or test data in [SzCORE](https://arxiv.org/html/2402.13005) |
| Known issues | Only 14 patients; patients were asked to stay in bed, so motion is limited |

#### Bonn EEG dataset (Andrzejak et al. 2001)
| Field | Value |
|---|---|
| Year & paper | Andrzejak et al. 2001, *Phys. Rev. E* 64, 061907 ([download page](https://www.ukbonn.de/epileptologie/arbeitsgruppen/ag-lehnertz-neurophysik/downloads/)) |
| Subjects / recordings | Sets A and B: surface EEG from healthy volunteers, eyes open and closed. Sets C and D: intracranial EEG from epilepsy patients between seizures, outside and inside the seizure onset zone. Set E: intracranial seizures. 100 segments per set ([Lu & Triesch](https://arxiv.org/pdf/1903.08100)). Five volunteers and five patients is the usual description; I could not open the original paper to confirm |
| Device & montage | Not reported on the download page; single channel per segment |
| Channels | 1 |
| Sampling rate | 173.61 Hz |
| Resolution | not reported on the pages I read |
| Labels | Set membership (recording site and state), not per-sample annotation |
| Duration / size | 4,096 samples per file (about 23.6 s); five ZIPs of 560–747 kB |
| Format | ASCII text |
| Access & license | Free download; must cite the paper. License not stated |
| Standard protocol | None. Papers use A vs E, AB vs CD vs E, and other groupings with random segment splits |
| Known issues | Segments are short, pre-selected and single-channel, unlike continuous clinical EEG. The healthy sets are scalp recordings and the patient sets are intracranial, so a classifier can separate recording type, not only pathology. Filtering is inconsistent in the literature: the download page says the files keep the 0.5–85 Hz acquisition bandwidth and the paper's 40 Hz low-pass was **not** applied, while many papers state 0.53–40 Hz. Results near 100% are common and do not transfer to clinical seizure detection |

#### HMS Harmful Brain Activity Classification (Kaggle, 2024)
| Field | Value |
|---|---|
| Year & paper | Kaggle competition, 2024; data from the Westover group at Massachusetts General Hospital / Harvard Medical School ([competition](https://www.kaggle.com/competitions/hms-harmful-brain-activity-classification); details read in [VIPEEGNet](https://arxiv.org/html/2507.08874) and [Peters' write-up](https://www.ryanirl.com/blog/hbac/)) |
| Subjects / recordings | Training: 1,950 patients, 106,800 labeled segments, recorded 2006–2020. Hidden test: segments from a further 1,532 patients ([VIPEEGNet](https://arxiv.org/html/2507.08874)). 17,089 EEG/EKG recordings and 11,138 spectrograms in training ([Peters](https://www.ryanirl.com/blog/hbac/)) |
| Device & montage | 10-20 placement; experts read a longitudinal bipolar ("double banana") view |
| Channels | 10-20 EEG electrodes plus one EKG channel; four precomputed spectrograms (LL, RL, LP, RP chains) |
| Sampling rate | 200 Hz |
| Resolution | not reported |
| Labels | Seizure, LPD, GPD, LRDA, GRDA or Other for the central 10 s of each 50-s segment; experts also saw the 10-min spectrogram. 1–28 votes per training segment; test segments had at least 10 votes. The target is the vote distribution ([VIPEEGNet](https://arxiv.org/html/2507.08874)) |
| Duration / size | 50-s EEG windows inside 10-min spectrogram windows; size not reported |
| Format | not reported |
| Access & license | Kaggle account and acceptance of the competition rules; license terms not read |
| Standard protocol | Kullback-Leibler divergence between predicted and vote distributions. Public leaderboard 35% / private 65% of the test set; 2,767 teams ([VIPEEGNet](https://arxiv.org/html/2507.08874)) |
| Known issues | Many training segments come from the same recording (106,800 segments from 17,089 recordings), so cross-validation must group by patient ([Peters](https://www.ryanirl.com/blog/hbac/) used GroupKFold by patient). Low-vote training labels are noisier than the ≥10-vote test labels |

#### Sleep-EDF Expanded and SHHS (brief)
Both are specified in full, with results, in the [EOG datasets file](../emg-eog-ecg/eog/DATASETS.md). In short:
- **Sleep-EDF Expanded** ([PhysioNet](https://physionet.org/content/sleep-edfx/1.0.0/)): 197 recordings; EEG Fpz-Cz and Pz-Oz at 100 Hz; R&K hypnograms; open (ODC-By). Common subsets are SleepEDF-20 (20-fold subject-wise CV) and SleepEDF-78 (10-fold).
- **SHHS** ([NSRR](https://sleepdata.org/datasets/shhs)): 5,804 adults aged 40+ on NSRR; EEG C3-A2 and C4-A1 at 125 Hz (SHHS1); NSRR data-use agreement; usually a 70/30 subject split.

#### DEAP (affective)
Full block in the [EOG datasets file](../emg-eog-ecg/eog/DATASETS.md). Key facts for EEG work: Koelstra et al. 2012, *IEEE Trans. Affective Computing*; 32 subjects × 40 one-minute music-video trials; 32 EEG channels at 512 Hz ([TSception Table 1](https://arxiv.org/pdf/2104.02935)), distributed preprocessed at 128 Hz with 4–45 Hz band-pass; self-ratings 1–9 for arousal, valence, dominance and liking, usually binarized at a threshold ([MSBAM](https://arxiv.org/pdf/2110.06462)); signed EULA. **Known issue:** with only 40 trials per subject, splitting 1–4 s segments at random lets segments of the same trial appear in train and test. [MSBAM](https://arxiv.org/pdf/2110.06462) states this leakage applies to its own >99% results; [TSception](https://arxiv.org/pdf/2104.02935) uses trial-wise splits to avoid it.

#### SEED
| Field | Value |
|---|---|
| Year & paper | Zheng & Lu 2015, *IEEE TAMD* 7(3); Duan, Zhu & Lu 2013 (DE features) ([SEED page](https://bcmi.sjtu.edu.cn/home/seed/seed.html)) |
| Subjects | 15 Chinese subjects, 7 male / 8 female, age 23.27 ± 2.37; 12 also have eye-tracking data |
| Device & montage | 62-channel ESI NeuroScan, 10-20 layout; SMI eye-tracking glasses |
| Sampling rate | Raw 1000 Hz (`.cnt`); preprocessed version downsampled to 200 Hz, 0–75 Hz band-pass |
| Resolution | not reported |
| Labels | 15 Chinese film clips of about 4 min, labeled by target emotion (positive / neutral / negative); self-reports collected after each clip |
| Sessions | 3 sessions per subject about one week apart; 15 trials per session (45 `.mat` files) |
| Format | MATLAB; precomputed DE, DASM, RASM features with moving-average and LDS smoothing |
| Access & license | Download and sign a license agreement, upload it on the APPLY page; link sent after review ([downloads](https://bcmi.sjtu.edu.cn/home/seed/downloads.html)) |
| Standard protocol | **Subject-dependent**: per subject, first 9 trials train, last 6 test, averaged over 2 sessions. **Subject-independent**: leave one subject out (train 14, test 1), one session ([RGNN](https://arxiv.org/pdf/1907.07835)) |
| Known issues | Labels are per clip, not per segment. Smoothed features (LDS) use information across the whole trial. Many papers use only the first session or a subset of sessions |

#### SEED-IV
| Field | Value |
|---|---|
| Year & paper | Zheng et al. 2019, "EmotionMeter", *IEEE Trans. Cybernetics* 49(3) ([SEED-IV page](https://bcmi.sjtu.edu.cn/home/seed/seed-iv.html)) |
| Subjects | 15; demographics not reported on the page |
| Device / channels | 62-channel ESI NeuroScan; SMI eye tracking |
| Sampling rate | Downsampled to 200 Hz, 1–75 Hz band-pass (raw rate not stated on the page) |
| Labels | 72 film clips chosen to induce happy, sad, fear or neutral |
| Sessions | 3 sessions on different days, 24 trials each; features on 4-s non-overlapping windows |
| Access & license | As SEED |
| Standard protocol | Subject-dependent: first 16 trials train, last 8 (2 per class) test, all 3 sessions. Subject-independent: leave one subject out ([RGNN](https://arxiv.org/pdf/1907.07835)) |
| Known issues | Different clips in each session |

#### SEED-V
| Field | Value |
|---|---|
| Year & paper | Liu, Qiu, Zheng & Lu 2021, *IEEE TCDS* ([SEED-V page](https://bcmi.sjtu.edu.cn/home/seed/seed-v.html)) |
| Subjects | 16 (6 male, 10 female), SJTU students, right-handed |
| Device / channels | 62-channel ESI NeuroScan; SMI eye tracking |
| Sampling rate | Features computed after downsampling to 200 Hz (1–75 Hz); raw `.cnt` provided; [CBraMod](https://arxiv.org/html/2412.07236) gives 1000 Hz raw |
| Labels | Happy, sad, neutral, disgust, fear; 3 clips per emotion per session; 0–5 self-rating of induction effect |
| Sessions | 3 sessions at least 3 days apart, 15 trials each, different clips each time |
| Access & license | As SEED |
| Standard protocol | Foundation-model papers split the 15 trials of each session 5:5:5 into train / val / test ([CBraMod](https://arxiv.org/html/2412.07236), [LaBraM](https://arxiv.org/html/2405.18765)) |
| Known issues | CBraMod notes it used the public 16-subject version, while LaBraM used a private 20-subject version, so their SEED-V numbers are not comparable. Session numbers in file names follow stimulus set, not time order |

#### DREAMER
| Field | Value |
|---|---|
| Year & paper | Katsigiannis & Ramzan 2018, *IEEE JBHI* 22(1):98–107 ([Zenodo record](https://zenodo.org/records/546113)) |
| Subjects | 23 (14 male, 9 female) ([MSBAM](https://arxiv.org/pdf/2110.06462)) |
| Device & montage | Emotiv EPOC wireless headset (EEG) and Shimmer2 (ECG) ([Zenodo](https://zenodo.org/records/546113)) |
| Channels | 14 EEG |
| Sampling rate | 128 Hz ([MSBAM](https://arxiv.org/pdf/2110.06462)) |
| Resolution | not reported |
| Labels | Self-ratings 1–5 of valence, arousal, dominance after each of 18 film clips (65–393 s); a neutral clip before each gives a baseline ([MSBAM](https://arxiv.org/pdf/2110.06462); [topological paper](https://arxiv.org/pdf/2203.06895)) |
| Size / format | not reported |
| Access & license | Restricted: log in to Zenodo and request access with name, institution, position and purpose (files restricted per the Zenodo API; form fields *unverified*) |
| Standard protocol | None official; binarized at a threshold of 3 is common ([topological paper](https://arxiv.org/pdf/2203.06895)) |
| Known issues | Consumer headset with few channels. Same segment-split leakage risk as DEAP. I could not read the original paper, so its baseline results are not given here |

#### Healthy Brain Network EEG (HBN-EEG) and the NeurIPS 2025 EEG Foundation Challenge
| Field | Value |
|---|---|
| Year & paper | HBN: Alexander et al. 2017, *Sci. Data* ([PMC5735921](https://pmc.ncbi.nlm.nih.gov/articles/PMC5735921/)). HBN-EEG (BIDS release): Shirazi et al. 2024, bioRxiv ([preprint](https://www.biorxiv.org/content/10.1101/2024.10.03.615261v2.full)). Challenge: Aristimunha et al. 2025, "EEG Foundation Challenge: From Cross-Task to Cross-Subject EEG Decoding" ([arXiv](https://arxiv.org/html/2506.19141)) |
| Subjects / recordings | Over 3,000 participants aged 5–21 in 11 public releases ([HBN-EEG page](https://neuromechanist.github.io/data/hbn/)); the bioRxiv version counted more than 2,600 participants in nine releases. Release 12 is withheld for testing ([challenge](https://arxiv.org/html/2506.19141)) |
| Device & montage | 128-channel EGI Geodesic HydroCel net, Cz reference, sound-shielded room ([PMC5735921](https://pmc.ncbi.nlm.nih.gov/articles/PMC5735921/)) |
| Channels | 128 |
| Sampling rate | 500 Hz, 0.1–100 Hz band-pass ([PMC5735921](https://pmc.ncbi.nlm.nih.gov/articles/PMC5735921/)). Challenge copy: filtered 0.5–50 Hz and downsampled to 100 Hz, BDF and SET ([data page](https://eeg2025.github.io/data/)) |
| Resolution | not reported |
| Labels | Six tasks: resting state, surround suppression, movie watching (passive); contrast change detection, sequence learning, symbol search (active). HED event annotations, behavioral responses, age, sex, handedness, and four CBCL-derived bifactor scores (p-factor, internalizing, externalizing, attention) |
| Duration / size | "multi-terabyte" ([challenge](https://arxiv.org/html/2506.19141)); exact size not reported |
| Format | BIDS; EEGLAB SET (original), BDF (challenge copy) |
| Access & license | Releases 1–11 free under CC BY-SA 4.0 via NEMAR / OpenNeuro ([challenge](https://arxiv.org/html/2506.19141)); some subjects are CC BY-NC-SA 4.0, left out of the OpenNeuro releases and distributed as a separate AWS S3 dataset (also on NEMAR) ([bioRxiv](https://www.biorxiv.org/content/10.1101/2024.10.03.615261v2.full)) |
| Standard protocol | Challenge split by release, no subject in two releases: train releases 1–11 except 5, validation release 5, hidden test release 12 ([challenge](https://arxiv.org/html/2506.19141)). Challenge 1: predict per-trial response time in contrast change detection. Challenge 2: predict the externalizing factor per subject (the other three factors were dropped) ([site](https://eeg2025.github.io/)). Metric for both: normalized RMSE = RMSE / std(y_true) ([rules](https://eeg2025.github.io/rules/)); 1.0 equals predicting the mean |
| Known issues | The organizers did not shuffle Challenge 2 test samples, so contiguous trials likely came from one subject, which some teams exploited. Only three teams beat 0.99 on Challenge 2. The two challenges were then ranked separately instead of the planned 0.3/0.7 weighting ([leaderboard](https://eeg2025.github.io/leaderboard/)) |

#### THINGS-EEG (Gifford et al. 2022)
| Field | Value |
|---|---|
| Year & paper | Gifford et al. 2022, *NeuroImage* 264:119754 ([PMC9771828](https://pmc.ncbi.nlm.nih.gov/articles/PMC9771828/)) |
| Subjects | 10 healthy adults, mean age 28.5 (SD 4), 8 female, 2 male |
| Device & montage | 64-channel EASYCAP, 10-10 system, BrainVision actiCHamp; online reference Fz |
| Channels | 64 recorded; NICE reports 63 channels in the released data ([NICE](https://arxiv.org/pdf/2308.13234)) |
| Sampling rate | 1000 Hz, online 0.1–100 Hz filter |
| Resolution | not reported |
| Labels | Image identity from the THINGS database. Training: 16,540 image conditions (1,654 concepts × 10 images) × 4 repetitions. Test: 200 conditions (200 concepts × 1 image) × 80 repetitions. Training and test concepts do not overlap. RSVP at 200 ms SOA (100 ms image + 100 ms blank) with a target-detection task |
| Sessions | 4 sessions per participant; 82,160 trials each |
| Format | Raw and preprocessed EEG, resting-state EEG, images and DNN features on [OSF](https://doi.org/10.17605/OSF.IO/3JK45) |
| Access & license | OSF; article CC BY-NC-ND 4.0; data license not read |
| Standard protocol | 200-way zero-shot identification of the test images (chance 0.5%), top-1 and top-5, subject-dependent or leave-one-subject-out ([NICE](https://arxiv.org/pdf/2308.13234)). Test responses are usually averaged over the 80 repetitions |
| Known issues | Averaging 80 test repetitions makes test inputs far cleaner than single trials. Preprocessing (channel subset, multivariate noise normalization, averaging) differs between papers, and re-implemented baselines can differ from their original numbers (see B.3) |

#### EEGEyeNet (brief)
356 healthy adults, 128-channel EGI at 500 Hz with an EyeLink eye tracker giving the gaze labels; subject-wise 70/15/15 split; CC BY 4.0. Full block and results in the [EOG datasets file](../emg-eog-ecg/eog/DATASETS.md).

#### KU Leuven auditory attention detection (AAD) dataset
| Field | Value |
|---|---|
| Year & paper | Biesmans, Das, Francart & Bertrand 2016, *IEEE TNSRE* 25(5) (the paper the record asks to cite); Zenodo v2.0, 2019-08-30 ([record](https://zenodo.org/records/4004271)) |
| Subjects | 16 normal-hearing subjects |
| Device / channels | BioSemi ActiveTwo, 64 channels |
| Sampling rate | Recorded at 8192 Hz (the record also says "8196 Hz" once, which looks like a typo); distributed high-passed at 0.5 Hz and downsampled to 128 Hz |
| Labels | Attended speaker in a two-talker scene: four Dutch short stories read by male speakers |
| Duration | 20 trials, about 72 min of EEG per subject |
| Access & license | Zenodo, CC BY-NC-SA 4.0 |
| Standard protocol | not reported on the record |
| Known issues | In January 2024 the authors added a warning: do not split segments of the same trial between train and test, because networks can recognize the trial from segments under 1 s ("trial fingerprints"); they also warn about gaze bias. No results are listed below because I did not read a paper with a trial-disjoint protocol |

---

### B.3 Published results

Rows within a table share protocol and metric unless marked otherwise. Many baseline rows in the TUAB, TUEV and CHB-MIT segment tables were run once by the BIOT authors and then copied unchanged by LaBraM, EEGPT and CBraMod; I cite the paper where I read them.

#### TUAB: 10-s segments, BIOT protocol (200 Hz, official eval set as test; 16 bipolar channels for BIOT, baselines and CBraMod, but 23 channels for LaBraM, EEGPT and SeizureTransformer)
| Paper | Year | Method | Protocol | Metric | Result (BAcc / AUROC) |
|---|---|---|---|---|---|
| SPaRCNet, via [BIOT Table 4](https://arxiv.org/html/2305.10351) | 2023 | CNN | as above | Balanced acc. / AUROC | 0.7896 ± 0.0018 / 0.8676 ± 0.0012 |
| ContraWR, via [BIOT](https://arxiv.org/html/2305.10351) | 2021 | Contrastive CNN | as above | same | 0.7746 ± 0.0041 / 0.8456 ± 0.0074 |
| CNN-Transformer, via [BIOT](https://arxiv.org/html/2305.10351) | 2022 | CNN + transformer | as above | same | 0.7777 ± 0.0022 / 0.8461 ± 0.0013 |
| FFCL, via [BIOT](https://arxiv.org/html/2305.10351) | 2022 | CNN + LSTM | as above | same | 0.7848 ± 0.0038 / 0.8569 ± 0.0051 |
| ST-Transformer, via [BIOT](https://arxiv.org/html/2305.10351) | 2021 | Spatio-temporal transformer | as above | same | 0.7966 ± 0.0023 / 0.8707 ± 0.0019 |
| [Yang et al. (BIOT)](https://arxiv.org/html/2305.10351) | 2023 | BIOT, from scratch | as above | same | 0.7925 ± 0.0035 / 0.8691 ± 0.0033 |
| [Yang et al. (BIOT)](https://arxiv.org/html/2305.10351) | 2023 | BIOT, pretrained on 6 EEG datasets | as above | same | 0.7959 ± 0.0057 / 0.8815 ± 0.0043 |
| [Jiang et al. (LaBraM)](https://arxiv.org/html/2405.18765) | 2024 | LaBraM-Base (5.8M) | as above | same | 0.8140 ± 0.0019 / 0.9022 ± 0.0009 |
| [Jiang et al. (LaBraM)](https://arxiv.org/html/2405.18765) | 2024 | LaBraM-Huge (369M) | as above | same | 0.8258 ± 0.0011 / 0.9162 ± 0.0016 |
| [Wang et al. (EEGPT)](https://papers.neurips.cc/paper_files/paper/2024/file/4540d267eeec4e5dbd9dae9448f0b739-Paper-Conference.pdf) | 2024 | EEGPT (25M); the paper says it uses linear probing downstream | as above | same | 0.7983 ± 0.0030 / 0.8718 ± 0.0050 |
| EEGNet, via [CBraMod Table 14](https://arxiv.org/html/2412.07236) | 2018 | Compact CNN | as above | same | 0.7642 ± 0.0036 / 0.8412 ± 0.0031 |
| EEG Conformer, via [CBraMod](https://arxiv.org/html/2412.07236) | 2022 | CNN + transformer | as above | same | 0.7758 ± 0.0049 / 0.8445 ± 0.0038 |
| [Wang et al. (CBraMod)](https://arxiv.org/html/2412.07236) | 2025 | CBraMod (4.0M), TUAB excluded from pretraining | as above | same | 0.8249 ± 0.0025 / 0.9156 ± 0.0017 |
| [Wang et al. (CBraMod)](https://arxiv.org/html/2412.07236) | 2025 | CBraMod (4.0M) | as above | same | 0.8289 ± 0.0022 / 0.9227 ± 0.0011 |
| [Wu et al. (SeizureTransformer)](https://arxiv.org/html/2504.00336) | 2025 | U-Net + transformer, no pretraining (7.3M) | as above | same | 0.8144 ± 0.0002 / 0.8568 ± 0.0019 |

Years for via-rows are the method's year as given in the citing paper's reference list.

#### TUAB: recording-level accuracy on the 276 eval recordings (Gemein et al. protocol). Not comparable with the table above
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| Lopez de Diego, via [Gemein](https://arxiv.org/html/2002.05115) | 2017 | Cepstral features + CNN/MLP | Recording-level | Accuracy | 78.8% |
| Schirrmeister et al., via [Gemein](https://arxiv.org/html/2002.05115) | 2017 | Deep4 ConvNet (TUAB v1.1.1, which had train/eval duplicates) | Recording-level | Accuracy | 85.4% |
| Roy et al. (ChronoNet), via [Gemein](https://arxiv.org/html/2002.05115) | 2019 | CNN + RNN, 250 Hz | Recording-level | Accuracy | 86.57% (Gemein also writes 86.56% elsewhere) |
| [Gemein et al.](https://arxiv.org/html/2002.05115) | 2020 | Riemannian geometry (tangent space, geometric mean) | v2.0.0; 21 electrodes, 100 Hz, first 60 s dropped, ≤20 min used | Accuracy | 85.87% |
| [Gemein et al.](https://arxiv.org/html/2002.05115) | 2020 | Braindecode TCN | same | Accuracy | 86.16% |
| [Gemein et al.](https://arxiv.org/html/2002.05115) | 2020 | Braindecode Deep4 / Shallow / EEGNet | same | Accuracy | 84.57% / 84.13% / 83.41% |

#### TUEV: 5-s segments, BIOT protocol (200 Hz, official eval set as test; 16 bipolar channels for BIOT, baselines and CBraMod, but 23 channels for LaBraM and EEGPT)
| Paper | Year | Method | Protocol | Metric | Result (BAcc / κ / weighted F1) |
|---|---|---|---|---|---|
| SPaRCNet, via [BIOT Table 5](https://arxiv.org/html/2305.10351) | 2023 | CNN | as above | BAcc / κ / wF1 | 0.4161 ± 0.0262 / 0.4233 ± 0.0181 / 0.7024 ± 0.0104 |
| ContraWR, via [BIOT](https://arxiv.org/html/2305.10351) | 2021 | Contrastive CNN | as above | same | 0.4384 ± 0.0349 / 0.3912 ± 0.0237 / 0.6893 ± 0.0136 |
| ST-Transformer, via [BIOT](https://arxiv.org/html/2305.10351) | 2021 | Transformer | as above | same | 0.3984 ± 0.0228 / 0.3765 ± 0.0306 / 0.6823 ± 0.0190 |
| EEGNet, via [CBraMod Table 13](https://arxiv.org/html/2412.07236) | 2018 | Compact CNN | as above | same | 0.3876 ± 0.0143 / 0.3577 ± 0.0155 / 0.6539 ± 0.0120 |
| EEG Conformer, via [CBraMod](https://arxiv.org/html/2412.07236) | 2022 | CNN + transformer | as above | same | 0.4074 ± 0.0164 / 0.3967 ± 0.0195 / 0.6983 ± 0.0152 |
| [Yang et al. (BIOT)](https://arxiv.org/html/2305.10351) | 2023 | BIOT, from scratch | as above | same | 0.4682 ± 0.0125 / 0.4482 ± 0.0285 / 0.7085 ± 0.0184 |
| [Yang et al. (BIOT)](https://arxiv.org/html/2305.10351) | 2023 | BIOT, supervised + unsupervised pretraining ("ultimate") | as above | same | 0.5281 ± 0.0225 / 0.5273 ± 0.0249 / 0.7492 ± 0.0082 |
| [Jiang et al. (LaBraM)](https://arxiv.org/html/2405.18765) | 2024 | LaBraM-Base | as above | same | 0.6409 ± 0.0065 / 0.6637 ± 0.0093 / 0.8312 ± 0.0052 |
| [Jiang et al. (LaBraM)](https://arxiv.org/html/2405.18765) | 2024 | LaBraM-Huge | as above | same | 0.6616 ± 0.0170 / 0.6745 ± 0.0195 / 0.8329 ± 0.0086 |
| [Wang et al. (EEGPT)](https://papers.neurips.cc/paper_files/paper/2024/file/4540d267eeec4e5dbd9dae9448f0b739-Paper-Conference.pdf) | 2024 | EEGPT (25M) | as above | same | 0.6232 ± 0.0114 / 0.6351 ± 0.0134 / 0.8187 ± 0.0063 |
| [Wang et al. (CBraMod)](https://arxiv.org/html/2412.07236) | 2025 | CBraMod, TUEV excluded from pretraining | as above | same | 0.6659 ± 0.0124 / 0.6744 ± 0.0121 / 0.8331 ± 0.0071 |
| [Wang et al. (CBraMod)](https://arxiv.org/html/2412.07236) | 2025 | CBraMod | as above | same | 0.6671 ± 0.0107 / 0.6772 ± 0.0096 / 0.8342 ± 0.0064 |

EEGPT's table orders the columns BAcc, weighted F1, κ; I reordered them to match.

#### TUSZ: NEDC any-overlap (OVLP) scoring, TUSZ v1.5.2 eval set
All rows read in [Khalkhali et al. 2021, Table 5](https://arxiv.org/pdf/2202.07796); sia and pnc98 are the top Neureka 2020 challenge systems, cnnlstm and mphase are earlier NEDC systems.
| Paper | Year | Method | Protocol | Metric | Result (sensitivity / FA per 24 h) |
|---|---|---|---|---|---|
| cnnlstm (Golmohammadi), via [Khalkhali](https://arxiv.org/pdf/2202.07796) | — | CNN + LSTM | OVLP, eval | Sens. / FA/24h | 51.47% / 19.25 |
| mphase (Shah), via [Khalkhali](https://arxiv.org/pdf/2202.07796) | — | Multiphase hybrid | OVLP, eval | same | 44.62% / 11.45 |
| sia (Neureka team), via [Khalkhali](https://arxiv.org/pdf/2202.07796) | 2020 | Challenge entry | OVLP, eval | same | 23.88% / 0.96 |
| pnc98 (Neureka team), via [Khalkhali](https://arxiv.org/pdf/2202.07796) | 2020 | Challenge entry | OVLP, eval | same | 8.41% / 0.16 |
| [Khalkhali et al.](https://arxiv.org/pdf/2202.07796) | 2021 | ResNet on grayscale EEG images, low latency | OVLP, eval | same | 37.18% / 3.82 |

On the v1.5.2 dev set the same ResNet scores 42.05% at 5.78 FA/24h. Under the stricter TAES scoring on eval, sia's sensitivity falls to 12.37% (same source). The Neureka challenge ranked systems by a weighted TAES score that penalized false alarms and channel count, which is why its winners trade sensitivity for very few false alarms.

#### TUSZ: SzCORE event-based scoring, TUSZ v2.0.3 eval set (no FA/24h reported)
All baselines were re-run by [Wu et al.](https://arxiv.org/html/2504.00336) with the SzCORE scorer (any overlap, 30 s pre / 60 s post tolerance, events merged under 90 s, split above 5 min, per [SzCORE](https://arxiv.org/html/2402.13005)).
| Paper | Year | Method | Protocol | Metric | Result (F1 / sensitivity / precision) |
|---|---|---|---|---|---|
| Gotman, via [Wu et al. Table 2](https://arxiv.org/html/2504.00336) | 1982 | Rule-based | event-based, eval | F1 / Sens. / Prec. | 0.2089 / 0.6199 / 0.1256 |
| EEGWaveNet, via [Wu et al.](https://arxiv.org/html/2504.00336) | 2021 | CNN | same | same | 0.2603 / 0.4427 / 0.1844 |
| DCRNN, via [Wu et al.](https://arxiv.org/html/2504.00336) | 2021 | Graph RNN | same | same | 0.3262 / 0.5723 / 0.2281 |
| Zhu-Transformer, via [Wu et al.](https://arxiv.org/html/2504.00336) | 2023 | CNN + transformer | same | same | 0.5387 / 0.6116 / 0.5259 |
| DeepSOZ-HEM, via [Wu et al.](https://arxiv.org/html/2504.00336) | 2023 | LSTM + transformer | same | same | 0.5940 / 0.6222 / 0.4306 |
| EventNet, via [Wu et al.](https://arxiv.org/html/2504.00336) | 2024 | U-Net | same | same | 0.5655 / 0.6116 / 0.5259 (sensitivity and precision identical to Zhu-Transformer in the source; possibly a copy error) |
| [Wu et al. (SeizureTransformer)](https://arxiv.org/html/2504.00336) | 2025 | U-Net + transformer, trained on TUSZ (+ Siena), threshold 0.8 | same | same | 0.6713 / 0.7168 / 0.6312 |

Sample-based F1 for SeizureTransformer is 0.5730 in the same table. The model also won the 2025 seizure detection challenge (International Conference on AI in Epilepsy) on a hidden test set with event F1 0.43, sensitivity 0.37, precision 0.45 and 1 FP per day ([Wu et al. Table 7](https://arxiv.org/html/2504.00336)); the source table does not name that test dataset.

#### SzCORE baselines: subject-independent models, cross-validation within each dataset, event-based scoring
Read in [SzCORE Table 2](https://arxiv.org/html/2402.13005). Each model was run on only some datasets.
| Paper | Year | Method | Protocol | Metric | Result (F1 / Sens. / Prec. / FP per day) |
|---|---|---|---|---|---|
| [Dan et al. (SzCORE)](https://arxiv.org/html/2402.13005) | 2024 | Random forest, zero-crossing features | CHB-MIT | event-based | 53.9 / 37.0 / 64.5 / 1.66 |
| [Dan et al. (SzCORE)](https://arxiv.org/html/2402.13005) | 2024 | XGBoost, DWT + zero-crossing features | CHB-MIT | event-based | 66.0 / 67.1 / 75.3 / 2.09 |
| [Dan et al. (SzCORE)](https://arxiv.org/html/2402.13005) | 2024 | Random forest | Siena | event-based | 59.3 / 32.9 / 62.5 / 1.7 |
| [Dan et al. (SzCORE)](https://arxiv.org/html/2402.13005) | 2024 | STFT vision transformer | Siena | event-based | 22.8 / 56.9 / 18.7 / 34.4 |
| [Dan et al. (SzCORE)](https://arxiv.org/html/2402.13005) | 2024 | STFT vision transformer | TUH (CV, not the official eval split) | event-based | 63.2 / 76.5 / 53.9 / 40.6 |

#### CHB-MIT: patient-specific detection
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Shoeb & Guttag](https://icml.cc/Conferences/2010/papers/493.pdf) | 2010 | Patient-specific SVM on spectral features | Per patient, leave one seizure record out (≥2 training seizures); 24 patients (23 pediatric CHB patients plus 1 adult from Beth Israel Deaconess), 916 h, 173 test seizures | Sensitivity; median false detections per 24 h; latency | 96% detected; median 2 per 24 h; mean latency 4.6 s (median 3 s) |

#### CHB-MIT: cross-patient, 10-s segments (patients 1–19 train, 20–21 val, 22–23 test, 16 bipolar channels, 200 Hz)
BIOT averages two runs with validation and test swapped; CBraMod describes only the first split. Treat the two sources as close but not identical.
| Paper | Year | Method | Protocol | Metric | Result (BAcc / AUC-PR / AUROC) |
|---|---|---|---|---|---|
| SPaRCNet, via [BIOT Table 2](https://arxiv.org/html/2305.10351) | 2023 | CNN | BIOT split | BAcc / AUC-PR / AUROC | 0.5876 ± 0.0191 / 0.1247 ± 0.0119 / 0.8143 ± 0.0148 |
| CNN-Transformer, via [BIOT](https://arxiv.org/html/2305.10351) | 2022 | CNN + transformer | BIOT split | same | 0.6389 ± 0.0067 / 0.2479 ± 0.0227 / 0.8662 ± 0.0082 |
| [Yang et al. (BIOT)](https://arxiv.org/html/2305.10351) | 2023 | BIOT, from scratch | BIOT split | same | 0.6640 ± 0.0037 / 0.2573 ± 0.0088 / 0.8646 ± 0.0030 |
| [Yang et al. (BIOT)](https://arxiv.org/html/2305.10351) | 2023 | BIOT, pretrained on 6 EEG datasets | BIOT split | same | 0.7068 ± 0.0457 / 0.3277 ± 0.0460 / 0.8761 ± 0.0284 |
| EEGNet, via [CBraMod Table 8](https://arxiv.org/html/2412.07236) | 2018 | Compact CNN | CBraMod split | same | 0.5658 ± 0.0106 / 0.1914 ± 0.0182 / 0.8048 ± 0.0136 |
| LaBraM-Base, via [CBraMod](https://arxiv.org/html/2412.07236) | 2024 | Fine-tuned by CBraMod authors | CBraMod split | same | 0.7075 ± 0.0358 / 0.3287 ± 0.0402 / 0.8679 ± 0.0199 |
| [Wang et al. (CBraMod)](https://arxiv.org/html/2412.07236) | 2025 | CBraMod | CBraMod split | same | 0.7398 ± 0.0284 / 0.3689 ± 0.0382 / 0.8892 ± 0.0154 |

#### Bonn: segment classification. Not directly comparable (class groupings and splits differ by paper)
All rows read in [Lu & Triesch 2019, Table 1](https://arxiv.org/pdf/1903.08100).
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| Chua et al., via [Lu & Triesch](https://arxiv.org/pdf/1903.08100) | 2009 | Higher-order spectra + GMM | as in original | Accuracy | 93.1% |
| Acharya et al., via [Lu & Triesch](https://arxiv.org/pdf/1903.08100) | 2011 | DWT + SVM | as in original | Accuracy | 96.3% |
| Sharma et al., via [Lu & Triesch](https://arxiv.org/pdf/1903.08100) | 2015 | EMD + LS-SVM | as in original | Accuracy | 98.67% |
| Acharya et al., via [Lu & Triesch](https://arxiv.org/pdf/1903.08100) | 2018 | 13-layer CNN on raw EEG | as in original | Accuracy | 88.67% (the text of the same paper says 88.0%) |
| Ahmedt-Aristizabal et al., via [Lu & Triesch](https://arxiv.org/pdf/1903.08100) | 2018 | LSTM on raw EEG | as in original | Accuracy | 95.53% |
| [Lu & Triesch](https://arxiv.org/pdf/1903.08100) | 2019 | Residual CNN on raw EEG | AB vs CD vs E; random 60/20/20 split of segments | Accuracy | 99.0% |

#### HMS Harmful Brain Activity: Kaggle leaderboard, KL divergence (lower is better)
Read in [VIPEEGNet Table 2](https://arxiv.org/html/2507.08874) (2,767 teams). Public = 35% of test, private = 65%.
| Paper | Year | Method | Protocol | Metric | Result (public / private) |
|---|---|---|---|---|---|
| Team Sony (rank 1), via [VIPEEGNet](https://arxiv.org/html/2507.08874) | 2024 | EEG: 4 ConvNeXt-Atto + InceptionNeXt-Tiny; spectrogram: 11 MaxViT-base + 14 SwinV2-Tiny (1,762M params) | Hidden test | KL divergence | 0.2161 / 0.2723 |
| Holiday (rank 2), via [VIPEEGNet](https://arxiv.org/html/2507.08874) | 2024 | EfficientNet-B5, PPHGNetV2, X3D-L ensembles | same | same | 0.2243 / 0.2738 |
| Nvidia/DD (rank 3), via [VIPEEGNet](https://arxiv.org/html/2507.08874) | 2024 | 1D CNN + Squeezeformer; MixNet | same | same | 0.2255 / 0.2741 |
| Aillis & GO & bilzard (rank 4), via [VIPEEGNet](https://arxiv.org/html/2507.08874) | 2024 | 1D CNN + MobileNetV2; SwinV2-Large; ViT-Tiny + CAFormer + ConvNeXt | same | same | 0.2186 / 0.2760 |
| KTMUD (rank 5), via [VIPEEGNet](https://arxiv.org/html/2507.08874) | 2024 | WaveNet + 2D CNN | same | same | 0.2259 / 0.2762 |
| Mikhail Kotyushev (rank 16), via [VIPEEGNet](https://arxiv.org/html/2507.08874) | 2024 | ViT-Tiny | same | same | 0.2377 / 0.2946 |
| [Peters (rank 60)](https://www.ryanirl.com/blog/hbac/) | 2024 | Multimodal 1D EEG + spectrogram | same | same | private 0.338933 |
| [Sun et al. (VIPEEGNet)](https://arxiv.org/html/2507.08874) | 2025 | EfficientNetV2-B3 (49M), submitted after the competition | same | same | 0.2233 / 0.2725 |

Peters also gives the winning private score as 0.272332, which matches the 0.2723 above.

#### NeurIPS 2025 EEG Foundation Challenge: final results (normalized RMSE, lower is better; 1.0 = predicting the mean)
Read on the [official leaderboard page](https://eeg2025.github.io/leaderboard/) (1,183 teams, over 8,000 submissions on Codabench). Test data: HBN release 12.
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| KUL_EEG (1st), [leaderboard](https://eeg2025.github.io/leaderboard/) | 2025 | not described on the page | Challenge 1: per-trial response time, contrast change detection | nRMSE | 0.88668 |
| Sigma Nova (2nd), [leaderboard](https://eeg2025.github.io/leaderboard/) | 2025 | not described | Challenge 1 | nRMSE | 0.90932 |
| MIN~C² (MIND-CICO) (3rd), [leaderboard](https://eeg2025.github.io/leaderboard/) | 2025 | not described | Challenge 1 | nRMSE | 0.91026 |
| Meta Brain & AI, [leaderboard](https://eeg2025.github.io/leaderboard/) | 2025 | not described | Challenge 1 | nRMSE | 0.9106 |
| MBZUAI \[dsml.kz\], [leaderboard](https://eeg2025.github.io/leaderboard/) | 2025 | not described | Challenge 1 | nRMSE | 0.91394 |
| BCILab, [leaderboard](https://eeg2025.github.io/leaderboard/) | 2025 | not described | Challenge 1 | nRMSE | 0.91856 |
| JLShen (1st), [leaderboard](https://eeg2025.github.io/leaderboard/) | 2025 | not described | Challenge 2: externalizing factor per subject | nRMSE | 0.97843 |
| MBZUAI \[dsml.kz\] (2nd), [leaderboard](https://eeg2025.github.io/leaderboard/) | 2025 | not described | Challenge 2 | nRMSE | 0.98519 |
| MIN~C² (MIND-CICO) (3rd), [leaderboard](https://eeg2025.github.io/leaderboard/) | 2025 | not described | Challenge 2 | nRMSE | 0.98817 |

Challenge 2 scores are affected by the unshuffled test order described in B.2; the organizers used 0.99 as the threshold for including Challenge 2 in the final scoring.

#### SEED: subject-dependent (first 9 trials train, last 6 test, all bands), accuracy % (mean / std)
All rows read in [RGNN Table 1](https://arxiv.org/pdf/1907.07835).
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| SVM, via [RGNN](https://arxiv.org/pdf/1907.07835) | — | SVM on DE features | as above | Accuracy | 83.99 / 9.92 |
| Zheng & Lu (DBN), via [RGNN](https://arxiv.org/pdf/1907.07835) | 2015 | Deep belief network | as above | Accuracy | 86.08 / 8.34 |
| DGCNN, via [RGNN](https://arxiv.org/pdf/1907.07835) | 2018 | Dynamical graph CNN | as above | Accuracy | 90.40 / 8.49 |
| BiDANN, via [RGNN](https://arxiv.org/pdf/1907.07835) | 2018 | Bi-hemisphere domain-adversarial NN | as above | Accuracy | 92.38 / 7.04 |
| BiHDM, via [RGNN](https://arxiv.org/pdf/1907.07835) | 2019 | Bi-hemisphere discrepancy model | as above | Accuracy | 93.12 / 6.06 |
| [Zhong et al. (RGNN)](https://arxiv.org/pdf/1907.07835) | 2020 | Regularized graph NN | as above | Accuracy | 94.24 / 5.95 |

#### SEED: subject-independent (leave one subject out, one session), accuracy % (mean / std)
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| SVM, via [RGNN Table 2](https://arxiv.org/pdf/1907.07835) | — | SVM | LOSO | Accuracy | 56.73 / 16.29 |
| DGCNN, via [RGNN](https://arxiv.org/pdf/1907.07835) | 2018 | Dynamical graph CNN | LOSO | Accuracy | 79.95 / 9.02 |
| DAN, via [RGNN](https://arxiv.org/pdf/1907.07835) | 2018 | Domain adaptation network | LOSO | Accuracy | 83.81 / 8.56 |
| BiDANN-S, via [RGNN](https://arxiv.org/pdf/1907.07835) | 2018 | BiDANN, subject-independent | LOSO | Accuracy | 84.14 / 6.87 |
| BiHDM, via [RGNN](https://arxiv.org/pdf/1907.07835) | 2019 | Bi-hemisphere discrepancy model | LOSO | Accuracy | 85.40 / 7.53 |
| [Zhong et al. (RGNN)](https://arxiv.org/pdf/1907.07835) | 2020 | Regularized graph NN | LOSO | Accuracy | 85.30 / 6.72 |

#### SEED-IV: same source, subject-dependent (first 16 trials train, last 8 test) and subject-independent (LOSO), accuracy %
| Paper | Year | Method | Protocol | Metric | Result (dependent / independent) |
|---|---|---|---|---|---|
| SVM, via [RGNN](https://arxiv.org/pdf/1907.07835) | — | SVM | as above | Accuracy | 56.61 / 37.99 |
| DGCNN, via [RGNN](https://arxiv.org/pdf/1907.07835) | 2018 | Dynamical graph CNN | as above | Accuracy | 69.88 / 52.82 |
| BiDANN / BiDANN-S, via [RGNN](https://arxiv.org/pdf/1907.07835) | 2018 | Domain-adversarial | as above | Accuracy | 70.29 / 65.59 |
| EmotionMeter, via [RGNN](https://arxiv.org/pdf/1907.07835) | 2019 | EmotionMeter | dependent only | Accuracy | 70.58 / – |
| BiHDM, via [RGNN](https://arxiv.org/pdf/1907.07835) | 2019 | Bi-hemisphere discrepancy model | as above | Accuracy | 74.35 / 69.03 |
| [Zhong et al. (RGNN)](https://arxiv.org/pdf/1907.07835) | 2020 | Regularized graph NN | as above | Accuracy | 79.37 / 73.84 |

#### SEED-V: foundation-model protocol (trials split 5:5:5 per session). The two tables are not directly comparable
CBraMod (public 16-subject version, 1-s samples), [Table 2](https://arxiv.org/html/2412.07236):
| Paper | Year | Method | Protocol | Metric | Result (BAcc / κ / wF1) |
|---|---|---|---|---|---|
| EEGNet, via [CBraMod](https://arxiv.org/html/2412.07236) | 2018 | Compact CNN | 16 subjects | BAcc / κ / wF1 | 0.2961 / 0.1006 / 0.2749 |
| BIOT, via [CBraMod](https://arxiv.org/html/2412.07236) | 2023 | Pretrained BIOT | 16 subjects | same | 0.3837 / 0.2261 / 0.3856 |
| LaBraM-Base, via [CBraMod](https://arxiv.org/html/2412.07236) | 2024 | Fine-tuned by CBraMod authors | 16 subjects | same | 0.3976 / 0.2386 / 0.3974 |
| [Wang et al. (CBraMod)](https://arxiv.org/html/2412.07236) | 2025 | CBraMod | 16 subjects | same | 0.4091 / 0.2569 / 0.4101 |

LaBraM (version with 20 subjects per CBraMod's footnote), [Table 6](https://arxiv.org/html/2405.18765):
| Paper | Year | Method | Protocol | Metric | Result (Acc / κ / wF1) |
|---|---|---|---|---|---|
| BIOT, via [LaBraM](https://arxiv.org/html/2405.18765) | 2023 | BIOT | LaBraM setup | Acc / κ / wF1 | 0.3802 / 0.2247 / 0.3809 |
| [Jiang et al. (LaBraM)](https://arxiv.org/html/2405.18765) | 2024 | LaBraM-Base | LaBraM setup | same | 0.4095 / 0.2613 / 0.4120 |
| [Jiang et al. (LaBraM)](https://arxiv.org/html/2405.18765) | 2024 | LaBraM-Huge | LaBraM setup | same | 0.4102 / 0.2646 / 0.4136 |

Standard deviations are in the sources.

#### DEAP: within-subject, binary high/low, three protocols. Only rows in the same sub-table are comparable
**(a) Leave-one-trial-out, per subject** (read in [TSception Table 5](https://arxiv.org/pdf/2104.02935))
| Paper | Year | Method | Protocol | Metric | Result (arousal / valence) |
|---|---|---|---|---|---|
| Koelstra et al. (DEAP baseline), via [TSception](https://arxiv.org/pdf/2104.02935) | 2012 | Baseline from the DEAP paper (labeled SVM in TSception) | Leave-one-trial-out | Accuracy; F1 | Acc 62.00% / 57.60%; F1 58.30% / 56.30% |
| FBTSC, via [TSception](https://arxiv.org/pdf/2104.02935) | — | Filter-bank tangent-space classifier | same | Accuracy | 60.60% / 61.09% |
| [Ding et al. (TSception)](https://arxiv.org/pdf/2104.02935) | 2022 | Multi-scale temporal + asymmetric spatial CNN | same | Accuracy; F1 | Acc 63.75% / 62.27%; F1 63.35% / 65.37% |

**(b) Trial-wise 10-fold CV, 4-s segments, per subject** ([TSception Table 3](https://arxiv.org/pdf/2104.02935))
| Paper | Year | Method | Protocol | Metric | Result (arousal / valence accuracy) |
|---|---|---|---|---|---|
| [Ding et al.](https://arxiv.org/pdf/2104.02935) | 2022 | SVM | Trial-wise 10-fold | Accuracy | 60.37% / 55.19% |
| [Ding et al.](https://arxiv.org/pdf/2104.02935) | 2022 | EEGNet | same | Accuracy | 58.29% / 54.56% |
| [Ding et al.](https://arxiv.org/pdf/2104.02935) | 2022 | DeepConvNet | same | Accuracy | 61.03% / 59.92% |
| [Ding et al.](https://arxiv.org/pdf/2104.02935) | 2022 | TSception | same | Accuracy | 61.57% / 59.14% |

**(c) Random 10-fold CV over 1-s segments, per subject: leaky** ([MSBAM Table 1](https://arxiv.org/pdf/2110.06462); the MSBAM authors state this setup has data leakage)
| Paper | Year | Method | Protocol | Metric | Result (valence / arousal accuracy) |
|---|---|---|---|---|---|
| Yang et al., via [MSBAM](https://arxiv.org/pdf/2110.06462) | 2018 | Continuous CNN | Segment-level CV | Accuracy | 90.80% / 91.03% |
| Cui et al., via [MSBAM](https://arxiv.org/pdf/2110.06462) | 2020 | as in original | Segment-level CV | Accuracy | 96.65% / 97.11% |
| [Wu et al. (MSBAM)](https://arxiv.org/pdf/2110.06462) | 2021 | Multi-scale bi-hemispheric asymmetric CNN | Random 10-fold over segments | Accuracy | 99.36% / 99.37% |

#### DREAMER: random 10-fold CV over 1-s segments, per subject: leaky
| Paper | Year | Method | Protocol | Metric | Result (valence / arousal / dominance) |
|---|---|---|---|---|---|
| [Wu et al. (MSBAM)](https://arxiv.org/pdf/2110.06462) | 2021 | MSBAM | as above | Accuracy | 99.69% / 99.76% / 99.79% |

These numbers mostly measure trial identification, not emotion recognition (see B.4). I did not find a trial- or subject-disjoint DREAMER result that I could read.

#### THINGS-EEG: 200-way zero-shot identification (chance 0.5%), top-1 / top-5 %
**NICE paper protocol** ([Song et al. Table 2](https://arxiv.org/pdf/2308.13234))
| Paper | Year | Method | Protocol | Metric | Result (top-1 / top-5) |
|---|---|---|---|---|---|
| BraVL, via [NICE](https://arxiv.org/pdf/2308.13234) | 2023 | Multimodal VAE | Subject-dependent | Top-1 / top-5 | 5.8 / 17.5 |
| [Song et al. (NICE)](https://arxiv.org/pdf/2308.13234) | 2024 | EEG–image contrastive (CLIP) | Subject-dependent | same | 13.8 / 39.5 |
| [Song et al. (NICE-GA)](https://arxiv.org/pdf/2308.13234) | 2024 | NICE + graph attention | Subject-dependent | same | 15.6 / 42.8 |
| BraVL, via [NICE](https://arxiv.org/pdf/2308.13234) | 2023 | Multimodal VAE | Leave one subject out | same | 1.8 / 7.0 |
| [Song et al. (NICE)](https://arxiv.org/pdf/2308.13234) | 2024 | NICE | Leave one subject out | same | 6.2 / 21.4 |
| [Song et al. (NICE-SA)](https://arxiv.org/pdf/2308.13234) | 2024 | NICE + self-attention | Leave one subject out | same | 7.0 / 23.1 |

**ATM paper protocol** (batch size 1024; its own re-runs; [Li et al. Table 8](https://arxiv.org/html/2403.07721)). Not comparable with the NICE table: ATM's re-run of NICE scores 19.32 top-1 vs 13.8 in the NICE paper.
| Paper | Year | Method | Protocol | Metric | Result (top-1 / top-5) |
|---|---|---|---|---|---|
| NICE, via [ATM](https://arxiv.org/html/2403.07721) | 2024 | Re-run by ATM authors | Subject-dependent | Top-1 / top-5 | 19.32 ± 5.33 / 49.26 ± 9.69 |
| EEGNetV4, via [ATM](https://arxiv.org/html/2403.07721) | 2018 | Re-run by ATM authors | Subject-dependent | same | 19.51 ± 5.19 / 48.99 ± 6.75 |
| [Li et al. (ATM-S)](https://arxiv.org/html/2403.07721) | 2024 | Adaptive thinking mapper | Subject-dependent | same | 28.64 ± 6.39 / 58.47 ± 8.97 |
| NICE, via [ATM](https://arxiv.org/html/2403.07721) | 2024 | Re-run by ATM authors | Leave one subject out | same | 8.24 ± 3.01 / 23.76 ± 5.09 |
| [Li et al. (ATM-S)](https://arxiv.org/html/2403.07721) | 2024 | Adaptive thinking mapper | Leave one subject out | same | 11.84 ± 4.80 / 33.73 ± 8.73 |

#### Sleep-EDF and SHHS
Not repeated here. Sleep-staging results (accuracy, κ, macro-F1 on SleepEDF-20, SleepEDF-78 and SHHS, EEG-only vs EEG + EOG) are in Part 2 of the [EOG datasets file](../emg-eog-ecg/eog/DATASETS.md).

---

### B.4 How to read these numbers

- **TUAB has two incompatible scores.** Recording-level accuracy on 276 eval recordings ([Gemein](https://arxiv.org/html/2002.05115), 81–86% for every method they tried) and 10-s segment-level balanced accuracy / AUROC (BIOT protocol, 0.78–0.83 balanced accuracy) are different tasks. Do not put them in one ranking.
- **Label ceilings.** Gemein et al. argue TUAB accuracy may saturate near 90% because published neurologist agreement on normal vs abnormal is 86–88%. TUEV, TUSZ and TUAR were labeled by trained annotators with agreement mostly not quantified in the releases, and HMS labels are vote distributions with 1–28 votes per training segment.
- **Foundation-model gains are small on TUAB and larger on TUEV.** From BIOT to CBraMod, TUAB balanced accuracy moves from 0.7959 to 0.8289, while TUEV moves from 0.5281 to 0.6671. A supervised U-Net without pretraining (SeizureTransformer, 0.8144) matches LaBraM-Base on TUAB balanced accuracy, though not on AUROC.
- **Pretraining overlap.** TUAB and TUEV are subsets of TUEG, which CBraMod pretrains on. LaBraM pretrains on other TUH subsets (TUAR, TUEP, TUSZ, TUSL) and states the TUAB and TUEV recordings are disjoint from its pretraining data; CBraMod re-pretrained without them and lost at most 0.004 balanced accuracy. Check this for any new model.
- **Copied baselines.** Most baseline rows in the TUAB, TUEV and CHB-MIT segment tables are the same BIOT runs copied forward. They were not re-tuned for each paper, and EEGPT says it uses linear probing while the baselines were fully fine-tuned.
- **Benchmarks disagree on whether foundation models win.** [EEG-Bench](https://arxiv.org/abs/2512.08959) (2025) reports that simpler models often stay competitive under clinical distribution shift. [EEG-Arena](https://arxiv.org/abs/2609.32743) (2026, 30 models, 57 tasks) reports that foundation models beat strong supervised baselines on most tasks. A [negative-control study](https://arxiv.org/abs/2607.24519) (2026) found all five encoders it tested could identify which dataset a recording came from with 1.000 accuracy, so cross-dataset results can be confounded by dataset identity.
- **Seizure scoring decides the number.** OVLP (any overlap) gives much higher sensitivity than TAES on the same system (sia: 23.88% vs 12.37% on TUSZ eval). SzCORE event scoring adds 30 s / 60 s tolerances and event merging. Sample-based and event-based F1 differ by about 0.1 for SeizureTransformer. Always report the scoring method, the TUSZ version and dev vs eval.
- **False alarms per 24 h is the clinical metric.** A segment AUROC of 0.89 (CBraMod on CHB-MIT) says nothing about how many false alarms a day a patient would get. Low-FA systems pay in sensitivity: pnc98 reached 0.16 FA/24h at 8.41% sensitivity.
- **Patient-specific vs cross-patient.** Shoeb & Guttag detect 96% of seizures with a median 2 false detections per day when trained on each patient's own seizures. Cross-patient models on the same data (SzCORE, BIOT protocol) are far lower. On CHB-MIT, also check that chb01 and chb21 (same person) are not split across train and test.
- **Bonn numbers are not clinical performance.** Short, hand-picked single-channel segments, healthy scalp vs patient intracranial recordings, and random segment splits produce results near 99% that say little about continuous scalp EEG.
- **Emotion datasets leak through segments.** With 15–40 trials per subject, random splits of 1–4 s segments put pieces of the same trial in train and test. On DEAP this gives about 99% (MSBAM, which admits the leakage) against about 60–64% for trial-wise or leave-one-trial-out splits (TSception). The KU Leuven AAD authors warn about the same "trial fingerprint" effect. Prefer trial-disjoint or subject-disjoint splits.
- **SEED subject-dependent vs subject-independent.** The same RGNN model scores 94.24% subject-dependent and 85.30% subject-independent on SEED (79.37% vs 73.84% on SEED-IV). SEED-V numbers from LaBraM (20 subjects) and CBraMod (16 subjects) use different data.
- **Leaderboards.** HMS public and private scores differ (Team Sony 0.2161 vs 0.2723); only private scores are final, and post-competition submissions such as VIPEEGNet were not ranked in the competition. In the NeurIPS 2025 challenge, nRMSE 1.0 means predicting the mean, so the Challenge 2 winner (0.97843) explains very little variance, and that score may be helped by the unshuffled test order.
- **THINGS-EEG results depend on re-implementation.** The same NICE model is 13.8% top-1 in its own paper and 19.32% in ATM's re-run. Compare only rows from the same paper, and note that test inputs are averages over 80 repetitions.
- **"via" numbers are second-hand.** They were read in the citing paper's table, which may use its own re-implementation or a different version of the data.
