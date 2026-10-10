# 10: EEG (electroencephalography)

**Measures:** electrical activity from the scalp. **Invasive:** no. **Resolution:** milliseconds in time, centimeters in space. **Cost:** low.
**When:** months 1–12. This is the core of Year 1.

## What EEG measures
- [ ] Pyramidal neurons and current dipoles
- [ ] Volume conduction: why every electrode sees a blurred mix of sources
- [ ] The 10-20 and 10-10 electrode placement systems
- [ ] Mu rhythm (sensorimotor) vs. occipital alpha
- [ ] Alpha blocking when the eyes open (Berger effect)

## Hardware and recording
- [ ] Electrodes: wet (gel), saline, dry; impedance
- [ ] Reference and ground electrodes
- [ ] Amplifiers, sampling rate, bit depth, common-mode rejection
- [ ] Triggers and markers; synchronizing stimuli with EEG
- [ ] OpenBCI boards (Ganglion, Cyton, Cyton + Daisy) and consumer headbands; their limits
- [ ] Electrode placement and checking signal quality before recording

## Data formats and MNE-Python
- [ ] File formats: EDF/BDF, BrainVision, FIF, GDF, XDF
- [ ] EEG-BIDS: organizing datasets the standard way
- [ ] Events, annotations, and channel metadata (types, positions, montage)
- [ ] MNE `Raw`, `Epochs`, `Evoked`, and `Info` objects
- [ ] Picking, cropping, filtering, resampling, epoching, baseline correction, rejecting epochs
- [ ] Plotting: raw traces, PSD, topographic maps, evoked responses

## Artifacts and preprocessing
- [ ] Recognizing artifacts: eye blinks, saccades, muscle, heart, line noise, electrode pops, sweat, movement
- [ ] Detecting and interpolating bad channels
- [ ] ICA for artifact removal; choosing components; ICLabel
- [ ] Signal-space projection (SSP)
- [ ] Automated cleaning: autoreject, artifact subspace reconstruction (ASR)
- [ ] When not to clean: how much preprocessing actually helps

## Source analysis (intro)
- [ ] Forward model, head model, leadfield
- [ ] The inverse problem: minimum norm, sLORETA, beamformers
- [ ] Why source estimates from few electrodes are uncertain

## Event-related potentials (ERPs)
- [ ] What an ERP is and why we average over trials
- [ ] Visual evoked potentials (VEP), P300, N170, N400, mismatch negativity (MMN)
- [ ] Error-related negativity (ERN) and error potentials
- [ ] Steady-state responses (SSVEP, auditory steady-state response)
- [ ] Readiness potential and movement-related cortical potentials

## Motor imagery
- [ ] Lateralized ERD/ERS over C3 and C4 during imagery
- [ ] Imagined vs. executed vs. attempted movement
- [ ] Log band power / log-variance features
- [ ] Common Spatial Patterns (CSP) as a generalized eigenvalue problem; regularized CSP
- [ ] Filter-bank CSP (FBCSP)
- [ ] Multi-class motor imagery (left hand, right hand, feet, tongue)

## P300
- [ ] The oddball paradigm
- [ ] The P300 speller: row-column and checkerboard layouts
- [ ] Averaging over repetitions; dynamic stopping
- [ ] xDAWN spatial filtering and xDAWN covariances

## SSVEP and code-modulated VEP
- [ ] Frequency tagging and harmonics
- [ ] Canonical correlation analysis (CCA), filter-bank CCA, TRCA
- [ ] Monitor refresh rate and stimulus design
- [ ] Code-modulated VEP (c-VEP)

## Other EEG paradigms
- [ ] Error-related potentials (ErrP) for automatic error correction
- [ ] Auditory and tactile BCIs
- [ ] Passive BCI: workload, attention, drowsiness (and how weak the evidence often is)

## Deep learning for EEG
- [ ] ShallowConvNet and DeepConvNet
- [ ] EEGNet: depthwise and separable convolutions as learned spatial and temporal filters
- [ ] Temporal convolutional networks (EEG-TCNet, ATCNet) and transformers (EEG Conformer)
- [ ] Input choices: raw signal vs. filtered vs. spectrogram vs. covariance
- [ ] Mapping learned filters back to frequencies and scalp topographies
- [ ] Large EEG corpora (e.g. TUH EEG Corpus) and their biases
- [ ] Handling different channel layouts across datasets
- [ ] EEG foundation models: BENDR, BIOT, LaBraM, EEGPT, CBraMod
- [ ] Do foundation models beat strong classical baselines? How to test it fairly

## Public datasets
- PhysioNet EEG Motor Movement/Imagery (109 subjects; used by `start.py`)
- BCI Competition IV 2a and 2b (motor imagery)
- MOABB: dozens of motor imagery, P300, and SSVEP datasets behind one API
- TUH EEG Corpus (large clinical EEG, for pretraining)

## Build
- [ ] Work through the starter notebook [01_load_and_explore_eeg.ipynb](01_load_and_explore_eeg.ipynb): raw EEG, spectrum, filtering, epochs, motor imagery ERD
- [ ] Notebook: eyes open vs. eyes closed alpha (PhysioNet runs 1–2); `start.py` gives you a head start
- [ ] Notebook: full preprocessing pipeline on one subject (filter → bad channels → ICA → epochs), with before/after plots
- [ ] Script: run the same pipeline on 10 subjects and write a short data-quality report
- [ ] Notebook: motor imagery with CSP + LDA on BCI Competition IV 2a
- [ ] Notebook: P300 classification with xDAWN + LDA
- [ ] Notebook: SSVEP with CCA and TRCA, including an ITR calculation
- [ ] Notebook: CSP+LDA vs. tangent space vs. MDM vs. EEGNet on 3 MOABB datasets, within- and cross-subject
- [ ] Notebook: augmentation study — which augmentations help motor imagery
- [ ] Project: evaluate one EEG foundation model against classical baselines, cross-subject
- [ ] Record your own eyes-open/eyes-closed alpha with OpenBCI and compare it to PhysioNet
- [ ] Real-time alpha neurofeedback (a bar that grows with your alpha power)
- [ ] Real-time SSVEP or motor imagery demo, with a video in this repo

## Resources
- Mike X Cohen, *Analyzing Neural Time Series Data*
- Steven Luck, *An Introduction to the Event-Related Potential Technique*
- Nunez & Srinivasan, *Electric Fields of the Brain* (deep reference on EEG physics)
- MNE-Python tutorials (mne.tools)
- Pernet et al. (2019), "EEG-BIDS, an extension to the brain imaging data structure for electroencephalography", *Scientific Data*
- Pion-Tonachini, Kreutz-Delgado & Makeig (2019), "ICLabel", *NeuroImage*
- Delorme (2023), "EEG is better left alone", *Scientific Reports*
- Pfurtscheller & Lopes da Silva (1999), "Event-related EEG/MEG synchronization and desynchronization: basic principles", *Clinical Neurophysiology*
- Blankertz et al. (2008), "Optimizing spatial filters for robust EEG single-trial analysis", *IEEE Signal Processing Magazine*
- Farwell & Donchin (1988), "Talking off the top of your head" (the original P300 speller)
- Nakanishi et al. (2018), "Enhancing detection of SSVEPs for a high-speed brain speller using task-related component analysis", *IEEE TBME*
- Schirrmeister et al. (2017), "Deep learning with convolutional neural networks for EEG decoding and visualization", *Human Brain Mapping*
- Lawhern et al. (2018), "EEGNet: a compact convolutional neural network for EEG-based brain–computer interfaces", *J Neural Eng*
- Jiang et al. (2024), "Large brain model for learning generic representations with tremendous EEG data in BCI" (LaBraM), *ICLR*
- OpenBCI documentation; Braindecode documentation
