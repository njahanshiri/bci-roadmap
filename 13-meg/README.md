# 13: MEG (magnetoencephalography)

**Measures:** magnetic fields produced by the same brain currents as EEG. **Invasive:** no. **Resolution:** milliseconds in time, millimeters to centimeters in space. **Cost:** very high (shielded room), falling with wearable sensors.
**When:** Year 2.

## What MEG measures
- [ ] Magnetic fields from neural currents; why the skull distorts them less than EEG
- [ ] Sensitivity to tangential vs. radial sources, and why EEG and MEG complement each other
- [ ] Magnetometers vs. gradiometers
- [ ] SQUID sensors vs. optically pumped magnetometers (OPM-MEG, wearable)

## Recording
- [ ] Magnetically shielded rooms and environmental noise
- [ ] Head position tracking (cHPI) and head movement
- [ ] Empty-room recordings for noise estimation

## Preprocessing
- [ ] Signal-space separation (SSS) / Maxwell filtering
- [ ] Head movement compensation
- [ ] ICA and SSP for heartbeat and eye artifacts in MEG

## Source analysis
- [ ] Co-registration of MEG sensors with the participant's MRI
- [ ] Forward models for MEG; boundary element models
- [ ] Minimum-norm estimates and beamformers on real data

## MEG for BCI
- [ ] MEG motor imagery and neurofeedback studies; why MEG BCIs are rare
- [ ] Wearable OPM-MEG as a path to practical MEG BCIs
- [ ] Decoding perceived speech from MEG/EEG with deep learning

## Public datasets
- MNE sample and somato datasets (MEG + EEG, built into MNE-Python)
- Cam-CAN (large MEG dataset, access by application)

## Build
- [ ] Notebook: MNE sample dataset — evoked responses, then a source estimate
- [ ] Notebook: compare EEG and MEG sensors on the same events — which one decodes the stimulus better?

## Resources
- Hämäläinen et al. (1993), "Magnetoencephalography—theory, instrumentation, and applications to noninvasive studies of the working human brain", *Reviews of Modern Physics*
- Boto et al. (2018), "Moving magnetoencephalography towards real-world applications with a wearable system", *Nature*
- Défossez et al. (2023), "Decoding speech perception from non-invasive brain recordings", *Nature Machine Intelligence*
- MNE-Python tutorials (MNE was originally built for MEG)
