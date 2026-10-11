# Intracranial EEG (ECoG and sEEG) Datasets and Benchmark Results

This page has specifications for the main public intracranial EEG (iEEG) datasets, covering electrocorticography (ECoG, grids and strips on the cortex) and stereo-EEG (sEEG, depth electrodes), and the published results on each. Almost all of these recordings come from people with drug-resistant epilepsy who had electrodes implanted to find their seizure focus. Every number links to the paper, leaderboard or repository where it was read. If a source did not report a value, the cell says "not reported". If I could not read a value in a source myself, it is left out or marked *not verified*. Sources were checked on 2026-10-11.

## Overview

| Dataset | Subjects | Electrodes | Sampling rate | Task / labels | Size on disk | License |
|---|---|---|---|---|---|---|
| BCI Competition IV, dataset 4 | 3 | ECoG grids, 62 / 48 / 64 ch | 1 kHz | Finger flexion (data glove, 5 fingers) | not reported | *not verified* |
| Miller ECoG library (Stanford) | 34 (204 datasets) | ECoG | not verified | 16 tasks (finger flexion, faces/houses, motor imagery, ...) | not reported | CC BY-SA 4.0 |
| Brain Treebank | 10 (ages 4–19) | sEEG, 1,688 contacts | 2048 Hz | Movie watching; 223,068 words with POS, parses, audio/visual features | ~130 GB zipped | CC BY 4.0 |
| Berezutskaya iEEG-fMRI film (ds003688) | 51 iEEG (+30 fMRI; 18 both) | ECoG (46), HD ECoG (6), sEEG (16) | 512 or 2048 Hz | 6.5-min film, 30 s speech/music blocks; word/phoneme annotations | 16.3 GB | CC0 |
| "Podcast" ECoG (ds005574) | 9 | ECoG grid/strip/depth, 1,330 total | 512 or 2048 Hz | 30-min story; word timings + LLM features | 3.5 GB | CC0 |
| Bellier Pink Floyd music | 29 | ECoG, 2,668 contacts | 1.2 kHz recorded (HFA released) | Passive listening to one 190.72 s song | not reported | CC BY 4.0 |
| Chen et al. 2024 NYU speech | 48 (1 public) | ECoG 8×8 grids (5 hybrid 128-ch) | 2048 Hz | 400 spoken words per person, 5 tasks | not reported | CC BY 4.0 (public participant) |
| SingleWordProductionDutch (Verwoert 2022) | 10 | sEEG, 1,103 recorded contacts | 1024 Hz | 100 read Dutch words, audio | not reported | CC BY 4.0 |
| Kaggle AES seizure prediction (2014) | 5 dogs + 2 humans | 16 ch (dogs); depth/grid (humans) | 400 Hz dogs, 5 kHz humans | Preictal vs interictal 10-min clips | not reported | *not verified* |
| Kaggle UPenn-Mayo seizure detection (2014) | 4 dogs + 8 humans | 16 ch (dogs); 16–72 ch (humans) | 400 Hz; 500 or 5000 Hz | Ictal vs interictal 1-s clips, plus "early seizure" | not reported | *not verified* |
| Melbourne Kaggle 2016 / Epilepsy Ecosystem | 3 | 16 subdural (4 × 4-contact strips) | 400 Hz | Preictal vs interictal 10-min clips | not reported | *not verified* (registration) |
| Mayo / FNUSA graphoelements | 25 Mayo + 14 FNUSA | Depth (FNUSA); depth/grid/strip (Mayo) | 5 kHz (downsampled) | 3-s clips: physiological / pathological / artifact / line noise | 2.4 + 6.1 GB (.mat zips) | CC0 |
| HUP iEEG epilepsy (ds004100) | 58 | ECoG (20) or sEEG (38) | varies (e.g. 500 Hz) | Ictal + interictal; SOZ and resection channels; outcome | 14.2 GB | CC0 |
| Fragility multicenter (ds003029) | 35 in release (91 in paper) | ECoG and sEEG | typically 1 kHz | Seizure snapshots; SOZ, resection, outcome | 11.1 GB | CC0 |
| SWEC-ETHZ (short / long-term) | 16 / 18 | Strip, grid, depth | 512 Hz / 512 or 1024 Hz | Seizure onset/offset | not reported | Research and education only |
| SWEC iEEG Dataset (Hugging Face, 2025) | 68 | Strip, grid, depth | 512 or 1024 Hz | 9,328 h, 704 seizures | 4.6 TB | CDLA-Permissive-2.0 |
| DARPA RAM public release | 251 | ECoG and depth | not verified | Free recall, paired associates, spatial navigation | not reported | Access by request |

Sources are in each dataset's block below.

---

## Part 1: Dataset specifications

### BCI Competition IV, dataset 4 (ECoG finger flexion)
| Field | Value |
|---|---|
| Year & paper | 2008; Miller & Schalk, competition description ([desc_4.pdf](https://www.bbci.de/competition/iv/desc_4.pdf)); results page ([bbci.de](https://www.bbci.de/competition/iv/results/)). The description asks users to cite Schalk et al. 2007, *J. Neural Eng.* 4:264–275 |
| Subjects | 3 epilepsy patients at Harborview Hospital, Seattle; age and sex not reported |
| Electrodes | Ad-Tech subdural grids, 8×6 or 8×8, 4 mm platinum contacts (2.3 mm exposed), 1 cm spacing; 62, 48 and 64 channels for subjects 1–3 |
| Sampling rate | 1000 Hz; band-pass 0.15–200 Hz (Synamps2 amplifiers, BCI2000) |
| Coverage / localization | Not released: channel order is scrambled and electrode positions are not given ([FingerFlex](https://arxiv.org/abs/2211.01960)) |
| Task / labels | Cued single-finger flexions (word cue for 2 s, 2 s rest), 30 cues per finger; finger position from a 5DT data glove at 25 Hz, upsampled to 1 kHz |
| Duration | About 10 min per subject: first 6 min 40 s train (400,000 samples), last 3 min 20 s test (200,000 samples) |
| Format | MATLAB, one `subX_comp.mat` per subject |
| Access & license | [bbci.de/competition/iv](https://www.bbci.de/competition/iv/); license *not verified* |
| Standard protocol | Within-subject, time split as above. Score = Pearson r between true and predicted flexion, averaged over 3 subjects × 4 fingers; the ring finger is excluded because it moves with the middle or little finger |
| Known issues | Only 3 subjects and 10 min each; 37 ± 3 ms lag between glove and amplifier; no anatomy, so results do not transfer across patients |

### Miller ECoG library (Stanford Digital Repository)
| Field | Value |
|---|---|
| Year & paper | 2019; Miller, *Nature Human Behaviour* 3:1225–1235 ([doi](https://doi.org/10.1038/s41562-019-0678-3)); data at [purl.stanford.edu/zk881ps0522](https://purl.stanford.edu/zk881ps0522) |
| Subjects | 34 patients, 204 datasets |
| Electrodes | Subdural ECoG; the finger-flexion subset has 9 subjects with 46–64 channels ([CORTEG](https://arxiv.org/html/2605.10337v1)) |
| Sampling rate | Same amplifiers, rate and filter settings for all datasets (per the repository); the value is *not verified* here |
| Coverage / localization | All electrode positions registered to brain anatomy |
| Tasks | 16 "benchmark" experiments; the [Neuromatch](https://compneuro.neuromatch.io/projects/ECoG/README.html) copy uses faces/houses, finger flexion, joystick tracking, memory n-back and motor imagery |
| Format | MATLAB data and commented MATLAB analysis scripts |
| Access & license | Open download; CC BY-SA 4.0, with a condition not to re-identify participants |
| Standard protocol | No official split. For finger flexion, later papers train on the first 400 s (about 2/3) and test on the rest ([CORTEG](https://arxiv.org/html/2605.10337v1)) |
| Known issues | Per-patient coverage differs; FingerFlex reports some subjects with r of only 0.2–0.4, which it attributes to grid placement ([FingerFlex](https://arxiv.org/abs/2211.01960)) |

### Brain Treebank (and the BrainBERT data)
| Field | Value |
|---|---|
| Year & paper | 2024; Wang et al., NeurIPS 2024 Datasets & Benchmarks ([proceedings](https://proceedings.neurips.cc/paper_files/paper/2024/hash/aefa2385b3f33abf1526ae4e2c208cd9-Abstract.html), [arXiv](https://arxiv.org/abs/2411.08343)) |
| Subjects | 10 (5 male, 5 female), age 4–19 (mean ≈ 11.9), epilepsy patients at Boston Children's Hospital |
| Electrodes | sEEG depth probes, 6–16 contacts each (0.8 mm diameter, 2 mm long); 12–18 probes per subject; 106–246 contacts per subject (mean ≈ 167), 1,688 total |
| Sampling rate | 2048 Hz; only a 60 Hz notch and harmonics applied |
| Coverage / localization | 1,504 of 1,688 contacts assigned to a brain region; 114 corrupted electrodes listed |
| Task / stimuli | Watching 21 Hollywood movies in full (26 viewing sessions, 43.5 h total, 2.6 movies per subject on average) |
| Labels | 38,572 sentences and 223,068 words: transcripts with word onsets (ASR + manual correction), POS tags and Universal Dependencies parses (Stanza + manual correction), 46,935 scene cuts, speaker identity, and 16 aligned audio/visual/language features |
| Size / format | ~130 GB zipped; HDF5 ([braintreebank.dev](https://braintreebank.dev/)) |
| Access & license | Open download; CC BY 4.0. Movies are not shared (copyright); alignment tools are provided |
| Standard protocol | BrainBERT/PopT tasks: sentence onset, speech vs non-speech, pitch, volume, ROC-AUC, 80/10/10 split ([BrainBERT](https://arxiv.org/abs/2302.14367), [PopT](https://arxiv.org/abs/2406.03044)). [Neuroprobe](https://arxiv.org/abs/2509.21671) adds 15 tasks and three fixed splits (within-session, cross-session, cross-subject), with a [public leaderboard](https://neuroprobe.dev) |
| BrainBERT data | BrainBERT (ICLR 2023) used the same 10 subjects, 1,688 electrodes and 26 sessions; 19 sessions (43.7 h) for pretraining and 7 held-out sessions on different movies for evaluation; 1,249 electrodes after preprocessing |
| Known issues | Pediatric cohort; each subject saw different movies, so cross-subject analysis is hard; per-subject electrode layouts differ completely |

### Berezutskaya open iEEG-fMRI film dataset (OpenNeuro ds003688)
| Field | Value |
|---|---|
| Year & paper | 2022; Berezutskaya et al., *Scientific Data* 9:91 ([PMC8938409](https://pmc.ncbi.nlm.nih.gov/articles/PMC8938409/)) |
| Subjects | 51 iEEG patients (mean age 25 ± 15; 32 female), 30 fMRI, 18 with both; UMC Utrecht, recorded 2007–2021; 28 participants under 18 |
| Electrodes | 46 with clinical ECoG grids (2.3 mm exposed, 10 mm spacing, 48–128 contacts); 6 with additional high-density grids (1.3 mm, 3–4 mm spacing, 32/64/128 contacts); 16 with sEEG (4–173 contacts). Median 79 good channels per subject |
| Sampling rate | 512 Hz (0.15–134.4 Hz; 38 patients) or 2048 Hz (0.3–500 Hz; 13 patients); two HD grids at 2000 Hz on Blackrock |
| Coverage / localization | Mostly perisylvian, frontal and motor; much denser in the left hemisphere; electrode renderings and coordinates provided |
| Task / stimuli | 6.5-min edited film from "Pippi on the Run", dubbed into Dutch: 13 alternating 30 s blocks (7 music, 6 speech); also 3 min of rest |
| Labels | Manual Praat annotation of phonemes, syllables, words, clauses, sentences, verbs and speakers; visual concepts from a commercial network; character presence |
| Size / format | 16.3 GB (snapshot 1.0.7, [OpenNeuro](https://openneuro.org/datasets/ds003688)); iBIDS |
| Access & license | CC0 (OpenNeuro); film available from the authors on request |
| Standard protocol | None defined; validation compares high-frequency band responses in speech vs music blocks |
| Known issues | Left-hemisphere bias; some localizations uncertain (prior resections, low-resolution CT); sub-44 HD and clinical recorded on separate days; HD and sEEG should be processed separately from clinical ECoG |

### "Podcast" ECoG dataset (OpenNeuro ds005574)
| Field | Value |
|---|---|
| Year & paper | 2025; Zada et al., *Scientific Data* 12:1135 ([PMC12226714](https://pmc.ncbi.nlm.nih.gov/articles/PMC12226714/)) |
| Subjects | 9 epilepsy patients at NYU; per-subject sex, age and IQ subtests in Table 1 of the paper |
| Electrodes | Grids (8×8, 5 or 10 mm), strips and depths; 1,330 electrodes total; 3 subjects with hybrid grids (64 extra 1 mm contacts) |
| Sampling rate | 512 Hz (NicoletOne, 0.16–250 Hz) or 2048 Hz (NeuroWorks Quantum) |
| Coverage / localization | MNI coordinates; varies by subject (some mostly left, some mostly right) |
| Task / stimuli | Passive listening to a 30-min "This American Life" story |
| Labels | Forced-aligned, manually corrected word timings (over 5,000 words); features: mel spectrogram, phonemes, syntax, GloVe, GPT-2 XL embeddings |
| Size / format | 3.5 GB; BIDS-iEEG, raw EDF plus preprocessed high-gamma (70–200 Hz) in MNE `.fif` |
| Access & license | [OpenNeuro](https://openneuro.org/datasets/ds005574), CC0 (the article itself is CC BY-NC-ND 4.0) |
| Standard protocol | Electrode-wise ridge encoding models, 2-fold cross-validation over halves of the story |
| Known issues | Only 9 subjects; one story; features with long autocorrelation (LLM, acoustic) inflate encoding scores, as the authors warn |

### Bellier et al. music dataset (Pink Floyd)
| Field | Value |
|---|---|
| Year & paper | 2023; Bellier et al., *PLoS Biology* ([PMC10427021](https://pmc.ncbi.nlm.nih.gov/articles/PMC10427021/)) |
| Subjects | 29 epilepsy patients (15 female; age 16–60, mean 33.4) |
| Electrodes | ECoG grids/strips (Ad-Tech), 10 mm spacing for 21 patients, 6 / 4 / 3 mm for the rest; 2,668 electrodes, 2,379 artifact-free |
| Signal released | Preprocessed high-frequency activity (70–150 Hz) per patient, MNI coordinates, and the song spectrograms ([Zenodo](https://doi.org/10.5281/zenodo.7876019)); raw ECoG was recorded at 1,200 Hz (g.USBamp, BCI2000) |
| Task | Passive listening to "Another Brick in the Wall, Part 1" (190.72 s) |
| License | CC BY 4.0 (Zenodo record) |
| Standard protocol | Paper: 60/20/20 split in 2-s blocks for encoding; 12 held-out 15-s segments for decoding |
| Known issues | One song, so train and test share the same piece of music; only 347 electrodes are song-responsive |

### Chen et al. 2024 NYU speech decoding data
| Field | Value |
|---|---|
| Year & paper | 2024; Chen et al., *Nature Machine Intelligence* ([PMC12965882](https://pmc.ncbi.nlm.nih.gov/articles/PMC12965882/)) |
| Subjects | 48 native English speakers (26 female, 22 male); 32 left- and 16 right-hemisphere implants |
| Electrodes | 64-contact 8×8 grids, 10 mm spacing (43 participants); 5 participants with hybrid grids adding 64 small contacts |
| Sampling rate | 2048 Hz, downsampled to 512 Hz; high gamma (70–150 Hz) at 125 Hz used for decoding |
| Task | 50 words produced in 5 tasks (repetition, auditory naming, sentence completion, reading, picture naming), 400 trials per person |
| Access & license | Only one participant's neural and audio data are public ([Mendeley Data](https://data.mendeley.com/datasets/fp4bv9gtwk/2)); the rest on request under IRB terms. The Mendeley record is CC BY 4.0 |
| Standard protocol | Per participant: 350 trials train, 50 test (10 per task); also word-level held-out folds |
| Known issues | The public release cannot reproduce the 48-person results |

### SingleWordProductionDutch-iBIDS (Verwoert et al. 2022)
| Field | Value |
|---|---|
| Year & paper | 2022; Verwoert et al., *Scientific Data* ([PMC9307753](https://pmc.ncbi.nlm.nih.gov/articles/PMC9307753/)) |
| Subjects | 10 epilepsy patients (5 male, 5 female; mean age 32, range 16–50), Kempenhaeghe / Maastricht |
| Electrodes | sEEG shafts (Dixi Microdeep, 0.8 mm, 2 mm contacts, 1.5 mm spacing, 5–18 contacts each); 1,317 implanted, 1,103 recorded (54–127 per subject) |
| Sampling rate | 1024 or 2048 Hz, stored at 1024 Hz; audio at 48 kHz (pitch-shifted for anonymity) |
| Coverage / localization | 40.3% of contacts in white matter, 12.6% unlabeled; most others in superior temporal sulcus, hippocampus and inferior parietal gyrus |
| Task | 100 Dutch words read aloud (2 s each, 1 s fixation), 300 s per subject |
| Format | NWB inside iBIDS |
| Access & license | [OSF](https://doi.org/10.17605/OSF.IO/NRGX6), CC BY 4.0 |
| Standard protocol | Paper: non-shuffled 10-fold CV; linear regression from high-gamma to 23 log-mel bins; metric Pearson r |
| Known issues | Only 5 min per person; sparse sEEG coverage; the authors note that r mostly measures speech vs silence |

### Kaggle "American Epilepsy Society Seizure Prediction Challenge" (2014)
| Field | Value |
|---|---|
| Year & paper | 2014 contest; Brinkmann et al., *Brain* 2016 ([PMC5022671](https://pmc.ncbi.nlm.nih.gov/articles/PMC5022671/)) |
| Subjects | 5 dogs with naturally occurring epilepsy (NeuroVista implant) + 2 Mayo Clinic patients (female, 70 and 48) |
| Electrodes | Dogs: 16 subdural contacts (two 4-contact strips per hemisphere). Patient 1: bitemporal 8-contact depths; patient 2: 3×8 grid (depths and strips were also implanted, but only the grid was used in the contest) |
| Sampling rate | Dogs 400 Hz; humans 5 kHz |
| Labels | 10-min clips. Preictal = six clips in the 66 min before a lead seizure, ending 5 min before onset; interictal clips at least 1 week from any seizure; annotated by an epileptologist |
| Duration | Dogs 1,920–8,208 h recorded each; patients 71.3 and 158.5 h |
| Format | MATLAB |
| Standard protocol | Training clips from the first part of each record, test from the later part; AUC on the test clips; public leaderboard on 40% of test, private on 60% |
| Known issues | Heavy class imbalance (about 90–95% interictal); the 2 humans have very few lead seizures (4 and 6) |

### Kaggle "UPenn and Mayo Clinic Seizure Detection Challenge" (2014)
| Field | Value |
|---|---|
| Year & paper | 2014 contest; Baldassano et al., *Brain* 2017 ([OUP](https://academic.oup.com/brain/article/140/6/1680/3814969), [PMC6075622](https://pmc.ncbi.nlm.nih.gov/articles/PMC6075622/)) |
| Subjects | 4 dogs + 8 humans |
| Electrodes | Dogs: NeuroVista, 16 subdural contacts on two 4-contact strips per side. Humans: Mayo Clinic, 16–72 channels |
| Sampling rate | Dogs 400 Hz; humans 500 or 5000 Hz |
| Labels | 1-s clips, ictal or interictal; "early" = within 15 s of the earliest electrographic change |
| Standard protocol | Score = ½ (AUC seizure + AUC early seizure); validation on 18 new patients (7 EMU, 11 NeuroVista) |

### Melbourne University AES-MathWorks-NIH Seizure Prediction (Kaggle 2016) and Epilepsy Ecosystem
| Field | Value |
|---|---|
| Year & paper | 2016 contest; Kuhlmann et al., *Brain* 2018 ([OUP](https://academic.oup.com/brain/article/141/9/2619/5063014), [PMC6136083](https://pmc.ncbi.nlm.nih.gov/articles/PMC6136083/)) |
| Subjects | 3 patients from the NeuroVista Seizure Advisory System trial, chosen because they had the lowest prediction performance in that trial |
| Electrodes | 16 subdural contacts (4 × 4-contact strips) |
| Sampling rate | 400 Hz, 16-bit |
| Duration | 559, 393 and 374 days of recording; 231, 186 and 216 lead seizures |
| Labels | 10-min clips: preictal in the 66 min before lead seizures, interictal far from seizures |
| Format | MATLAB |
| Access & license | Contest data and top algorithms on [epilepsyecosystem.org](https://www.epilepsyecosystem.org/) after registration; terms *not verified* |
| Standard protocol | Test data follow training data in time, and the held-out data follow test data; AUC |
| Known issues | Only 3 patients; different algorithms work best for different patients |

### Mayo Clinic / FNUSA multicenter graphoelement dataset
| Field | Value |
|---|---|
| Year & paper | 2020; Nejedly et al., *Scientific Data* 7:179 ([PMC7297990](https://pmc.ncbi.nlm.nih.gov/articles/PMC7297990/)) |
| Subjects | FNUSA (St. Anne's, Brno): 14 patients, 30 min awake rest. Mayo Clinic: 25 patients, 2 h of the first night after implantation |
| Electrodes | FNUSA: depth electrodes (5–15 contacts, 0.8 mm). Mayo: depth (4 or 8 contacts) and/or grids and strips |
| Sampling rate | Recorded at 25 kHz (FNUSA) and 32 kHz (Mayo); released at 5 kHz |
| Labels | Single-channel 3-s clips (15,000 samples): physiological, pathological (spikes, HFOs), artifact, power-line noise. Each recording reviewed by one of 3 reviewers |
| Size | FNUSA 193,118 clips, Mayo 155,182 clips (Table 1 totals; the text swaps the two counts). [Figshare](https://doi.org/10.6084/m9.figshare.c.4681208.v1): Mayo 2.4 GB, FNUSA 6.12 GB, BIDS_MAYO 6.84 GB |
| Format / license | `.mat` per clip, plus BIDS versions; CC0 |
| Standard protocol | Paper: cross-reviewer and out-of-institution tests (train on one hospital, test on the other); AUROC/AUPRC |
| Known issues | Single-channel clips, so no spatial context; one reviewer per recording; later papers use different class merges, patient counts (MVPFormer reports 24 Mayo patients) and resampling |

### HUP iEEG epilepsy dataset (OpenNeuro ds004100)
| Field | Value |
|---|---|
| Year & paper | Released with Bernabei & Li et al. (in preparation); subsets used in Kini et al., *Brain* 2019 and Bernabei et al., *Brain* 2022 ([PMC9630716](https://pmc.ncbi.nlm.nih.gov/articles/PMC9630716/)) |
| Subjects | 58 in `participants.tsv` (31 F, 27 M), Hospital of the University of Pennsylvania; 36 successful and 22 failed surgical outcomes; resection or laser ablation |
| Electrodes | 20 ECoG (grid/strip/depth), 38 sEEG |
| Sampling rate | Varies by run (e.g. 500 Hz for sub-HUP060, from the BIDS sidecar) |
| Coverage / localization | MNI (ICBM152) and fsaverage electrode coordinates; clinician seizure-onset channels; channels inside the segmented resection cavity |
| Labels | Ictal runs with seizure onset/offset events; interictal runs; Engel outcome, lesional status, therapy |
| Size / format | 14.2 GB; BIDS, EDF |
| Access & license | [OpenNeuro](https://openneuro.org/datasets/ds004100), CC0 |
| Standard protocol | None fixed; typical task is SOZ localization or outcome prediction, leave-one-patient-out |
| Known issues | README says 58 subjects but the OpenNeuro summary lists 57 IDs; mixed ECoG/sEEG; clinical SOZ labels are themselves uncertain |

### Fragility multicenter iEEG dataset (OpenNeuro ds003029)
| Field | Value |
|---|---|
| Year & paper | 2021; Li et al., *Nature Neuroscience* ([PMC8547387](https://pmc.ncbi.nlm.nih.gov/articles/PMC8547387/)) |
| Subjects | Paper: 91 patients from 5 centers (44 success, 47 failure; age at surgery 31.5 ± 12.3), 462 seizures. Public release: 35 subjects from NIH, JHH, UMMC and UMF; Cleveland Clinic data need a separate DUA ([README](https://openneuro.org/datasets/ds003029)) |
| Electrodes | ECoG and sEEG; 14,703 contacts in the paper (159.8 ± 45.4 per subject) |
| Sampling rate | Typically 1000 Hz; patients below 250 Hz excluded |
| Coverage / localization | No coordinates (no MRI/CT processed); approximate regions in metadata |
| Labels | Seizure onset/offset markers (naming not consistent across centers), clinical SOZ, resected/ablated contacts, Engel/ILAE outcome |
| Size / format | 11.1 GB; BIDS, BrainVision |
| Access & license | CC0 |
| Standard protocol | Paper: predict surgical outcome from feature maps of SOZ vs non-SOZ contacts, random forest, 10-fold nested CV |
| Known issues | Public subset is smaller than the paper's cohort; marker names inconsistent |

### SWEC-ETHZ iEEG database and SWEC iEEG Dataset
| Field | Value |
|---|---|
| Year & paper | Short-term: Burrello et al., BioCAS 2018. Long-term: Burrello et al., DATE 2019 ([database page](http://ieeg-swez.ethz.ch/)). Large release: Carzaniga et al., ICLR 2026 ([arXiv 2506.20354](https://arxiv.org/abs/2506.20354), [Hugging Face](https://huggingface.co/datasets/NeuroTec/SWEC_iEEG_Dataset)) |
| Subjects | Short-term: 16 patients, 100 seizure recordings. Long-term: 18 patients, 116 seizures in 2,656 h. Hugging Face: 68 patients, 9,328 h, 704 seizures. All from Inselspital Bern |
| Electrodes | Strip, grid and depth (24–128 electrodes in the long-term set) |
| Sampling rate | Short-term 512 Hz (0.5–150 Hz); long-term 512 or 1024 Hz (0.5–120 Hz), median-referenced |
| Coverage / localization | Not provided (privacy) |
| Labels | Seizure onsets/offsets marked by a board-certified epileptologist; artifact channels removed |
| Format | `.mat` (short: 3 min pre + seizure + 3 min post; long: 1-h files); Hugging Face: lz4-compressed HDF5, 4.6 TB |
| Access & license | ETHZ page: free for research and education only. Hugging Face: CDLA-Permissive-2.0, ungated; research use only, not for diagnosis |
| Standard protocol | Patient-specific detection (train on 1–2 seizures, test on the rest). MVPFormer: pretrain/fine-tune on 18 subjects, zero-shot test on the other 50, Cohen's kappa vs expert |
| Known issues | No electrode locations; very large files |

### DARPA RAM public data release (Cognitive Electrophysiology Data Portal)
| Field | Value |
|---|---|
| Year & paper | Phase I and II of DARPA Restoring Active Memory ([memory.psych.upenn.edu/RAM](https://memory.psych.upenn.edu/RAM)) |
| Subjects | 251 |
| Content | iEEG recordings split by channel, demographics, contact atlas locations and coordinates, FreeSurfer surfaces, SOZ / interictal spiking / bad leads, behavioral events |
| Tasks | Free recall (FR), categorized free recall (CatFR), paired associates (PAL), Yellow Cab and Treasure Hunt spatial navigation; stimulation versions (FR2/3 etc.) |
| Access | By request on the website; sampling rate, size and license *not verified* |

---

## Part 2: Results

Within each table, rows use the same protocol and metric unless a row is marked otherwise. A number tagged "via X" was read in paper X's comparison table, not in the original paper. Almost all iEEG results are **within-patient** (one model per person) unless the protocol column says otherwise.

### BCI Competition IV dataset 4: official test set, within-patient, Pearson r (mean over 3 subjects × 4 fingers, ring finger excluded)
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Liang (INRIA), leaderboard](https://www.bbci.de/competition/iv/results/) | 2008 | Competition winner | Official split | Mean r | 0.46 |
| [Flamary (LITIS), leaderboard](https://www.bbci.de/competition/iv/results/) | 2008 | 2nd place | Official split | Mean r | 0.42 |
| [Salvaris (Essex), leaderboard](https://www.bbci.de/competition/iv/results/) | 2008 | 3rd place | Official split | Mean r | 0.27 |
| [Popescu (Fraunhofer FIRST), leaderboard](https://www.bbci.de/competition/iv/results/) | 2008 | 4th place | Official split | Mean r | 0.10 |
| [Yoon (USC), leaderboard](https://www.bbci.de/competition/iv/results/) | 2008 | 5th place | Official split | Mean r | 0.05 |

### BCI Competition IV dataset 4: post-competition papers, as compiled by FingerFlex (S1 / S2 / S3 / average)
Same split, but these numbers use the released test labels after the competition. Whether every paper excluded the ring finger is not stated in the FingerFlex table. The 2012 papers by the 1st- and 2nd-place teams report slightly different averages than the leaderboard.

| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| Flamary & Rakotomamonjy, via [FingerFlex Table 2](https://arxiv.org/abs/2211.01960) | 2012 | Switching linear models (2nd place) | Official split | Mean r | 0.48 / 0.24 / 0.56 / 0.43 |
| Liang & Bougrain, via [FingerFlex Table 2](https://arxiv.org/abs/2211.01960) | 2012 | Competition winner | Official split | Mean r | 0.45 / 0.39 / 0.59 / 0.48 |
| Xie et al., via [FingerFlex Table 2](https://arxiv.org/abs/2211.01960) | 2018 | CNN + LSTM | Official split | Mean r | 0.56 / 0.41 / 0.58 / 0.52 |
| Frey et al., via [FingerFlex Table 2](https://arxiv.org/abs/2211.01960) | 2021 | Multi-purpose CNN | Official split | Mean r | average 0.52 (per subject n/a) |
| Petrosyan et al., via [FingerFlex Table 2](https://arxiv.org/abs/2211.01960) | 2021 | Compact interpretable CNN | Official split | Mean r | 0.45 / 0.34 / 0.56 / 0.45 |
| Yao, Zhu, Shoaran, via [FingerFlex Table 2](https://arxiv.org/abs/2211.01960) | 2022 | Riemannian features + LightGBM | Official split | Mean r | 0.52 / 0.47 / 0.61 / 0.53 |
| [Lomtev et al. (FingerFlex)](https://arxiv.org/abs/2211.01960) | 2022 | Wavelet features + conv encoder-decoder | Official split; Table 3 lists all 5 fingers | Mean r | 0.66 / 0.62 / 0.74 / 0.67 |

FingerFlex tuned its model on subject 1 and reports both its development steps (Table 1) and its final scores (Table 3) on the "provided validation set", which is the competition test set. Its subject 1 score is therefore not a clean held-out result.

### Miller ECoG library, finger flexion (9 subjects): first 400 s (≈2/3) train, rest test, within-patient, Pearson r over 5 fingers
| Paper | Year | Method | Protocol | Metric | Result (mean ± SD across subjects) |
|---|---|---|---|---|---|
| PLS, via [CORTEG Table 1](https://arxiv.org/html/2605.10337v1) (from Sun et al. 2025) | 2025 | Partial least squares, multi-band wavelet | as above | Mean r | 0.402 ± 0.115 |
| CNN-LSTM, via [CORTEG Table 1](https://arxiv.org/html/2605.10337v1) (from Sun et al. 2025) | 2025 | CNN-LSTM | as above | Mean r | 0.411 ± 0.124 |
| LSTM (high gamma), via [CORTEG Table 1](https://arxiv.org/html/2605.10337v1) (from Sun et al. 2025) | 2025 | LSTM | as above | Mean r | 0.485 ± 0.136 |
| HiLoFuseNet, via [CORTEG Table 1](https://arxiv.org/html/2605.10337v1) (from Sun et al. 2025, TechRxiv) | 2025 | Dual-stream conv + LSTM | as above | Mean r | 0.534 ± 0.138 |
| DeepFingerNet, via [CORTEG Table 1](https://arxiv.org/html/2605.10337v1) (from Tao et al. 2025, IEEE TIM) | 2025 | UNet++ on wavelets | as above | Mean r | 0.542 ± 0.129 |
| [CORTEG](https://arxiv.org/html/2605.10337v1) | 2026 | Scalp-EEG foundation model adapted to ECoG, per-subject | as above | Mean r | 0.539 ± 0.140 |
| [CORTEG](https://arxiv.org/html/2605.10337v1) | 2026 | Same, leave-one-subject-out fine-tuning | as above | Mean r | 0.551 ± 0.147 |
| [CORTEG](https://arxiv.org/html/2605.10337v1) | 2026 | Same, pooled training | as above | Mean r | 0.554 ± 0.154 |

Not directly comparable: [FingerFlex](https://arxiv.org/abs/2211.01960) (2022) Table 4 gives per-subject averages from 0.22 (wm) to 0.71 (cc) on the same 9 subjects, without stating the split.

### Brain Treebank, BrainBERT protocol: per-electrode decoding on the top-10 electrodes, 80/10/10 split, fine-tuned, ROC-AUC (sentence onset / speech vs non-speech / pitch / volume)
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Wang et al. (BrainBERT)](https://arxiv.org/abs/2302.14367) | 2023 | Linear, 5 s raw | as above | ROC-AUC | .63 / .58 / .58 / .56 |
| [Wang et al. (BrainBERT)](https://arxiv.org/abs/2302.14367) | 2023 | Deep NN (5 FF layers) | as above | ROC-AUC | .72 / .67 / .57 / .54 |
| [Wang et al. (BrainBERT)](https://arxiv.org/abs/2302.14367) | 2023 | BrainBERT (STFT input) | as above | ROC-AUC | .82 / .93 / .75 / .83 |

### Brain Treebank, PopT protocol: multi-channel (up to 90 electrodes), per-subject fine-tuning, 80/10/10, ROC-AUC (pitch / volume / sentence onset / speech vs non-speech)
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Chau et al. (PopT)](https://arxiv.org/abs/2406.03044) | 2025 | BrainBERT embeddings + linear aggregation | as above | ROC-AUC | 0.59 / 0.66 / 0.70 / 0.71 |
| [Chau et al. (PopT)](https://arxiv.org/abs/2406.03044) | 2025 | Brant, fine-tuned + linear aggregation | as above | ROC-AUC | 0.61 / 0.74 / 0.80 / 0.80 |
| [Chau et al. (PopT)](https://arxiv.org/abs/2406.03044) | 2025 | PopT on TOTEM embeddings | as above | ROC-AUC | 0.64 / 0.79 / 0.90 / 0.88 |
| [Chau et al. (PopT)](https://arxiv.org/abs/2406.03044) | 2025 | Pretrained PopT on BrainBERT embeddings | as above | ROC-AUC | 0.74 / 0.87 / 0.90 / 0.93 |
| [Carzaniga et al. (MVPFormer-S)](https://arxiv.org/abs/2506.20354) | 2025 | Multi-variate parallel attention, no electrode positions | **Not directly comparable:** "follows" BrainBERT/PopT, but the table header says "acc" and the channel selection differs | "acc" | 0.83 / 0.88 / 0.87 / 0.90 |

The MVPFormer table copies PopT's AUROC numbers as baselines while labeling the column "acc". The metric is therefore probably AUROC, but this is *not verified*.

### Brain Treebank, Neuroprobe leaderboard: mean AUROC over 15 tasks (within-session / cross-session / cross-subject)
Read from [neuroprobe.dev](https://neuroprobe.dev) on 2026-10-11. Leaderboard entries are dated by submission and are not peer-reviewed. "—" means the entry is not on that split's board. The Neuroprobe paper's own supplementary numbers differ slightly from the board (e.g. Laplacian + spectrogram linear cross-session 0.648 in [the paper](https://arxiv.org/html/2509.21671v1) vs 0.651 on the board).

| Paper / entry | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Neuroprobe baseline](https://neuroprobe.dev) | 2026 | Linear, raw voltage | Neuroprobe splits | Mean AUROC | 0.604 / 0.574 / 0.509 |
| [Neuroprobe baseline](https://neuroprobe.dev) | 2026 | PopT, off-the-shelf | same | Mean AUROC | 0.549 / 0.564 / — |
| [Neuroprobe baseline](https://neuroprobe.dev) | 2026 | BrainBERT frozen, off-the-shelf | same | Mean AUROC | 0.585 / 0.580 / 0.522 |
| [Neuroprobe baseline](https://neuroprobe.dev) | 2026 | Linear, spectrogram | same | Mean AUROC | 0.625 / 0.626 / 0.528 |
| [Neuroprobe baseline](https://neuroprobe.dev) | 2026 | Linear, Laplacian re-reference + spectrogram | same | Mean AUROC | 0.660 / 0.651 / 0.539 |
| [Leaderboard (Gross, Columbia)](https://neuroprobe.dev) | 2026 | GLIS-GNN | same | Mean AUROC | 0.553 / 0.550 / 0.515 |
| [Leaderboard (Chau, Caltech)](https://neuroprobe.dev) | 2026 | BrainBERT frozen, global z-scoring | same | Mean AUROC | 0.626 / 0.633 / 0.547 |
| [Leaderboard (Chau, Caltech)](https://neuroprobe.dev) | 2026 | MLP, Laplacian + spectrogram | same | Mean AUROC | 0.656 / 0.655 / 0.566 |
| [Leaderboard (Chau, Caltech)](https://neuroprobe.dev) | 2026 | CNN, Laplacian + spectrogram | same | Mean AUROC | 0.669 / 0.670 / 0.578 |
| [Leaderboard (Chau, Caltech)](https://neuroprobe.dev) | 2026 | PopT, global z-scoring | same | Mean AUROC | 0.670 / 0.663 / 0.575 |
| [Leaderboard (Gwon, SNU)](https://neuroprobe.dev) | 2026 | DIVER-1 (0.1 s, tiny, frozen) | same | Mean AUROC | 0.678 / — / — |
| [Leaderboard (Tang, Duke)](https://neuroprobe.dev) | 2026 | MAPA | same | Mean AUROC | 0.695 / 0.691 / 0.608 |

Sentence onset is the easiest task: the best within-session entry (MAPA) reaches 0.933, while frame brightness stays near chance (0.505).

### Berezutskaya film dataset (ds003688): within-patient ("same patient") classification, F1
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Ostadsharif Memar et al. (RISE-iEEG v1)](https://arxiv.org/abs/2408.14477v1) | 2024 | Patient-specific projection + shared DNN | Speech vs music, 2-s events (90 speech / 105 music per patient), 51 patients | F1 | 0.79 ± 0.02 |
| [Ostadsharif Memar et al. (RISE-iEEG v1)](https://arxiv.org/abs/2408.14477v1) | 2024 | same | Question vs non-question sentence, 3-s events | F1 | 0.69 ± 0.01 |

HTNet and EEGNet were not run on this dataset because it has no MNI coordinates. I found no published speech or music *reconstruction* number on ds003688.

### Bellier music dataset: spectrogram reconstruction (pooled electrodes from all 29 patients unless noted)
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Bellier et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC10427021/) | 2023 | Linear decoding, 347 song-responsive electrodes | Held-out 15-s segments | Median effective r² over 128 frequency bins | 0.325 |
| [Bellier et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC10427021/) | 2023 | Two-layer MLP, same electrodes | same | Median effective r² | 0.429 |
| [Bellier et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC10427021/) | 2023 | MLP, one patient (P29, 61 electrodes, 3 mm grid) | same | Effective r² | 0.363 |

### Bellier music dataset: singing vs instrumental music, 2-s events, F1. Not comparable with the reconstruction table
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [RISE-iEEG v1](https://arxiv.org/abs/2408.14477v1) | 2024 | Minimum distance / EEGNet / HTNet / random forest / RISE-iEEG | Same patient | F1 | 0.58 / 0.74 / 0.73 / 0.78 / 0.83 |
| [RISE-iEEG v1](https://arxiv.org/abs/2408.14477v1) | 2024 | Same five models | **Unseen patient** (projection layer fine-tuned) | F1 | 0.49 / 0.67 / 0.60 / 0.71 / 0.80 |

The v2 text of [RISE-iEEG](https://arxiv.org/html/2408.14477v2) gives different baseline numbers: HTNet 0.76 ± 0.04 and random forest 0.71 ± 0.02 (same patient), and HTNet 0.70 ± 0.09 (unseen patient).

### Speech decoding. Each table uses a different dataset; none are comparable with each other

**Chen et al. 2024 NYU data (48 participants, only 1 public): within-patient, 50 held-out trials, PCC between decoded and true spectrogram (mean over participants)**

| Paper | Year | Method | Protocol | Metric | Result (non-causal / causal) |
|---|---|---|---|---|---|
| [Chen et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC12965882/) | 2024 | LSTM decoder + differentiable speech synthesizer | as above | PCC | 0.745 / 0.712 |
| [Chen et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC12965882/) | 2024 | 3D Swin transformer decoder | as above | PCC | 0.792 / 0.798 |
| [Chen et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC12965882/) | 2024 | 3D ResNet decoder | as above | PCC | 0.806 / 0.797 |

Per-participant PCC ranges from 0.62 to 0.92. No word error rate is reported.

**SingleWordProductionDutch (10 sEEG participants): within-patient, 80/20 split, mel-cepstral distortion (dB, lower is better), mean of 10 speakers**

| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Arthur & Csapó](https://doi.org/10.36244/ICJ.2024.1.6) | 2024 | Linear regression + Griffin-Lim (the Verwoert baseline) | as above | MCD | 5.39 dB |
| [Arthur & Csapó](https://doi.org/10.36244/ICJ.2024.1.6) | 2024 | 3D-CNN + WaveGlow | as above | MCD | 5.04 dB |
| [Arthur & Csapó](https://doi.org/10.36244/ICJ.2024.1.6) | 2024 | 2D-CNN + WaveGlow | as above | MCD | 4.78 dB |
| [Arthur & Csapó](https://doi.org/10.36244/ICJ.2024.1.6) | 2024 | FC-DNN + WaveGlow | as above | MCD | 4.55 dB |

[Verwoert et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC9307753/) report the linear baseline as a Pearson r per participant (10-fold CV) in a figure only, with no number in the text. Arthur & Csapó describe the synthesized speech as still not intelligible.

### Kaggle AES seizure prediction 2014: leaderboard AUC (public on 40% / private on 60% of the test clips)
| Paper | Year | Method | Protocol | Metric | Result (public / private) |
|---|---|---|---|---|---|
| QMSDP, in [Brinkmann et al. Table 2](https://pmc.ncbi.nlm.nih.gov/articles/PMC5022671/) | 2014 | LassoGLM + bagged SVM + random forest | Contest split | AUC | 0.86 / 0.82 |
| Birchwood, same source | 2014 | SVM on log spectral power + covariance | same | AUC | 0.84 / 0.80 |
| ESAI CEU-UCH, same source | 2014 | Neural network + kNN, Bayesian combination | same | AUC | 0.82 / 0.79 |
| Michael Hills, same source | 2014 | SVM, genetic feature selection | same | AUC | 0.86 / 0.79 |
| KPZZ, same source | 2014 | not described | same | AUC | 0.82 / 0.79 |
| Carlos Fernandez, same source | 2014 | not described | same | AUC | 0.84 / 0.79 |
| Isaac, same source | 2014 | not described | same | AUC | 0.84 / 0.79 |
| Wei Wu, same source | 2014 | SVM + GLMNet | same | AUC | 0.82 / 0.79 |
| Golondrina, same source | 2014 | CNN | same | AUC | 0.82 / 0.78 |
| Sky Kerzner, same source | 2014 | not described | same | AUC | 0.84 / 0.78 |

**Held-out data from 4 dogs (5,000 new clips, run by the organizers after the contest)** from [Brinkmann et al. Table 3](https://pmc.ncbi.nlm.nih.gov/articles/PMC5022671/) (2016), AUC: QMSDP 0.75, Birchwood 0.74, ESAI CEU-UCH 0.72, Michael Hills 0.79, Wei Wu 0.77, Golondrina 0.76 (0.77 without test calibration). The top private-leaderboard model dropped by 8%, while 4th place held its score.

### Kaggle UPenn-Mayo seizure detection 2014: score = ½ (AUC seizure + AUC early seizure)
| Paper | Year | Method | Protocol | Metric | Result (private / public) |
|---|---|---|---|---|---|
| Michael Hills, in [Baldassano et al.](https://academic.oup.com/brain/article/140/6/1680/3814969) | 2014 | 1st place | Contest split | Mean AUC | 0.96288 / 0.97490 |
| Olson and Mingle, same source | 2014 | 2nd place | same | Mean AUC | 0.95655 / 0.96803 |
| cdipsters, same source | 2014 | 3rd place | same | Mean AUC | 0.95643 / 0.96199 |

**Out-of-sample validation on 18 new patients** ([Baldassano et al.](https://academic.oup.com/brain/article/140/6/1680/3814969), 2017), top 3 in the same order: overall 0.972 / 0.946 / 0.974; seizure AUC 0.981 / 0.976 / 0.984; early-seizure AUC 0.964 / 0.916 / 0.964.

### Melbourne University Kaggle 2016 (3 patients): AUC (public / private leaderboard / held-out)
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| notsorandomanymore (rank 1), in [Kuhlmann et al. Table 2](https://academic.oup.com/brain/article/141/9/2619/5063014) | 2016 | Contest entry | Time-ordered train → test → held-out | AUC | 0.85276 / 0.80701 / 0.75275 |
| Arete Associates (2), same source | 2016 | same | same | AUC | 0.78328 / 0.79898 / 0.73364 |
| GarethJones (3), same source | 2016 | same | same | AUC | 0.81524 / 0.79652 / 0.65523 |
| QingnanTang (4), same source | 2016 | same | same | AUC | 0.7965 / 0.79458 / 0.71805 |
| Nullset (5), same source | 2016 | same | same | AUC | 0.81423 / 0.79363 / 0.62929 |
| tralala boum boum pouet pouet (6), same source | 2016 | same | same | AUC | 0.80493 / 0.79197 / 0.71822 |
| Michaln (8), same source | 2016 | same | same | AUC | 0.80396 / 0.79074 / 0.73441 |
| Chipicito + Solver World (special prize), same source | 2016 | same | same | AUC | 0.80334 / 0.73968 / 0.76632 |

Held-out drops range from −6.7% (rank 1) to −20.7% (rank 5). The special-prize entry improved by 3.6% on held-out data.

### Mayo / FNUSA. The tables use different class definitions and splits and are not comparable with each other

**Dataset paper technical validation (Convolutional LSTM; 4 classes)**, [Nejedly et al. 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7297990/):

| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Nejedly et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC7297990/) | 2020 | Conv-LSTM on spectrograms | Cross-reviewer (train on 2 reviewers' labels, test on the 3rd), average | AUROC / AUPRC | Mayo 0.97 / 0.93; FNUSA 0.92 / 0.80 |
| [Nejedly et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC7297990/) | 2020 | same | Out-of-institution: train FNUSA → test Mayo | AUROC / AUPRC | 0.80 / 0.71 |
| [Nejedly et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC7297990/) | 2020 | same | Out-of-institution: train Mayo → test FNUSA | AUROC / AUPRC | 0.84 / 0.74 |

**Earlier subset (11 FNUSA + 25 Mayo patients, 3 classes, no line-noise class), train FNUSA → test Mayo**, [Nejedly et al. 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6684807/):

| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| Nejedly et al. 2018 CNN, in [Nejedly et al. 2019 Table 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC6684807/) | 2018 | CNN | Out-of-institution | F1 (physiological / pathological / artifact / average) | 0.90 / 0.64 / 0.89 / 0.81 |
| [Nejedly et al. 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6684807/) | 2019 | Convolutional LSTM | same | F1 (same order) | 0.86 / 0.73 / 0.80 / 0.80 |

**Foundation models, other protocols:**

| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Carzaniga et al. (MVPFormer)](https://arxiv.org/abs/2506.20354) | 2025 | MVPFormer-M / MVPFormer-S / Brant-2 | Pathological vs (physiological + noise); fine-tune on first 4 patients, test on the rest; pooled F1 | F1, Mayo | 0.36 / 0.35 / 0.19 |
| [Carzaniga et al. (MVPFormer)](https://arxiv.org/abs/2506.20354) | 2025 | same | same | F1, FNUSA | 0.46 / 0.46 / 0.46 |
| [Yuan et al. (BrainWave)](https://arxiv.org/abs/2402.10251) | 2024 | BrainWave foundation model | Fine-tune on FNUSA, zero-shot on Mayo (clips resampled to 1 kHz) | AUROC | 93.82% |

On FNUSA all three MVPFormer-table models reach specificity of only 0.02–0.10, so an F1 of 0.46 means they flag almost everything as pathological. MVPFormer also calls the pathological class "ictal", although these are interictal clips.

### HUP and Fragility datasets (SOZ / surgical outcome)
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Bernabei et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC9630716/) | 2022 | Normative atlas, univariate + connectivity z-scores | SOZ vs normal channels; 166 subjects (HUP + MNI atlas data; a subset is in ds004100) | AUC | 0.77 |
| [Li et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC8547387/) | 2021 | Neural fragility + random forest | Surgical outcome, 91 patients from 5 centers (Cleveland data not in ds003029), 10-fold nested CV | AUC | 0.88 ± 0.064 |
| [Li et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC8547387/) | 2021 | Beta-band power (best of 20 baseline features) | same | AUC | 0.82 ± 0.040 |

The two rows answer different questions (channel-level SOZ vs patient-level outcome) and are not comparable.

### SWEC iEEG Dataset: zero-shot seizure detection on 50 unseen patients (≈7,000 h), 32 selected channels
| Paper | Year | Method | Protocol | Metric | Result (kappa / F1) |
|---|---|---|---|---|---|
| [Carzaniga et al. (MVPFormer)](https://arxiv.org/abs/2506.20354) | 2025 | BrainBERT (fine-tuned) | Train 18 patients, test 50 | Cohen's kappa vs expert / F1 | 0.00 / 0.00 |
| [Carzaniga et al.](https://arxiv.org/abs/2506.20354) | 2025 | Brant-2 (fine-tuned) | same | kappa / F1 | 0.06 / 0.01 |
| [Carzaniga et al.](https://arxiv.org/abs/2506.20354) | 2025 | MV-Llama (vanilla attention ablation) | same | kappa / F1 | 0.11 / 0.01 |
| [Carzaniga et al.](https://arxiv.org/abs/2506.20354) | 2025 | MVPFormer-S | same | kappa / F1 | 0.57 / 0.53 |
| [Carzaniga et al.](https://arxiv.org/abs/2506.20354) | 2025 | MVPFormer-M | same | kappa / F1 | 0.61 / 0.59 (0.15 false positives/h) |

The text gives Brant-2's kappa as 0.05 while Table 1 gives 0.06. The authors treat kappa above 0.53 as expert-level agreement. For the older long-term SWEC-ETHZ set (18 patients), the [database page](http://ieeg-swez.ethz.ch/) states that Laelaps (local binary patterns + hyperdimensional computing, patient-specific) had no false alarms over 1,357 h of testing. I did not read the DATE 2019 paper's sensitivity numbers.

### DARPA RAM free recall: within-patient memory classifier
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Ezzyat et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC5802791/) | 2018 | Penalized logistic regression on spectral power (3–180 Hz) during word encoding | Trained on ≥3 record-only sessions, tested on NoStim lists of closed-loop sessions; 25 patients, 29 stimulation targets | AUC (recalled vs forgotten) | 0.61 (mean) |

Whether all 25 patients are in the public RAM release is *not verified*.

---

## How to read these numbers

- **Almost everything is per-patient.** Electrode count, type and placement differ for every patient (BCI IV ds4: 62/48/64 channels with no anatomy; Brain Treebank: 106–246 contacts). Most decoders are trained one patient at a time. Cross-patient numbers are much lower: on Neuroprobe the best entry drops from 0.695 within-session to 0.608 cross-subject, and the linear Laplacian baseline from 0.660 to 0.539 ([leaderboard](https://neuroprobe.dev)).
- **Check which electrodes were used.** BrainBERT's numbers come from the 10 best electrodes per task, picked by a linear probe. PopT aggregates up to 90 electrodes. MVPFormer picks 32 channels by variance and kurtosis. Neuroprobe uses all electrodes, capped at 120 per subject. The same model can look very different under these choices.
- **The split decides the number.** Kaggle seizure contests split by time. The winning entries lost about 8% (AES 2014) and 6.7% (Melbourne 2016) from private leaderboard to later held-out data, and the Melbourne rank-5 entry lost 20.7% ([Brinkmann](https://pmc.ncbi.nlm.nih.gov/articles/PMC5022671/), [Kuhlmann](https://academic.oup.com/brain/article/141/9/2619/5063014)). Random-window splits over the same recording leak autocorrelated signal and inflate scores.
- **Test-set reuse.** BCI IV ds4 and Brain Treebank have released test labels. Papers that tune on them (FingerFlex tuned on subject 1's "validation set", which is the test set) report optimistic numbers.
- **Metrics with the same name are not the same.** "Pearson r" for finger flexion is averaged over 4 fingers in the competition and often over 5 later. Speech "PCC" is measured on spectrograms and is driven mostly by speech vs silence ([Verwoert et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC9307753/)). MCD, STOI and WER measure different things. Kaggle detection scores average two AUCs.
- **Class definitions drift on Mayo/FNUSA.** The dataset has 4 classes. Papers merge them differently (3 classes, pathological vs rest, or "seizure detection") and resample to 1 kHz, so numbers do not line up.
- **Imbalance.** Seizure data are 90–95% interictal. AUC hides false-alarm rates, which is why SWEC papers report false positives per hour and kappa against an expert.
- **Leaderboards are living documents.** Neuroprobe numbers were read on 2026-10-11 and may change; they also differ slightly from the paper's tables.
- **"via" numbers are second-hand.** They were read in the citing paper's table and may come from a re-implementation (e.g. the Miller finger-flexion baselines in CORTEG, retrained or transcribed from Sun et al. 2025 and Tao et al. 2025).
