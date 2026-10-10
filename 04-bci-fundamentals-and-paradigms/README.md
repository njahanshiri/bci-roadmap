# Part 04: BCI fundamentals and paradigms

**When:** months 3–6, alongside Part 05.

## What a BCI is
- [ ] The BCI loop: acquisition → preprocessing → features → decoding → output → feedback
- [ ] Active, reactive, and passive BCIs
- [ ] Synchronous (cue-based) vs. asynchronous (self-paced) BCIs
- [ ] Calibration sessions; how the user and the decoder adapt to each other
- [ ] BCI inefficiency ("BCI illiteracy"): why some users can't control some paradigms
- [ ] Neurofeedback and closed-loop systems

## Evaluation
- [ ] Accuracy, balanced accuracy, Cohen's kappa, ROC AUC
- [ ] Information transfer rate (ITR, Wolpaw formula) and its pitfalls
- [ ] False positives per minute for asynchronous BCIs
- [ ] Offline vs. online performance

## Motor imagery
- [ ] Sensorimotor rhythms and lateralized ERD/ERS
- [ ] Imagined vs. executed vs. attempted movement
- [ ] Log band power / log-variance features over C3, Cz, C4
- [ ] Common Spatial Patterns (CSP) and filter-bank CSP (FBCSP)
- [ ] Multi-class motor imagery (left hand, right hand, feet, tongue)

## P300
- [ ] The oddball paradigm
- [ ] The P300 speller: row-column and checkerboard layouts
- [ ] Averaging over repetitions; dynamic stopping
- [ ] xDAWN spatial filtering; shrinkage LDA

## SSVEP and code-modulated VEP
- [ ] Frequency tagging and harmonics
- [ ] Canonical correlation analysis (CCA), filter-bank CCA, TRCA
- [ ] Monitor refresh rate and stimulus design
- [ ] Code-modulated VEP (c-VEP)

## Other paradigms
- [ ] Error-related potentials (ErrP) for automatic error correction
- [ ] Auditory and tactile BCIs
- [ ] Hybrid BCIs (e.g. SSVEP + motor imagery, EEG + EOG)
- [ ] Passive BCI: workload, attention, drowsiness (and how weak the evidence often is)

## Build
- [ ] Notebook: motor imagery with CSP + LDA on BCI Competition IV 2a
- [ ] Notebook: P300 classification with xDAWN + LDA
- [ ] Notebook: SSVEP with CCA and TRCA, including an ITR calculation

## Resources
- Wolpaw & Wolpaw (eds.), *Brain-Computer Interfaces: Principles and Practice*
- Wolpaw et al. (2002), "Brain–computer interfaces for communication and control", *Clinical Neurophysiology*
- Pfurtscheller & Lopes da Silva (1999), "Event-related EEG/MEG synchronization and desynchronization: basic principles", *Clinical Neurophysiology*
- Farwell & Donchin (1988), "Talking off the top of your head" (the original P300 speller)
- Nakanishi et al. (2018), "Enhancing detection of SSVEPs for a high-speed brain speller using task-related component analysis", *IEEE TBME*
