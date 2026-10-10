# Part 02: Signal processing

**When:** months 0–3.

## Sampling
- [ ] Sampling rate, Nyquist frequency, aliasing
- [ ] Anti-aliasing; resampling and decimation
- [ ] Quantization and ADC resolution; the microvolt scale of EEG

## Frequency domain
- [ ] Fourier transform, DFT, FFT
- [ ] Frequency resolution vs. window length
- [ ] Windowing (Hann, Hamming) and spectral leakage
- [ ] Zero-padding: what it does and doesn't do
- [ ] Power spectral density: periodogram, Welch, multitaper
- [ ] Log power and decibels; absolute vs. relative band power

## Filters
- [ ] FIR vs. IIR filters
- [ ] Cutoff, transition band, filter order, ripple
- [ ] Phase distortion; zero-phase (forward-backward) vs. causal filtering
- [ ] Why real-time BCI needs causal filters
- [ ] High-pass, low-pass, band-pass, notch (50/60 Hz line noise)
- [ ] Filter ringing and edge effects; what filters do to ERPs

## Time-frequency analysis
- [ ] Short-time Fourier transform (STFT)
- [ ] Morlet wavelets and the time-frequency trade-off (number of cycles)
- [ ] Hilbert transform, analytic signal, instantaneous amplitude and phase
- [ ] Baseline normalization: percent change, dB, z-score
- [ ] Inter-trial phase coherence (ITC) vs. power

## Spatial processing
- [ ] Re-referencing: common average, linked mastoids, REST
- [ ] Surface Laplacian / current source density
- [ ] Spatial filters as weighted sums of channels

## Connectivity (intro)
- [ ] Coherence, phase-locking value (PLV), phase-lag index (PLI)
- [ ] Why volume conduction creates false connectivity
- [ ] Phase-amplitude coupling

## Build
- [ ] Notebook: build a signal from sines plus noise, then recover it with FFT, Welch, and wavelets
- [ ] Notebook: design FIR and IIR band-pass filters and compare their phase and ringing on a simulated ERP

## Resources
- Mike X Cohen, *Analyzing Neural Time Series Data*, and his YouTube lectures
- Steven W. Smith, *The Scientist and Engineer's Guide to Digital Signal Processing* (free at dspguide.com)
- Widmann, Schröger & Maess (2015), "Digital filter design for electrophysiological data – a practical approach", *J Neurosci Methods*
- de Cheveigné & Nelken (2019), "Filters: when, why, and how (not) to use them", *Neuron*
