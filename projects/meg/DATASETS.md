# MEG Datasets and Benchmark Results

This page has full specifications for the main public MEG datasets and the published results on each. Every number links to the paper, dataset page or leaderboard where it was read. If a source did not report a value, the cell says "not reported". If I could not read the value in a source myself, it is left out or marked *not verified*. Checked on 2026-10-11.

## Overview

| Dataset | Subjects | Channels | Sampling rate | Task / classes | Size on disk | License |
|---|---|---|---|---|---|---|
| MNE sample / somato / Brainstorm auditory | 1 each | 306 + 60 EEG / Neuromag / CTF 275 | not reported | Audio-visual evoked; median-nerve ERD/ERS; auditory oddball | 0.2 / 0.3 / 2.5 GB (OpenNeuro BIDS copies) | CC0 (OpenNeuro copies); Brainstorm terms for the fetcher |
| Cam-CAN (Stage 2) | 656 (18–87 y) | 306 (VectorView) | 1 kHz | Rest, sensorimotor task, passive audio-visual | not reported | Data request; terms *not verified* |
| HCP MEG (S1200) | 95 | 248 magnetometers + 23 reference | 2034.5 Hz | Rest, motor, working memory, story/math | not reported | HCP Open Access Data Use Terms |
| OMEGA (v3.1.1) | 644 (444 controls, 200 patients) | 275 axial gradiometers + 26 reference | 2400 Hz | Resting state only | not reported | Controlled access + DUA |
| Wakeman & Henson faces | 19 | 306 MEG + 70 EEG | 1100 Hz | Famous / unfamiliar / scrambled faces | 90.1 GB (ds000117) | CC0 |
| MOUS (Schoffelen 2019) | 204 | 275 axial gradiometers | 1200 Hz | Sentences vs word lists, read or heard (Dutch) | not reported | Donders DUA (RU-DI-HD-1.0) |
| MEG-MASC (Gwilliams 2023) | 27 | 208 axial gradiometers | 1 kHz | Story listening + word lists (English) | not reported | CC0 |
| Armeni 2022 | 3 (~10 h each) | 275 axial gradiometers | 1200 Hz | Audiobook listening (Sherlock Holmes) | not reported | Donders DUA (RU-DI-HD-1.0) |
| LibriBrain (2025) | 1 (52.3 h in released splits) | 306 (MEGIN Triux Neo) | 250 Hz (from 1 kHz) | Speech detection, 39 phonemes, words | ~50 GB serialized | CC BY-NC 4.0 (HF card) |
| THINGS-MEG | 4 | 275 (CTF) | 1200 Hz | 22,448 unique object images, 1,854 concepts | 255.2 GB (ds004212) | CC0 |
| DECOMEG (Brain2Qwerty v1 data) | 35 (20 MEG, 20 EEG, 5 both) | 306 MEG / 64 EEG | 1 kHz | Typing memorized Spanish sentences | ~262 GB | CC BY-NC 4.0 |
| BCI Competition IV ds3 | 2 | 10 (motor area) | 400 Hz (from 625 Hz) | 4 wrist-movement directions | not reported | Free; citation required |
| Emotion videos (ds007640) | 23 | not reported | 1024 Hz | 4 valence × arousal quadrants, 40 clips | 95.4 GB | CC0 |

Sources are in each dataset's block below.

---

## Part 1: Dataset specifications

### MNE-Python example datasets (sample, somato, Brainstorm auditory)

These are teaching datasets, not benchmarks. All facts from the [MNE datasets page](https://mne.tools/stable/documentation/datasets.html) unless noted.

| Field | Value |
|---|---|
| Year & paper | Bundled with MNE-Python; no single data paper |
| Subjects | 1 per dataset |
| System & sensors | **sample**: Neuromag VectorView at MGH/HMS/MIT Martinos Center. **somato**: Elekta, 306 MEG channels (ds003104 `meg.json`). **Brainstorm auditory**: CTF 275, native `.ds` |
| Other modalities | sample: 60-channel EEG cap recorded simultaneously; 1.5 T Siemens Sonata MPRAGE MRI |
| Task / labels | sample: checkerboards left/right visual field and tones left/right ear every 750 ms, occasional smiley face with button press (event codes LA, RA, LV, RV, smiley, button). somato: somatosensory stimulation with ERS/ERD. Brainstorm auditory: auditory oddball (see the Brainstorm tutorial) |
| Size / format | BIDS copies on OpenNeuro: [ds000248](https://openneuro.org/datasets/ds000248) (sample, 0.2 GB), [ds003104](https://openneuro.org/datasets/ds003104) (somato, 0.3 GB), [ds000246](https://openneuro.org/datasets/ds000246) (Brainstorm AEF sample, 2.5 GB); all CC0 |
| Access & license | Fetched by `mne.datasets.*`; Brainstorm fetchers require accepting the Brainstorm license terms |
| Known issues | MNE says the sample data "should not be used to evaluate the performance of the MEG or MRI system employed" |

MNE also ships `ucl_opm_auditory`, an auditory evoked-field recording on an **OPM** (optically pumped magnetometer) setup from FIL/UCL, plus phantom recordings for KIT, 4D/BTi and Kernel OPM systems.

### Cam-CAN (Cambridge Centre for Ageing and Neuroscience)
| Field | Value |
|---|---|
| Year & paper | 2017; Taylor et al., *NeuroImage* ([PMC5182075](https://pmc.ncbi.nlm.nih.gov/articles/PMC5182075)) |
| Subjects | Stage 2 repository: 656 healthy adults aged 18–87, population-based; target 50 men + 50 women per decade, but only 56 tested in the 18–27 decade. 623 have all three MEG sessions processed to artefact rejection |
| System & sensors | Elekta Neuromag VectorView, 102 magnetometers + 204 planar gradiometers; light shielded room; 4 HPI coils for continuous head tracking |
| Channels | 306 MEG + bipolar VEOG, HEOG, ECG |
| Sampling rate | 1 kHz, high-pass 0.03 Hz |
| Other modalities | Structural MRI (T1, T2, DWI, MT), fMRI (rest, movie, sensorimotor), 14 cognitive tasks |
| Task / labels | Resting state (eyes closed, at least 8 min 40 s); sensorimotor task (audio-visual stimuli + button press); passive audio-visual task (120 trials: 60 checkerboards, 60 tones) |
| Duration | not reported per subject beyond the rest minimum |
| Size / format | Size not reported; raw and MaxFiltered FIF, preprocessed SPM12 |
| Access & license | SSH/SFTP access after request; instructions at mrc-cbu.cam.ac.uk/datasets/camcan (per the paper). Current data-use terms *not verified* |
| Standard protocol | None official. Brain-age papers use repeated k-fold cross-validation (see Part 2) |
| Known issues | Youngest decade under-recruited; MEG count (623 complete) differs from MRI count (614 complete), so multimodal studies use a smaller intersection (Engemann et al. used 536 complete cases) |

### HCP MEG (Human Connectome Project, Young Adult)
| Field | Value |
|---|---|
| Year & paper | 2013 design paper; Larson-Prior et al., *NeuroImage* ([PMC3784249](https://pmc.ncbi.nlm.nih.gov/articles/PMC3784249)); final release S1200 ([announcement](https://humanconnectome.org/study/hcp-young-adult/article/announcing-1200-subject-data-release)) |
| Subjects | 95 subjects in S1200 with some resting and/or task MEG; healthy young adults; design called for 100 subjects as 50 same-sex monozygotic twin pairs |
| System & sensors | 4D Neuroimaging MAGNES 3600 at Saint Louis University; magnetometers ([S1200 Reference Manual](https://www.humanconnectome.org/storage/app/media/documentation/s1200/HCP_S1200_Release_Reference_Manual.pdf)) |
| Channels | 248 magnetometers + 23 reference channels |
| Sampling rate | 2034.5 Hz ([S1200 Reference Manual](https://www.humanconnectome.org/storage/app/media/documentation/s1200/HCP_S1200_Release_Reference_Manual.pdf)); the 2013 paper planned 2 kHz |
| Other modalities | Full HCP protocol: structural MRI, fMRI on the same tasks, dMRI, behaviour, genetics |
| Task / labels | Resting state; motor (hand/foot movements, block design); working memory (0-back/2-back with tools and faces); language (30 s stories vs arithmetic) |
| Duration | not reported here |
| Size / format | Size not reported; original 4D Magnes format |
| Access & license | ConnectomeDB after registering and accepting the HCP Open Access Data Use Terms |
| Standard protocol | None for decoding |
| Known issues | Daily 5-min empty-room recordings are provided (S1200 Reference Manual); 4D system differs from the CTF/Elekta systems used by most other sets, so channel layouts do not transfer |

### OMEGA (Open MEG Archive)
| Field | Value |
|---|---|
| Year & paper | 2016; Niso et al., *NeuroImage* ([doi](https://doi.org/10.1016/j.neuroimage.2015.04.028)); current release 3.1.1, 2025-07-17 ([site](https://omega.bic.mni.mcgill.ca)) |
| Subjects | 644: 444 healthy controls + 200 patients (Parkinson's disease, ADHD, chronic pain) |
| System & sensors | CTF MEG at the Montreal Neurological Institute: 275 axial gradiometers + 26 reference sensors, 3rd-order gradient compensation ([Niso et al. 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6461064)) |
| Channels | 275 MEG + bipolar ECG, VEOG, HEOG |
| Sampling rate | 2400 Hz, anti-aliasing low-pass 600 Hz |
| Other modalities | Defaced T1 MRI for most participants (MEG-MRI co-registration for 480 in v3.1.1); demographics and questionnaires |
| Task / labels | Resting state only (eyes open, fixation); patient group labels |
| Duration | About 1,800 resting recordings, over 150 h in total |
| Size / format | Size not reported; BIDS (MEG-BIDS) |
| Access & license | Controlled access: register, provide ethics approval, accept the OMEGA DUA (no re-identification, no redistribution). A 5-subject sample is open on OpenNeuro as [ds000247](https://openneuro.org/datasets/ds000247) (CC0) |
| Standard protocol | None |
| Known issues | Earlier releases were smaller (the 2019 Brainstorm paper used 5 subjects); co-registration still incomplete for some subjects |

### Wakeman & Henson multimodal faces
| Field | Value |
|---|---|
| Year & paper | 2015; Wakeman & Henson, *Sci. Data* 2:150001 ([PMC4412149](https://pmc.ncbi.nlm.nih.gov/articles/PMC4412149)) |
| Subjects | 19 healthy: 8 female, 11 male; age 23–37 |
| System & sensors | Elekta Neuromag VectorView 306 |
| Channels | 306 MEG + 70 EEG (Easycap, extended 10–10) + VEOG, HEOG, ECG |
| Sampling rate | 1100 Hz, low-pass 350 Hz, no high-pass |
| Other modalities | Simultaneous EEG; fMRI (same paradigm, other session); T1, multi-echo FLASH, DWI |
| Task / labels | Famous, unfamiliar and scrambled faces (150 famous + 150 unfamiliar photos in the M/EEG set, plus scrambled versions), each shown twice (immediate or delayed repeat); symmetry judgement. About 880–889 epochs per participant |
| Duration | Six 7.5-min runs |
| Size / format | 90.1 GB on OpenNeuro [ds000117](https://openneuro.org/datasets/ds000117) (v2.0.0); FIF (MaxFiltered versions also provided) |
| Access & license | CC0 on OpenNeuro; authors ask for acknowledgement and citation |
| Standard protocol | None official. 16 participants formed the training set of the Kaggle DecMeg2014 face-vs-scrambled cross-subject competition (per the paper) |
| Known issues | EOG/ECG channels mislabeled in the FIF files (EEG061 = HEOG, EEG062 = VEOG, EEG063 = ECG); fixed 34 ms trigger-to-screen delay; famous images f076 and f117 are the same identity |

### MOUS (Mother Of Unification Studies)
| Field | Value |
|---|---|
| Year & paper | 2019; Schoffelen et al., *Sci. Data* ([PMC6472396](https://pmc.ncbi.nlm.nih.gov/articles/PMC6472396)) |
| Subjects | 204 native Dutch speakers (100 male), mean age 22 (18–33), right-handed, healthy. Each did the task either visually (sub-V*) or auditorily (sub-A*) |
| System & sensors | CTF 275-channel axial gradiometer system; continuous head localization |
| Channels | 275 MEG + horizontal/vertical EOG + ECG; audio recorded on an ADC channel in the auditory group |
| Sampling rate | 1200 Hz (anti-aliasing low-pass 300 Hz) |
| Other modalities | Task and resting fMRI, structural MRI, DWI, all on the same subjects (MR spectroscopy acquired but not released) |
| Task / labels | 120 sentences + 120 scrambled word lists in MEG (half of sentences with relative clauses); word-level events with timing; 5 min resting state; 20% of trials followed by a yes/no question |
| Duration | Auditory group used by Défossez et al.: 96 subjects, 80.9 h in total ([Défossez et al.](https://ar5iv.labs.arxiv.org/html/2208.12266)); reading group: 99 subjects, 106 h ([LibriBrain Table 1](https://arxiv.org/html/2506.02098v1)) |
| Size / format | Size not reported; BIDS with CTF `.ds` |
| Access & license | [Donders Repository](http://hdl.handle.net/11633/di.dccn.DSC_3011020.09_236) after registration and a Data Use Agreement for identifiable human data |
| Standard protocol | None official; Défossez et al. split segments ~70/20/10 with no sentence shared across splits |
| Known issues | No empty-room recording; a few records have issues listed in the paper's Usage Notes; subject numbering has gaps from dropouts |

### MEG-MASC
| Field | Value |
|---|---|
| Year & paper | 2023; Gwilliams et al., *Sci. Data* 10:862 ([PMC10695966](https://pmc.ncbi.nlm.nih.gov/articles/PMC10695966)) |
| Subjects | 27 English speakers (15 female), age 24.8 ± 6.4, right-handed, healthy |
| System & sensors | KIT (Kanazawa Institute of Technology) axial-gradiometer MEG at NYU Abu Dhabi |
| Channels | 208 |
| Sampling rate | 1000 Hz, online band-pass 0.01–200 Hz |
| Other modalities | T1 MRI (defaced; four subjects get a scaled FreeSurfer average instead); laser-scanned head shape |
| Task / labels | Four MASC stories (synthetic text-to-speech, three voices, varying rate) mixed with random word lists; word and phoneme onsets; comprehension questions |
| Duration | Two identical ~1 h sessions per subject (~2 h), except five subjects (S3, S12, S16, S20, S21) with one session; 56.2 h in total in Défossez et al. |
| Size / format | Size not reported; BIDS (MNE-BIDS), raw |
| Access & license | [OSF](https://osf.io/ag3kj), CC0 |
| Standard protocol | None official; Défossez et al. assign each segment to one split across repetitions |
| Known issues | Stories are repeated across sessions, so splits must be by segment, not by recording; speech is synthetic; five subjects did only one session |

### Armeni et al. 2022 (10 h within-participant)
| Field | Value |
|---|---|
| Year & paper | 2022; Armeni, Güçlü, van Gerven, Schoffelen, *Sci. Data* ([PMC9177538](https://pmc.ncbi.nlm.nih.gov/articles/PMC9177538)) |
| Subjects | 3 healthy native English speakers (1 female), ages 35, 30, 28; UK, US and South African English |
| System & sensors | CTF 275-channel axial gradiometers; individual head casts |
| Channels | 275 MEG + eye-tracker channels (x, y, pupil) stored in the MEG files |
| Sampling rate | 1200 Hz |
| Other modalities | EyeLink 1000 eye tracking at 1000 Hz; structural MRI; session-specific empty-room recordings |
| Task / labels | Listening to *The Adventures of Sherlock Holmes* (10 stories, one per session); forced-aligned word onsets; comprehension questions after each run |
| Duration | 10 sessions per participant, nearly 10 h each |
| Size / format | Size not reported; BIDS-style folders with CTF `.ds` |
| Access & license | Donders repository under the RU-DI-HD-1.0 DUA (the DUA page link on the Donders site is dead) |
| Standard protocol | None official |
| Known issues | Only 3 subjects; three accents may add between-subject variability |

### LibriBrain
| Field | Value |
|---|---|
| Year & paper | 2025; Özdogan, Landau, Elvers et al. ([arXiv 2506.02098](https://arxiv.org/html/2506.02098v1)); competition: Landau et al. ([arXiv 2506.10165](https://arxiv.org/html/2506.10165v1)) |
| Subjects | 1 healthy right-handed male, native English speaker |
| System & sensors | MEGIN Triux Neo at OHBA, Oxford |
| Channels | 306 |
| Sampling rate | Recorded at 1 kHz, released at 250 Hz |
| Other modalities | not reported (audio, transcripts, alignments provided) |
| Task / labels | Listening to 7 Sherlock Holmes audiobooks (LibriVox); speech/non-speech, word and phoneme (39 ARPAbet) alignments |
| Duration | 95 sessions recorded (~34 ± 15 min each); released splits: train 51.57 h (91 sessions), validation 0.36 h, test 0.38 h; total 52.32 h, plus private competition holdout sessions |
| Size / format | ~50 GB serialized ([competition paper](https://arxiv.org/html/2506.10165v1)); one HDF5 + one TSV event file per session; BIDS/FIF raw release planned |
| Access & license | `pip install pnpl` or [Hugging Face](https://huggingface.co/datasets/pnpl/LibriBrain) (card license CC BY-NC 4.0); a one-session sample is on OpenNeuro as [ds008101](https://openneuro.org/datasets/ds008101) (CC0) |
| Standard protocol | Fixed train/val/test sessions; competition holdout with hidden labels; metric F1-macro |
| Known issues | Single subject, single author and narrator; minimal preprocessing (head-motion correction, filtering, downsampling); the competition holdout had a different amplitude distribution from val/test ([MEGConformer §7.4](https://arxiv.org/html/2512.01443v2)) |

**2026 extension.** The [2026 PNPL competition](https://neural-processing-lab.github.io/2025-libribrain-competition/editions/2026/tracks/) uses *LibriBrain100*: over 100 h across 33 subjects (the deep subject subj0 plus 32 subjects with ~10–40 min of labelled audiobook data each). The task is 50-word classification scored by top-10 balanced accuracy; final ranking is on holdout data with new stimuli. Submissions close 2026-10-15, so there are no final results yet.

### THINGS-MEG
| Field | Value |
|---|---|
| Year & paper | 2023; Hebart et al., *eLife* 12:e82580 ([PMC10038662](https://pmc.ncbi.nlm.nih.gov/articles/PMC10038662)) |
| Subjects | 4 healthy volunteers (2 female, 2 male), mean age 23.25 |
| System & sensors | CTF 275 MEG, radial 1st-order gradiometer SQUID channels, 3rd-order gradient balancing; individual head casts |
| Channels | 275 (three dysfunctional, so 272 recorded; the authors also exclude MRO11, leaving 271; NICE and ATM report 271 channels, Benchetrit et al. 272) |
| Sampling rate | 1200 Hz |
| Other modalities | EyeLink 1000 Plus eye tracking; T1 MRI; fMRI and behaviour in other THINGS-data cohorts |
| Task / labels | 22,248 images from 1,854 THINGS concepts (12 exemplars each) shown once, plus 200 test images repeated 12× (22,448 unique images in total); 500 ms on, 1000 ± 200 ms fixation; oddball catch images |
| Duration | 12 main sessions × 10 runs (~5 min); 27,048 trials per participant |
| Size / format | 255.2 GB on OpenNeuro [ds004212](https://openneuro.org/datasets/ds004212) (v3.0.0, BIDS); preprocessed/epoched MNE data on [Figshare](https://doi.org/10.25452/figshare.plus.c.6161151) |
| Access & license | CC0 |
| Standard protocol | Original: 22,248 training images, 200 test images × 12 repeats. Zero-shot protocol (NICE onward): drop the 200 test concepts from training (1,654 training concepts), 200-way retrieval with the 12 test repeats averaged |
| Known issues | Head position measured only before and after each run (head casts used); brief (<200 ms) signal dropouts in one run each for M1 and M2; only 4 subjects, so cross-subject results are noisy |

### DECOMEG (Brain2Qwerty v1 data)
| Field | Value |
|---|---|
| Year & paper | 2025 paper; Lévy et al., "Brain-to-Text Decoding: A Non-invasive Approach via Typing" ([arXiv 2502.17480](https://arxiv.org/html/2502.17480)); data released on [Hugging Face](https://huggingface.co/datasets/bcbl190626/SpanishBCBL) in 2026 (linked from the [official repo](https://github.com/facebookresearch/brain2qwerty)) |
| Subjects | 35 healthy native Spanish speakers (23% men, 77% women), age 31.6 ± 5.2, right-handed skilled typists; 20 EEG + 20 MEG (5 did both); one excluded from MEG for a metallic component |
| System & sensors | MEGIN (Elekta Neuromag): 102 magnetometers + 204 planar gradiometers; custom non-magnetic keyboard |
| Channels | 306 MEG; EEG: 64 (61 EEG + 3 ocular, BrainVision actiCAP) |
| Sampling rate | 1 kHz; MEG online high-pass 0.1 Hz, low-pass 330 Hz |
| Other modalities | Separate EEG cohort; keystroke logs; tapping localizer |
| Task / labels | Read a 5–8-word Spanish sentence (RSVP), wait, type it from memory without feedback; labels are keystrokes (characters) |
| Duration | MEG 0.93 ± 0.01 h per subject (21.5 h total, ~5.1K sentences, ~193K characters); EEG 0.88 h per subject (17.7 h) |
| Size / format | ~262 GB; raw FIF (MEG), BrainVision (EEG), behavioural `.mat` |
| Access & license | CC BY-NC 4.0 |
| Standard protocol | Unique sentences split 80/10/10 (train/val/test) by clustering similar sentences; models trained across subjects; metric: character error rate (CER) |
| Known issues | 128 unique sentences per session, repeated, so vocabulary is small; typos in 3.9% of keystrokes; the v2 dataset (EnglishBCBL: 9 subjects × 10 h, 22,000 sentences) is under embargo per the repo |

### BCI Competition IV, data set 3 (directionally modulated MEG)
| Field | Value |
|---|---|
| Year & paper | Competition description ([desc_3.pdf](https://www.bbci.de/competition/iv/desc_3.pdf)); review: Tangermann et al. 2012 ([PMC3396284](https://pmc.ncbi.nlm.nih.gov/articles/PMC3396284)); underlying study Waldert et al., *J. Neurosci.* 2008 |
| Subjects | 2 healthy, right-handed |
| System & sensors | MEG at the University of Tübingen MEG Center; sensor type not stated in the description |
| Channels | 10 MEG channels over motor areas (about a quarter of the original study's channels) |
| Sampling rate | Recorded at 625 Hz; provided band-passed 0.5–100 Hz and resampled to 400 Hz |
| Other modalities | none |
| Task / labels | Centre-out joystick movement with the right wrist to one of 4 targets (self-chosen); labels 1–4 |
| Duration | Trials cut from −0.4 to +0.6 s around movement onset; 160 labelled trials per subject (40 per class); test sets of 74 (S1) and 73 (S2) trials ([Hajipour Sardouie & Shamsollahi](https://pmc.ncbi.nlm.nih.gov/articles/PMC3317063)) |
| Size / format | Size not reported; MATLAB `.mat` |
| Access & license | Free at bbci.de after agreeing to credit the recording group and cite the paper in the description (Waldert et al. 2008) ([terms](https://www.bbci.de/competition/iv/)) |
| Standard protocol | Train on the labelled set, predict the test set; metric: accuracy (chance 25%) |
| Known issues | Very small test sets; S2 is much harder than S1 for every entry |

### MEG emotion dataset (OpenNeuro ds007640)
| Field | Value |
|---|---|
| Year & paper | 2026; Yoo, Kim, Choi, Kim, Kim ([OpenNeuro ds007640](https://openneuro.org/datasets/ds007640)); paper citation listed as "TBD" in `dataset_description.json` |
| Subjects | 23 MEG participants; plus an online survey of 500 participants rating the stimuli |
| System & sensors / channels | not reported in the README or `meg.json` |
| Sampling rate | 1024 Hz (from `meg.json`; 60 Hz line frequency) |
| Task / labels | 40 validated video clips in 4 sessions: high/low arousal × high/low valence; SAM valence/arousal ratings, PrEmo discrete emotions, highlight-scene selection |
| Size / format | 95.4 GB; BIDS FIF |
| Access & license | CC0 |
| Standard protocol / known issues | none published yet |

**Other public MEG sets, in brief** (OpenNeuro, all CC0):
- *Le Petit Prince* (French), Pallier 2025: [ds007523](https://openneuro.org/datasets/ds007523) listening, 58 subjects, 477.6 GB; [ds007524](https://openneuro.org/datasets/ds007524) reading, 50 subjects, 320.6 GB. LibriBrain's Table 1 listed the d'Ascoli et al. versions as not public; these releases appeared later.
- [MEG-SCANS](https://openneuro.org/datasets/ds006468): speech (audiobooks, OLSA sentences), 24 subjects.
- [NOD-MEG](https://openneuro.org/datasets/ds005810): ImageNet images, 31 subjects.
- [ForrestGump-MEG](https://openneuro.org/datasets/ds003633): movie watching, 11 subjects.
- Clinical: [ds003568](https://openneuro.org/datasets/ds003568) mood induction in adolescents with and without major depression (51 subjects); [ds004998](https://openneuro.org/datasets/ds004998) Parkinson's disease with DBS (20 subjects).
- MEG-BCI imagery (Rathee et al. 2021): 17 participants, Elekta Triux 306, hand/feet imagery + subtraction + word generation, as described by [GLCNet](https://pmc.ncbi.nlm.nih.gov/articles/PMC11973346).
- **Epilepsy:** I found no public MEG epilepsy dataset with a citable spec page in this pass. None of the OpenNeuro MEG dataset titles mention epilepsy.

---

## Part 2: Results

Within each table, rows use the same protocol and metric unless a row is marked otherwise. A number tagged "via X" was read in paper X's comparison table, not in the original paper.

### MOUS and MEG-MASC: speech perception, 3 s segment retrieval (Défossez protocol)

Models are trained on all subjects of a dataset (with a subject layer) and tested on held-out segments from the same subjects. Candidates are all test segments: 1,363 for Gwilliams (MEG-MASC) and 1,270 for Schoffelen (MOUS). Chance top-10 is under 1%.

| Paper | Year | Method | Protocol | Metric | Gwilliams (MEG-MASC) | Schoffelen (MOUS) |
|---|---|---|---|---|---|---|
| [Défossez et al.](https://ar5iv.labs.arxiv.org/html/2208.12266) | 2023 | Random model | as above | Top-10 | 0.7 ± 0.1% | 0.8 ± 0.1% |
| [Défossez et al.](https://ar5iv.labs.arxiv.org/html/2208.12266) | 2023 | Base: CNN regressing Mel spectrogram | as above | Top-10 | 12.4 ± 1.2% | 20.6 ± 1.8% |
| [Défossez et al.](https://ar5iv.labs.arxiv.org/html/2208.12266) | 2023 | + contrastive (CLIP) loss | as above | Top-10 | 55.1 ± 0.7% | 55.1 ± 0.9% |
| [Défossez et al.](https://ar5iv.labs.arxiv.org/html/2208.12266) | 2023 | + Deep Mel target | as above | Top-10 | 64.4 ± 0.8% | 61.2 ± 0.6% |
| [Défossez et al.](https://www.nature.com/articles/s42256-023-00714-5) | 2023 | + wav2vec 2.0 target (full model) | as above | Top-10 | **70.7 ± 0.1%** | **67.5 ± 0.4%** |
| [Défossez et al.](https://ar5iv.labs.arxiv.org/html/2208.12266) | 2023 | Full model | as above | Top-1 | 41.3 ± 0.1% | 36.8 ± 0.4% |

The ablation rows come from the arXiv version (Table 2, Table A.1). The *Nature Machine Intelligence* text gives the same full-model 70.7% / 41.3%. ± is SD over 3 seeds. For comparison, the same model on EEG reaches 25.7% (Brennan, 190 candidates) and 17.7% (Broderick, 1,842 candidates) top-10.

**Not directly comparable:**

| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Interpretable MEG decoding of perceived speech](https://arxiv.org/html/2608.01481v1) | 2026 | Interpretable branch decoder (0.49M params) | MEG-MASC; test = last 7 pieces of *The Black Willow*, **1,005** candidates; ocular/cardiac components removed; 6 seeds | Top-1 / Top-10 | 39.8% / 70.4% |

The authors say it cannot be compared directly with Défossez et al., whose test segments are aligned to word onsets and whose preprocessing does not remove ocular or cardiac components.

### DECOMEG (Brain2Qwerty v1): typing decoding, held-out sentences, subjects seen in training, CER (lower is better)
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Lévy et al. (Brain2Qwerty)](https://arxiv.org/html/2502.17480) | 2025 | Conv + Transformer + character LM | **MEG**, 20 subjects, mean over subjects | CER | 32 ± 0.6% (best subject 19 ± 1.1%, worst 45 ± 1.2%) |
| [Lévy et al. (Brain2Qwerty)](https://arxiv.org/html/2502.17480) | 2025 | Same model | **EEG**, 20 subjects | CER | 67 ± 1.5% (best 61 ± 2.0%, worst 71 ± 2.3%) |

The paper says Brain2Qwerty improves CER 2.25-fold over EEGNet on MEG and 1.14-fold on EEG; the baseline values are only shown in figures.

Brain2Qwerty v2 ([arXiv 2608.18114](https://arxiv.org/html/2608.18114v1), 2026) re-ran encoders on this data **without a language model**: synchronous encoder CER 0.39 ± 0.02, asynchronous (CTC) encoder 0.59 ± 0.02. These are not comparable with the 32% above, which includes the LM.

### EnglishBCBL (Brain2Qwerty v2, data under embargo): 9 subjects × 10 h, held-out sentences
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Brain2Qwerty v2](https://arxiv.org/html/2608.18114v1) | 2026 | Synchronous / asynchronous encoder, no LM | MEG, mean over 9 subjects | CER | 0.23 ± 0.03 / 0.25 ± 0.03 |
| [Brain2Qwerty v2](https://arxiv.org/html/2608.18114v1) | 2026 | Encoder alone (greedy CTC) | same | CER / WER | 0.28 ± 0.03 / 0.55 ± 0.04 |
| [Brain2Qwerty v2](https://arxiv.org/html/2608.18114v1) | 2026 | Full pipeline (encoder + MEG tokens + fine-tuned LLM) | same | CER / WER | 0.31 ± 0.03 / **0.39 ± 0.04** |

The LLM lowers WER but raises CER, because wrong outputs are fluent but different sentences.

### LibriBrain 2025 PNPL competition: holdout split, F1-macro (higher is better)

Reference and naive baselines from the [competition proposal (Table 2)](https://arxiv.org/html/2506.10165v1): speech detection 68.04% (reference) / 45.30% (majority class); phoneme classification 60.39% (reference, phonemes averaged over 100 samples) / 0.47% (majority class). Prizes required beating these references.

Scores below were read from the public [EvalAI leaderboard](https://eval.ai/web/challenges/challenge-page/2504/leaderboard) (split "Competition Holdout"). The **official placings** come from the [organisers' archive page](https://neural-processing-lab.github.io/2025-libribrain-competition/editions/2025/leaderboard/) and do *not* follow the EvalAI order. The rules say final rankings use independent holdout data and verified (code-reviewed) submissions. I could not tell from these pages whether the EvalAI numbers are the leaderboard subset or the final-ranking subset, so treat the scores as leaderboard values.

**Speech detection, Standard track (LibriBrain data only)**
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| Parameter Team, [EvalAI](https://eval.ai/web/challenges/challenge-page/2504/leaderboard) | 2025 | "MEGNet" (submission name); **official winner** | Standard, holdout | F1-macro | 91.66% |
| SHINE, [EvalAI](https://eval.ai/web/challenges/challenge-page/2504/leaderboard) | 2025 | not described; placed 2nd in the *Extended* track | Standard, holdout | F1-macro | 91.55% |
| alvi, [EvalAI](https://eval.ai/web/challenges/challenge-page/2504/leaderboard) | 2025 | "conv-v3-v4"; **official 3rd** | Standard, holdout | F1-macro | 91.00% |
| TheLimbicLad, [EvalAI](https://eval.ai/web/challenges/challenge-page/2504/leaderboard) | 2025 | "NeuralNet"; **official 2nd** | Standard, holdout | F1-macro | 90.59% |
| [neural2speech (MEGConformer)](https://arxiv.org/html/2512.01443v2) | 2025 | Compact Conformer, 2.5 s windows, smoothing | Standard, holdout | F1-macro | 88.90% (matches EvalAI) |

**Speech detection, Extended track (any training data)**
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| Sherlock Holmes, [EvalAI](https://eval.ai/web/challenges/challenge-page/2504/leaderboard) | 2025 | not described; **official winner** | Extended, holdout | F1-macro | 96.20% |
| SHINE, [EvalAI](https://eval.ai/web/challenges/challenge-page/2504/leaderboard) | 2025 | not described; **official 2nd** | Extended, holdout | F1-macro | 91.84% |

**Phoneme classification, Standard track** (39 classes, averaged windows)
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| Null-1, [EvalAI](https://eval.ai/web/challenges/challenge-page/2504/leaderboard) | 2025 | not described; not among official placings | Standard, holdout | F1-macro | 73.82% |
| labubuyes / Hachimi, [EvalAI](https://eval.ai/web/challenges/challenge-page/2504/leaderboard) | 2025 | not described; not among official placings | Standard, holdout | F1-macro | 73.30% (identical) |
| I_love_silksong, [EvalAI](https://eval.ai/web/challenges/challenge-page/2504/leaderboard) | 2025 | "brain_network(best)" | Standard, holdout | F1-macro | 72.36% |
| BrainWatson, [EvalAI](https://eval.ai/web/challenges/challenge-page/2504/leaderboard) | 2025 | not described; **official 2nd** | Standard, holdout | F1-macro | 68.41% |
| [neural2speech (MEGConformer)](https://arxiv.org/html/2512.01443v2) | 2025 | Conformer + instance norm + ensembling; **official winner** | Standard, holdout | F1-macro | 65.8% (EvalAI 65.83%) |
| sigint, [EvalAI](https://eval.ai/web/challenges/challenge-page/2504/leaderboard) | 2025 | not described; **official 3rd** | Standard, holdout | F1-macro | 63.98% |

**Phoneme classification, Extended track:** top EvalAI entry NaMeiLuDuo 76.18%; the only official placing listed is an honourable mention (I_love_silksong).

### LibriBrain: dataset-paper baselines (standard *test* split, not the holdout). Not comparable with the competition tables
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Özdogan et al. (LibriBrain)](https://arxiv.org/html/2506.02098v1) | 2025 | SEANet-style CNN vs random baseline | Speech detection, 10 seeds | F1 / balanced accuracy | 0.8989 vs 0.7848 / 0.7082 vs 0.4990 |
| [Özdogan et al. (LibriBrain)](https://arxiv.org/html/2506.02098v1) | 2025 | Same CNN, no averaging, unweighted loss | Phoneme (39), single phoneme windows | Macro-F1 / balanced accuracy | 0.0253 (random 0.0258) / 0.0399 (random 0.0259) |

### Armeni 2022 vs LibriBrain: word classification, 250 most frequent words, within-subject
| Paper | Year | Method | Protocol | Metric | Armeni | LibriBrain |
|---|---|---|---|---|---|---|
| Jayalath et al., via [LibriBrain Table 5](https://arxiv.org/html/2506.02098v1) | 2025 | Word-onset windows → transformer → T5 embeddings, SigLIP-style loss | 250-word vocabulary; chance 10/250 = 4% | Top-10 balanced accuracy | 32.61 ± 0.19% | 36.21 ± 0.31% |

### THINGS-MEG: 200-way zero-shot image retrieval, within-subject, 12 test repeats averaged (NICE protocol)
| Paper | Year | Method | Protocol | Metric | Top-1 | Top-5 |
|---|---|---|---|---|---|---|
| [Song et al. (NICE)](https://arxiv.org/html/2308.13234) | 2023 | Contrastive EEG/MEG–CLIP encoder | 200 test concepts held out of training | Retrieval accuracy | 12.8% | 36.0% |
| [Song et al. (NICE-GA)](https://arxiv.org/html/2308.13234) | 2023 | + graph-attention spatial module | same | Retrieval accuracy | 14.3% | 42.3% |
| UBP (Wu et al.), via [CORTIVA Table II](https://arxiv.org/html/2608.01355v1) | 2025 | Uncertainty-aware blur prior | same | Retrieval accuracy | 26.7% | 55.2% |
| ViEEG (Liu et al.), via [RPA Table 7](https://arxiv.org/html/2609.31698v2) | 2026* | Hierarchical visual representation | same | Retrieval accuracy | 25.5% | 63.2% |
| NeuroBridge (Zhang et al.), via [CORTIVA Table II](https://arxiv.org/html/2608.01355v1) | 2026* | — | same | Retrieval accuracy | 32.2% | 60.8% |
| BrainHIVE (Zheng et al.), via [RPA Table 7](https://arxiv.org/html/2609.31698v2) | 2026* | — | same | Retrieval accuracy | 33.9% | 60.9% |
| [CORTIVA](https://arxiv.org/html/2608.01355v1) | 2026 | Score fusion of three visual teachers, 6 seeds | same | Retrieval accuracy | 42.4% | 73.6% |
| Blur (Liu et al.), via [RPA Table 7](https://arxiv.org/html/2609.31698v2) | 2026* | — | same | Retrieval accuracy | 44.0% | 72.0% |
| Shallow Alignment (Du et al.), via [RPA Table 7](https://arxiv.org/html/2609.31698v2) | 2026* | — | same | Retrieval accuracy | 48.0% | 74.4% |
| [RPA](https://arxiv.org/html/2609.31698v2) | 2026 | Residual patch-token adapter | same | Retrieval accuracy | **65.2 ± 1.0%** | **85.7 ± 0.8%** |

\*Year as cited by RPA. NICE's own 200-way *classification* (concept templates instead of the stimulus images) is lower: 10.1% / 28.4%. Per-subject spread is large: in CORTIVA, subject 1 gets 20.6% top-1 and subject 2 gets 65.6%. Chance is 0.5% top-1 / 2.5% top-5.

### THINGS-MEG: Benchetrit et al. protocol. Not directly comparable with the table above
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Benchetrit et al.](https://arxiv.org/html/2310.19812) | 2023 | Ridge regression → VGG-19 latents | "Small" test set: 200 images, test categories removed from training, predictions averaged over 12 repeats, −0.5 to 1.0 s window | Top-5 | 11.5% |
| [Benchetrit et al.](https://arxiv.org/html/2310.19812) | 2023 | Deep ConvNet (Défossez brain module) → VGG-19 / CLIP-Vision / DINOv2 | same | Top-5 | 70.33% / 68.66% / 68.00% |
| [Benchetrit et al.](https://arxiv.org/html/2310.19812) | 2023 | Ridge → VGG-19 vs ConvNet → VGG-19 | "Large" test set: 2,400 images (12 per category) | Top-5 | 0.67% vs 12.29% |

Chance is 2.5% (small) and 0.21% (large). Benchetrit et al. report top-5 and median rank, not top-1, and use a different window. Whether they train one model per subject is *not verified*.

### BCI Competition IV ds3: official test sets (74 + 73 trials), 4-class accuracy, chance 25%
| Paper | Year | Method | Protocol | Metric | Mean | S1 | S2 |
|---|---|---|---|---|---|---|---|
| [Hajipour Sardouie & Shamsollahi](https://pmc.ncbi.nlm.nih.gov/articles/PMC3317063) (competition 1st) | 2012 | Statistical + spectral + wavelet features, GA selection, SVM + LDA vote | as above | Accuracy | 46.9% | 59.5% | 34.3% |
| Jing Li et al., [competition results](https://www.bbci.de/competition/iv/results/) (2nd) | — | Low-pass 0.5–8 Hz, FFT + PCA, Fisher discriminant | as above | Accuracy | 25.1% | 31.1% | 19.2% |
| Nasim Montazeri, [competition results](https://www.bbci.de/competition/iv/results/) (3rd) | — | Statistical/wavelet features, PCA + GA, linear SVM | as above | Accuracy | 23.9% | 16.2% | 31.5% |
| Jinjia Wang, [competition results](https://www.bbci.de/competition/iv/results/) (4th) | — | Same pipeline as 2nd | as above | Accuracy | 20.4% | 23.0% | 17.8% |

Year left blank for rows read only on the results page, which carries no date. The data providers report about 67% with low-frequency features on the full channel set of their original study (as quoted by [Hajipour Sardouie & Shamsollahi](https://pmc.ncbi.nlm.nih.gov/articles/PMC3317063)), which is not comparable.

**Later re-evaluation:** [GLCNet](https://pmc.ncbi.nlm.nih.gov/articles/PMC11973346) (2025, Table 6) describes the same 160-trial training sets and 74/73-trial test sets but uses its own two-stage training. Its 4-class accuracies: FBCSP 26.7%, FBCNet 28.9%, Shallow ConvNet 45.5%, Deep ConvNet 51.1%, EEGNet 53.4%, MEGNet 55.7%, GLCNet 59.9%. These are re-implementations, so treat the baselines as GLCNet's numbers, not the original authors'.

### Cam-CAN: age prediction (brain age), mean absolute error in years (lower is better). The two papers use different samples and CV, so they are not directly comparable
| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Engemann et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC7308092) | 2020 | Dummy (mean age) | 536 subjects with all modalities; 10-fold CV × 10 repeats | MAE | ~15.5 y |
| [Engemann et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC7308092) | 2020 | MEG sensor-space features, stacked | same | MAE | ~12 y |
| [Engemann et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC7308092) | 2020 | MEG source power / source connectivity | same | MAE | 7.40 / 7.58 y |
| [Engemann et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC7308092) | 2020 | MEG full (power + connectivity), stacked ridge → random forest | same | MAE | 6.75 y |
| [Engemann et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC7308092) | 2020 | Anatomical MRI only / MRI + fMRI + MEG | same | MAE | ~6 y / ~4.7 y |
| [Stier et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC11873822) | 2025 | Dummy (mean age) | Resting MEG, n = 350; PLSR; 10-fold CV × 50 repeats | MAE | 16.78 y |
| [Stier et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC11873822) | 2025 | Best conventional feature (alpha centre of gravity) / all conventional features (LASSO, nested CV) | same | MAE | 11.93 / 9.82 y |
| [Stier et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC11873822) | 2025 | Temporal autocorrelation, lag 11 / all lags (LASSO, nested CV) | same | MAE | 10.34 / 8.71 y |

"~" marks values the paper gives as approximate ("around 12 years", "about 6 years", "about 4.7 years").

**No results sourced** for HCP MEG, OMEGA, Wakeman & Henson (the Kaggle DecMeg2014 leaderboard needs a login), MOUS beyond Défossez et al., or the emotion set.

---

## How to read these numbers

- **Candidate-set size sets the scale.** Top-10 out of 1,363 segments (Défossez) and top-10 out of 1,005 segments (2026 interpretable decoder) are different tasks with different chance levels. THINGS-MEG 200-way top-1 has 0.5% chance; Benchetrit's "large" set has 2,400 candidates. Only compare rows with the same candidate set.
- **"Cross-subject" often means pooled training, not unseen people.** Défossez et al. and Brain2Qwerty train one model on all subjects but test on held-out *segments or sentences* from the same subjects. THINGS-MEG within-subject results train and test on one person. Leave-one-subject-out results (in RPA's Table 8, not reproduced here) are much lower.
- **Averaging repetitions inflates single-trial ability.** THINGS-MEG test images are averaged over 12 repeats; LibriBrain phoneme classification averages 100 samples. With no averaging, the LibriBrain paper's phoneme macro-F1 is at chance (0.0253 vs 0.0258).
- **Language models change the metric.** Brain2Qwerty v1's 32% CER includes a character n-gram LM; v2's LLM lowers WER (0.55 → 0.39) but raises CER (0.28 → 0.31). Encoder-only CERs are a separate column.
- **Leaderboard ≠ final ranking.** In the 2025 PNPL competition, the public EvalAI order differs from the official winners (e.g. phoneme Standard: 73.8% on EvalAI vs the official winner's 65.8%). The organisers ranked on independent holdout data and verified code. The holdout also had a different amplitude distribution from val/test.
- **Artifacts can carry the label.** Eye movements and heartbeats track stimulus structure. The 2026 MEG-MASC study removes ocular/cardiac components and calls this out as a shortcut risk; THINGS-MEG and Armeni ship eye-tracking channels you can use to check for it.
- **Sensor types and layouts differ.** CTF 275 (axial gradiometers), Elekta/MEGIN 306 (102 magnetometers + 204 planar gradiometers), KIT 208, 4D 248 magnetometers and OPM arrays do not share channel layouts. Pooling datasets needs a spatial remapping (e.g. Défossez's spatial-attention layer) or source-space features.
- **Brain-age MAE depends on the age range and sample.** Chance MAE is ~15.5 y (Engemann, 536 subjects) vs 16.78 y (Stier, 350 subjects). Compare improvements over each paper's own dummy model, not raw MAE across papers.
- **"via" numbers are second-hand.** They were checked in the citing paper's table (CORTIVA, RPA, LibriBrain), not in the original, and may be that paper's re-run.
