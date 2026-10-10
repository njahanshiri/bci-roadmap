# Part 03: EEG data and preprocessing

**When:** months 1–4.

## Hardware and recording
- [ ] Electrodes: wet (gel), saline, dry; impedance
- [ ] Reference and ground electrodes
- [ ] Amplifiers, sampling rate, bit depth, common-mode rejection
- [ ] Triggers and markers; synchronizing stimuli with EEG

## Data formats and standards
- [ ] File formats: EDF/BDF, BrainVision, FIF, GDF, XDF
- [ ] EEG-BIDS: organizing datasets the standard way
- [ ] Events, annotations, and channel metadata (types, positions, montage)

## MNE-Python core
- [ ] `Raw`, `Epochs`, `Evoked`, and `Info` objects
- [ ] Picking channels, cropping, filtering, resampling
- [ ] Epoching, baseline correction, rejecting epochs
- [ ] Plotting: raw traces, PSD, topographic maps, evoked responses

## Artifacts
- [ ] Recognizing artifacts: eye blinks, saccades, muscle (EMG), heart (ECG), line noise, electrode pops, sweat, movement
- [ ] Detecting and interpolating bad channels
- [ ] ICA for artifact removal; choosing components; ICLabel
- [ ] Signal-space projection (SSP)
- [ ] Regression-based EOG removal
- [ ] Automated cleaning: autoreject, artifact subspace reconstruction (ASR)
- [ ] When not to clean: how much preprocessing actually helps

## Source analysis (intro)
- [ ] Forward model, head model, leadfield
- [ ] The inverse problem: minimum norm, sLORETA, beamformers
- [ ] Why source estimates from few electrodes are uncertain

## Build
- [ ] Notebook: full preprocessing pipeline on one subject (filter → bad channels → ICA → epochs), with before/after plots
- [ ] Script: run the same pipeline on 10 subjects and write a short data-quality report

## Resources
- MNE-Python tutorials (mne.tools), "Preprocessing" section
- Pernet et al. (2019), "EEG-BIDS, an extension to the brain imaging data structure for electroencephalography", *Scientific Data*
- Pion-Tonachini, Kreutz-Delgado & Makeig (2019), "ICLabel", *NeuroImage*
- Delorme (2023), "EEG is better left alone", *Scientific Reports*
