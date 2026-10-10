# 12: fNIRS (functional near-infrared spectroscopy)

**Measures:** blood oxygenation in the outer cortex, using near-infrared light. **Invasive:** no. **Resolution:** seconds in time, centimeters in space. **Cost:** medium.
**When:** Year 2.

## What fNIRS measures
- [ ] The hemodynamic response: oxygenated (HbO) and deoxygenated (HbR) hemoglobin
- [ ] Why the response is slow (peaks about 5–8 s after activity) and what that means for BCI speed
- [ ] The modified Beer-Lambert law: from light intensity to concentration changes
- [ ] Source-detector separation and depth sensitivity; short-separation channels

## Hardware and recording
- [ ] Continuous-wave fNIRS devices; wavelengths; sources and detectors (optodes)
- [ ] Optode placement and scalp coupling (hair matters)
- [ ] The SNIRF file format and fNIRS-BIDS

## Preprocessing
- [ ] Raw intensity → optical density → HbO/HbR concentration
- [ ] Scalp coupling index for bad channel detection
- [ ] Motion artifacts and their correction (e.g. TDDR, spline interpolation)
- [ ] Physiological noise: heartbeat (~1 Hz), breathing (~0.3 Hz), Mayer waves (~0.1 Hz)
- [ ] Short-channel regression to remove scalp blood flow

## Analysis and decoding
- [ ] Block averaging of hemodynamic responses
- [ ] The general linear model (GLM) with a hemodynamic response function
- [ ] BCI features: mean, slope, peak, variance of HbO/HbR in a window
- [ ] fNIRS BCI tasks: mental arithmetic, motor imagery, word generation
- [ ] Hybrid EEG + fNIRS BCIs

## Public datasets
- Shin et al. (2017) open-access hybrid EEG + fNIRS dataset (motor imagery and mental arithmetic)
- MNE-NIRS example datasets

## Build
- [ ] Notebook: MNE-NIRS pipeline on a public dataset, from raw intensity to HbO/HbR block averages
- [ ] Notebook: mental arithmetic vs. rest — EEG alone vs. fNIRS alone vs. both, on Shin et al. (2017)

## Resources
- Pinti et al. (2020), "The present and future use of functional near-infrared spectroscopy (fNIRS) for cognitive neuroscience", *Annals of the New York Academy of Sciences*
- Naseer & Hong (2015), "fNIRS-based brain-computer interfaces: a review", *Frontiers in Human Neuroscience*
- Shin et al. (2017), "Open access dataset for EEG+NIRS single-trial classification", *IEEE TNSRE*
- Fishburn et al. (2019), "Temporal Derivative Distribution Repair (TDDR)", *NeuroImage*
- MNE-NIRS documentation
