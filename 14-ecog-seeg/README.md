# 14: ECoG and sEEG (intracranial field potentials)

**Measures:** electrical activity from electrodes on the brain surface (ECoG) or inside it (stereo-EEG). **Invasive:** yes (surgery). **Resolution:** milliseconds in time, millimeters in space.
**When:** Years 2–3.

## What ECoG and sEEG measure
- [ ] Grids and strips on the cortex (ECoG) vs. depth electrodes (sEEG)
- [ ] Why signal quality and spatial resolution are much better than EEG
- [ ] High-gamma power (~70–150 Hz) as a proxy for local neural activity
- [ ] Endovascular recording from inside blood vessels (e.g. Stentrode)

## Recording context
- [ ] Most human data comes from epilepsy patients during clinical monitoring
- [ ] Electrode localization on MRI/CT images
- [ ] iEEG-BIDS
- [ ] Ethics of research with patients in a clinical setting

## Preprocessing
- [ ] Re-referencing: common average, bipolar
- [ ] Line noise and its harmonics
- [ ] Recognizing epileptic activity and bad channels
- [ ] Extracting high-gamma: band-pass + Hilbert envelope

## Decoding
- [ ] Finger and hand movement decoding
- [ ] Speech decoding: phonemes, words, and sentences with neural networks and language models
- [ ] Long-term implanted ECoG BCIs (e.g. epidural ECoG controlling an exoskeleton)
- [ ] Thin-film high-density surface arrays

## Public datasets
- BCI Competition IV, dataset 4 (ECoG finger flexion)
- Kai Miller's ECoG library (16 tasks, many patients)
- OpenNeuro iEEG datasets

## Build
- [ ] Notebook: decode finger flexion from ECoG (BCI Competition IV dataset 4) — high-gamma features + linear regression vs. a small network
- [ ] Notebook: reproduce one figure from Miller's ECoG library

## Resources
- Miller (2019), "A library of human electrocorticographic data and analyses", *Nature Human Behaviour*
- Moses et al. (2021), "Neuroprosthesis for decoding speech in a paralyzed person with anarthria", *NEJM*
- Metzger et al. (2023), "A high-performance neuroprosthesis for speech decoding and avatar control", *Nature*
- Benabid et al. (2019), "An exoskeleton controlled by an epidural wireless brain–machine interface in a tetraplegic patient", *Lancet Neurology*
- MNE-Python iEEG tutorials
