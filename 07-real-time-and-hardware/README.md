# Part 07: Real-time BCI and hardware

**When:** months 6–12.

## Hardware
- [ ] OpenBCI boards (Ganglion, Cyton, Cyton + Daisy), electrode caps and headbands
- [ ] Consumer EEG headbands and their limits
- [ ] Electrode placement and checking signal quality before recording
- [ ] Electrical safety basics

## Streaming and timing
- [ ] BrainFlow: one API for many boards
- [ ] Lab Streaming Layer (LSL): streams, clocks, synchronization
- [ ] Latency and jitter: how to measure them, and why they break ERP paradigms
- [ ] Recording to XDF; marker streams

## Online processing
- [ ] Ring buffers and sliding windows
- [ ] Causal filters that keep state between chunks (scipy `lfilter` with `zi`)
- [ ] Decision rules: thresholds, smoothing, dwell time
- [ ] Training offline, applying online; the offline-online accuracy gap
- [ ] Adaptive classifiers that update during use

## Experiment design
- [ ] Stimulus presentation with PsychoPy; frame-accurate timing
- [ ] Trial structure (fixation, cue, task, rest), randomization, counterbalancing
- [ ] Feedback design and user fatigue
- [ ] Informed consent and data protection, even when testing on friends

## Deployment
- [ ] Efficient inference: small models, quantization, on-device decoding
- [ ] Packaging a BCI app: GUI, logging, reproducible configs

## Build
- [ ] Record your own eyes-open/eyes-closed alpha with OpenBCI and compare it to PhysioNet
- [ ] Real-time alpha neurofeedback (a bar that grows with your alpha power)
- [ ] Real-time SSVEP or motor imagery demo, with a video in this repo

## Resources
- OpenBCI documentation
- BrainFlow documentation
- Lab Streaming Layer documentation (labstreaminglayer.org)
- PsychoPy documentation
