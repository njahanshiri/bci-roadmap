# Intracortical (Spikes / LFP) Datasets and Benchmark Results

This page gives specifications for the main public intracortical datasets (Utah arrays, Neuropixels and similar probes) and the published results on each. Every number links to the paper, leaderboard or official page where I read it. If a source did not report a value, the cell says "not reported". If I could not check a value in a source myself, I left it out or marked it *not verified*. Leaderboard numbers were read on 2026-10-11; open leaderboards keep changing.

## Overview

| Dataset | Species / subjects | Probe & area | Channels / units | Released signal | Task / labels | Size | License |
|---|---|---|---|---|---|---|---|
| NLB MC_Maze (+ S/M/L) | Macaque, 1 (Jenkins) | 2 × 96-ch Utah, M1 + PMd | 182 sorted units (main); 142–162 (scaled) | Sorted spike times | Delayed maze reaching, 108 conditions (27 scaled), hand velocity | 0.69 GB (main) | CC BY 4.0 |
| NLB MC_RTT | Macaque, 1 (Indy) | 96-ch Utah, M1 | 130 units | Sorted spike times | Self-paced random-target reaching | 0.05 GB | CC BY 4.0 |
| NLB Area2_Bump | Macaque, 1 (Han) | 96-ch Utah, area 2 (S1) | 65 units | Sorted spike times | Center-out reaching with bumps | 1.8 GB | CC BY 4.0 |
| NLB DMFC_RSG | Macaque, 1 (Haydn) | 3 Plexon probes, DMFC | 54 units | Sorted spike times | Ready-Set-Go timing | 0.02 GB | CC BY 4.0 |
| O'Doherty / Sabes reaching | Macaque, 2 (Indy, Loco) | 96-ch Utah M1 (+ 96-ch S1 in some sessions) | 96 or 192 ch, sorted units + "hash" | Threshold crossings sorted into units, waveforms | Self-paced reaching on a grid | 24.0 GB | CC BY 4.0 |
| Churchland maze (DANDI 000070) | Macaque, 2 | 2 × 96-ch Utah, M1 + PMd | not verified | not verified | Reaching | 53.3 GB | CC BY 4.0 |
| Brain-to-Text '24 (Willett 2023) | Human, 1 (T12, ALS) | 4 × 64-electrode arrays: 2 in area 6v, 2 in area 44 | 128 electrodes in 6v used for decoding | Threshold crossings + spike band power, binned | Attempted speech → text | 80.4 GB (all files) | CC0 |
| Brain-to-Text '25 (Card 2024) | Human, 1 (T15, ALS) | 4 × 64-electrode arrays, left precentral gyrus | 256 electrodes, 512 features | Threshold crossings + spike band power, 20 ms bins | Attempted speech → text | 11.6 GB | CC0 |
| Willett 2021 handwriting | Human, 1 (T5, SCI) | 2 × 96-electrode arrays, hand knob of precentral gyrus | 192 electrodes | not verified | Attempted handwriting → characters | 1.41 GB | CC0 |
| FALCON (M1, M2, H1, H2, B1) | 2 macaques (M1), 1 macaque (M2), humans (H1, H2), 1 zebra finch (B1) | FMAs, Utah arrays, Neuropixels 1.0 | 64–192 ch (see block) | Unsorted threshold crossings | EMG, finger kinematics, 7-DoF arm, handwriting, song | 0.1–15.9 GB per task | CC BY 4.0 |
| Allen Visual Coding – Neuropixels | Mouse, 58 (32 + 26 across 2 DANDI sets) | Neuropixels; 6 cortical + 2 thalamic visual regions | 374/383 ch per probe | Kilosort2 units + LFP (2.5 kHz) | Passive visual stimuli | 477.6 + 375.0 GB | CC BY 4.0 on DANDI, plus Allen terms of use |
| IBL Brain-wide Map | Mouse, 139 (12 labs) | 699 Neuropixels insertions, 279 areas | 621,733 units (75,708 well-isolated) | Sorted spikes, raw, behavior | Visual decision task (wheel) | 49.7 TB (DANDI) | CC BY 4.0 |
| Steinmetz 2019 | Mouse, 10 | Neuropixels, 42 regions | ~30,000 neurons | Sorted spikes (LFP separate) | Visual 2-choice discrimination | 8.86 GB | CC BY 4.0 |
| CRCNS (hc-*, pvc-*) | Rat, macaque, cat, mouse | Tetrodes, silicon probes, Utah | varies | varies | varies | varies | CRCNS terms (no redistribution) |

Sources are in each dataset's block below.

---

## Part 1: Dataset specifications

### Neural Latents Benchmark '21 (NLB): shared protocol
| Field | Value |
|---|---|
| Year & paper | 2021; Pei et al., NeurIPS Datasets & Benchmarks ([arXiv HTML](https://arxiv.org/html/2109.04463)); site [neurallatents.github.io](https://neurallatents.github.io/) |
| What it tests | Latent variable models of spiking population activity, not decoders as such |
| Released signal | Spike-sorted unit spike times; spike sorting is treated as a separate problem |
| Format / access | NWB on DANDI, CC BY 4.0: MC_Maze [000128](https://dandiarchive.org/dandiset/000128), MC_Maze-L [000138](https://dandiarchive.org/dandiset/000138), -M [000139](https://dandiarchive.org/dandiset/000139), -S [000140](https://dandiarchive.org/dandiset/000140), MC_RTT [000129](https://dandiarchive.org/dandiset/000129), Area2_Bump [000127](https://dandiarchive.org/dandiset/000127), DMFC_RSG [000130](https://dandiarchive.org/dandiset/000130) |
| Standard protocol | 25% of units are **held out**. For test trials only held-in units are released; held-out units and a 200 ms future window are kept on EvalAI. Users submit firing-rate predictions in 5 ms bins (a 20 ms phase also exists). Train/val/test splits are fixed |
| Metrics | **co-bps** (primary: Poisson log-likelihood of held-out units, in bits/spike over a mean-rate baseline); **vel R²** (ridge regression from submitted train rates to hand velocity, scored on test); **psth R²** (match of trial-averaged rates to PSTHs); **fp-bps** (forward prediction of the next 200 ms); **tp corr** for DMFC_RSG (correlation of neural speed with produced interval) |
| Leaderboard | [EvalAI challenge 1256](https://eval.ai/web/challenges/challenge-page/1256/leaderboard), test phase. Both the validation and test phases closed on 2026-01-31; the leaderboard is still viewable |
| Known issues | Absolute co-bps cannot be compared across datasets (the paper says so). vel R² uses a linear decoder by design, so it measures the rates, not the best possible decoder. Some sessions overlap with larger public releases, but those releases exclude the NLB sessions |

### NLB MC_Maze, MC_Maze-L / -M / -S
| Field | Value |
|---|---|
| Year & paper | Data: Churchland, Kaufman et al. (Shenoy lab); benchmark: [Pei et al. 2021](https://arxiv.org/html/2109.04463) |
| Species & subjects | 1 rhesus macaque (Jenkins) |
| Implant & areas | Two 96-electrode Utah arrays, M1 and PMd |
| Units | MC_Maze: 137 held-in + 45 held-out = 182 units. Scaled: S 107 + 35, M 114 + 38, L 122 + 40 |
| Sampling / released | 30 kHz recording, spike-sorted offline; units below 0.1 Hz or with high cross-correlation removed; NWB spike times |
| Behavior | Hand, cursor and eye position; hand velocity computed offline. Maze: 108 conditions; scaled sets 27 conditions |
| Sessions & trials | MC_Maze (2009-09-25): 2,295 train + 574 test trials (2,869 total). S / M / L: 100 / 250 / 500 train trials + 100 test, each a separate session |
| Size | MC_Maze 0.69 GB; L 0.15 GB; M 0.08 GB; S 0.03 GB ([DANDI](https://dandiarchive.org/dandiset/000128)) |
| Standard protocol | NLB (above). Scaled sets test data efficiency |
| Known issues | Highly stereotyped, near-autonomous dynamics: the paper calls it a "neuroscience MNIST", useful for validation but easy to saturate. A hand-position recording error was corrected by subtracting 8 mm from y |

### NLB MC_RTT
| Field | Value |
|---|---|
| Year & paper | Data: O'Doherty et al. (Sabes lab); benchmark: [Pei et al. 2021](https://arxiv.org/html/2109.04463) |
| Species & subjects | 1 macaque (Indy), session 2017-07-02 |
| Implant & areas | One 96-electrode Utah array, M1 |
| Units | 98 held-in + 32 held-out = 130 |
| Sampling / released | TDT RZ2 at 24.4 kHz, 500–5000 Hz band-pass, spikes sorted online; "hash" units removed |
| Behavior | Fingertip position at 250 Hz (Polhemus), low-passed at 10 Hz; velocity computed offline |
| Duration | 10.8 min train (1,080 "trials") + 3.62 min test (271); continuous data cut into 600 ms snippets |
| Size | 0.05 GB ([DANDI 000129](https://dandiarchive.org/dandiset/000129)) |
| Known issues | No trial structure, so PSTH metrics are not computed; unpredictable target onsets make forward prediction hard |

### NLB Area2_Bump
| Field | Value |
|---|---|
| Year & paper | Data: Chowdhury et al. (Miller lab); benchmark: [Pei et al. 2021](https://arxiv.org/html/2109.04463) |
| Species & subjects | 1 macaque (Han), session 2017-12-07 |
| Implant & areas | One 96-electrode Utah array, area 2 of somatosensory cortex |
| Units | 49 held-in + 16 held-out = 65 |
| Sampling / released | Blackrock Cerebus at 30 kHz; threshold crossings sorted manually (Plexon Offline Sorter) |
| Behavior | Hand position, forces, muscle lengths/velocities and joint angles from Kinect marker tracking; 50% of trials have a 2 N bump |
| Trials | 364 train + 98 test, 16 conditions |
| Size | 1.8 GB ([DANDI 000127](https://dandiarchive.org/dandiset/000127)) |
| Known issues | Few units; input-driven activity after unexpected bumps |

### NLB DMFC_RSG
| Field | Value |
|---|---|
| Year & paper | Data: Sohn et al. (Jazayeri lab); benchmark: [Pei et al. 2021](https://arxiv.org/html/2109.04463) |
| Species & subjects | 1 macaque (Haydn), session 2016-12-11 |
| Implant & areas | 3 Plexon probes, dorsomedial frontal cortex |
| Units | 40 held-in + 14 held-out = 54 |
| Sampling / released | 30 kHz (CerePlex); single and multi-units sorted with Kilosort |
| Behavior | Task timing, condition and produced interval t_p (saccade or joystick); 40 conditions |
| Trials | 1,006 train + 283 test |
| Size | 0.02 GB ([DANDI 000130](https://dandiarchive.org/dandiset/000130)) |
| Known issues | Cognitive area with no moment-by-moment behavioral readout; only deep models beat spike smoothing in the paper |

### O'Doherty / Sabes self-paced reaching (Zenodo)
| Field | Value |
|---|---|
| Year & paper | 2017; O'Doherty, Cardoso, Makin, Sabes, Zenodo ([10.5281/zenodo.583331](https://zenodo.org/record/583331)) |
| Species & subjects | 2 macaques: Indy (37 sessions over ~10 months) and Loco (10 sessions over ~1 month) |
| Implant & areas | 96-channel Utah array in M1; some sessions also a 96-channel S1 array (192 channels) |
| Released signal | Threshold crossing times sorted into up to 5 units per channel (unit 1 is the unsorted "hash"), plus waveform snippets. Raw broadband data are in separate Zenodo records for some Indy sessions |
| Behavior | Fingertip x, y (and sometimes orientation) and target position at 250 Hz; cursor position |
| Size | ~20,000 reaches (Indy) + 6,500 (Loco); 47 `.mat` files, 24.0 GB |
| Format / license | MATLAB `.mat`; CC BY 4.0 |
| Standard protocol | None official. NLB MC_RTT is one Indy session with a fixed split; papers otherwise choose their own sessions and splits |
| Known issues | Number of sorted units per channel changes across sessions (2 or 4 sorted units); long span makes it a common testbed for cross-day drift, but splits are not standardized |

### Churchland / Kaufman maze data (DANDI 000070)
| Field | Value |
|---|---|
| Year & paper | 2012; Churchland et al., "Neural population dynamics during reaching" ([DANDI 000070](https://dandiarchive.org/dandiset/000070)) |
| Species & subjects | 2 rhesus macaques |
| Implant & areas | Two 96-channel Utah arrays (Blackrock), M1 and PMd |
| Sessions / size | 10 files, 53.3 GB |
| Format / license | NWB; CC BY 4.0 |
| Standard protocol | None; NLB MC_Maze sessions are excluded from this release |
| Known issues | Unit counts, sorting quality and trial counts per file *not verified* |

### Brain-to-Text '24 (Willett et al. 2023 speech data)
| Field | Value |
|---|---|
| Year & paper | 2023; Willett et al., *Nature* 620 ([PMC10468393](https://pmc.ncbi.nlm.nih.gov/articles/PMC10468393/)); benchmark summary: Willett et al. 2024 ([arXiv](https://arxiv.org/html/2412.17227)) |
| Species & subjects | 1 human (T12, ALS, BrainGate2) |
| Implant & areas | Four microelectrode arrays: two in area 6v (ventral premotor), two in area 44. Decoding uses the 6v arrays: "128-electrode Utah arrays in ventral motor cortex" per [LightBeam](https://arxiv.org/html/2603.14002) |
| Released signal | Multi-unit threshold crossings and spike band power, temporally binned (RNN emits phonemes every 80 ms) |
| Labels | Sentence text and phonemes; sentences from Switchboard |
| Sessions | 25 sessions over 4 months, 12,100 sentences ([LightBeam](https://arxiv.org/html/2603.14002), [Dryad](https://doi.org/10.5061/dryad.x69p8czpq)); the paper itself says 10,850 sentences |
| Size | 80.4 GB on Dryad in total; `competitionData.tar.gz` is 3.67 GB; the 5-gram LM alone is 38.2 GB |
| Format / license | MATLAB `.mat` (loadable with `scipy.io.loadmat`); CC0 |
| Standard protocol | Per day: **test** = last block (40 sentences); **competitionHoldOut** = first two blocks (80 sentences, transcripts redacted); **train** = the rest ([speechBCI README](https://github.com/fwillett/speechBCI)). Holdout = 1,200 sentences, scored as WER on [EvalAI challenge 2099](https://eval.ai/web/challenges/challenge-page/2099/leaderboard/4944) |
| Known issues | Within-day and across-day non-stationarity (the paper's "proximal test set" drops WER from 17.4% to 11.8%). The leaderboard is open indefinitely with no hidden final round, so heavy resubmission is possible. The baseline needs a 5-gram LM using ~320 GB RAM ([LightBeam](https://arxiv.org/html/2603.14002)) |

### Brain-to-Text '25 (Card et al. 2024)
| Field | Value |
|---|---|
| Year & paper | 2024; Card et al., *NEJM* ([PMC11328962](https://pmc.ncbi.nlm.nih.gov/articles/PMC11328962/)); code + data notes: [nejm-brain-to-text](https://github.com/Neuroprosthetics-Lab/nejm-brain-to-text) |
| Species & subjects | 1 human (T15, 45-year-old man with ALS) |
| Implant & areas | Four 64-electrode arrays in left ventral precentral gyrus (ventral 6v, area 4, 55b, dorsal 6v) |
| Channels / features | 256 electrodes → 512 features: threshold crossings at −4.5 RMS + spike band power per electrode |
| Sampling / released | 20 ms bins |
| Labels | Sentence and phoneme labels (none for the test split); corpora: Switchboard, OpenWebText2, 50-word set, frequent words, random word sequences; mostly vocalized, some silent attempts |
| Sessions | 10,948 sentences, 45 sessions over 20 months |
| Size / format | 11.6 GB on [Dryad](https://datadryad.org/stash/dataset/doi:10.5061/dryad.dncjsxm85); HDF5; CC0 |
| Standard protocol | 8,072 train / 1,426 val / 1,450 test trials; val+test = 67 blocks from 41 of 45 days ([LightBeam appendix](https://arxiv.org/html/2603.14002)). [Kaggle competition](https://www.kaggle.com/competitions/brain-to-text-25), 2025-07-07 to 2026-01-01, aggregate WER; public leaderboard = 33% of test, private = rest; 463 teams |
| Known issues | Single participant; speaking strategy per block intentionally not labeled; public/private split means public WER is optimistic |

### Willett et al. 2021 handwriting
| Field | Value |
|---|---|
| Year & paper | 2021; Willett et al., *Nature* ([PMC8163299](https://pmc.ncbi.nlm.nih.gov/articles/PMC8163299/)); code: [handwritingBCI](https://github.com/fwillett/handwritingBCI) |
| Species & subjects | 1 human (T5, hand paralysed from spinal cord injury) |
| Implant & areas | Two 96-electrode arrays in the hand area of motor cortex |
| Labels | Cued sentences, character-level; real-time decoder outputs included |
| Duration | 1,000 sentences (43,501 characters), 10.7 hours ([Dryad](https://doi.org/10.5061/dryad.wh70rxwmv)) |
| Size / license | 1.41 GB; CC0 |
| Format | Described in `readme.pdf` on Dryad; *not verified* |
| Standard protocol | Two splits: **HeldOutTrials** (single sentences held out uniformly) and **HeldOutBlocks** (later blocks held out; harder because of drift) |
| Known issues | Single participant; FALCON H2 reuses T5 handwriting sessions with its own split |

### FALCON (Few-shot Algorithms for COnsistent Neural decoding)
| Field | Value |
|---|---|
| Year & paper | 2024; Karpowicz et al., NeurIPS Datasets & Benchmarks ([PDF](https://proceedings.neurips.cc/paper_files/paper/2024/file/8c2e6bb15be1894b8fb4e0f9bcad1739-Paper-Datasets_and_Benchmarks_Track.pdf)); site [snel-repo.github.io/falcon](https://snel-repo.github.io/falcon/) |
| M1 | 2 macaques (M1-A, M1-B), Floating Microelectrode Arrays in M1; 64/96 ch; 16-muscle intramuscular EMG during reach-to-grasp (4 objects × 8 locations). M1-A: 4 held-in sessions over 5 days (53–61 min each) + 3 held-out over 21 days (1.1–2.2 min calibration). M1-B: 4 + 4 sessions over 7 + 7 days |
| M2 | 1 macaque, two 64-ch Utah arrays in precentral gyrus, 96 ch released; 2-D finger movements (index, middle-ring-small). 4 held-in sessions over 10 days + 4 held-out over 26 days |
| H1 | 1 human, Utah arrays in hand/arm motor cortex, 172 ch; open-loop 7-DoF arm velocity. 6 held-in sessions over 20 days + 7 held-out over 15 days |
| H2 | T5 (BrainGate2), two 96-ch Utah arrays, 192 ch, 30 kHz recorded, 20 ms bins; attempted handwriting of sentences. 21 held-in sessions over 287 days + 5 held-out over 176 days; 40% of trials reserved for evaluation; only 3 trials released per held-out session |
| B1 | 1 zebra finch, Neuropixels 1.0 in RA, 85 ch; song spectrograms. 3 held-in days + 3 held-out days |
| Released signal | Unsorted multi-unit threshold crossings + behavior |
| Size / format | NWB on DANDI, CC BY 4.0: M1-A [000941](https://dandiarchive.org/dandiset/000941) 0.31 GB, M1-B [001209](https://dandiarchive.org/dandiset/001209) 0.23 GB, M2 [000953](https://dandiarchive.org/dandiset/000953) 15.9 GB, H1 [000954](https://dandiarchive.org/dandiset/000954) 0.10 GB, H2 [000950](https://dandiarchive.org/dandiset/000950) 1.22 GB, B1 [001046](https://dandiarchive.org/dandiset/001046) 1.29 GB |
| Standard protocol | Decoders are Docker containers run on [EvalAI challenge 2319](https://eval.ai/web/challenges/challenge-page/2319/leaderboard); predictions must be causal and streamed time-step by time-step (per sentence for H2, per motif for B1). Scored separately on **held-in** and **held-out** (few-shot) sessions. Metrics: variance-weighted R² (M1, M2, H1), WER (H2), spectrogram MSE (B1). Method classes: oracle (OR), zero-shot (ZS), few-shot unsupervised (FSU), few-shot supervised (FSS), test-time adaptive (TTA) |
| Known issues | Private evaluation data; the paper notes the benchmark may reward models that exploit implicit trial structure. An "H3" split exists on EvalAI with no entries |

### Allen Brain Observatory Visual Coding – Neuropixels
| Field | Value |
|---|---|
| Year & paper | 2021; Siegle et al., *Nature* ([PMC10399640](https://pmc.ncbi.nlm.nih.gov/articles/PMC10399640/)); [AllenSDK docs](https://allensdk.readthedocs.io/en/latest/visual_coding_neuropixels.html) |
| Species & subjects | Mouse; 32 subjects in the Brain Observatory 1.1 set ([DANDI 000021](https://dandiarchive.org/dandiset/000021)) + 26 in the Functional Connectivity set ([DANDI 000022](https://dandiarchive.org/dandiset/000022)) |
| Probe & areas | Neuropixels probes (374 or 383 channels each); six cortical and two thalamic visual regions |
| Sampling / released | Spike band 30 kHz, LFP band 2.5 kHz. Released: Kilosort2 spike times, amplitudes, mean waveforms, quality metrics, LFP for channels in the brain |
| Stimuli | Gabors for receptive fields, flashes, then either the two-photon Brain Observatory stimulus set or a Functional Connectivity set with more repeats + dot motion |
| Duration | ~3 h per recording |
| Size / format | 477.6 GB + 375.0 GB on DANDI; NWB |
| License | DANDI lists CC BY 4.0; the description adds that Allen Institute terms of use apply |
| Standard protocol | None for decoding. AllenSDK hides units with presence_ratio < 0.95, isi_violations > 0.5 or amplitude_cutoff > 0.1 by default |
| Known issues | Probe drift ~40 µm per recording, so waveform-based quality metrics drift too; no single-unit vs multi-unit label |

### IBL Brain-wide Map
| Field | Value |
|---|---|
| Year & paper | 2025; International Brain Laboratory, *Nature* ([PMC12408349](https://pmc.ncbi.nlm.nih.gov/articles/PMC12408349/)) |
| Species & subjects | 139 mice (94 male, 45 female), 12 labs |
| Probe & areas | 699 Neuropixels insertions, 279 brain areas (left forebrain and midbrain, right hindbrain and cerebellum) |
| Units | 621,733 units; 75,708 well-isolated (~108 per probe) |
| Behavior | Visual decision task (wheel turn), block priors, choice, feedback, wheel, video |
| Sessions | 459 sessions after quality control (*unverified*: in the cited paper 459 may be a reaction-time sample size rather than a session count) |
| Size / format | 49.7 TB on [DANDI 000409](https://dandiarchive.org/dandiset/000409) (NWB, CC BY 4.0); also via the IBL ONE API ([instructions](https://int-brain-lab.github.io/iblenv/notebooks_external/data_release_brainwidemap.html)) |
| Standard protocol | None for ML benchmarking. The paper decodes per region and corrects R² against a null distribution |
| Known issues | Probe-placement variability across labs (see the IBL [reproducibility paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC12068871/)); most units fail strict isolation criteria |

### Steinmetz et al. 2019
| Field | Value |
|---|---|
| Year & paper | 2019; Steinmetz, Zatka-Haas, Carandini, Harris, *Nature* ([PMC6913580](https://pmc.ncbi.nlm.nih.gov/articles/PMC6913580/)) |
| Species & subjects | 10 mice, 39 sessions |
| Probe & areas | Neuropixels; ~30,000 neurons in 42 brain regions |
| Released | Sorted spikes + behavior (wheel, pupil, stimuli, choices); raw LFP and behavior videos in separate figshare records |
| Size / format | 8.86 GB ([figshare](https://doi.org/10.6084/m9.figshare.9598406)); ONE format, with an NWB copy |
| License | CC BY 4.0 |
| Standard protocol | None; widely used for teaching (e.g. choice decoding) |

### CRCNS (brief)
[CRCNS.org](https://crcns.org/data-sets) needs a free account to download. Unless a page says otherwise, data are for scientific use only and may not be redistributed ([terms](https://crcns.org/terms)).
- [hc-2](https://crcns.org/data-sets/hc/hc-2): multi-unit recordings from rat hippocampus during open-field foraging (Buzsáki lab).
- [hc-3](https://crcns.org/data-sets/hc/hc-3): single units from rat hippocampal and entorhinal regions across multiple behavioral tasks (Buzsáki lab).
- [hc-11](https://crcns.org/data-sets/hc/hc-11): CA1 recordings before, during and after novel spatial learning (Grosmark, Long, Buzsáki).
- [pvc-1](https://crcns.org/data-sets/vc/pvc-1): single- and multi-unit V1 recordings (Ringach lab).
- [pvc-8](https://crcns.org/data-sets/vc/pvc-8): multi-electrode recordings of anesthetized macaque V1 to natural images and gratings (Kohn).
- [pvc-11](https://crcns.org/data-sets/vc/pvc-11): Utah-array recordings of spontaneous and evoked activity in anesthetized macaque V1 (Smith, Kohn).

### DANDI as a hub
[DANDI](https://dandiarchive.org) hosts most of the sets above in NWB: NLB (000127–000140), FALCON (000941, 001209, 000950, 000953, 000954, 001046), Churchland maze (000070), Allen Neuropixels (000021, 000022) and the IBL Brain-wide Map (000409). Its API (`api.dandiarchive.org`) reports size, license and subject counts per dandiset; those are the values used above.

---

## Part 2: Results

Within each table, rows use the same protocol and metric unless a row is marked otherwise. A number tagged "via X" was read in X, not in the original paper. For leaderboards, "Year" is the submission year shown on the board; rows are a selection (baselines, named methods and the top entries), not the full board.

### NLB MC_Maze: EvalAI test phase, 5 ms bins
Source for every row: [EvalAI NLB leaderboard, MC_Maze 5 ms](https://eval.ai/web/challenges/challenge-page/1256/leaderboard/3188). Higher is better for all four metrics. "—" = not submitted.

| Paper/Team | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| Neural Latents (baseline) | 2021 | Spike smoothing | as above | co-bps / vel R² / psth R² / fp-bps | 0.2109 / 0.6238 / 0.1853 / — |
| Neural Latents (baseline) | 2021 | GPFA | as above | same | 0.1872 / 0.6399 / 0.5150 / — |
| Neural Latents (baseline) | 2021 | SLDS | as above | same | 0.2249 / 0.7947 / 0.5330 / −1.1579 |
| Neural Latents (baseline) | 2021 | NDT | as above | same | 0.3229 / 0.8862 / 0.5308 / 0.2206 |
| Neural Latents (baseline) | 2021 | AutoLFADS | as above | same | 0.3364 / 0.9097 / 0.6360 / 0.2349 |
| Churchland Lab | 2021 | MINT | as above | same | 0.3304 / 0.9121 / 0.7496 / 0.2076 |
| AE Studio | 2022 | AESMTE3 (ensemble) | as above | same | 0.3676 / 0.9114 / 0.6683 / 0.2589 |
| Hennequin Lab | 2022 | iLQR-VAE | as above | same | 0.3559 / 0.8840 / 0.6062 / 0.1480 |
| UW NeuroAI | 2022 | STNDT (ensemble) | as above | same | **0.3862** / 0.9095 / 0.6693 / **0.2686** |
| Makin Lab | 2022 | Neural RoBERTa | as above | same | 0.3551 / 0.8731 / 0.6780 / 0.2282 |
| SNEL | 2022 | SSLFADS | as above | same | 0.3748 / 0.9013 / 0.6366 / 0.2580 |
| Linderman Lab | 2022 | S5 | as above | same | 0.3823 / 0.9043 / 0.6431 / 0.2581 |
| Ctrl-TNDM | 2023 | BAND | as above | same | 0.3215 / **0.9362** / 0.6187 / 0.2241 |
| He Cui Lab, CIBR | 2023 | NDT-L | as above | same | 0.3536 / 0.8938 / 0.6314 / 0.2242 |
| fmODE | 2025 | DLFM | as above | same | 0.3779 / 0.9019 / 0.6525 / **0.2686** |

The NLB paper's own Table 1 gives slightly different MC_Maze baseline values (e.g. AutoLFADS 0.346 co-bps, 0.907 vel R²; NDT 0.329 / 0.897) ([Pei et al.](https://arxiv.org/html/2109.04463)); treat paper and leaderboard as separate runs.

### NLB MC_RTT (O'Doherty data): EvalAI test phase, 5 ms bins
Source: [EvalAI MC_RTT 5 ms](https://eval.ai/web/challenges/challenge-page/1256/leaderboard/3187). No psth R² for this dataset.

| Paper/Team | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| Neural Latents (baseline) | 2021 | Spike smoothing | as above | co-bps / vel R² / fp-bps | 0.1468 / 0.4142 / — |
| Neural Latents (baseline) | 2021 | GPFA | as above | same | 0.1548 / 0.5339 / — |
| Neural Latents (baseline) | 2021 | SLDS | as above | same | 0.1649 / 0.5206 / 0.0620 |
| Neural Latents (baseline) | 2021 | NDT | as above | same | 0.1749 / 0.5656 / 0.0970 |
| Neural Latents (baseline) | 2021 | AutoLFADS | as above | same | 0.1868 / 0.6167 / 0.1213 |
| Churchland Lab | 2021 | MINT (back-sorted PSTH mesh) | as above | same | 0.1676 / 0.5953 / 0.1012 |
| AE Studio | 2022 | AESMTE3 (ensemble) | as above | same | 0.2053 / 0.6334 / 0.1344 |
| UW NeuroAI | 2022 | STNDT (ensemble) | as above | same | 0.2065 / 0.6352 / 0.1260 |
| Makin Lab | 2022 | Neural RoBERTa + RNNf (ensemble) | as above | same | 0.2168 / 0.6489 / 0.1341 |
| Linderman Lab | 2022 | S5 | as above | same | **0.2296** / 0.6450 / 0.1271 |
| Churchland Lab | 2023 | MINT (AutoLFADS mesh) | as above | same | 0.2014 / 0.6559 / 0.1099 |
| Ctrl-TNDM | 2023 | BAND | as above | same | 0.1846 / **0.6705** / 0.1275 |
| YueAndyMax | 2025 | LangevinFlow | as above | same | 0.1900 / 0.4748 / 0.1300 |
| fmODE | 2025 | DLFM | as above | same | 0.2073 / 0.6663 / **0.1419** |

### NLB Area2_Bump: EvalAI test phase, 5 ms bins
Source: [EvalAI Area2_Bump 5 ms](https://eval.ai/web/challenges/challenge-page/1256/leaderboard/3186).

| Paper/Team | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| Neural Latents (baseline) | 2021 | Spike smoothing | as above | co-bps / vel R² / psth R² / fp-bps | 0.1544 / 0.5736 / 0.2084 / — |
| Neural Latents (baseline) | 2021 | GPFA | as above | same | 0.1680 / 0.5975 / 0.5289 / — |
| Neural Latents (baseline) | 2021 | SLDS | as above | same | 0.1960 / 0.7385 / 0.5740 / 0.0242 |
| Neural Latents (baseline) | 2021 | NDT | as above | same | 0.2623 / 0.8672 / 0.6619 / 0.1184 |
| Neural Latents (baseline) | 2021 | AutoLFADS | as above | same | 0.2569 / 0.8492 / 0.6318 / 0.1505 |
| Churchland Lab | 2021 | MINT | as above | same | 0.2735 / 0.8877 / **0.9135** / 0.1483 |
| AE Studio | 2022 | AESMTE3 (ensemble) | as above | same | 0.2860 / 0.8999 / 0.7109 / **0.1603** |
| Domenick Mifsud | 2022 | NDT-U | as above | same | 0.2861 / 0.8701 / 0.6871 / 0.1401 |
| UW NeuroAI | 2022 | STNDT (ensemble) | as above | same | 0.2904 / 0.8937 / 0.7303 / 0.1491 |
| Makin Lab | 2022 | Neural RoBERTa + RNNf (ensemble) | as above | same | **0.2931** / 0.8761 / 0.6613 / 0.1464 |
| Linderman Lab | 2022 | S5 | as above | same | 0.2901 / 0.8727 / 0.7258 / 0.1518 |
| Ctrl-TNDM | 2023 | BAND | as above | same | 0.2686 / 0.8950 / 0.6436 / 0.1424 |
| NNs | 2024 | FreLayerSSTNDT-18 | as above | same | 0.2870 / **0.9077** / 0.6739 / 0.1346 |
| YueAndyMax | 2025 | LangevinFlow | as above | same | 0.2772 / 0.8580 / 0.7567 / 0.1526 |
| fmODE | 2025 | DLFM | as above | same | 0.2844 / 0.8820 / 0.7199 / 0.1567 |

### NLB DMFC_RSG: EvalAI test phase, 5 ms bins
Source: [EvalAI DMFC_RSG 5 ms](https://eval.ai/web/challenges/challenge-page/1256/leaderboard/3185). tp corr is expected to be negative (faster neural speed, shorter produced interval).

| Paper/Team | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| Neural Latents (baseline) | 2021 | Spike smoothing | as above | co-bps / tp corr / psth R² / fp-bps | 0.1202 / −0.5139 / 0.2993 / — |
| Neural Latents (baseline) | 2021 | GPFA | as above | same | 0.1176 / −0.3763 / 0.2142 / — |
| Neural Latents (baseline) | 2021 | SLDS | as above | same | 0.1243 / −0.5412 / 0.3372 / −0.0418 |
| Neural Latents (baseline) | 2021 | NDT | as above | same | 0.1720 / −0.5624 / 0.4377 / 0.1404 |
| Neural Latents (baseline) | 2021 | AutoLFADS | as above | same | 0.1829 / −0.8248 / 0.6359 / 0.1844 |
| Churchland Lab | 2021 | MINT | as above | same | 0.1821 / −0.6929 / 0.7013 / 0.1650 |
| AE Studio | 2022 | AESMTE3 (ensemble) | as above | same | 0.1886 / −0.7601 / 0.6064 / 0.1828 |
| UW NeuroAI | 2022 | STNDT (ensemble) | as above | same | 0.1940 / −0.4857 / 0.6452 / 0.1910 |
| Linderman Lab | 2022 | S5 | as above | same | **0.2020** / −0.4269 / 0.4407 / 0.1841 |
| YueAndyMax | 2025 | LangevinFlow | as above | same | 0.1841 / −0.5466 / 0.6092 / 0.1689 |
| fmODE | 2025 | DLFM | as above | same | 0.1869 / −0.5377 / 0.6373 / **0.1993** |

### NLB MC_Maze scaling (S = 100, M = 250, L = 500 training trials): EvalAI test phase, 5 ms bins
Source: [EvalAI MC_Maze Scaling 5 ms](https://eval.ai/web/challenges/challenge-page/1256/leaderboard/3184).

| Paper/Team | Year | Method | Protocol | Metric | Result (100 / 250 / 500 trials) |
|---|---|---|---|---|---|
| Neural Latents (baseline) | 2021 | Spike smoothing | as above | co-bps; vel R² | 0.1914 / 0.1673 / 0.2245; 0.4646 / 0.5220 / 0.5772 |
| Neural Latents (baseline) | 2021 | GPFA | as above | same | 0.2140 / 0.1725 / 0.2385; 0.5138 / 0.5664 / 0.5765 |
| Neural Latents (baseline) | 2021 | SLDS | as above | same | 0.2491 / 0.2232 / 0.3031; 0.6324 / 0.7557 / 0.7954 |
| Neural Latents (baseline) | 2021 | NDT | as above | same | 0.2368 / 0.2412 / 0.3592; 0.6421 / 0.7206 / 0.8834 |
| Neural Latents (baseline) | 2021 | AutoLFADS | as above | same | 0.2854 / 0.3036 / 0.3740; 0.7982 / 0.8680 / 0.9178 |
| Churchland Lab | 2021 | MINT | as above | same | 0.3463 / 0.3331 / 0.3847; 0.8711 / 0.8958 / **0.9330** |
| AE Studio | 2022 | AESMTE3 (ensemble) | as above | same | 0.3555 / 0.3354 / 0.3938; 0.8669 / 0.9019 / 0.9252 |
| Domenick Mifsud | 2022 | NDT-U | as above | same | **0.3711** / **0.3358** / 0.3849; 0.8490 / **0.9026** / 0.9157 |
| Makin Lab | 2022 | Neural RoBERTa + RNNf (ensemble) | as above | same | 0.3541 / 0.3298 / **0.3981**; 0.8254 / 0.8762 / 0.9185 |
| He Cui Lab, CIBR | 2023 | TLNDT | as above | same | 0.3010 / 0.2733 / 0.3867; 0.8128 / 0.8591 / 0.9189 |

### NLB '21 paper, Table 2: co-smoothing (bits/spike ± s.e.m.). Authors' own runs; not directly comparable with the leaderboard rows
| Paper/Team | Year | Method | Protocol | Metric | MC_Maze / L / M / S / MC_RTT / Area2_Bump / DMFC_RSG |
|---|---|---|---|---|---|
| [Pei et al.](https://arxiv.org/html/2109.04463) | 2021 | Smoothing | NLB test | co-bps | 0.211 / 0.224 / 0.167 / 0.191 / 0.147 / 0.154 / 0.120 |
| [Pei et al.](https://arxiv.org/html/2109.04463) | 2021 | GPFA | NLB test | co-bps | 0.187 / 0.239 / 0.172 / 0.217 / 0.155 / 0.168 / 0.118 |
| [Pei et al.](https://arxiv.org/html/2109.04463) | 2021 | SLDS | NLB test | co-bps | 0.219 / 0.290 / 0.210 / 0.250 / 0.165 / 0.187 / 0.120 |
| [Pei et al.](https://arxiv.org/html/2109.04463) | 2021 | NDT | NLB test | co-bps | 0.329 / 0.362 / 0.259 / 0.251 / 0.160 / 0.267 / 0.162 |
| [Pei et al.](https://arxiv.org/html/2109.04463) | 2021 | AutoLFADS | NLB test | co-bps | 0.346 / 0.374 / 0.304 / 0.301 / 0.192 / 0.259 / 0.181 |

### Supervised velocity decoding on NLB MC_Maze and MC_RTT (O'Doherty, Indy). POYO protocol; not comparable with NLB vel R²
POYO trains decoders directly on velocity on the NLB evaluation segments; NLB vel R² instead fits a ridge decoder to submitted rates. All rows via [POYO Table 3](https://arxiv.org/html/2310.16046) (Azabou et al., NeurIPS 2023).

| Paper/Team | Year | Method | Protocol | Metric | NLB-Maze / NLB-RTT |
|---|---|---|---|---|---|
| Wiener filter, via [POYO](https://arxiv.org/html/2310.16046) | 2023 | Linear | from scratch | R² | 0.7485 / 0.5438 |
| GRU, via [POYO](https://arxiv.org/html/2310.16046) | 2023 | RNN | from scratch | R² | 0.8887 / 0.5951 |
| MLP, via [POYO](https://arxiv.org/html/2310.16046) | 2023 | MLP | from scratch | R² | 0.8794 / 0.6953 |
| AutoLFADS + linear, via [POYO](https://arxiv.org/html/2310.16046) | 2023 | LVM + linear | from scratch | R² | 0.9062 / 0.5931 |
| NDT + linear, via [POYO](https://arxiv.org/html/2310.16046) | 2023 | LVM + linear | from scratch | R² | 0.8929 / 0.5895 |
| NDT-Sup / EIT, via [POYO](https://arxiv.org/html/2310.16046) | 2023 | Supervised transformers | from scratch | R² | 0.8708 / 0.4621; 0.8791 / 0.4691 |
| [Azabou et al. (POYO)](https://arxiv.org/html/2310.16046) | 2023 | POYO single-session | from scratch | R² | 0.9470 / 0.6850 |
| [Azabou et al. (POYO)](https://arxiv.org/html/2310.16046) | 2023 | POYO-mp + unit ID / + fine-tune | pretrained on other monkeys | R² | 0.8962 / 0.7107; 0.9466 / 0.7318 |
| [Azabou et al. (POYO)](https://arxiv.org/html/2310.16046) | 2023 | POYO-1 + unit ID / + fine-tune | pretrained, multi-lab | R² | 0.9329 / 0.7294; **0.9482** / **0.7378** |

I found no standard protocol for the full O'Doherty Zenodo release (all 47 sessions); papers pick their own sessions and splits, so no table is given for it.

### Brain-to-Text '24: Willett et al. 2023, real-time and offline results (paper Table 1)
| Paper/Team | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Willett et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC10468393/) | 2023 | RNN + LM, online | 125,000-word vocab, vocal / silent | WER | 23.8% / 24.7% |
| [Willett et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC10468393/) | 2023 | RNN + LM, online | 50-word vocab, vocal / silent | WER | 9.1% / 11.2% |
| [Willett et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC10468393/) | 2023 | Offline, improved LM | 125k vocab | WER | 17.4% |
| [Willett et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC10468393/) | 2023 | Offline, improved LM + proximal test set | 125k vocab, **easier split** | WER | 11.8% |

Phoneme error rate online, before the LM: 19.7% (vocal), 20.9% (silent). The [speechBCI README](https://github.com/fwillett/speechBCI) reports 18.8% (RNN + 3-gram) and 13.7% (RNN + 5-gram + OPT) WER on the "test" partition, which is a different split from the competition holdout.

### Brain-to-Text '24: competition holdout (1,200 sentences), EvalAI, word error rate (lower is better)
Source for every row: [EvalAI B2T '24 leaderboard](https://eval.ai/web/challenges/challenge-page/2099/leaderboard/4944). The competition ended 2024-06-01; the board stays open, so rows after that date were not part of the official ranking.

| Paper/Team | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| NPTL Baseline | 2023 | RNN + 3-gram LM | as above | WER | 15.43% |
| NPTL Baseline | 2023 | RNN + 5-gram + OPT (original TF baseline) | as above | WER | 11.06% |
| NPTL PyTorch Baseline | 2024 | 5-gram + OPT-6.7B | as above | WER | 9.76% |
| Stanford Silent Speech (LISA) | 2024 | 10 × (RNN + 5-gram) + fine-tuned LLM merge | as above | WER | 8.93% |
| TeamCyber | 2024 | 2 RNNs + LLM selection | as above | WER | 8.26% |
| Linderman Lab | 2024 | Mamba (deep SSM) | as above | WER | 13.07% |
| DCoND-LIFT | 2024 | Diphone RNN + ensemble + fine-tuned GPT-3.5 merge | as above | WER | 5.77% |
| Linderman Lab | 2024 | Modified PyTorch RNN | as above | WER | 8.00% |
| BraIn-to-Text (BIT) | 2025 | Pretrained cross-species encoder, cascaded, ensemble | as above | WER | 5.10% |
| BraIn-to-Text (BIT) | 2025 | BIT end-to-end (audio LLM) + ensemble | as above | WER | 10.22% |
| Brainaudio | 2026 | LightBeam, unidirectional | as above | WER | 4.98% |
| CoDec | 2026 | not described | as above | WER | 4.57% |
| BBIC | 2026 | MOST-OPSD | as above | WER | 3.63% |
| LENS | 2026 | DeepEn | as above | WER | **3.34%** |

Official ranking at the 2024-06-01 deadline, from the organizers' [lessons-learned paper](https://arxiv.org/html/2412.17227): 1st DCoND-LIFT (5.8%; the [EvalAI overview](https://eval.ai/web/challenges/challenge-page/2099/overview) gives 5.81% at the deadline, and the 5.77% row above is a later 2024-08-01 entry), 2nd TeamCyber (8.26%), 3rd LISA (8.9%), 4th Linderman Lab (9.22%); baseline 9.7%. Feghhi et al. 2025 (time-masked Transformer): 5.68%, via [BIT](https://arxiv.org/html/2511.21740).

### Brain-to-Text '25: Kaggle private leaderboard (~67% of 1,450 test sentences), aggregate WER
Source: [Kaggle leaderboard](https://www.kaggle.com/competitions/brain-to-text-25/leaderboard) (scores shown as fractions there; converted to %).

| Paper/Team | Year | Method | Protocol | Metric | Result (private; public in brackets) |
|---|---|---|---|---|---|
| Infera-Neuro (1st) | 2025 | not described | Kaggle private | WER | **1.537%** (1.363%) |
| EPFL-INL (2nd) | 2025 | not described | Kaggle private | WER | 1.663% (1.393%) |
| BIT (3rd) | 2025 | not described on board | Kaggle private | WER | 1.773% (1.757%) |
| Tether Evo Engineers (4th) | 2025 | not described | Kaggle private | WER | 1.867% (1.666%) |
| Stanford-NPTL (unranked host entry) | 2025 | Causal RNN ensemble + 5-gram | Kaggle private | WER | 3.892% (3.090%) |
| Baseline (rank 40) | 2025 | Baseline, no 5-gram, no ensemble | Kaggle private | WER | 7.423% (7.181%) |

### Brain-to-Text '25: same test split, single-model results from LightBeam (mean ± SEM over 10 seeds; not directly comparable with ensembled Kaggle entries)
| Paper/Team | Year | Method | Protocol | Metric | Result (public / private) |
|---|---|---|---|---|---|
| Card et al. baseline GRU + WFST, via [LightBeam Table 1](https://arxiv.org/html/2603.14002) | 2024 | GRU + 5-gram WFST (single seed, original authors) | Kaggle split | WER | 6.67% / 7.00% |
| [LightBeam](https://arxiv.org/html/2603.14002) | 2026 | Baseline GRU + LightBeam decoder | Kaggle split | WER | 5.77 ± 0.12% / 6.47 ± 0.05% |
| [LightBeam](https://arxiv.org/html/2603.14002) | 2026 | Causal time-masked Transformer + WFST | Kaggle split | WER | 4.95 ± 0.26% / 4.81 ± 0.13% |
| [LightBeam](https://arxiv.org/html/2603.14002) | 2026 | Causal time-masked Transformer + LightBeam | Kaggle split | WER | 4.44 ± 0.21% / 4.59 ± 0.14% |

### Card et al. 2024: real-time accuracy (online, not the Kaggle split)
| Paper/Team | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Card et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC11328962/) | 2024 | RNN + LM | Day 1, 50-word vocab | Word accuracy | 99.6% |
| [Card et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC11328962/) | 2024 | RNN + LM | Day 2, 125,000-word vocab | Word accuracy | 90.2% |
| [Card et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC11328962/) | 2024 | RNN + LM | Sustained over 8.4 months | Word accuracy | 97.5% |

### Willett 2021 handwriting
| Paper/Team | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| [Willett et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC8163299/) | 2021 | RNN, online | Real-time copy typing, 90 characters/min | Raw accuracy | 94.1% (>99% offline with autocorrect) |
| [Willett (handwritingBCI repo)](https://github.com/fwillett/handwritingBCI) | 2021 | RNN raw / + bigram LM / + GPT-2 rescore | HeldOutTrials | CER; WER | 2.78 / 0.80 / 0.34%; 12.88 / 3.64 / 1.97% |
| [Willett (handwritingBCI repo)](https://github.com/fwillett/handwritingBCI) | 2021 | RNN raw / + bigram LM / + GPT-2 rescore | **HeldOutBlocks** (harder) | CER; WER | 5.32 / 1.69 / 0.90%; 23.28 / 6.10 / 3.21% |

### FALCON: paper baselines (Table 1), held-out / held-in, mean over sessions
All rows from [Karpowicz et al. 2024, Table 1](https://proceedings.neurips.cc/paper_files/paper/2024/file/8c2e6bb15be1894b8fb4e0f9bcad1739-Paper-Datasets_and_Benchmarks_Track.pdf). OR (oracle) rows use unreleased held-out data, so they are upper bounds, not competing methods.

| Paper/Team | Year | Method | Protocol | Metric | M1-A / M2 / H1 (held-out ± s.d. / held-in) |
|---|---|---|---|---|---|
| [Karpowicz et al.](https://proceedings.neurips.cc/paper_files/paper/2024/file/8c2e6bb15be1894b8fb4e0f9bcad1739-Paper-Datasets_and_Benchmarks_Track.pdf) | 2024 | Wiener filter | OR | R² | 0.53±0.04/0.54; 0.26±0.03/0.27; 0.21±0.04/0.24 |
| same | 2024 | RNN | OR | R² | 0.75±0.05/0.75; 0.56±0.04/0.59; 0.44±0.13/0.51 |
| same | 2024 | NDT2 Multi | OR | R² | 0.78±0.04/0.77; 0.58±0.04/0.62; 0.63±0.08/0.68 |
| same | 2024 | Wiener filter | ZS | R² | 0.34±0.06/0.46; 0.06±0.04/0.15; 0.16±0.03/0.20 |
| same | 2024 | RNN | ZS | R² | −0.60±0.45/0.52; −0.07±0.23/0.20; 0.09±0.18/0.31 |
| same | 2024 | CycleGAN + WF | FSU | R² | 0.43±0.04/0.61; 0.22±0.06/0.32; 0.12±0.06/0.15 |
| same | 2024 | NoMAD + WF | FSU | R² | 0.49±0.03/0.64; 0.20±0.10/0.35; 0.13±0.10/0.21 |
| same | 2024 | NDT2 Multi | FSS | R² | 0.59±0.07/0.77; 0.43±0.08/0.63; 0.52±0.04/0.62 |

| Paper/Team | Year | Method | Protocol | Metric | Result (held-out ± s.d. / held-in) |
|---|---|---|---|---|---|
| [Karpowicz et al.](https://proceedings.neurips.cc/paper_files/paper/2024/file/8c2e6bb15be1894b8fb4e0f9bcad1739-Paper-Datasets_and_Benchmarks_Track.pdf) | 2024 | RNN Multi / + LM | H2, OR | WER | 0.15±0.01/0.11; 0.03±0.00/0.02 |
| same | 2024 | RNN Multi / + LM | H2, ZS | WER | 0.53±0.02/0.11; 0.37±0.01/0.02 |
| same | 2024 | CORP | H2, TTA | WER | 0.11±0.01/0.02 |
| same | 2024 | EnSongdec | B1, OR / ZS | MSE ×10⁻⁴ | 7.47±0.99/5.61; 21.8±3.91/5.18 |

### FALCON: EvalAI leaderboard, held-out R² / held-in R² (higher is better)
Sources: [H1](https://eval.ai/web/challenges/challenge-page/2319/leaderboard/5747), [M1](https://eval.ai/web/challenges/challenge-page/2319/leaderboard/5750), [M2](https://eval.ai/web/challenges/challenge-page/2319/leaderboard/5751). Class labels (OR, ZS, FSU, FSS) are as written by submitters; oracle rows are upper bounds. The board's baseline values differ slightly from the paper's Table 1.

| Paper/Team | Year | Method | Protocol | Metric | H1 / M1 / M2 (held-out / held-in) |
|---|---|---|---|---|---|
| FALCON baseline | 2024 | Wiener filter | ZS | R² | 0.1641/0.1951; 0.3434/0.4614; 0.0600/0.1493 |
| FALCON baseline | 2024 | RNN | ZS | R² | 0.0893/0.3132; −0.5960/0.5195; −0.0667/0.2049 |
| FALCON baseline | 2024 | CycleGAN | FSU | R² | 0.1241/0.1535; 0.4273/0.6086; 0.2224/0.3151 |
| FALCON baseline | 2024 | NoMAD | FSU | R² | 0.1255/0.2108; 0.4929/0.6407; 0.1997/0.3540 |
| FALCON baseline | 2024 | NDT2 | FSS | R² | 0.5206/0.6240; 0.5850/0.7680; not on board |
| FALCON baseline | 2024 | NDT2 Multi | OR | R² | 0.6292/0.6763; 0.7762/0.7731; 0.5849/0.6216 |
| ndt3 | 2024 | NDT3 (H1, M2: from scratch; M1: 350M, 200 h pretrained) | FSS | R² | 0.5743/0.7014; 0.5842/0.7635; 0.4778/0.6176 |
| OMEN | 2025 | OMEN | FSS | R² | 0.5977/0.6776; 0.6088/0.7167; 0.4051/0.4897 |
| SPINT | 2025 | Gradient-free | FSU | R² | 0.2892/0.4678; 0.6636/0.7686; 0.2550/0.5879 |
| zju | 2026 | TaskFuse | FSS | R² | 0.6047/0.6714; 0.6195/0.7916; 0.5043/0.6445 |
| Credasis | 2026 | VERITY BCI | FSU | R² | **0.6766**/0.7741; not on board; not on board |
| NoahZhang | 2026 | "meaty tortellini" | not stated | R² | 0.6396/0.7153; 0.6910/0.7715; 0.5269/0.6130 |

FALCON H2 on EvalAI ([leaderboard](https://eval.ai/web/challenges/challenge-page/2319/leaderboard/5748), held-out WER, lower is better): baseline RNN Multi ZS 0.7873; RNN Multi + LM ZS 0.3861; RNN Multi OR 0.2303; CORP (TTA) 0.0923; RNN Multi + LM OR 0.0343; TeamCyber (2026) 0.0741. FALCON B1 ([leaderboard](https://eval.ai/web/challenges/challenge-page/2319/leaderboard/5752), held-out MSE): EnSongdec multi-model oracle 7.92 × 10⁻⁴; single-model oracle 22.8 × 10⁻⁴; CK Loo & QD Ng (2026) 15.8 × 10⁻⁴.

### Allen Visual Coding – Neuropixels, IBL Brain-wide Map, Steinmetz 2019
I found no standard decoding benchmark (fixed split, metric and leaderboard) for these sets. Papers such as [NEDS](https://arxiv.org/html/2504.08201) report IBL encoding/decoding results mostly in figures, with their own session selections, so no rows are given.

---

## How to read these numbers

- **NLB metrics measure different things.** co-bps rewards predicting held-out neurons; vel R² is a *linear* readout of submitted rates. BAND has the best MC_Maze vel R² (0.9362) but one of the lower co-bps scores; MINT has by far the best Area2_Bump psth R² (0.9135) without the best co-bps. Pick the metric that matches the question.
- **co-bps cannot be compared across datasets.** It depends on neuron count and firing rates (the NLB paper says this directly). Compare methods within a dataset, or across MC_Maze S/M/L, which come from the same experiment.
- **Paper vs leaderboard.** The NLB and FALCON papers' own tables differ slightly from the EvalAI boards for the same baselines (e.g. AutoLFADS MC_Maze co-bps 0.346 in the paper, 0.3364 on the board; CORP H2 WER 0.11 vs 0.0923). Do not mix them in one comparison.
- **Ensembles and LLMs dominate speech leaderboards.** Top B2T '24 and '25 entries merge many decoders with a fine-tuned LLM; single-model papers (LightBeam, mean of 10 seeds) are a different setting. The organizers' paper credits ensembling with the largest gains.
- **Open leaderboards keep moving.** B2T '24 went from 5.81% (competition winner at the deadline) to 3.34% in 2026 on the same holdout, with unlimited time and no fresh test set. Kaggle's private split (B2T '25) is the more reliable number; its public split was optimistic for every top team (e.g. 1.363% public vs 1.537% private for the winner).
- **Online ≠ offline.** Willett 2023 and Card 2024 report real-time WER/accuracy on their own evaluation days; competition WER is offline on a fixed holdout. The 50-word-vocabulary numbers are a much easier task than the 125k vocabulary.
- **Non-stationarity is the main split effect.** Testing on sentences close in time to training cut Willett 2023 WER from 17.4% to 11.8%; handwriting HeldOutBlocks is about twice as hard as HeldOutTrials; FALCON held-out R² falls well below held-in for every non-oracle method.
- **Oracle rows are not competitors.** FALCON "OR" decoders train on data that submitters never see; use them only as ceilings.
- **Sorted units vs threshold crossings.** NLB releases sorted units; FALCON, B2T and most human BCI data release unsorted threshold crossings (plus spike band power). Results on one do not carry over directly to the other.
