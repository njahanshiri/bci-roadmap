# EMG Datasets and Benchmark Results

This page has full specifications for the main public EMG datasets and the published results on each. Every number links to the paper or official page where it was read. If a source did not report a value, the cell says "not reported". If I could not read the value in a source myself, it is left out or marked *not verified*.

## Overview

| Dataset | Subjects | Channels | Sampling rate | Task / classes | Size on disk | License |
|---|---|---|---|---|---|---|
| Ninapro DB1 | 27 intact | 10 | 100 Hz (RMS signal) | 52 movements + rest | not reported | CC BY 4.0 |
| Ninapro DB2 | 40 intact | 12 | 2 kHz | 49 movements + rest | not reported | CC BY 4.0 |
| Ninapro DB3 | 11 amputees | 12 (10 for 2 subjects) | 2 kHz | up to 49 + rest | not reported | CC BY 4.0 |
| Ninapro DB5 | 10 intact | 16 (2 Myo) | 200 Hz | 52 + rest | not reported | *not verified* |
| Ninapro DB7 | 20 intact + 2 amputees | 12 (+ 9-axis IMU) | 2 kHz | 40 movements | 30.9 GB (per TinyMyo) | *not verified* |
| CapgMyo (DB-a/b/c) | 23 (18 / 10 / 10 per subset) | 128 (8×16 grid) | 1 kHz | 8 / 8 / 12 gestures | not reported | *not verified* |
| CSL-HDEMG | 5 | 192 electrodes, 7×24 bipolar channels | 2048 Hz | 27 finger gestures | not reported | *not verified* |
| Hyser | 20 | 256 (4 × 8×8 grids) | 2048 Hz | 34 gestures + finger forces | 142.8 GB | ODC-By 1.0 |
| GRABMyo | 43 | 28 (16 forearm + 12 wrist) | 2048 Hz | 16 gestures + rest | 9.4 GB | CC BY 4.0 |
| EMG-EPN-612 | 612 | 8 (Myo) | 200 Hz | 5 gestures + relax | 5.5 GB | CC BY 4.0 |
| putEMG | 44 | 24 (3×8) | 5120 Hz | 7 gestures + idle | not reported | CC BY-NC 4.0 |
| emg2qwerty | 108 | 2 × 16 (both wrists) | 2 kHz | Typing → characters | not reported | CC BY-NC-SA 4.0 |
| emg2pose | 193 | 16 per wrist | 2 kHz (from 22 kHz) | 20-DoF hand angles | 431 GB (per TinyMyo) | CC BY-NC-SA 4.0 |
| Meta Generic Neuromotor Interface | 100 per task | 16 | 2 kHz | Discrete gestures, handwriting, wrist angle | not reported | CC BY-NC 4.0 |

Sources are in each dataset's block below.

---

## Part 1: Dataset specifications

### Ninapro DB1
| Field | Value |
|---|---|
| Year & paper | 2014; Atzori et al., *Scientific Data* ([PMC4421935](https://pmc.ncbi.nlm.nih.gov/articles/PMC4421935)); the official site also cites an Atzori et al. 2014 IEEE TNSRE paper ([DB1 page](https://ninapro.hevs.ch/instructions/DB1.html)) |
| Subjects | 27 intact: 20 male, 7 female; 25 right-handed; age 28 ± 3.4 |
| Device & electrodes | 10 Otto Bock MyoBock 13E200-50 electrodes; CyberGlove II (22 sensors) |
| Channels & placement | 8 equally spaced around the forearm at the radio-humeral joint, plus 2 on the flexor and extensor digitorum superficialis |
| Sampling rate | 100 Hz. The electrodes output an RMS-rectified signal, not raw EMG |
| ADC resolution | 12-bit (National Instruments card) |
| Hardware filters | Band-pass and 50 Hz filtering inside the Otto Bock electrode (cutoffs not reported) |
| Tasks / labels | 52 movements + rest in 3 exercises; labels from the stimulus, with a relabeled version ("restimulus"); CyberGlove kinematics |
| Repetitions | 10 per movement, 5 s movement + 3 s rest; one session |
| Size / format | Size not reported; one MATLAB file per subject per exercise |
| License | CC BY 4.0 (metadata CC0) |
| Standard protocol | Train on about 2/3 of repetitions, test on repetitions 2, 5 and 7 ([PMC4421935](https://pmc.ncbi.nlm.nih.gov/articles/PMC4421935)) |
| Known issues | Signal is pre-rectified and low-rate, so raw-EMG methods do not apply directly; labels are relabeled offline with a likelihood-ratio algorithm; recordings drift with repetition number in some subjects |

### Ninapro DB2
| Field | Value |
|---|---|
| Year & paper | 2014; Atzori et al., *Scientific Data* ([PMC4421935](https://pmc.ncbi.nlm.nih.gov/articles/PMC4421935)) |
| Subjects | 40 intact: 28 male, 12 female; 34 right-handed; age 29.9 ± 3.9 |
| Device & electrodes | 12 Delsys Trigno wireless; CyberGlove II; Finger Force Linear Sensor |
| Channels & placement | 8 around the forearm at the radio-humeral joint, 2 on the flexor digitorum superficialis, 2 on the extensor digitorum, 2 on biceps/triceps ([DB2 page](https://ninapro.hevs.ch/instructions/DB2.html)) |
| Sampling rate | EMG 2 kHz; accelerometers 148 Hz |
| ADC resolution | not reported |
| Hardware filters | not reported; 50 Hz harmonics removed with a Hampel filter |
| Tasks / labels | 49 movements + rest (exercises B 17, C 23, D 9 force patterns); glove kinematics; force for exercise D |
| Repetitions | 6 per movement; one session |
| Size / format | Size not reported; MATLAB |
| License | CC BY 4.0 |
| Standard protocol | Repetitions 1, 3, 4, 6 train; 2, 5 test |
| Known issues | Same relabeling and drift notes as DB1 |

### Ninapro DB3
| Field | Value |
|---|---|
| Year & paper | 2014; Atzori et al., *Scientific Data* ([PMC4421935](https://pmc.ncbi.nlm.nih.gov/articles/PMC4421935)) |
| Subjects | 11 trans-radial amputees, all male; age 42.36 ± 11.96; 0–90% of forearm remaining; 1–14 years since amputation ([DB3 page](https://ninapro.hevs.ch/instructions/DB3.html)) |
| Device, channels, rates | Same as DB2 (12 Delsys at 2 kHz), but only 10 electrodes for subjects 7–8 because there was not enough space |
| Tasks | Up to 49 movements + rest, 6 repetitions |
| License / format | CC BY 4.0; MATLAB |
| Standard protocol | Repetitions 2, 5 test |
| Known issues | Subjects 1, 3 and 10 stopped early from fatigue or pain (39, 49 and 43 movements done); channel count varies |

### Ninapro DB5
| Field | Value |
|---|---|
| Year & paper | 2017; Pizzolato et al., *PLoS One* ([PMC5638457](https://pmc.ncbi.nlm.nih.gov/articles/PMC5638457/)) |
| Subjects | 10 intact: 8 male, 2 female; age 22–34 ([DB5 page](https://ninapro.hevs.ch/instructions/DB5.html)) |
| Device & electrodes | Two Thalmic Myo armbands; CyberGlove (22 sensors) |
| Channels & placement | 16: one Myo at the radio-humeral joint, the second rotated 22.5° |
| Sampling rate / ADC | 200 Hz, 8-bit signed |
| Hardware filters | Built-in 50 Hz notch on the Myo |
| Tasks | 52 movements + rest (the paper's analysis used 41 classes: exercises B and C + rest) |
| Repetitions | 6 per movement |
| Format / license | MATLAB; license *not verified* |
| Standard protocol | Repetitions 1, 3, 4, 6 train; 2, 5 test |
| Known issues | 200 Hz is below the EMG band (aliasing); many papers use different class subsets (18, 41 or 52 classes) |

### Ninapro DB7
| Field | Value |
|---|---|
| Year & paper | 2017; Krasoulis et al., *J. NeuroEng. Rehabil.* ([PMC5505040](https://pmc.ncbi.nlm.nih.gov/articles/PMC5505040/)) |
| Subjects | 20 intact + 2 trans-radial amputees (male, 28 and 54); age range 22–54 ([DB7 page](https://ninapro.hevs.ch/instructions/DB7.html)) |
| Device | 12 Delsys Trigno IM (EMG + accelerometer, gyroscope, magnetometer per sensor) |
| Sampling rate | EMG 2 kHz |
| Tasks | 40 movements in 2 exercises (subject 21 did 38) |
| Repetitions | 6 |
| Size / format | 30.9 GB as reported by [TinyMyo](https://arxiv.org/html/2512.15729v2); MATLAB |
| Standard protocol | 6-fold cross-validation over repetitions (train on 5, test on 1) |

**Other Ninapro sets, in brief** ([ninapro.hevs.ch](https://ninapro.hevs.ch/)):
- DB4: 10 subjects, 12 Cometa sensors, sEMG + kinematics.
- DB6: repeatability study, 10 subjects recorded twice a day for 5 days with 14 Delsys sensors.
- DB8: finger regression, 10 intact + 2 amputees, 16 Delsys.
- DB9: 77 subjects, large-scale kinematics.
- DB10: 30 intact + 15 amputees, 12 Delsys + eye tracking.

### CapgMyo (DB-a, DB-b, DB-c)
| Field | Value |
|---|---|
| Year & paper | 2016–2017; Geng et al., *Sci. Rep.* 2016 ([PMC5109222](https://pmc.ncbi.nlm.nih.gov/articles/PMC5109222/)); Du et al., *Sensors* 2017 ([PMC5375744](https://pmc.ncbi.nlm.nih.gov/articles/PMC5375744)) |
| Subjects | 23 able-bodied, age 23–26; DB-a 18, DB-b 10, DB-c 10 (overlapping); sex not reported |
| Device & electrodes | Custom wearable with 8 modules; silver wet disposable electrodes, 3 mm diameter; 7.5 mm × 10.05 mm spacing |
| Channels & placement | 128 (8×16 array) wrapped around the right forearm |
| Sampling rate / ADC | 1000 Hz, 16-bit |
| Hardware filters | Band-pass 20–380 Hz; 45–55 Hz band-stop |
| Tasks | DB-a and DB-b: 8 isometric/isotonic gestures (Ninapro nos. 13–20). DB-c: 12 finger movements (Ninapro nos. 1–12) |
| Repetitions / sessions | 10 trials per gesture; DB-b has 2 sessions at least 7 days apart (band re-donned) |
| Format | MATLAB `.mat`; preprocessed files keep the middle 1 s of each trial |
| Access / license | http://zju-capg.org/myo/data (per paper; link not checked); a DB-a copy is on [figshare](https://figshare.com/articles/Data_from_Gesture_Recognition_by_Instantaneous_Surface_EMG_Images_CapgMyo-DBa/7210397); license *not verified* |
| Standard protocol | Intra-session: half or most trials train, rest test. Inter-session (DB-b): train session 1, test session 2. Inter-subject: leave-one-subject-out |
| Known issues | Electrode shift between sessions; the released "middle 1 s" segments remove gesture transitions, which makes the task easier than online use |

### CSL-HDEMG
| Field | Value |
|---|---|
| Year & paper | 2015; Amma, Krings, Böer, Schultz, CHI 2015 ([dblp](https://dblp.org/pid/57/5234)); specs below as described by [Geng et al. 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC5109222/) |
| Subjects | 5 |
| Electrodes / channels | 192 electrodes, recorded bipolar as a 7×24 channel grid |
| Sampling rate | 2048 Hz |
| Tasks | 27 finger gestures |
| Sessions / repetitions | 5 sessions per subject, 10 trials per gesture per session |
| ADC, filters, format, license, access | not verified |
| Standard protocol | Leave-one-trial-out within a session |
| Known issues | Only 5 subjects; Geng et al. apply a 3×3 spatial median filter before use |

### Hyser
| Field | Value |
|---|---|
| Year & paper | 2021; Jiang et al., *IEEE TNSRE* ([author manuscript](https://physionet.org/files/hd-semg/1.0.0/manuscript_author_version.pdf), [PhysioNet](https://physionet.org/content/hd-semg/2.0.0/)) |
| Subjects | 20: 12 male, 8 female; age 22–34; 2 sessions on different days |
| Device & electrodes | OT Bioelettronica Quattrocento, gain 150; four 8×8 gelled arrays (10 mm spacing), two on the extensors and two on the flexors |
| Channels | 256 |
| Sampling rate / ADC | 2048 Hz, 16-bit |
| Hardware filters | High-pass 10 Hz, low-pass 500 Hz |
| Tasks / labels | PR set: 34 gestures, each trial with 3 dynamic (1 s) + 1 maintenance (4 s) task. MVC, 1-DoF, N-DoF and random sets with finger forces at 100 Hz |
| Size / format | 142.8 GB (PR 37.1 GB); WFDB `.dat`/`.hea` |
| License | Open Data Commons Attribution v1.0 |
| Standard protocol | PR: within-session leave-one-out; cross-day and cross-subject left to users |
| Known issues | Arrays cannot be placed exactly over specific muscles; large files |

### GRABMyo
| Field | Value |
|---|---|
| Year & paper | 2022; Pradhan, He, Jiang, *Scientific Data* 9:733 ([Europe PMC](https://europepmc.org/article/PMC/PMC9712490), [PhysioNet](https://physionet.org/content/grabmyo/1.1.0/)) |
| Subjects | 43: 23 male, 20 female; age 26.35 ± 2.89 |
| Device & electrodes | OT Bioelettronica EMGUSB2+, gain 500; Ambu monopolar pre-gelled electrodes |
| Channels & placement | 16 forearm (2 rings of 8) + 12 wrist (2 rings of 6), 2 cm apart; 32 stored channels, 4 unused |
| Sampling rate / ADC | 2048 Hz; stored as 16-bit WFDB |
| Filters | Released signals band-passed 10–500 Hz (4th-order Butterworth) with a 60 Hz notch |
| Tasks | 16 hand/finger gestures + rest; 7 trials of 5 s; also used for biometrics |
| Sessions | 3 days (day 1, day 8, day 29) |
| Size / format | 9.4 GB; WFDB (PhysioNet) or `.mat` (IEEE DataPort) |
| License | CC BY 4.0 |
| Standard protocol | Paper baseline is user-specific; cross-day evaluation is the main intended use |

### EMG-EPN-612
| Field | Value |
|---|---|
| Year & paper | 2020 (Zenodo v2.1, [record](https://zenodo.org/record/4023305)); EPN AI lab, Quito |
| Subjects | 612: 306 training users, 306 testing users; demographics not reported |
| Device / channels / rate | Myo armband; 8 channels at 200 Hz (channels and rate as described by [TinyMyo](https://arxiv.org/html/2512.15729v2)) |
| Tasks | 5 gestures (wave-in, wave-out, pinch, open, fist) + relaxed |
| Repetitions | 50 recordings per gesture per user, plus 50 relaxed |
| Size / license | 5.5 GB; CC BY 4.0 |
| Standard protocol | Official split: user-general models trained on the 306 training users and tested on the 306 testing users |
| Known issues | Low sampling rate; only 5 gestures, so accuracies saturate |

### putEMG
| Field | Value |
|---|---|
| Year & paper | 2019; Kaczmarek, Mańkowski, Tomczyński, *Sensors* 19:3548 ([PMC6720505](https://pmc.ncbi.nlm.nih.gov/articles/PMC6720505), [arXiv](https://ar5iv.labs.arxiv.org/html/1907.07428)) |
| Subjects | 44 able-bodied: 8 female, 36 male; age 19–37 |
| Device & electrodes | OT Bioelettronica MEBA, gain 200; reusable wet Ag/AgCl electrodes (10 mm) |
| Channels & placement | 24 (3 bands × 8) on the right forearm at about 14%, 29% and 44% of forearm length |
| Sampling rate / ADC | 5120 Hz, 12-bit |
| Hardware filters | Band-pass 3–900 Hz |
| Tasks / labels | Fist, flexion, extension, 4 pinches, idle (8 classes); labels refined from RGB video (1080p, 30 fps) and depth camera (60 fps) |
| Repetitions / sessions | 20 per gesture per session, 2 sessions one week apart |
| Format / license | HDF5 and CSV (raw ADC values); CC BY-NC 4.0 ([dataset page](https://biolab.put.poznan.pl/putemg-dataset/)) |
| Standard protocol | Per subject and day, 3-fold cross-validation over trials |

### emg2qwerty
| Field | Value |
|---|---|
| Year & paper | 2024; Sivakumar et al., NeurIPS Datasets & Benchmarks ([arXiv](https://arxiv.org/html/2410.20081v1)) |
| Subjects | 108; demographics not reported |
| Device & electrodes | Meta sEMG research device (sEMG-RD), one band per wrist; 16 differential pairs of dry gold-plated electrodes |
| Channels | 32 (16 per wrist) |
| Sampling rate / ADC | 2 kHz, 12-bit, max amplitude 6.6 mV |
| Hardware filters | Band-pass 20–850 Hz (−3 dB) |
| Labels | Keylogger (key-down/up timestamps); prompts are dictionary words and Wikipedia sentences |
| Sessions | 1,135 sessions (1–18 per user); 346.4 h; 5,262,671 keystrokes |
| Format / license | HDF5; CC BY-NC-SA 4.0 ([repo](https://github.com/facebookresearch/emg2qwerty)) |
| Standard protocol | 100 users for training; 8 held-out test users, each with 2 validation + 2 test sessions; metric is character error rate (CER); generic (zero-shot) and personalized results reported |
| Known issues | Band re-donning between sessions; recorded on a physical keyboard, so it may not transfer to typing without a keyboard |

### emg2pose
| Field | Value |
|---|---|
| Year & paper | 2024; Salter et al., NeurIPS Datasets & Benchmarks ([arXiv](https://arxiv.org/html/2412.02725v1)) |
| Subjects | 193 (158 train / 15 val / 20 test) |
| Device | sEMG-RD wristband, 16 bipolar channels, dry gold-plated electrodes |
| Sampling rate / ADC | Recorded at 22 kHz, stored at 2 kHz; 12-bit |
| Filters | Hardware band-pass 20–850 Hz; data then high-passed at 40 Hz |
| Labels | 26-camera OptiTrack motion capture at 60 Hz → 20 joint angles per hand |
| Stages / sessions | 29 stages (23 train, 6 held out); 751 sessions, each with a new band placement; 370.3 h |
| Size / format | 25,253 HDF5 files; 431 GB as reported by [TinyMyo](https://arxiv.org/html/2512.15729v2) |
| License | CC BY-NC-SA 4.0 |
| Standard protocol | Three test splits: held-out users, held-out stages, both. Two tasks: *regression* (pose from EMG only) and *tracking* (initial pose given) |

### Meta Generic Neuromotor Interface data
| Field | Value |
|---|---|
| Year & paper | 2025; Kaifosh, Reardon et al., *Nature* ([paper](https://ideas.repec.org/a/nat/nature/v645y2025i8081d10.1038_s41586-025-09255-w.html), [repo](https://github.com/facebookresearch/generic-neuromotor-interface)) |
| Subjects | 100 per task, split 80 / 10 / 10 |
| Device / channels | Meta sEMG wristband; 16 channels (per [TinyMyo](https://arxiv.org/html/2512.15729v2)) |
| Sampling / filters | 2 kHz; high-passed at 40 Hz |
| Tasks | Discrete gestures (about 63.9 h), handwriting (about 140.7 h), wrist angle (about 77.2 h) |
| Format / license | HDF5; CC BY-NC 4.0 |
| Known issues | The repo warns that metrics may differ slightly from the paper because test participants are subsampled |

---

## Part 2: Results

Within each table, rows use the same protocol and metric unless a row is marked otherwise. A number tagged "via X" was read in paper X's comparison table, not in the original paper.

### Ninapro DB1: intra-subject, about 2/3 of repetitions to train, ~52 classes, accuracy
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Atzori et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC4421935) | 2014 | Random forest, combined features | Reps 2, 5, 7 test; 200 ms | Accuracy | 75.32% |
| [Atzori et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC5013051) | 2016 | Simple CNN | ~2/3 train; **150 ms** | Accuracy | 66.59 ± 6.40% |
| [Geng et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC5109222/) | 2016 | CNN on instantaneous EMG images | ~2/3 train; 28-frame vote (280 ms) | Accuracy | 75.3% (65.1% per frame) |
| [Hu et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC6207326) | 2018 | Attention CNN-RNN | ~2/3 train; 200 ms | Accuracy | 87.0% |
| Wei et al. (MV-CNN), via [HVPN Table 4](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8413066/) | 2019 | Multi-view CNN | 200 ms | Accuracy | 88.2% |
| [Wei, Hong, Wu (HVPN, *Comput. Intell. Neurosci.*)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8413066/) | 2021 | Hierarchical view pooling CNN | Reps 2, 5, 10 test; 200 ms | Accuracy | 88.4% |

### Ninapro DB1: cross-subject (leave one subject out, with MS-AdaBN adaptation)
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| Wei et al. (MV-CNN), via [HVPN Table 5](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8413066/) | 2019 | Multi-view CNN | LOSOCV, 200 ms | Accuracy | 84.3% |
| [Wei, Hong, Wu (HVPN)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8413066/) | 2021 | HVPN | LOSOCV, 200 ms | Accuracy | 84.9% |

### Ninapro DB2: intra-subject, repetitions 1, 3, 4, 6 train / 2, 5 test, 49 gestures (+rest), accuracy
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Atzori et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC4421935) | 2014 | Random forest | 200 ms | Accuracy | 75.27% |
| [Atzori et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC5013051) | 2016 | Simple CNN | **150 ms** | Accuracy | 60.27 ± 7.7% |
| [Hu et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC6207326) | 2018 | Attention CNN-RNN | 200 ms | Accuracy | 82.2% |
| Wei et al. (MV-CNN), via [TraHGR Table III](https://arxiv.org/abs/2203.16336) | 2019 | Multi-view CNN | 200 ms | Accuracy | 83.70% |
| [Wei, Hong, Wu (HVPN)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8413066/) | 2021 | HVPN | 200 ms | Accuracy | 85.8% |
| [Zabihi et al. (TraHGR)](https://arxiv.org/abs/2203.16336) | 2022 | Transformer + CNN hybrid | 200 ms | Accuracy | 86.18 ± 4.99% |

Cross-subject DB2 (LOSOCV + MS-AdaBN, 200 ms), via [HVPN Table 5](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8413066/): MV-CNN 80.1%, HVPN 82.0%.

### Ninapro DB3 (amputees): intra-subject, reps 2, 5 test
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Atzori et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC4421935) | 2014 | SVM | 200 ms | Accuracy | 46.27% |
| [Atzori et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC5013051) | 2016 | Simple CNN | 150 ms | Accuracy | 38.09 ± 14.29% |
| Wei et al. (MV-CNN), via [HVPN Table 4](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8413066/) | 2019 | Multi-view CNN | 200 ms | Accuracy | 64.3% |
| [Wei, Hong, Wu (HVPN)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8413066/) | 2021 | HVPN | 200 ms | Accuracy | 68.2% |

### Ninapro DB5: intra-subject, 41 classes (exercises B + C + rest), reps 2, 5 test, 200 ms windows with 100 ms step
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Pizzolato et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC5638457/) | 2017 | SVM + mDWT, both Myos | as above | Accuracy | 69.04% (one Myo: 55.31% / 54.76%) |
| Wei et al. (MV-CNN), via [HVPN Table 4](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8413066/) | 2019 | Multi-view CNN | as above | Accuracy | 90.0% |
| [Wei, Hong, Wu (HVPN)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8413066/) | 2021 | HVPN | as above | Accuracy | 90.3% |

Cross-subject DB5 (LOSOCV + MS-AdaBN, 41 classes), via [HVPN Table 5](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8413066/): MV-CNN 87.2%, HVPN 88.9%.

### Ninapro DB5: TinyMyo protocol (reps 1, 3, 4, 6 train / 2 validation / 5 test). Not directly comparable with the table above
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| OTiS, via [TinyMyo](https://arxiv.org/html/2512.15729v2) | — | 45M-parameter foundation model | as above | Accuracy | 81.79 ± 1.56% |
| PhysioWave-Small, via [TinyMyo](https://arxiv.org/html/2512.15729v2) | 2025 | Wavelet transformer | as above | Accuracy | 84.78% |
| MOMENT, via [TinyMyo](https://arxiv.org/html/2512.15729v2) | — | 385M time-series foundation model | as above | Accuracy | 86.41 ± 1.13% |
| WaveFormer, via [TinyMyo](https://arxiv.org/html/2512.15729v2) | — | 3.1M transformer | as above | Accuracy | 87.53 ± 0.92% |
| [Fasulo et al. (TinyMyo)](https://arxiv.org/html/2512.15729v2) | 2025 | 3.6M pretrained transformer, fine-tuned, 200 ms | as above | Accuracy | 89.41 ± 0.16% |

### Ninapro DB5: exercise A only (18 gestures). Different subset
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Côté-Allard et al.](https://arxiv.org/abs/1801.07756v5) | 2019 | Raw-EMG ConvNet + transfer learning | 18 gestures, 10 participants | Accuracy | 68.98% |

### Ninapro DB7: 6-fold cross-validation over repetitions, 40 classes, LDA
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Krasoulis et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC5505040/) | 2017 | LDA, EMG only | 20 able-bodied | Median accuracy | 60.1% |
| [Krasoulis et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC5505040/) | 2017 | LDA, EMG + IMU | 20 able-bodied | Median accuracy | 82.7% |
| [Krasoulis et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC5505040/) | 2017 | LDA, EMG only / EMG + IMU | 2 amputees | Median accuracy | 40.7% / 77.8% |

### CapgMyo DB-a: intra-subject, 8 gestures
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Geng et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC5109222/) | 2016 | CNN on instantaneous HD-EMG images | Single frame / 40-frame vote / 150-frame vote | Accuracy | 89.3% / 99.0% / 99.5% |
| [Hu et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC6207326) | 2018 | Attention CNN-RNN | Half of trials train; 150 ms | Accuracy | 99.7% |

### CapgMyo DB-b / DB-c: Du et al. 2017 protocols (majority vote over 150 ms; per-frame in brackets)
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Du et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC5375744) | 2017 | CNN | Intra-session, DB-b / DB-c | Accuracy | 98.6% (85.6) / 99.2% (84.6) |
| [Du et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC5375744) | 2017 | CNN without → with multi-stream AdaBN | Inter-session, DB-b | Accuracy | 47.9% → 63.3% |
| [Du et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC5375744) | 2017 | CNN without → with multi-stream AdaBN | Inter-subject, DB-b | Accuracy | 39.0% → 55.3% |
| [Du et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC5375744) | 2017 | CNN without → with multi-stream AdaBN | Inter-subject, DB-c | Accuracy | 26.3% → 35.1% |

These come from Du et al. Table 7; its column headers say which protocol each number belongs to.

### CSL-HDEMG: intra-session, 27 gestures (rows differ in window; see column)
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| Amma et al., via [Du et al. Table 5](https://pmc.ncbi.nlm.nih.gov/articles/PMC5375744) | 2015 | Original paper method | Trial-level, per-session leave-one-out | Accuracy | 90.4% |
| [Geng et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC5109222/) | 2016 | CNN, whole-trial vote | same | Accuracy | 96.8% (55.8% per frame) |
| [Hu et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC6207326) | 2018 | Attention CNN-RNN | **150 ms window**, leave-one-trial-out | Accuracy | 94.5% |

The Amma et al. number is as reproduced by Du et al.; I did not read the CHI paper itself.

### Hyser (PR set, 34 gestures): within-session leave-one-out, averaged over 2 sessions
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Jiang et al.](https://physionet.org/files/hd-semg/1.0.0/manuscript_author_version.pdf) | 2021 | PCA + LDA | Dynamic / maintenance tasks | Accuracy | 96.86 ± 2.49% / 93.80 ± 3.80% |
| [Jiang et al.](https://physionet.org/files/hd-semg/1.0.0/manuscript_author_version.pdf) | 2021 | Toolbox CNN | Dynamic / maintenance tasks | Accuracy | 88.96 ± 1.76% / 89.84 ± 1.91% |

### GRABMyo: user-specific, across 3 days
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Pradhan et al.](https://europepmc.org/article/PMC/PMC9712490) | 2022 | Hudgins TD features | Gesture recognition, forearm / wrist | AUC | 0.948 / 0.941 |
| [Pradhan et al.](https://europepmc.org/article/PMC/PMC9712490) | 2022 | Mahalanobis matching | Biometric verification, forearm / wrist | EER | 0.028 / 0.038 |

### EMG-EPN-612. The two tables use different splits and are not directly comparable
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Benalcázar et al.](https://redi.cedia.edu.ec/document/4570) | 2023 | Best supervised model | User-general (tested on users not seen in training) | Classification / recognition accuracy | 90.49 ± 9.7% / 86.83 ± 11.30% |

| Paper | Year | Method | Protocol (TinyMyo subject-wise split) | Metric | Result |
|---|---|---|---|---|---|
| PhysioWave-Small, via [TinyMyo](https://arxiv.org/html/2512.15729v2) | 2025 | Wavelet transformer | as above | Accuracy | 93.12% |
| MOMENT, via [TinyMyo](https://arxiv.org/html/2512.15729v2) | — | 385M foundation model | as above | Accuracy | 93.83 ± 0.76% |
| WaveFormer, via [TinyMyo](https://arxiv.org/html/2512.15729v2) | — | 3.1M transformer | as above | Accuracy | 95.21 ± 0.68% |
| [Fasulo et al. (TinyMyo)](https://arxiv.org/html/2512.15729v2) | 2025 | 3.6M pretrained transformer, 1000 ms | as above | Accuracy | 96.74 ± 0.09% |

### putEMG: per subject and day, 3-fold cross-validation over trials
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Kaczmarek et al.](https://ar5iv.labs.arxiv.org/html/1907.07428) | 2019 | SVM + RMS; LDA + Hudgins; LDA + Du features | as above | Accuracy | about 90% (best three, as stated by the authors) |

### emg2qwerty: 8 held-out test users, character error rate (lower is better)
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Sivakumar et al.](https://arxiv.org/html/2410.20081v1) | 2024 | TDS-ConvNet + CTC | Generic (unseen users), test, no LM / 6-gram LM | CER | 55.38 ± 4.10% / 51.78 ± 4.61% |
| [Sivakumar et al.](https://arxiv.org/html/2410.20081v1) | 2024 | Same, personalized from random init | test, no LM / LM | CER | 15.38 ± 5.88% / 9.55 ± 5.16% |
| [Sivakumar et al.](https://arxiv.org/html/2410.20081v1) | 2024 | Same, personalized by fine-tuning the generic model | test, no LM / LM | CER | 11.28 ± 4.45% / 6.95 ± 3.61% |

**Mehlman et al. 2025** ([TMLR](https://arxiv.org/html/2507.22094)) report their own baseline TDS-ConvNet at 55.57% generic and 11.39% personalized CER. Those numbers equal the emg2qwerty *validation, no-LM* figures, so read this table as validation CER without a language model.

| Paper | Year | Method | Generic CER | Personalized CER |
|---|---|---|---|---|
| [Mehlman et al.](https://arxiv.org/html/2507.22094) | 2025 | TDS-ConvNet baseline (5.3M) | 55.57% | 11.39% |
| [Mehlman et al.](https://arxiv.org/html/2507.22094) | 2025 | Tiny transformer (2.2M) | 35.9 ± 0.9% | 9.7 ± 0.13% |
| [Mehlman et al.](https://arxiv.org/html/2507.22094) | 2025 | Large transformer (109M) | 30.5 ± 0.6% | 6.8 ± 0.07% |
| [Mehlman et al.](https://arxiv.org/html/2507.22094) | 2025 | Tiny transformer distilled from Large | 31.9 ± 0.4% | not reported |

Not comparable: [MyoText](https://arxiv.org/abs/2601.03098) (2026) reports 5.4% CER and 6.5% WER on 30 emg2qwerty users with finger classification + transformer decoding. Its protocol (generic or personalized, which split) is not stated in the abstract.

### emg2pose: regression task (EMG only), held-out splits
| Paper | Year | Method | Held-out users | Held-out stages | Held-out users + stages |
|---|---|---|---|---|---|
| SensingDynamics baseline, in [Salter et al.](https://arxiv.org/html/2412.02725v1) | 2024 | 2D CNN | 15.5° / 21.8 mm | 18.8° / 26.6 mm | 18.7° / 27.2 mm |
| NeuroPose baseline, in [Salter et al.](https://arxiv.org/html/2412.02725v1) | 2024 | U-Net | 13.2° / 17.5 mm | 17.2° / 24.0 mm | 17.5° / 24.9 mm |
| [Salter et al. (vemg2pose)](https://arxiv.org/html/2412.02725v1) | 2024 | Velocity-integrating model | 12.2° / 15.8 mm | 15.2° / 20.4 mm | 15.8° / 21.6 mm |

Metrics are mean joint-angle error / mean fingertip landmark distance. In the *tracking* task (initial pose given), vemg2pose reaches 7.7° / 10.3 mm on held-out users. [REACT](https://arxiv.org/abs/2605.30127) (2026) reports up to 3.9% lower angular error by adding under 45 s of per-user calibration. That is a personalized protocol, and the abstract gives no absolute numbers.

### Generic Neuromotor Interface: discrete gestures, subject-wise 80/10/10 split
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| Kaifosh et al. LSTM, via [TinyMyo](https://arxiv.org/html/2512.15729v2) | 2025 | LSTM (6.4M) | Windowed inference (8 s window, 2 s stride) | Classification error rate | 0.1596 |
| [Fasulo et al. (TinyMyo)](https://arxiv.org/html/2512.15729v2) | 2025 | TinyMyo from scratch / fine-tuned | same | Classification error rate | 0.144 ± 0.004 / 0.153 ± 0.006 |

Closed-loop results with new users, which are not offline metrics, from the [Nature paper](https://ideas.repec.org/a/nat/nature/v645y2025i8081d10.1038_s41586-025-09255-w.html): 0.88 gesture detections/s, 0.66 target acquisitions/s, handwriting at 20.9 WPM, and +16% handwriting performance with personalization.

---

## How to read these numbers

- **Check the split before comparing.** "Intra-subject" (a model per person, tested on held-out repetitions of the same session) gives far higher numbers than cross-session or cross-subject tests. On CapgMyo DB-b the same CNN gets 98.6% within a session but 47.9% across sessions and 39.0% across subjects ([Du et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC5375744)). On emg2qwerty, generic CER is about 52% versus about 7% personalized.
- **Window leakage.** Sliding windows overlap heavily (often a 10 ms step). If windows from the *same repetition* land in both train and test, accuracy is inflated. Split by repetition (as the Ninapro protocols do), session or subject, never by random window.
- **Voting and window length change the score.** Per-frame, 150 ms, 200 ms and whole-trial majority vote are different tasks. Geng et al. go from 65.1% to 96.7% on Ninapro DB1 just by voting over the whole trial ([PMC5109222](https://pmc.ncbi.nlm.nih.gov/articles/PMC5109222/)). Whole-trial voting is not possible in a real-time controller.
- **Class subsets differ.** Ninapro DB5 is reported with 18, 40, 41 or 52 classes; DB2 with 49 or 50 (rest included or not). Only compare like with like.
- **Preprocessed segments are easier.** CapgMyo's "middle 1 s" files and Ninapro's relabeled "restimulus" remove transitions. Online control has to handle them.
- **"via" numbers are second-hand.** They were checked in the citing paper's table, not in the original, and may use that paper's re-implementation.
- **Per-subject vs generic models.** Most Ninapro, CapgMyo and CSL results train one model per person. emg2qwerty, emg2pose, EPN-612 (official split) and the Generic Neuromotor Interface test on unseen people, which is the setting that matters for consumer products.
