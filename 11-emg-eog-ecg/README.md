# 11: EMG, EOG, and ECG (peripheral signals)

**Measures:** electrical activity of muscles (EMG), eye movements (EOG), and the heart (ECG). **Invasive:** no. **Cost:** low.
**When:** months 4–6, alongside EEG preprocessing.
These signals matter in two ways: they are the main **artifacts** in EEG, and they are useful **control signals** in hybrid BCIs.

## What they measure
- [ ] EMG: muscle action potentials; frequency range (~20–450 Hz) and sampling needs
- [ ] EOG: the eye as an electrical dipole; blinks vs. saccades
- [ ] ECG: the heartbeat waveform; heart rate and heart-rate variability (HRV)

## As artifacts in EEG
- [ ] How each one appears in EEG: frequency, timing, and scalp distribution
- [ ] Recording dedicated EOG/ECG channels to help remove them
- [ ] Regression-based EOG removal
- [ ] Finding blink and heartbeat components with ICA using EOG/ECG channels

## As control and state signals
- [ ] Surface EMG gesture decoding; high-density EMG
- [ ] Classic EMG features: mean absolute value, RMS, zero crossings, waveform length
- [ ] EOG-based eye-movement interfaces
- [ ] Hybrid BCIs: EEG + EMG, EEG + EOG
- [ ] EMG for detecting movement intent in rehabilitation
- [ ] Heart rate and HRV as passive measures of workload and stress

## Public datasets
- Ninapro (surface EMG of hand gestures)
- PhysioNet (many ECG databases)

## Build
- [ ] Notebook: find blinks in PhysioNet EEG using frontal channels as an EOG proxy, and remove them with ICA
- [ ] Notebook: EMG gesture classification on Ninapro — classic features + LDA vs. a small CNN

## Resources
- Hudgins, Parker & Scott (1993), "A new strategy for multifunction myoelectric control", *IEEE TBME*
- Atzori et al. (2014), "Electromyography data for non-invasive naturally-controlled robotic hand prostheses" (Ninapro), *Scientific Data*
- Pfurtscheller et al. (2010), "The hybrid BCI", *Frontiers in Neuroscience*
- MNE-Python tutorials: "Overview of artifact detection" and "Repairing artifacts with ICA"
