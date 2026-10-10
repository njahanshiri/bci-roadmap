# EOG datasets and benchmark results

This file covers public datasets that contain EOG, either as the main signal or as a channel alongside EEG, and the published results on them. I copied every number from the linked source. Where a source does not give a value, the entry says "not reported". I did not estimate anything.

## Overview

| Dataset | Subjects | EOG channels | EOG Hz (as distributed) | Task / labels | Size | Access |
|---|---|---|---|---|---|---|
| Sleep-EDF Expanded | 78 (SC) + 22 (ST); 197 recordings | 1 horizontal | 100 | Sleep stages (R&K) | 8.1 GB | Open (ODC-By) |
| SHHS | 5,804 (NSRR) | 2 (left, right) | 50 (SHHS1) | Sleep stages, events | not reported | NSRR data-use agreement |
| MASS (cohort 1) | 200 nights | ROC-LOC (per XSleepNet) | not reported | Sleep stages | not reported | Ethics approval required |
| ISRUC-Sleep | 100 + 8 + 10 | yes (count not reported on site) | not reported | Sleep stages, 2 scorers | 14.12 + 2.2 + 1.35 GB | Public download |
| SEED-VIG | 23 | 4 forehead | 1000 (raw) | PERCLOS vigilance | not reported | Request via BCMI |
| EEGdenoiseNet | n/a (built from other datasets) | 3,400 EOG segments | 256 | Clean/artifact pairs | not reported | GitHub, MIT |
| Klados & Bamidis 2016 | 27 | HEOG, VEOG | 200 | Pure vs. contaminated EEG | not reported | Mendeley, open |
| Bulling EOG activity | 8 | hEOG, vEOG | 128 | 5 office activities + NULL | 22 MB | DaRUS, CC BY-NC-SA 4.0 |
| EEGEyeNet | 356 | none (video eye tracker as label) | 500 (EEG and ET) | Gaze direction and position | 47+ h | CC BY 4.0 |
| DEAP | 32 | hEOG, vEOG | 512 raw / 128 preprocessed | Valence, arousal, etc. | not reported | EULA (*unverified*) |
| ALS locked-in EEG+EOG | 4 patients | 4 electrodes (2 H, 2 V) | 500 | Yes/no answers, spelling | not reported | Open, CC BY 4.0 |
| JINS MEME driving | 51 | 4 (L, R, H, V) | 200 | Simulator vs. real road | not reported | IEEE DataPort subscription |

---

## Part 1: Dataset specifications

### Sleep-EDF Expanded ([PhysioNet](https://physionet.org/content/sleep-edfx/1.0.0/))

| Field | Value |
|---|---|
| Year & paper | v2 (197 PSGs) released March 2018. Cite Kemp et al. 2000 (IEEE-BME 47(9)) and Mourtazaev et al. 1995 (Sleep 18(7)) |
| Subjects | Sleep Cassette (SC): 78 healthy Caucasians aged 25–101 with no sleep medication (153 recordings). Sleep Telemetry (ST): 22 subjects with mild difficulty falling asleep (44 recordings) |
| Device & electrodes | not reported |
| EOG & other channels | 1 horizontal EOG; EEG Fpz-Cz and Pz-Oz; submental chin EMG. SC also has oro-nasal respiration, rectal temperature and an event marker |
| Sampling rate | EEG, EOG and EMG at 100 Hz; other signals at 1 Hz |
| Resolution / filters | not reported (SC EMG is high-passed, rectified and low-passed to 1 Hz RMS) |
| Labels | Manual hypnograms scored by trained technicians with the 1968 R&K manual: W, R, 1, 2, 3, 4, M, ? |
| Sessions | SC: two ~20 h day-night home recordings per subject. ST: two ~9 h hospital nights per subject (temazepam and placebo) |
| Size / format | 8.1 GB, EDF and EDF+ |
| Access | Open Data Commons Attribution v1.0 |
| Standard subsets | **SleepEDF-20**: 20 SC subjects, 39 recordings ([L-SeqSleepNet](https://arxiv.org/html/2301.03441), [EOGNet](https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2021.573194/full)). **SleepEDF-78**: the larger SC set ([Maiti 2023](https://arxiv.org/abs/2310.03757)). N3 and N4 are usually merged; M and ? are dropped; recordings are trimmed to 30 min before and after the in-bed period ([SleepTransformer](https://arxiv.org/html/2105.11043)). Usual protocols: 20-fold CV for SleepEDF-20 and 10-fold CV for SleepEDF-78, split by subject ([XSleepNet](https://ar5iv.labs.arxiv.org/html/2007.05492)) |
| Known issues | First nights of SC subjects 36 and 52 and the second night of subject 13 are lost. Only one EOG channel. R&K labels, not AASM |

### SHHS, Sleep Heart Health Study ([NSRR](https://sleepdata.org/datasets/shhs))

| Field | Value |
|---|---|
| Year & paper | Visit 1 1995–1998, Visit 2 2001–2003. Quan et al. 1997 (Sleep 20(12)); Zhang et al. 2018 (JAMIA) |
| Subjects | 6,441 enrolled, aged 40 and over; 5,804 adults on NSRR. PSG available for 5,793 subjects at Visit 1 and 2,651 at Visit 2 ([PSG intro](https://sleepdata.org/datasets/shhs/pages/05-polysomnography-introduction.md)) |
| Device & electrodes | Unattended home PSG by certified technicians. EOG uses gold-cup electrodes ([montage SHHS1](https://sleepdata.org/datasets/shhs/pages/10-montage-and-sampling-rate-information-shhs1.md)) |
| EOG & other channels | EOG(L) and EOG(R); EEG C3-A2 and C4-A1; plus ECG, EMG, respiratory and SpO2 |
| Sampling rate | EOG 50 Hz, EEG 125 Hz (SHHS1) |
| Filters | EOG and EEG hardware high-pass at 0.15 Hz |
| Resolution | not reported |
| Labels | Sleep stages and events scored in Compumedics Profusion (rule set not reported on the pages read) |
| Format | EDF signals plus two XML annotation versions (Profusion and NSRR) |
| Access | Request through NSRR with a data-use agreement |
| Standard protocol | 70/30 train/test split by subject ([XSleepNet](https://ar5iv.labs.arxiv.org/html/2007.05492)) |
| Known issues | Some desaturation events were changed during software conversion. Settings may differ for a small share of studies |

### MASS, Montreal Archive of Sleep Studies ([CEAMS](http://ceams-carsm.ca/mass/))

| Field | Value |
|---|---|
| Year & paper | O'Reilly et al. 2014, J Sleep Res 23(6) |
| Subjects | 200 nights from 97 men and 103 women aged 18–76 (mean 38.3), split into subsets SS1–SS5 |
| EOG & other channels | XSleepNet uses EEG C4-A1/C3-A2, EOG ROC-LOC and EMG CHIN1-CHIN2, with AASM/R&K scoring ([XSleepNet Table I](https://ar5iv.labs.arxiv.org/html/2007.05492)). EOGNet uses the right EOG of SS3 (62 nights) ([EOGNet](https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2021.573194/full)) |
| Sampling / resolution / filters | not reported |
| Format | EDF++ |
| Access | Biosignals require a project description and proof of ethics approval; some annotations are on [Borealis](https://borealisdata.ca/dataverse/MASS) |
| Known issues | Users are asked to state which subset they used (e.g. MASS-C1/SS3), so results across papers often cover different subsets |

### ISRUC-Sleep ([site](https://sleeptight.isr.uc.pt/))

| Field | Value |
|---|---|
| Year & paper | Khalighi et al. 2016, Comput Methods Programs Biomed 124 |
| Subjects | Group I: 100 subjects, one session each. Group II: 8 subjects, two sessions each. Group III: 10 healthy subjects |
| EOG & other channels | EEG, EOG, EMG, ECG, respiratory signals and SpO2 ([extracted channels page](https://sleeptight.isr.uc.pt/?page_id=76)). Exact EOG derivations are not reported on the site |
| Sampling / resolution / filters | not reported on the pages read |
| Labels | Each recording scored by two human experts |
| Size / format | 14.12 GB (I), 2.2 GB (II), 1.35 GB (III); .rec/EDF plus MATLAB extracts ([download page](https://sleeptight.isr.uc.pt/?page_id=48)) |
| Access | Public download; citation required |
| Known issues | The MATLAB extracts drop the last 30 epochs, so they are 30 epochs shorter than the hypnograms. The site's cohort descriptions are not consistent (Cohort II is called "healthy" on the download page) |

### SEED-VIG ([BCMI](https://bcmi.sjtu.edu.cn/home/seed/seed-vig.html); [paper](https://ar5iv.labs.arxiv.org/html/1611.08492))

| Field | Value |
|---|---|
| Year & paper | Zheng & Lu 2017, J Neural Eng 14(2) 026017 |
| Subjects | 23 (mean age 23.3, SD 1.4, 12 female), normal or corrected vision |
| Device & electrodes | Neuroscan system plus eye-tracking glasses, in a simulated driving setup with a real car body |
| EOG & other channels | 4 forehead EOG channels; posterior and temporal EEG (17 channels in the released features) |
| Sampling rate | 1000 Hz raw; EEG downsampled to 200 Hz in the paper |
| Filters | EEG band-pass 1–75 Hz |
| Labels | Continuous PERCLOS (0–1) from the eye-tracking glasses. 36 EOG features (blink, saccade, fixation) |
| Sessions | About 2 h of afternoon driving per experiment; 885 samples per experiment |
| Access | Request through the BCMI lab |
| Standard protocol | 5-fold CV over time sessions within each experiment (within-subject). Leave-one-subject-out is used for cross-subject work ([Zhang & Etemad](https://ar5iv.labs.arxiv.org/html/1912.07812)) |
| Known issues | Within-subject folds are cut from one continuous 2-hour session, so neighbouring samples are strongly correlated. PERCLOS comes from glasses, not expert scoring |

### EEGdenoiseNet ([paper](https://arxiv.org/abs/2009.11662); [GitHub](https://github.com/ncclabsustech/EEGdenoiseNet))

| Field | Value |
|---|---|
| Year & paper | Zhang et al. 2021, J Neural Eng 18(5) |
| Content | 4,514 clean EEG, 3,400 EOG and 5,598 EMG single-channel 2-second segments |
| Sources | Clean EEG: 52 participants, 64-channel motor-task data at 512 Hz, cleaned with ICLabel. EOG: horizontal and vertical channels from several open EEG datasets |
| Sampling rate | EEG and EOG resampled to 256 Hz (EMG 512 Hz) |
| Filters | EEG 1–80 Hz plus notch; EOG 0.3–10 Hz; all segments z-scored and inspected by an expert |
| Labels | Semi-synthetic: contaminated = EEG + λ·EOG, with known clean ground truth |
| Format | MATLAB and NumPy arrays |
| Access | GitHub, MIT license |
| Standard protocol | EOG task: 3,400 EEG + 3,400 EOG segments split 80/10/10, mixed at 10 SNR levels from −7 to 2 dB. Metrics: RRMSE temporal, RRMSE spectral, CC |
| Known issues | Artifacts are added linearly and are single-channel, which is not real contamination. Later papers change the SNR range (D4PM uses −5 to 5 dB) |

### Semi-simulated EEG/EOG, Klados & Bamidis 2016 ([paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC4969208/); [Mendeley](https://data.mendeley.com/datasets/wb6yvr725d/1))

| Field | Value |
|---|---|
| Subjects | 27 healthy: 14 male (28.2 ± 7.5 y) and 13 female (27.1 ± 5.2 y) |
| Channels | 19 EEG channels (10–20 system, mastoid references). EOG from electrodes above and below the left eye and at both outer canthi, giving bipolar VEOG and HEOG |
| Sampling / filters | 200 Hz; EEG 0.5–40 Hz plus 50 Hz notch; EOG 0.5–5 Hz |
| Labels | Eyes-closed EEG contaminated as Pure_EEG + a·VEOG + b·HEOG, so the clean EEG is known |
| Duration | 54 datasets of 30 s each |
| Format / access | MATLAB arrays; unrestricted download; article CC BY 4.0 |
| Known issues | Linear contamination model; short recordings |

### Bulling EOG activity dataset ([DaRUS](https://doi.org/10.18419/darus-3135); [TPAMI 2011](https://perceptualui.org/publications/bulling11_pami/))

| Field | Value |
|---|---|
| Subjects | 8 (2 female, 6 male), aged 23–31 |
| Channels / rate | Separate horizontal and vertical EOG at 128 Hz from a wearable EOG system ([b2find record](https://b2find.eudat.eu/dataset/af9a16df-dbee-5e54-a98f-fb941fde90e3)) |
| Device | not reported in sources read |
| Labels | Copying text, reading paper, handwritten notes, watching video, web browsing, plus rest (NULL) |
| Sessions | 2 runs per participant, about 8 h in total |
| Size / format | 18 files, 22 MB, .mat |
| Access | CC BY-NC-SA 4.0 |
| Protocol | Leave-one-person-out |

### EEGEyeNet ([paper](https://ar5iv.labs.arxiv.org/html/2111.05100); [GitHub](https://github.com/ardkastrati/EEGEyeNet))

| Field | Value |
|---|---|
| Year | NeurIPS 2021 Datasets & Benchmarks |
| Subjects | 356 healthy adults (190 female, 166 male), aged 18–80 |
| Device | 128-channel EGI Geodesic Hydrocel EEG at 500 Hz; EyeLink 1000 Plus eye tracker at 500 Hz |
| EOG | No separate EOG. Frontal EEG channels carry the eye signal, and the eye tracker supplies the labels |
| Tasks | Pro/antisaccade, Large Grid (25 positions), Visual Symbol Search. Benchmarks: left-right, angle/amplitude, absolute position |
| Size | More than 47 h |
| Access | CC BY 4.0. Raw, minimally preprocessed and maximally preprocessed versions |
| Protocol | Split by subject: 70/15/15 |

### DEAP ([paper](https://research.utwente.nl/en/publications/deap-a-database-for-emotion-analysis-using-physiological-signals/); [readme](https://www.eecs.qmul.ac.uk/mmv/datasets/deap/readme.html))

| Field | Value |
|---|---|
| Year & paper | Koelstra et al. 2012, IEEE Trans Affective Computing 3(1) |
| Subjects | 32, each watching 40 one-minute music videos; face video for 22 of them |
| Channels | 32 EEG plus 8 peripheral channels: hEOG, vEOG, zEMG, tEMG, GSR, respiration, blood volume, temperature ([summary](https://arxiv.org/pdf/2001.00191)) |
| Sampling / filters | Preprocessed version downsampled from 512 to 128 Hz, band-pass 4–45 Hz (as summarised by secondary sources; the readme was offline when checked) |
| Labels | Self-rated arousal, valence, like/dislike, dominance and familiarity |
| Trials | 63 s each, including a 3 s baseline |
| Access | EULA (*unverified*; the site was down) |

### ALS locked-in EEG+EOG ([Sci Data 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC7801642/))

| Field | Value |
|---|---|
| Subjects | 4 ALS patients in advanced locked-in state |
| Device | Brain Products V-Amp DC, 16 channels, Ag/AgCl active electrodes |
| EOG & other channels | At least 4 EOG electrodes: LO1 and LO2 (horizontal), SO1 and IO1 (vertical). At least 7 EEG channels; chin EMG in some sessions |
| Sampling / filters | 500 Hz; no hardware or software filter beyond the amplifier band (DC–320 Hz) |
| Tasks | Auditory EOG speller: training, feedback, copy spelling, free spelling |
| Sessions | 2–10 visits; 3.22 ± 1.21 days per visit; 5.57 ± 2.61 sessions per day |
| Format / access | BrainVision (.vhdr, .vmrk, .eeg) plus a MATLAB export script; open repository; CC BY 4.0 |

### JINS MEME real & simulated driving ([IEEE DataPort](https://ieee-dataport.org/documents/real-simulated-driving))

| Field | Value |
|---|---|
| Year & authors | 2024, Piaseczna, Doniec, Grzegorzek (DOI 10.21227/d5yr-v464) |
| Subjects | 51: 21 in the simulator, 30 on real roads |
| Device | JINS MEME ES_R with 3-point EOG |
| EOG channels | EOG_L, EOG_R, EOG_H, EOG_V at 200 Hz |
| Samples | 1,976 (simulator) and 390 (real road) |
| Format | CSV (zip), .mat, .h5 |
| Access | IEEE DataPort subscription; the page said files were not yet uploaded |

---

## Part 2: Results

### Sleep-EDF-20, sleep staging (5 classes)

**Table A. EEG only (Fpz-Cz), recordings trimmed ±30 min, subject-wise CV**

| Paper | Year | Method | Input | Protocol | Acc | κ | MF1 |
|---|---|---|---|---|---|---|---|
| [DeepSleepNet, via L-SeqSleepNet Table III](https://arxiv.org/html/2301.03441) | 2017 | CNN + BiLSTM | EEG | 20-fold CV | 82.0 | 0.760 | 76.9 |
| [U-Time, via XSleepNet Table II](https://ar5iv.labs.arxiv.org/html/2007.05492) | 2019 | Fully convolutional | EEG | as reported | – | – | 79.0 |
| [XSleepNet](https://ar5iv.labs.arxiv.org/html/2007.05492) | 2020 | SeqSleepNet baseline | EEG | 20-fold CV | 85.2 | 0.798 | 78.4 |
| [XSleepNet](https://ar5iv.labs.arxiv.org/html/2007.05492) | 2020 | XSleepNet2 | EEG | 20-fold CV | 86.3 | 0.813 | 80.6 |
| [L-SeqSleepNet](https://arxiv.org/html/2301.03441) | 2023 | L-SeqSleepNet | EEG | LOSO, 5 repeats | 86.3 ± 0.2 | 0.813 | 79.3 |
| [L-SeqSleepNet](https://arxiv.org/html/2301.03441) | 2023 | L-SeqSleepNet with SHHS pretraining | EEG | LOSO, 5 repeats | 88.6 ± 0.1 | 0.845 | 82.9 |

XSleepNet's table lists DeepSleepNet's 82.0 / 0.760 / 76.9 under the EEG·EOG column. L-SeqSleepNet and Maiti 2023 both list it as EEG only.

**Table B. EEG + EOG, same protocol as Table A**

| Paper | Year | Method | Input | Protocol | Acc | κ | MF1 |
|---|---|---|---|---|---|---|---|
| [XSleepNet](https://ar5iv.labs.arxiv.org/html/2007.05492) | 2020 | SeqSleepNet baseline | EEG + EOG | 20-fold CV | 86.0 | 0.809 | 79.7 |
| [XSleepNet](https://ar5iv.labs.arxiv.org/html/2007.05492) | 2020 | XSleepNet2 | EEG + EOG | 20-fold CV | 86.4 | 0.813 | 80.9 |

**Table C. EOG only (horizontal EOG)**

These rows are not directly comparable with each other because the protocols differ.

| Paper | Year | Method | Input | Protocol | Acc | κ | MF1 |
|---|---|---|---|---|---|---|---|
| [EOGNet](https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2021.573194/full) | 2021 | EOGNet | EOG | LOSO | 76.3 | 0.672 | 69.3 |
| [Maiti et al.](https://arxiv.org/html/2310.03757) | 2023 | DeepSleepNet trained on EOG | EOG | as reported by Maiti | 73.5 | 0.66 | 68.2 |
| [Maiti et al.](https://arxiv.org/html/2310.03757) | 2023 | SE-ResNet-Transformer | EOG | 20-fold CV (split type not stated) | 79.26 | 0.72 | 74.72 |
| [Maiti et al.](https://arxiv.org/html/2310.03757) | 2023 | SE-ResNet-Transformer | EEG | 20-fold CV | 82.4 | 0.75 | 76.5 |

### Sleep-EDF-78, sleep staging, ±30 min, 10-fold subject-wise CV

| Paper | Year | Method | Input | Acc | κ | MF1 |
|---|---|---|---|---|---|---|
| [U-Time, via XSleepNet](https://ar5iv.labs.arxiv.org/html/2007.05492) | 2019 | U-Time | EEG | – | – | 76.0 |
| [XSleepNet](https://ar5iv.labs.arxiv.org/html/2007.05492) | 2020 | SeqSleepNet baseline | EEG | 82.6 | 0.760 | 76.4 |
| [XSleepNet](https://ar5iv.labs.arxiv.org/html/2007.05492) | 2020 | XSleepNet2 | EEG | 84.0 | 0.778 | 77.9 |
| [SleepTransformer](https://arxiv.org/html/2105.11043) | 2021 | SleepTransformer | EEG | 81.4 | 0.743 | 74.3 |
| [SleepTransformer](https://arxiv.org/html/2105.11043) | 2021 | SleepTransformer with SHHS pretraining | EEG | 84.9 | 0.789 | 78.8 |
| [XSleepNet](https://ar5iv.labs.arxiv.org/html/2007.05492) | 2020 | SeqSleepNet baseline | EEG + EOG | 83.8 | 0.776 | 78.2 |
| [XSleepNet](https://ar5iv.labs.arxiv.org/html/2007.05492) | 2020 | XSleepNet2 | EEG + EOG | 84.0 | 0.778 | 78.7 |
| [Maiti et al.](https://arxiv.org/html/2310.03757) | 2023 | SE-ResNet-Transformer | EOG only | 73.56 | 0.68 | 70.63 |

The EOG-only row is not directly comparable: Maiti does not state a ±30 min trim or a subject-wise split.

### SHHS and MASS, effect of adding EOG (XSleepNet2, same model and split)

| Dataset | Paper | Protocol | EEG: Acc / κ / MF1 | EEG+EOG | EEG+EOG+EMG |
|---|---|---|---|---|---|
| SHHS | [XSleepNet](https://ar5iv.labs.arxiv.org/html/2007.05492) (2020) | 70/30 by subject | 87.6 / 0.826 / 80.7 | 88.8 / 0.843 / 81.8 | 89.1 / 0.847 / 82.3 |
| MASS (200 subj.) | [XSleepNet](https://ar5iv.labs.arxiv.org/html/2007.05492) (2020) | 20-fold CV | 85.2 / 0.788 / 80.6 | 86.9 / 0.813 / 82.7 | 87.6 / 0.823 / 83.8 |

The EOG-only rows below are not directly comparable with the table above, because they use different subsets and protocols:

| Dataset | Paper | Year | Input | Protocol | Acc | κ | MF1 |
|---|---|---|---|---|---|---|---|
| SHHS (329-subject subset) | [Maiti et al.](https://arxiv.org/html/2310.03757) | 2023 | EOG | 5-fold CV | 79.04 | 0.71 | 69.26 |
| MASS SS3 | [EOGNet](https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2021.573194/full) | 2021 | EOG | LOSO | 81.2 | 0.718 | 73.7 |

### SEED-VIG, vigilance regression (PERCLOS)

**Within-subject: 5-fold CV inside each experiment.** Possible leakage: folds are cut from one continuous session.

| Paper | Year | Method | Input | RMSE | COR/PCC |
|---|---|---|---|---|---|
| [Zheng & Lu](https://ar5iv.labs.arxiv.org/html/1611.08492) | 2017 | ICA-MINUS forehead-EOG features | EOG | 0.1188 | 0.7773 |
| [Zheng & Lu](https://bcmi.sjtu.edu.cn/home/blu/papers/2017/3.pdf) | 2017 | Posterior EEG, 2 Hz DE features | EEG | 0.1327 | 0.7001 |
| [Zheng & Lu, as reported by Zhang & Etemad](https://ar5iv.labs.arxiv.org/html/1912.07812) | 2017 | CCNF fusion | EEG + EOG | 0.09 | 0.85 |
| [Zhang & Etemad](https://ar5iv.labs.arxiv.org/html/1912.07812) | 2019 | CNN-LSTM baseline | EEG + EOG | 0.0425 | 0.9387 |
| [Zhang & Etemad](https://ar5iv.labs.arxiv.org/html/1912.07812) | 2019 | LSTM-CapsAtt | EEG + EOG | 0.0295 | 0.9887 |

**Cross-subject: leave-one-subject-out**

| Paper | Year | Method | Input | RMSE | PCC |
|---|---|---|---|---|---|
| [Li et al., as reported by Zhang & Etemad](https://ar5iv.labs.arxiv.org/html/1912.07812) | – | DANN | EEG + EOG | 0.1427 | 0.8402 |
| [Zhang & Etemad](https://ar5iv.labs.arxiv.org/html/1912.07812) | 2019 | LSTM-CapsAtt | EEG + EOG | 0.1089 | 0.8823 |

The jump from PCC ≈ 0.99 within subjects to ≈ 0.88 across subjects shows how much the within-session protocol flatters results.

### EEGdenoiseNet, EOG artifact removal (lower RRMSE is better, higher CC is better)

**Table 1. Original protocol: 80/10/10 split, SNR −7 to 2 dB, averaged across SNRs, numbers as reported by [Gabardi et al. 2023](https://ar5iv.labs.arxiv.org/html/2310.17335)**

| Paper | Year | Method | Input | RRMSE_t | RRMSE_s | CC |
|---|---|---|---|---|---|---|
| DeepSeparator (Yu et al.) | 2022 | as reported | single-ch EEG + EOG mix | 0.705 | 0.747 | 0.769 |
| EEGDnet (Pu et al.) | 2022 | 2D transformer | same | 0.497 | 0.491 | 0.868 |
| [Gabardi et al.](https://ar5iv.labs.arxiv.org/html/2310.17335) | 2023 | Frequency-domain model | same | 0.405 | 0.490 | 0.917 |

The original EEGdenoiseNet paper reports its FCNN, CNN and RNN baselines only as figures, so they are not listed.

**Table 2. Not directly comparable: [D4PM](https://arxiv.org/html/2509.14302) protocol, SNR −5 to 5 dB, 80/10/10. It is not stated whether the baselines were retrained.**

| Paper | Year | Method | RRMSE_t | RRMSE_s | CC |
|---|---|---|---|---|---|
| D4PM Table 1 | 2025 | FCNN | 0.451 | 0.328 | 0.873 |
| D4PM Table 1 | 2025 | SimpleCNN | 0.313 | 0.226 | 0.928 |
| D4PM Table 1 | 2025 | DuoCL | 0.407 | 0.265 | 0.880 |
| D4PM Table 1 | 2025 | GCTNet | 0.281 | 0.224 | 0.939 |
| D4PM Table 1 | 2025 | EEGDfus | 0.257 | 0.165 | 0.943 |
| D4PM Table 1 | 2025 | EEGIFNet | 0.241 | 0.179 | 0.962 |
| [D4PM](https://arxiv.org/abs/2509.14302) | 2025 | Dual-branch diffusion | 0.098 | 0.072 | 0.995 |

**Protocol not stated in the source read:** [EEGPARnet](https://lmerin.owlstown.net/projects/6870-eegparnet) (Med Biol Eng Comput 2025) reports RRMSE_t 0.230, RRMSE_s 0.228 and CC 0.967 on EEGdenoiseNet ocular artifacts.

### EEGEyeNet, gaze from EEG (subject-wise 70/15/15, [paper](https://ar5iv.labs.arxiv.org/html/2111.05100), 2021)

| Task | Metric | Naive baseline | Best reported |
|---|---|---|---|
| Left-right | Accuracy | 52.3% | 98.8% (Xception) |
| Angle | RMSE (rad) | 1.90 | 0.33 (CNN) |
| Amplitude | RMSE (mm) | 74.7 | 30.7 (PyramidalCNN) |
| Absolute position | RMSE (mm) | 123.3 | 70.2 (CNN) |

Input is EEG only. Which preprocessing variant (minimal or maximal) these numbers come from is *unverified*.

### Bulling EOG activity dataset

| Paper | Year | Method | Input | Protocol | Precision | Recall |
|---|---|---|---|---|---|---|
| [Bulling et al., TPAMI](https://perceptualui.org/publications/bulling11_pami/) | 2011 | 90 features, mRMR selection + SVM | EOG | Leave-one-person-out | 76.1% | 70.5% |

---

## How to read these numbers

- **SleepEDF-20 vs. SleepEDF-78.** These are different subject sets with different fold counts (20-fold vs. 10-fold). The 78-subject version includes older subjects and gives lower scores; XSleepNet2 drops from 86.3 to 84.0% accuracy on EEG. Also check the trim: XSleepNet reports SleepEDF-20 both with ±30 min trimming (86.3%) and without it (83.9%).
- **Epoch-wise vs. subject-wise splits.** A subject-wise split (LOSO, k-fold by subject) is the honest test. Splits inside one recording, like SEED-VIG's within-session 5-fold, let the model learn each person's signal and inflate scores: PCC 0.99 within subjects vs. 0.88 across subjects for the same model.
- **Pretraining.** Results marked "with SHHS pretraining" use extra data and should not be compared directly with models trained from scratch.
- **Semi-synthetic vs. real artifacts.** EEGdenoiseNet and Klados mix clean EEG with recorded EOG linearly, so the ground truth is known but the mixing is idealised. SNR ranges also differ between papers (−7 to 2 dB vs. −5 to 5 dB), and the baselines are often re-run by each new paper, so cross-paper EEGdenoiseNet numbers are only loosely comparable.
- **What EOG adds.** On the same model and split, adding EOG to EEG improves results by at most about 1–2 points (XSleepNet2, SHHS and MASS) and not at all on SleepEDF-20. EOG alone reaches roughly 74–79% accuracy on SleepEDF-20, a few points below EEG.
