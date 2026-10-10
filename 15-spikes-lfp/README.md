# 15: Spikes and LFP (intracortical recordings)

**Measures:** action potentials of individual neurons (spikes) and local field potentials (LFP), from electrodes inside the cortex. **Invasive:** yes (surgery). **Resolution:** sub-millisecond, single neurons.
**When:** Years 2–3. The highest-performance BCIs today use this data.

## What intracortical arrays measure
- [ ] Intracortical arrays: Utah array, Neuropixels, flexible thread electrodes
- [ ] Spikes vs. multi-unit activity vs. LFP vs. high-gamma
- [ ] Signal stability over months; tissue response and array degradation

## Preprocessing
- [ ] Spike detection by threshold crossing
- [ ] Spike sorting: assigning spikes to individual neurons (Kilosort, SpikeInterface)
- [ ] Threshold crossings without sorting: why many BCIs skip spike sorting
- [ ] Firing rates: binning and smoothing
- [ ] NWB (Neurodata Without Borders) file format

## Decoding movement and speech
- [ ] Population vectors, linear decoders, and Wiener filters
- [ ] Kalman filter decoders for cursor control; ReFIT
- [ ] Neural population dynamics and latent variable models (GPFA, LFADS, CEBRA)
- [ ] Handwriting and speech decoding with RNNs and language models
- [ ] Closed-loop learning: the brain adapts to the decoder

## Writing information into the brain
- [ ] Intracortical microstimulation (ICMS) for artificial touch
- [ ] Bidirectional BCIs that both read and stimulate

## Public datasets
- Neural Latents Benchmark (monkey reaching and other tasks)
- DANDI Archive (thousands of NWB datasets)
- Released data from the handwriting and speech decoding papers below

## Build
- [ ] Notebook: decode reach direction from a public spiking dataset with a Kalman filter vs. an RNN
- [ ] Reproduce one figure from a recent speech or handwriting decoding paper using its released data

## Resources
- Hochberg et al. (2012), "Reach and grasp by people with tetraplegia using a neurally controlled robotic arm", *Nature*
- Gilja et al. (2012), "A high-performance neural prosthesis enabled by control algorithm design", *Nature Neuroscience*
- Pandarinath et al. (2018), "Inferring single-trial neural population dynamics using sequential auto-encoders" (LFADS), *Nature Methods*
- Flesher et al. (2016), "Intracortical microstimulation of human somatosensory cortex", *Science Translational Medicine*
- Willett et al. (2021), "High-performance brain-to-text communication via handwriting", *Nature*
- Willett et al. (2023), "A high-performance speech neuroprosthesis", *Nature*
- Card et al. (2024), "An accurate and rapidly calibrating speech neuroprosthesis", *NEJM*
- SpikeInterface documentation
