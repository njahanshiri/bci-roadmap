# 04: BCI systems and real-time

**Shared by all data types.** **When:** months 6–12.
Hardware for each data type lives in its own folder; this part is about turning any signal into a working BCI.

## What a BCI is
- [ ] The BCI loop: acquisition → preprocessing → features → decoding → output → feedback
- [ ] Active, reactive, and passive BCIs
- [ ] Synchronous (cue-based) vs. asynchronous (self-paced) BCIs
- [ ] Calibration; how the user and the decoder adapt to each other
- [ ] BCI inefficiency ("BCI illiteracy"): why some users can't control some paradigms
- [ ] Neurofeedback and closed-loop systems

## Streaming and timing
- [ ] BrainFlow: one API for many devices
- [ ] Lab Streaming Layer (LSL): streams, clocks, synchronization
- [ ] Latency and jitter: how to measure them, and why they break event-locked paradigms
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
- [ ] Replay a recorded EEG file through LSL as a fake live stream and decode it online (no hardware needed)
- [ ] Measure the end-to-end latency of your pipeline

## Resources
- Wolpaw & Wolpaw (eds.), *Brain-Computer Interfaces: Principles and Practice*
- Wolpaw et al. (2002), "Brain–computer interfaces for communication and control", *Clinical Neurophysiology*
- BrainFlow documentation; Lab Streaming Layer documentation (labstreaminglayer.org); PsychoPy documentation
