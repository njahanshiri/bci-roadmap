# BCI Roadmap

Every concept I need to go from AI engineer to brain-computer interface (BCI) researcher, organized by **type of brain data**, over 5 years.

## Start

```bash
./start.sh
```

The first run sets up Python, downloads 2 minutes of real EEG, measures your first brain signal (alpha waves with eyes open vs. closed), and prints your progress through the roadmap. Run it again any time to see your progress.

## Layout

**00–05: shared foundations**, used by every data type.

| Folder | When | What |
|---|---|---|
| [00 Math and statistics](00-math-and-stats/) | Weeks 1–4 | Linear algebra for spatial filters, statistics for small neural datasets |
| [01 Neuroscience basics](01-neuroscience-basics/) | Months 0–2 | Neurons, anatomy, brain rhythms, recording types compared |
| [02 Signal processing](02-signal-processing/) | Months 0–3 | Sampling, Fourier, filters, time-frequency, referencing |
| [03 ML and evaluation](03-ml-and-evaluation/) | Months 3–9 | Classifiers, Riemannian geometry, honest evaluation, deep learning for neural data |
| [04 BCI systems and real-time](04-bci-systems-and-real-time/) | Months 6–12 | The BCI loop, LSL, online decoding, experiment design |
| [05 Research and community](05-research-and-community/) | All 5 years | Papers, open science, the field, ethics, community |

**10–15: one folder per data type.** Each has the same sections: what it measures, hardware, preprocessing, decoding, public datasets, build projects.

| Folder | Measures | Invasive | When |
|---|---|---|---|
| [10 EEG](10-eeg/) | Electrical activity at the scalp | No | Months 1–12 (core of Year 1) |
| [11 EMG, EOG, ECG](11-emg-eog-ecg/) | Muscles, eyes, heart: EEG artifacts and hybrid control | No | Months 4–6 |
| [12 fNIRS](12-fnirs/) | Blood oxygenation, with light | No | Year 2 |
| [13 MEG](13-meg/) | Magnetic fields from brain currents | No | Year 2 |
| [14 ECoG and sEEG](14-ecog-seeg/) | Electrical activity on or inside the brain | Yes | Years 2–3 |
| [15 Spikes and LFP](15-spikes-lfp/) | Individual neurons | Yes | Years 2–3 |

## Five-year plan

| Period | Focus |
|---|---|
| Year 1 | 00–04 + EEG + EMG/EOG/ECG. Make the repo public around month 10. |
| Year 2 | fNIRS and MEG, then start ECoG and spikes. Pick a niche. First preprint. |
| Year 3 | Finish ECoG and spikes. Go deep on your niche. First open-source tool or benchmark. |
| Years 4–5 | Peer-reviewed papers, talks, tutorials built from this repo, mentoring. |

## How to use it

- Each week, take one section (a heading inside a README), learn its concepts, and write one notebook for it in that folder.
- Tick a box (`- [x]`) only when you can **explain the concept in plain words** and **have used it in code in this repo**.
- Each folder ends with a **Build** section: those projects show you understood it, and each one is a good post to share.

## Traps for ML engineers working with brain data

1. **Leakage:** never split trials from the same session randomly. Split by subject or by session.
2. **Artifacts:** a model can learn eye blinks or muscle noise instead of brain activity.
3. **Small data:** typical datasets have about 10 subjects and a few hundred trials each.
4. **Non-stationarity:** the same person's signals change from day to day.
