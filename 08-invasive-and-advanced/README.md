# Part 08: Invasive and advanced BCI

**When:** year 2 onward.

## Invasive recording
- [ ] Intracortical arrays (Utah array), Neuropixels, ECoG, stereo-EEG, endovascular (Stentrode)
- [ ] Spikes vs. multi-unit activity vs. LFP vs. high-gamma power
- [ ] Spike detection and spike sorting
- [ ] Firing rates, binning, smoothing
- [ ] Signal stability over months; tissue response and array degradation

## Decoding movement and speech
- [ ] Linear decoders and Wiener filters
- [ ] Kalman filter decoders for cursor control; ReFIT
- [ ] Neural population dynamics and latent variable models (GPFA, LFADS, CEBRA)
- [ ] Handwriting and speech decoding with RNNs and language models
- [ ] Closed-loop learning: the brain adapts to the decoder

## Beyond decoding
- [ ] Stimulation: deep brain stimulation, intracortical microstimulation for touch, functional electrical stimulation of muscles
- [ ] Bidirectional BCIs
- [ ] fNIRS- and MEG-based BCIs

## Applications and industry
- [ ] Clinical uses: ALS and locked-in syndrome, spinal cord injury, stroke rehabilitation
- [ ] Companies and their approaches: Neuralink, Synchron, Paradromics, Blackrock Neurotech, Precision Neuroscience
- [ ] Regulation: medical device approval (e.g. FDA) and clinical trials

## Build
- [ ] Notebook: decode reach direction from a public spiking dataset with a Kalman filter vs. an RNN
- [ ] Reproduce one figure from a recent speech or handwriting decoding paper using its released data

## Resources
- Hochberg et al. (2012), "Reach and grasp by people with tetraplegia using a neurally controlled robotic arm", *Nature*
- Gilja et al. (2012), "A high-performance neural prosthesis enabled by control algorithm design", *Nature Neuroscience*
- Pandarinath et al. (2018), "Inferring single-trial neural population dynamics using sequential auto-encoders" (LFADS), *Nature Methods*
- Willett et al. (2021), "High-performance brain-to-text communication via handwriting", *Nature*
- Willett et al. (2023), "A high-performance speech neuroprosthesis", *Nature*
- Card et al. (2024), "An accurate and rapidly calibrating speech neuroprosthesis", *NEJM*
- Neural Latents Benchmark and the DANDI Archive (public spiking datasets)
