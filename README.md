# BCI Roadmap

Every concept I need to go from AI engineer to brain-computer interface (BCI) researcher, split into 10 parts over 5 years.

## Start

```bash
./start.sh
```

The first run sets up Python, downloads 2 minutes of real EEG, measures your first brain signal (alpha waves with eyes open vs. closed), and prints your progress through the roadmap. Run it again any time to see your progress.

## Parts

| Part | When | What |
|---|---|---|
| [00 Math and statistics](00-math-and-stats/) | Weeks 1–4 | Linear algebra for spatial filters, statistics for small neural datasets |
| [01 Neuroscience](01-neuroscience/) | Months 0–2 | Where EEG comes from, brain rhythms, ERPs, recording methods |
| [02 Signal processing](02-signal-processing/) | Months 0–3 | Sampling, Fourier, filters, time-frequency, referencing |
| [03 EEG data and preprocessing](03-eeg-data-and-preprocessing/) | Months 1–4 | Hardware, formats, MNE-Python, artifacts, ICA |
| [04 BCI fundamentals and paradigms](04-bci-fundamentals-and-paradigms/) | Months 3–6 | The BCI loop, evaluation, motor imagery, P300, SSVEP |
| [05 Classical ML for BCI](05-classical-ml-for-bci/) | Months 3–6 | CSP, LDA, Riemannian geometry, honest evaluation |
| [06 Deep learning for EEG](06-deep-learning-for-eeg/) | Months 6–12 | EEGNet, transfer learning, EEG foundation models |
| [07 Real-time and hardware](07-real-time-and-hardware/) | Months 6–12 | OpenBCI, LSL, online decoding, experiment design |
| [08 Invasive and advanced](08-invasive-and-advanced/) | Year 2+ | Spikes, intracortical decoding, speech BCIs, industry |
| [09 Research, ethics, and community](09-research-ethics-and-community/) | All 5 years | Papers, open science, ethics, open source, community |

## How to use it

- Work through Parts 00–02 together, then 03, then 04–05 together.
- Tick a box (`- [x]`) only when you can **explain the concept in plain words** and **have used it in code in this repo**.
- Put your notebooks in the folder of the part they belong to.
- Each part ends with a **Build** section: those projects show you understood the part, and each one is a good post to share.

## Traps for ML engineers working with EEG

1. **Leakage:** never split trials from the same session randomly. Split by subject or by session.
2. **Artifacts:** a model can learn eye blinks or muscle noise instead of brain activity.
3. **Small data:** typical datasets have about 10 subjects and a few hundred trials each.
4. **Non-stationarity:** the same person's EEG changes from day to day.
