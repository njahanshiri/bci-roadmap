# Spikes and LFP (Intracortical recordings)

Intracortical recordings use microelectrodes pushed 1–2 mm (or deeper) into the brain to pick up the action potentials ("spikes") of individual neurons near each tip, plus the slower local field potential (LFP) that sums synaptic activity around it. They give the highest-resolution signal any BCI uses, and they power every record-setting brain-computer interface so far: cursor control near able-bodied mouse speed, handwriting at 90 characters per minute, and speech decoding at 97.5% word accuracy ([Willett 2021](https://doi.org/10.1038/s41586-021-03506-2), [Card 2024](https://doi.org/10.1056/NEJMoa2314132), [Neuralink](https://neuralink.com/updates/two-years-of-telepathy/)). The cost is brain surgery, so in humans they are used only in clinical trials, mostly for paralysis. In animals, high-density probes such as Neuropixels have become standard tools of systems neuroscience ([Jun 2017](https://doi.org/10.1038/nature24636)).

Items marked *unverified* could not be confirmed from a source. Cells marked "—" mean the maker did not publish the spec, or I could not find it.

## 1. The data

**What is measured.** Each microelectrode sees a voltage relative to a reference. That voltage has two parts. The fast part (hundreds of Hz to several kHz) holds the action potentials of neurons within roughly 100 µm of the tip. The slow part (below a few hundred Hz) is the LFP: mostly summed synaptic and dendritic currents from a larger volume ([Buzsáki, Anastassiou & Koch 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC4907333/)). Neuropixels, for example, splits every channel into an "AP" band (0.3–10 kHz, sampled at 30 kHz) and an LFP band (0.5–1000 Hz, sampled at 2.5 kHz) ([Jun 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5955206/)).

**The signal types you will meet, from finest to coarsest**

| Signal | What it is | How you get it | Who uses it |
|---|---|---|---|
| Single-unit activity (SUA) | Spikes you can assign to one neuron | Spike sorting: detect spikes, cluster them by waveform shape (and by position, on dense probes) | Neuroscience; older BCIs |
| Multi-unit activity (MUA) | Spikes from several nearby neurons that you do not separate | Detect spikes and keep all of them per channel | BCIs, neuroscience |
| Threshold crossings (TC) | Count of times the high-pass signal falls below a threshold, usually −3 to −4.5 × RMS noise | One comparison per sample, no sorting | Default feature of modern human BCIs ([Christie 2015](https://doi.org/10.1088/1741-2560/12/1/016009); the UC Davis speech data use −4.5 × RMS, [nejm-brain-to-text](https://github.com/Neuroprosthetics-Lab/nejm-brain-to-text)) |
| Spike-band power (SBP) | Power of the 300–1,000 Hz band, downsampled | Band-pass, square or take magnitude, average | Decodes as well as or better than TC, and needs much less power ([Nason 2020](https://doi.org/10.1038/s41551-020-0591-0)) |
| LFP | Low-frequency voltage (< ~300 Hz; classic LFP band < 100 Hz) | Low-pass and downsample | Brain-state, oscillations, closed-loop DBS; adds information to spikes in some decoders ([Buzsáki 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC4907333/)) |

**Spike sorting.** Sorting turns a voltage trace into a list of (time, neuron) events. Classic pipelines filter, detect peaks, extract waveform features (e.g. PCA) and cluster them. On dense probes, modern sorters such as Kilosort fit spike templates across many neighbouring sites and correct for probe drift ([Pachitariu 2016](https://proceedings.neurips.cc/paper/2016/hash/1145a30ff80745b56fb0cecf65305017-Abstract.html), [Kilosort4, 2024](https://doi.org/10.1038/s41592-024-02232-7)). Human BCIs usually skip sorting. With Utah arrays, using threshold crossings instead of sorted units cost little decoding performance ([Christie 2015](https://doi.org/10.1088/1741-2560/12/1/016009)). It also makes the decoder robust to small electrode movements.

**Firing rates and binning.** Decoders work on spike counts (or SBP) per channel in fixed time bins. Typical bins are 10–20 ms in recent speech BCIs: 20 ms in the public Card 2024 dataset (512 features = TC + SBP on 256 electrodes) and 10 ms in real-time voice synthesis ([nejm-brain-to-text](https://github.com/Neuroprosthetics-Lab/nejm-brain-to-text), [Wairagkar 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12369848/)). Neuroscience analyses smooth counts with a Gaussian kernel or average across trials to get a peri-stimulus time histogram (PSTH).

**Neural population dynamics.** Activity across hundreds of neurons is low-dimensional and evolves smoothly in time. Motor cortex during reaching shows rotational dynamics, not just direction tuning ([Churchland 2012](https://doi.org/10.1038/nature11129)). This is why latent-variable models work well: LFADS (a sequential auto-encoder) infers single-trial latent trajectories and improves decoding ([Pandarinath 2018](https://doi.org/10.1038/s41592-018-0109-9)), and the Neural Latents Benchmark scores such models ([NLB '21](https://arxiv.org/abs/2109.04463)). For an ML engineer, think of the data as a multivariate point process (or count time series) with a hidden low-dimensional state.

**Signal characteristics**

| Property | Typical value | Source |
|---|---|---|
| Spike amplitude | Tens to a few hundred µV at the electrode *unverified* (amplifier input ranges are ±8.192 mV on Blackrock CerePlex W) | [CerePlex W](https://blackrockneurotech.com/products/cereplex-w/) |
| Spike duration | Strongest extracellular fields last < 2 ms | [Buzsáki 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC4907333/) |
| Bands | AP/spike band ~0.3–10 kHz; LFP ~0.5–1000 Hz (Neuropixels); classic LFP < 100 Hz; SBP 300–1,000 Hz | [Jun 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5955206/), [Buzsáki 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC4907333/), [Nason 2020](https://doi.org/10.1038/s41551-020-0591-0) |
| Sampling rate | 30 kHz is standard for raw data (Blackrock, Intan, Neuropixels AP band); Plexon digitizes at 40 kHz; LFP is stored at lower rates (2.5 kHz on Neuropixels); the 2019 Neuralink ASIC sampled at 19.3 kHz, 10-bit | [NeuroPort](https://blackrockneurotech.com/products/neuroport/), [Intan RHD2000](https://intantech.com/products_RHD2000.html), [Plexon](https://plexon.com/products/omniplex-software/), [Musk 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6914248/) |
| Channel counts | 96 per Utah array (human trials use 2–6 arrays, i.e. 192–256+ channels); 384 recorded channels per Neuropixels probe (960–5,120 sites); 421 electrodes per Paradromics module; 1,024 electrodes in Neuralink N1 | [Blackrock](https://blackrockneurotech.com/products/neuroport-electrode/), [BrainGate2](https://clinicaltrials.gov/study/NCT00912041), [Steinmetz 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8244810/), [Paradromics](https://www.paradromics.com/connexus), [Neuralink](https://neuralink.com/updates/prime-study-progress-update/) |
| Noise floor | ~5 µV RMS in the Neuropixels AP band, ~9 µV in the LFP band; Intan amplifiers 2.4 µV RMS | [Jun 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5955206/), [Intan](https://intantech.com/products_RHD2000.html) |
| Main noise and artifacts | Line noise, movement and chewing artifacts (removed well by common-median referencing), stimulation artifacts in bidirectional systems, probe drift | [Jun 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5955206/), [Steinmetz 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8244810/) |
| Stability over time | Signals change day to day (nonstationarity), so decoders need recalibration. Utah arrays: mean usable lifetime 622 days across 55 arrays, some > 1,000 days, one 9 years; human implants lasted longer than monkey ones. Neuropixels 2.0 plus motion correction tracked the same neurons for > 2 months. Neuralink's first participant temporarily lost performance when threads retracted | [Sponheim 2021](https://doi.org/10.1088/1741-2552/ac3eaf), [Steinmetz 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8244810/), [Neuralink](https://neuralink.com/updates/prime-study-progress-update-second-participant/), [FALCON](https://doi.org/10.1101/2024.09.15.613126) |

**File formats**

| Format | Who writes it | Notes |
|---|---|---|
| NWB (Neurodata Without Borders) | Standard for sharing; required by the DANDI archive | HDF5-based, with defined types for raw ephys, LFP, sorted units and behaviour ([Rübel 2022](https://doi.org/10.7554/elife.78362), [nwb.org](https://www.nwb.org/), [DANDI](https://dandiarchive.org/)) |
| Blackrock `.nev` / `.nsX` | NeuroPort / Cerebus | `.nev` holds spike events and waveforms; `.ns1`–`.ns6` hold continuous data at different rates (`.ns5`/`.ns6` = 30 kHz raw) *unverified*; readers in [NPMK](https://github.com/BlackrockNeurotech/NPMK), [Python-Utilities](https://github.com/BlackrockNeurotech/Python-Utilities) and [neo](https://neo.readthedocs.io/en/latest/iolist.html) |
| Open Ephys Binary / Open Ephys / NWB | Open Ephys GUI | Binary is the default; other formats are plugins ([docs](https://open-ephys.github.io/gui-docs/User-Manual/Data-formats/index.html)) |
| SpikeGLX `.bin` + `.meta` | SpikeGLX (Neuropixels) | Raw interleaved int16 plus a text metadata file ([SpikeGLX](https://billkarsh.github.io/SpikeGLX/), [reader code](https://github.com/jenniferColonell/SpikeGLX_Datafile_Tools)) |
| Others | Plexon, Intan, SpikeGadgets, Neuralynx, Ripple | All readable by [python-neo](https://neo.readthedocs.io/en/latest/iolist.html) and SpikeInterface |
| ML-ready derived data | Research groups | Binned features in HDF5 or pickled arrays, e.g. the Card 2024 speech data ([nejm-brain-to-text](https://github.com/Neuroprosthetics-Lab/nejm-brain-to-text)) |

## 2. Devices and specifications

**Human-implantable arrays**

| Device | Company | Type | Electrodes/channels | Sampling rate | Wireless? | Regulatory | Typical use | Status |
|---|---|---|---|---|---|---|---|---|
| NeuroPort Array (Utah array) | Blackrock Neurotech | 10×10 rigid silicon needle array, 4×4 mm, 400 µm pitch, 1.0 or 1.5 mm long, Pt or SIROF tips | 96 recording channels | Set by amplifier (30 kS/s on NeuroPort) | No: percutaneous pedestal; wireless CerePlex W headstage exists for research | FDA 510(k) for temporary (< 30 days) recording ([K110010](https://www.accessdata.fda.gov/cdrh_docs/pdf11/K110010.pdf)); chronic BCI use only under IDE, e.g. BrainGate2 | Nearly all academic human BCIs since 2004 | Current ([Blackrock](https://blackrockneurotech.com/products/neuroport-electrode/)) |
| N1 Implant ("Link") + R1 Robot | Neuralink | Flexible polymer threads inserted by a robot, sealed skull-mounted implant | 1,024 electrodes on 64 threads; plan to go to 3,000 | — for N1 (2019 prototype ASIC: 19.3 kHz, 10-bit) | Yes, fully implanted, inductively charged | FDA IDE May 2023; Breakthrough designations for Blindsight (Sep 2024) and speech (May 2025) | Cursor, typing, robotic arm, speech (trials) | 21 participants by Jan 2026 ([N1 specs](https://neuralink.com/updates/prime-study-progress-update/), [IDE](https://neuralink.com/updates/first-clinical-trial-open-for-recruitment/), [21 participants](https://neuralink.com/updates/two-years-of-telepathy/), [Breakthrough designations](https://neuralink.com/updates/neuralink-raises-650m-series-e/), [Musk 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6914248/)) |
| Connexus | Paradromics | Microwire array, electrodes reach 1.5 mm deep, chest transceiver, optical data link | 421 electrodes per module | — | Yes, fully implanted, inductive power, near-infrared optical link | Breakthrough (Mar 2023, Apr 2024), TAP (Apr 2024), FDA IDE Nov 2025 | Speech and computer control | First chronic implant Jun 2026 ([Connexus](https://www.paradromics.com/connexus), [company](https://paradromics.com/company/), [NCT07357428](https://clinicaltrials.gov/study/NCT07357428)) |
| Neuropixels (human variant) | IMEC consortium / research use | Thicker Neuropixels 1.0 shank for intraoperative use | 384 channels; > 200 single units in one recording | Same as 1.0 *unverified* | No (acute) | Research under IRB, minutes-long intraoperative recordings | Single-neuron neuroscience in surgery patients | Research ([Paulk 2022](https://doi.org/10.1038/s41593-021-00997-0)) |
| Soft probe ("Fleuron" material) | Axoft | Ultra-soft polymer probe | — | — | — | FDA Breakthrough *unverified*; 5-patient first-in-human study (FINESSE) completed 2025 | Recording, aimed at long-term stability | Clinical research ([NCT06673264](https://clinicaltrials.gov/study/NCT06673264), [BioSpace](https://www.biospace.com/press-releases/axoft-to-begin-brain-implant-clinical-study-marking-the-first-time-bio-inspired-material-is-authorized-for-use-in-humans)) |
| Layer 7-T | Precision Neuroscience | Thin-film **surface** electrode array (ECoG, not intracortical) | — | — | No | FDA 510(k) [K242618](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm?ID=K242618), Mar 2025 | Intraoperative mapping, BCI research | See the [ECoG/sEEG folder](../ecog-seeg/) |

**Research probes (mostly animals)**

| Device | Company | Type | Electrodes/channels | Sampling rate | Wireless? | Regulatory | Typical use | Status |
|---|---|---|---|---|---|---|---|---|
| Neuropixels 1.0 | IMEC (consortium with HHMI Janelia, Allen, UCL) | CMOS silicon probe, 10 mm × 70×20 µm shank | 960 sites, 384 selectable channels | AP 30 kHz, LFP 2.5 kHz | No (wired headstage); third-party loggers exist | Research only | Brain-wide recording in rodents | Current; neuropixels.org lists an "NP1.0 EOL notice" (details *unverified*) ([Jun 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5955206/), [neuropixels.org](https://www.neuropixels.org/)) |
| Neuropixels 2.0 | IMEC | Miniaturized, 1- or 4-shank | 1,280 sites per shank, 5,120 on 4-shank; 384 channels; 2 probes per headstage | — | No | Research only | Chronic recordings in freely moving mice | Current ([Steinmetz 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8244810/)) |
| Neuropixels 1.0 NHP | IMEC | 45 mm long, 125 µm wide, 90 µm thick shank | 4,416 sites, 384 channels | Same as 1.0 *unverified* | No | Research only | Monkey and large-brain recording | Current ([Trautmann 2025](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12229894/)) |
| Silicon probes (ASSY series) | Cambridge NeuroTech | Multi-shank silicon probes | Up to 64 channels in < 80 µm shank width | Set by amplifier | Via third-party headstages | Research only | Rodent single units, CSD analysis | Current ([Cambridge NeuroTech](https://www.cambridgeneurotech.com/neural-probes)) |
| Silicon probes | NeuroNexus | Michigan-style planar probes | — | Set by amplifier | — | Research only | Rodent and NHP recording | Current ([NeuroNexus](https://www.neuronexus.com/products/electrode-arrays/)) |
| V-Probe | Plexon | Stainless-steel linear probe | 8–64 channels, up to 150 mm long | Set by amplifier | No | Research only | Acute NHP recording | Current ([Plexon](https://plexon.com/products/plexon-v-probe/)) |

**Acquisition systems**

| Device | Company | Type | Electrodes/channels | Sampling rate | Wireless? | Regulatory | Typical use | Status |
|---|---|---|---|---|---|---|---|---|
| NeuroPort Biopotential Signal Processing System | Blackrock | Clinical-grade neural signal processor | 32–512 channels | 30 kS/s | No | FDA 510(k) [K090957](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm?ID=K090957) (2009); Digital NeuroPort [K202174](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm?ID=K202174) (2021) | Human BCI trials, epilepsy research | Current ([Blackrock](https://blackrockneurotech.com/products/neuroport/)) |
| Cerebus | Blackrock | Research NSP | 16–512 channels | 30 kS/s | No | Research | NHP BCI labs | Current ([Blackrock](https://blackrockneurotech.com/products/cerebus/)) |
| CerePlex W | Blackrock | Wireless digital headstage | 96 channels, 16-bit, 0.3 Hz–7.5 kHz | 30 kS/s | Yes, 3 m line of sight, 2.5 h battery | Research | Freely moving large animals; also used on human pedestals in research *unverified* | Current ([Blackrock](https://blackrockneurotech.com/products/cereplex-w/)) |
| RHD2000 chips and RHD recording controller | Intan Technologies | Amplifier-on-chip (RHD2132: 32 ch, RHD2164: 64 ch), 16-bit ADC | Controller up to 1,024 channels | Up to 30 kS/s per channel | Intan sells none, but many third-party wireless loggers use its chips | Research | The amplifier inside most open-source systems | Current ([RHD2000](https://intantech.com/products_RHD2000.html), [RHD system](https://intantech.com/RHD_system.html)) |
| RHS stim/recording system | Intan | Recording plus stimulation | Up to 128 channels | Up to 30 kS/s | No | Research | Closed-loop and microstimulation experiments | Current ([Intan](https://intantech.com/RHS_system.html)) |
| Acquisition Board / ONIX | Open Ephys | Open-source USB board (Intan headstages) / its successor ONIX | Up to 512 channels (board) | Set by Intan chips | ONIX targets freely moving animals | Research | Low-cost academic labs; ~$1,000 to build the board yourself | Current ([board docs](https://open-ephys.github.io/acq-board-docs/), [ONIX](https://open-ephys.github.io/onix-docs/)) |
| Trodes systems, Pixie384 / Bennu / Satori | SpikeGadgets | Tethered and datalogging headstages, incl. Neuropixels | 32–384 channels per logger; Bennu takes up to 3 Neuropixels | — | Wireless datalogging | Research | Freely moving rodents and primates | Current ([SpikeGadgets](https://spikegadgets.com/)) |
| Grapevine NIP / Summit | Ripple Neuro | Neural interface processor with stimulation | 32–512 channels | — | Summit: Wi-Fi + on-board storage | "Meets safety standards for laboratory and clinical research" | Neuroprosthesis development, human research | Current ([Ripple](https://rippleneuro.com/ripple-products/grapevine-processors/)) |
| OmniPlex | Plexon | Acquisition with digital or analog headstages | Up to 512 channels | 40 kHz, 16-bit | No | Research | NHP and rodent labs | Current ([Plexon](https://plexon.com/products/omniplex-software/)) |
| SpikeGLX (software) | HHMI Janelia (Bill Karsh) | Acquisition software for Neuropixels and NI-DAQ | All Neuropixels generations | — | — | Research | Standard Neuropixels recording software | Current ([SpikeGLX](https://billkarsh.github.io/SpikeGLX/)) |

## 3. Applications (domains)

| Domain | How spikes/LFP are used | Examples | Maturity |
|---|---|---|---|
| Motor BCI: cursor and computer control | Decode intended hand or arm velocity from motor cortex, map it to a cursor and clicks | BrainGate ([Hochberg 2006](https://doi.org/10.1038/nature04970), [Gilja 2012](https://doi.org/10.1038/nn.3265)); several Neuralink participants reach or exceed the 8–10 bits/s of able-bodied mouse users; one passed 10 bits/s in his first week (company-reported, [Neuralink](https://neuralink.com/updates/two-years-of-telepathy/)) | Clinical trials, daily home use |
| Motor BCI: robotic arm and fingers | Decode multi-degree-of-freedom arm, hand or finger movement | Self-feeding monkey ([Velliste 2008](https://doi.org/10.1038/nature06996)); human reach and grasp ([Hochberg 2012](https://doi.org/10.1038/nature11076)); 7D arm ([Collinger 2013](https://doi.org/10.1016/S0140-6736(12)61816-9)); 4-DoF fingers flying a virtual quadcopter ([Willsey 2025](https://doi.org/10.1038/s41591-024-03341-8)); Neuralink CONVOY robotic-arm trial ([Neuralink](https://neuralink.com/updates/convoy-study-launch/)) | Clinical trials |
| Typing | Point-and-click keyboards; Neuralink's "ten-finger keyboard" maps attempted finger moves to keys | 1.4–4.2× faster typing than earlier iBCIs ([Pandarinath 2017](https://doi.org/10.7554/eLife.18554)); up to 40 words/min on the ten-finger keyboard (company-reported, [Neuralink](https://neuralink.com/updates/two-years-of-telepathy/)) | Clinical trials |
| Handwriting neuroprosthesis | RNN decodes attempted handwriting into characters | 90 characters/min, 94.1% raw accuracy, > 99% with autocorrect ([Willett 2021](https://doi.org/10.1038/s41586-021-03506-2)) | Research (one participant) |
| Speech neuroprosthesis | Arrays in ventral precentral gyrus; RNN/Transformer → phonemes → language model → text or voice | 62 words/min ([Willett 2023](https://doi.org/10.1038/s41586-023-06377-x)); 97.5% accuracy, ~32 words/min in daily use ([Card 2024](https://doi.org/10.1056/NEJMoa2314132)); voice synthesized within 10 ms ([Wairagkar 2025](https://doi.org/10.1038/s41586-025-09127-3)); Paradromics Connect-One and Neuralink VOICE trials ([NCT07357428](https://clinicaltrials.gov/study/NCT07357428), [NCT07224256](https://clinicaltrials.gov/study/NCT07224256)) | Clinical trials, the fastest-moving area |
| Sensory feedback via ICMS | Intracortical microstimulation of somatosensory cortex evokes touch felt on the hand | Somatotopic, graded percepts ([Flesher 2016](https://doi.org/10.1126/scitranslmed.aaf8083)); adding touch improved robotic-arm control ([Flesher 2021](https://doi.org/10.1126/science.abd0380)); Johns Hopkins–led INTENT trial (Blackrock Neurotech collaborating), up to 8 recording and stimulating arrays ([NCT07521930](https://clinicaltrials.gov/study/NCT07521930)) | Clinical trials |
| Vision prosthetics | Microstimulation of visual cortex creates phosphenes (dots of light) | 1,024-channel prosthesis in monkey V1/V4 lets animals see shapes and letters ([Chen 2020](https://doi.org/10.1126/science.abd7435)); 96-channel Utah array in a blind person's occipital cortex for 6 months ([Fernández 2021](https://doi.org/10.1172/jci151331)); Neuralink Blindsight (FDA Breakthrough Sep 2024, [Neuralink](https://neuralink.com/updates/neuralink-receives-breakthrough-device-designation-for-blindsight/)) | Research / early human |
| Basic systems neuroscience | Record thousands of neurons across many brain areas at once in behaving animals | Brain-wide choice coding with Neuropixels ([Steinmetz 2019](https://doi.org/10.1038/s41586-019-1787-x)); IBL Brain-Wide Map and Allen Visual Coding datasets (section 9); population dynamics ([Churchland 2012](https://doi.org/10.1038/nature11129)) | Standard research tool |
| Drug discovery / neuropharmacology | Measure how a drug changes firing, bursting and LFP across regions, and block it with antagonists to test mechanism | Psilocybin vs ketanserin, 46,360 units from 35 mice ([Momi 2026, bioRxiv](https://doi.org/10.64898/2026.08.14.744865)); psychedelic TCB-2 in mouse prefrontal cortex ([Dearnley 2021, bioRxiv](https://doi.org/10.1101/2021.08.22.457198)) | Preclinical research |
| Closed-loop neuromodulation | LFP (e.g. beta power in Parkinson's) recorded from stimulation leads adjusts stimulation automatically | Medtronic adaptive DBS approved by FDA 20 Feb 2025 ([P960009/S478](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpma/pma.cfm?id=P960009S478)); ADAPT-PD long-term results ([Bronte-Stewart 2025](https://doi.org/10.1001/jamaneurol.2025.2781)) | Commercial (LFP-based); spike-based closed loop is research |
| Gaming and consumer demos | BCI cursor or finger control drives games | Neuralink participant playing Counter-Strike and using CAD ([Neuralink](https://neuralink.com/updates/prime-study-progress-update-second-participant/)); quadcopter game ([Willsey 2025](https://doi.org/10.1038/s41591-024-03341-8)) | Demonstrations within medical trials |

## 4. Companies

| Company | Country | Focus | Key product | Status 2025–2026 |
|---|---|---|---|---|
| Neuralink | US | Fully implanted high-channel BCI | N1 Implant, R1 Robot | $650M Series E (Jun 2025, [Neuralink](https://neuralink.com/updates/neuralink-raises-650m-series-e/)). 21 participants by 28 Jan 2026, zero serious device-related adverse events reported by the company ([Neuralink](https://neuralink.com/updates/two-years-of-telepathy/)). Trials: PRIME (US), CAN-PRIME, GB-PRIME, UAE-PRIME, CONVOY (robotic arm), VOICE (speech) ([ClinicalTrials.gov](https://clinicaltrials.gov/study/NCT06429735), [NCT07224256](https://clinicaltrials.gov/study/NCT07224256)). Seven UK patients implanted at UCLH Oct–Dec 2025 *unverified* ([UCLH](https://www.uclh.nhs.uk/news/seven-gb-prime-patients-now-participating-neuralink-trial)). Blindsight: Breakthrough designation, first human implant not confirmed as of this writing |
| Blackrock Neurotech | US | Utah-array hardware for human BCI | NeuroPort Array and NSP | Tether invested $200M and became majority owner (Apr 2024, [MassDevice](https://www.massdevice.com/bci-blackrock-neurotech-200m-investment-tether/)). Claims > 30,000 days of human recording with no device-related serious adverse events ([Blackrock](https://blackrockneurotech.com/products/neuroport-electrode/)). INTENT trial (Johns Hopkins–led, Blackrock collaborating; up to 8 arrays, recording + stimulation) registered, start est. Jan 2027 ([NCT07521930](https://clinicaltrials.gov/study/NCT07521930)) |
| Paradromics | US | High-data-rate implanted BCI for speech | Connexus | First-in-human recording during epilepsy surgery Jun 2025 ([Paradromics](https://www.paradromics.com/news/paradromics-completes-first-in-human-recording-with-the-connexus-brain-computer-interface)); FDA IDE Nov 2025; first Connect-One implant Jun 2026; real-time speech in first participant Sep 2026; FDA approval to use personal devices Aug 2026; "4+ years of stable recording" in preclinical studies, Oct 2026 ([Paradromics news](https://www.paradromics.com/news), [CBS Austin](https://cbsaustin.com/news/local/i-have-a-lot-to-say-austin-brain-implant-helps-patient-communicate-in-real-time)) |
| Synchron | US/Australia | Endovascular (stent) electrode | Stentrode | Not intracortical; see the [ECoG/sEEG folder](../ecog-seeg/) |
| Precision Neuroscience | US | Thin-film surface arrays | Layer 7 | 510(k) cleared Mar 2025 ([K242618](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm?ID=K242618)); says 100+ clinical study patients ([Precision](https://precisionneuro.io/)). Surface ECoG, so see the [ECoG/sEEG folder](../ecog-seeg/) |
| Science Corp. | US | Vision restoration, BCI | PRIMA subretinal implant (retinal, not cortical) | NEJM trial: 26 of 32 patients (81%) gained clinically meaningful acuity at 12 months ([Holz 2025](https://doi.org/10.1056/nejmoa2501396)); CE mark and European launch Jul 2026 ([Eyewire](https://eyewire.news/news/science-corporation-launches-prima-in-europe-following-ce-mark-for-vision-restoring-retinal-implant)); no FDA approval yet *unverified* |
| Axoft | US | Soft implantable probes | Fleuron material, soft BCI | 5-patient first-in-human study completed 2025 ([NCT06673264](https://clinicaltrials.gov/study/NCT06673264)); $55M Series A Apr 2026 ([HIT Consultant](https://hitconsultant.net/2026/04/30/axoft-series-a-funding-bio-inspired-ibci-fleuron/)) |
| Motif Neurotech | US | Skull-embedded micro-stimulator for depression (does not touch the brain) | DOT | FDA IDE Apr 2026 ([Patient Worthy](https://patientworthy.com/2026/04/28/motif-neurotech-gains-fda-clearance-to-launch-first-in-human-trial-of-implantable-bci-for-depression/)); RESONATE trial recruiting ([NCT07594483](https://clinicaltrials.gov/study/NCT07594483)) |
| IMEC / Neuropixels consortium | Belgium (with HHMI, Allen, UCL) | High-density silicon probes | Neuropixels 1.0, 2.0, NHP | Selling to research labs; NHP probe published 2025 ([Trautmann 2025](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12229894/), [neuropixels.org](https://www.neuropixels.org/)) |
| Medtronic | US/Ireland | DBS with LFP sensing | Percept with BrainSense, adaptive DBS | FDA approval of adaptive DBS Feb 2025 ([FDA](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpma/pma.cfm?id=P960009S478)) |
| Ripple Neuro, Intan, Plexon, SpikeGadgets, Open Ephys, Cambridge NeuroTech, NeuroNexus | US / UK | Research hardware | See section 2 | Selling |

## 5. Patents

| Patent number | Holder | Title/topic | Year | Why it matters |
|---|---|---|---|---|
| [US 5,215,088](https://patents.google.com/patent/US5215088A/en) | University of Utah (Normann) | Three-dimensional electrode device | Granted 1993 (filed 1989) | The Utah array: spire-shaped silicon electrodes on a rigid base. Basis of Blackrock's NeuroPort; now expired |
| [US 5,361,760](https://patents.google.com/patent/US5361760A/en) | University of Utah Research Foundation (Normann) | Impact inserter for a biomedical device | 1994 | Impact inserter for implanting arrays like the Utah array |
| [US 11,103,695](https://patents.google.com/patent/US11103695B2/en) | Neuralink | Device implantation using a cartridge | 2021 (priority 2018) | Thread/needle cartridge for robotic insertion, the R1 approach |
| [US 10,824,579](https://patents.google.com/patent/US10824579B2/en) | Neuralink | Network-on-chip for neurological data | 2020 (priority 2018) | On-implant data handling for thousands of channels |
| [US 10,653,330](https://patents.google.com/patent/US10653330B2/en) | Paradromics | System and methods for processing neural signals | 2020 | On-implant feature extraction to cut data rate, a core idea for high-channel wireless BCIs |
| [US 11,583,679](https://patents.google.com/patent/US11583679B2/en) | IMEC | Electrode arrangement switchable between stimulating and recording; neural probe | 2023 (priority 2019) | Switchable electrode arrays from the Neuropixels maker; whether it covers shipping Neuropixels products is *unverified* |
| [US 12,008,987](https://patents.google.com/patent/US12008987B2/en) | Stanford University | Decoding intended speech from neuronal activity | 2024 (priority 2018) | Licensed to Blackrock Neurotech and Neuralink, per author disclosures in [Wairagkar 2025](https://pubmed.ncbi.nlm.nih.gov/40506548/) |
| [US 12,449,901](https://patents.google.com/patent/US12449901B2/en) | Stanford University (Willett) | Decoding intended symbols from neural activity | 2025 | Covers handwriting-style symbol decoding |

## 6. Most-cited papers

Citation counts are from [OpenAlex](https://openalex.org/) on 2026-10-11 and differ from Google Scholar.

| Paper | Authors | Venue/year | Citations | Why it matters |
|---|---|---|---|---|
| [Neuronal population coding of movement direction](https://doi.org/10.1126/science.3749885) | Georgopoulos, Schwartz, Kettner | Science 1986 | 3,187 | Population vector: direction is read from many broadly tuned neurons |
| [Instant neural control of a movement signal](https://doi.org/10.1038/416141a) | Serruya, Hatsopoulos, Paninski et al. | Nature 2002 | 1,413 | Monkeys moved a cursor with motor-cortex activity in real time |
| [Direct cortical control of 3D neuroprosthetic devices](https://doi.org/10.1126/science.1070291) | Taylor, Helms Tillery, Schwartz | Science 2002 | 1,542 | 3D closed-loop control; showed that the brain adapts to the decoder |
| [Neuronal ensemble control of prosthetic devices by a human with tetraplegia](https://doi.org/10.1038/nature04970) | Hochberg et al. | Nature 2006 | 3,296 | First human Utah-array BCI (BrainGate) |
| [Cortical control of a prosthetic arm for self-feeding](https://doi.org/10.1038/nature06996) | Velliste et al. | Nature 2008 | 1,579 | Monkeys fed themselves with a robotic arm |
| [Reach and grasp by people with tetraplegia using a neurally controlled robotic arm](https://doi.org/10.1038/nature11076) | Hochberg et al. | Nature 2012 | 2,716 | Human robotic-arm control; a participant drank coffee |
| [A high-performance neural prosthesis enabled by control algorithm design](https://doi.org/10.1038/nn.3265) | Gilja et al. | Nat. Neurosci. 2012 | 563 | ReFIT Kalman filter: decoder design matters as much as signals |
| [Neural population dynamics during reaching](https://doi.org/10.1038/nature11129) | Churchland et al. | Nature 2012 | 1,653 | Rotational dynamics; the "dynamical systems" view of motor cortex |
| [The origin of extracellular fields and currents — EEG, ECoG, LFP and spikes](https://doi.org/10.1038/nrn3241) | Buzsáki, Anastassiou, Koch | Nat. Rev. Neurosci. 2012 | 4,249 | The standard explanation of where LFP comes from |
| [High-performance neuroprosthetic control by an individual with tetraplegia](https://doi.org/10.1016/S0140-6736(12)61816-9) | Collinger et al. | Lancet 2013 | 1,854 | 7D robotic-arm control |
| [Fast and accurate spike sorting of high-channel count probes with KiloSort](https://proceedings.neurips.cc/paper/2016/hash/1145a30ff80745b56fb0cecf65305017-Abstract.html) | Pachitariu, Steinmetz, Kadir, Carandini, Harris | NeurIPS 2016 | 751 (bioRxiv version) | Template-matching sorter that made dense-probe data usable |
| [Fully integrated silicon probes for high-density recording of neural activity](https://doi.org/10.1038/nature24636) | Jun et al. | Nature 2017 | 2,212 | Neuropixels |
| [Inferring single-trial neural population dynamics using sequential auto-encoders](https://doi.org/10.1038/s41592-018-0109-9) | Pandarinath et al. | Nat. Methods 2018 | 702 | LFADS, the first big deep-learning latent model for spikes |
| [High-performance brain-to-text communication via handwriting](https://doi.org/10.1038/s41586-021-03506-2) | Willett et al. | Nature 2021 | 970 | Handwriting BCI, 90 characters/min |
| [A high-performance speech neuroprosthesis](https://doi.org/10.1038/s41586-023-06377-x) | Willett et al. | Nature 2023 | 575 | First intracortical speech-to-text BCI, 62 words/min |
| [An accurate and rapidly calibrating speech neuroprosthesis](https://doi.org/10.1056/NEJMoa2314132) | Card et al. | NEJM 2024 | 238 | 97.5% accuracy in daily use; calibration in 30 minutes |

## 7. New achievements (2023–2026)

- **Speech to text.** Willett et al. (2023) decoded attempted speech at 62 words/min, with 9.1% word error rate (WER) on a 50-word vocabulary and 23.8% on 125,000 words ([Nature](https://doi.org/10.1038/s41586-023-06377-x)). Card et al. (2024) reached 99.6% accuracy on 50 words on day one after 30 minutes of calibration, 90.2% on 125,000 words on day two, and 97.5% sustained over 8.4 months at about 32 words/min for more than 248 hours of conversation ([NEJM](https://doi.org/10.1056/NEJMoa2314132)).
- **Speech to voice.** Wairagkar et al. (2025) synthesized the participant's own voice from 256 electrodes, with the neural-to-audio step done within 10 ms, and he could change intonation and sing short melodies ([Nature](https://doi.org/10.1038/s41586-025-09127-3), [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12369848/)).
- **Inner speech.** Kunz et al. (2025) decoded imagined sentences from motor cortex in 4 participants, with 26–54% WER on a 125,000-word vocabulary (tested in 2 of them). They also showed ways to stop a BCI from decoding private inner speech, such as a keyword "unlock" detected with 98.75% accuracy ([Cell](https://doi.org/10.1016/j.cell.2025.06.015), [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12360486/)).
- **Neuralink.** It went from 3 participants in 2024 to 21 by January 2026. Several users reach or exceed the 8–10 bits/s of able-bodied mouse users on the Webgrid task (one passed 10 bits/s in his first week), the "ten-finger keyboard" reaches 40 words/min, and one participant uses the device up to 17 hours a day ([Neuralink](https://neuralink.com/updates/two-years-of-telepathy/); company-reported, not peer reviewed). In October 2026 Neuralink reported self-supervised encoders pretrained on 50,000 hours of unlabeled data that kept decoders working for weeks without recalibration and set an 11.32 bits/s record ([Neuralink](https://neuralink.com/updates/pretraining-on-50000-hours/); company blog, not peer reviewed).
- **Paradromics.** Paradromics completed its first human recording in June 2025, got its FDA IDE in November 2025, and implanted the first Connect-One participant in June 2026. In September 2026 that participant, a woman with motor neuron disease, used it for real-time speech and text ([Paradromics](https://www.paradromics.com/news), [CBS Austin](https://cbsaustin.com/news/local/i-have-a-lot-to-say-austin-brain-implant-helps-patient-communicate-in-real-time)). WER and speed are not reported yet.
- **Fingers and games.** A person with tetraplegia controlled 4 finger degrees of freedom at 76 targets/min and flew a virtual quadcopter ([Willsey 2025](https://doi.org/10.1038/s41591-024-03341-8)).
- **Probes.** Neuropixels 1.0 NHP (4,416 sites on a 45 mm shank) brought dense recording to monkeys ([Trautmann 2025](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12229894/)), building on Neuropixels 2.0 (5,120 sites, the same neurons tracked for > 2 months, [Steinmetz 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8244810/)).
- **Pretrained neural-data models.**
  - NDT2 pretrains a spatiotemporal Transformer across sessions, subjects and tasks ([Ye 2023](https://doi.org/10.1101/2023.09.18.558113), NeurIPS 2023).
  - NDT3 pretrains on 2,000 hours of spiking data from over 30 monkeys and humans. It helps on 8 downstream decoding tasks, but the authors warn that scaling alone will not fix sensor variability ([Ye 2025](https://doi.org/10.52202/085713-3692)).
  - POYO tokenizes individual spikes and trains on 158 sessions and 27,373 units from 7 monkeys ([Azabou 2023](https://arxiv.org/abs/2310.16046)).
  - POYO+ extends this to multi-task decoding, but on two-photon calcium imaging from the Allen Brain Observatory, not spikes ([ICLR 2025](https://openreview.net/forum?id=IuU0wcO0mo)).
  - CEBRA learns joint behaviour-neural embeddings ([Schneider 2023](https://doi.org/10.1038/s41586-023-06031-6)).
- **Benchmarks.**
  - FALCON (NeurIPS 2024) tests whether decoders hold up across days, using 5 datasets: human reach-grasp (H1), human handwriting (H2), two monkey tasks (M1, M2) and songbird (B1) ([Karpowicz 2024](https://doi.org/10.1101/2024.09.15.613126)).
  - Brain-to-Text '25 is a Kaggle competition built on the Card 2024 data ([Kaggle](https://www.kaggle.com/competitions/brain-to-text-25), [repo](https://github.com/Neuroprosthetics-Lab/nejm-brain-to-text)).

## 8. Current state of the field

**Where intracortical recording is used today, and where it is still research**

| Maturity | Applications |
|---|---|
| Established | Neuropixels and silicon probes in animal neuroscience; Utah arrays in academic human trials (since 2004); LFP-sensing adaptive DBS (FDA-approved 2025) |
| Multi-site clinical trials | Cursor and computer control (BrainGate, Neuralink PRIME family), speech BCIs (BrainGate, Neuralink VOICE, Paradromics Connect-One), robotic arms (CONVOY), ICMS touch feedback |
| Early human / feasibility | Cortical vision prostheses (Fernández 2021 Utah-array study; Neuralink Blindsight, not yet confirmed implanted), soft probes (Axoft), real-time voice synthesis, inner-speech decoding |
| Research | Pretrained foundation models for spikes, closed-loop spike-based neuromodulation, neuropharmacology with brain-wide probes |
| Not yet | Any FDA-approved chronic implanted BCI on the market (all are investigational as of 2026-10) |

**Open problems**
- **Nonstationarity.** Neurons drift in and out of view day to day, so decoders degrade without recalibration. This is the main reason FALCON exists. Neuralink's thread retraction was an extreme case ([FALCON](https://doi.org/10.1101/2024.09.15.613126), [Neuralink](https://neuralink.com/updates/prime-study-progress-update-second-participant/)).
- **Longevity and biocompatibility.** Rigid arrays lose signal over months to years (mean 622 days in [Sponheim 2021](https://doi.org/10.1088/1741-2552/ac3eaf)). Soft and flexible probes (Neuralink, Axoft) are trying to fix this.
- **Variability between people.** Neuralink reports performance differences linked to anatomy and disease stage ([Neuralink](https://neuralink.com/updates/two-years-of-telepathy/)). Some arrays record almost nothing (e.g. one participant's 55b arrays in [Kunz 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12360486/)).
- **Small n.** Most human results come from 1–4 participants, so it is hard to tell how well a method generalizes.
- **Power and bandwidth.** Wireless implants cannot send 30 kHz raw data from thousands of channels. On-implant features (threshold crossings, SBP, spike detection) and compression are required ([Nason 2020](https://doi.org/10.1038/s41551-020-0591-0), [Paradromics patent](https://patents.google.com/patent/US10653330B2/en)).
- **Scaling laws are unclear.** NDT3 found that bigger autoregressive Transformers do not overcome sensor variability ([Ye 2025](https://doi.org/10.52202/085713-3692)).
- **Privacy and ethics.** Inner speech is decodable, so BCIs need guards against unintended output ([Kunz 2025](https://doi.org/10.1016/j.cell.2025.06.015)).

**Where an AI engineer can contribute.**
- Sequence models with language-model fusion for speech and handwriting (CTC/RNN/Transformer → n-gram or LLM rescoring); Brain-to-Text '25 is a ready-made entry point.
- Self-supervised pretraining across sessions and subjects, and tokenizing spikes (NDT, POYO, torch_brain).
- Few-shot and zero-shot recalibration, scored honestly on FALCON's held-out days.
- Latent dynamics models (LFADS-style) for denoising.
- Low-latency, low-power inference on implants.
- Better spike sorting and drift correction.
- Tooling: NWB conversion, real-time pipelines (BRAND).

## 9. Public datasets

| Dataset | Content | Size | Link |
|---|---|---|---|
| NLB MC_Maze (+ Large/Medium/Small) | Monkey M1/PMd during delayed reaching | 694 MB (MC_Maze) | [DANDI 000128](https://dandiarchive.org/dandiset/000128) |
| NLB MC_RTT, Area2_Bump, DMFC_RSG | Self-paced reaching; somatosensory area 2; timing task | 51 MB, 1.8 GB, 16 MB | [000129](https://dandiarchive.org/dandiset/000129), [000127](https://dandiarchive.org/dandiset/000127), [000130](https://dandiarchive.org/dandiset/000130) |
| FALCON H1 / H2 / M1 / M2 / B1 | Human reach-grasp, human handwriting, monkey reach-grasp and finger, songbird Neuropixels; split across days | 0.1 / 1.2 / 0.3 / 15.9 / 1.3 GB | [000954](https://dandiarchive.org/dandiset/000954), [000950](https://dandiarchive.org/dandiset/000950), [000941](https://dandiarchive.org/dandiset/000941), [000953](https://dandiarchive.org/dandiset/000953), [001046](https://dandiarchive.org/dandiset/001046) |
| Willett 2023 speech | Human speech BCI, TC + SBP features, 128 electrodes *unverified* | — | [Dryad](https://doi.org/10.5061/dryad.x69p8czpq) |
| Card 2024 speech (T15) | 10,948 sentences, 45 sessions over 20 months, 512 features, 20 ms bins | 11.6 GB | [Dryad](https://doi.org/10.5061/dryad.dncjsxm85) |
| Willett 2021 handwriting | Attempted handwriting, Utah arrays | 1.4 GB | [Dryad](https://doi.org/10.5061/dryad.wh70rxwmv) |
| O'Doherty / Sabes reaching | Monkey self-paced reaching, sensorimotor cortex | — | [Zenodo](https://doi.org/10.5281/zenodo.583331) |
| Paulk 2022 human Neuropixels | Intraoperative human cortex recordings | — | [Dryad](https://doi.org/10.5061/dryad.d2547d840) |
| IBL Brain-Wide Map | Mouse Neuropixels across the brain, standardized decision task | ~49.7 TB | [DANDI 000409](https://dandiarchive.org/dandiset/000409) |
| Allen Visual Coding – Neuropixels | Mouse visual system, many stimuli | ~478 GB | [DANDI 000021](https://dandiarchive.org/dandiset/000021) |

Sizes are from the DANDI and DataCite APIs (checked 2026-10-11).

Full specifications for each dataset, and tables of published results on them, are in [DATASETS.md](DATASETS.md).

## 10. GitHub repositories

Stars and dates checked via the GitHub API on 2026-10-11.

"Custom" means GitHub could not detect a standard license (`NOASSERTION`), so read the repo's LICENSE file before reusing the code. "—" means no license file or no detected language.

**Spike sorting**

| Repo | What it does | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [MouseLand/Kilosort](https://github.com/MouseLand/Kilosort) | Kilosort4: the most-used template-matching sorter for dense probes, with drift correction. Needs a GPU | Python | 631 | 2026-09 | GPL-3.0 |
| [SpikeInterface/spikeinterface](https://github.com/SpikeInterface/spikeinterface) | One API to read any format, preprocess, run many sorters, compare them and compute quality metrics. Start here | Python | 859 | 2026-10 | MIT |
| [flatironinstitute/mountainsort5](https://github.com/flatironinstitute/mountainsort5) | MountainSort 5, a CPU-friendly sorter | Python | 64 | 2026-10 | Apache-2.0 |
| [cortex-lab/phy](https://github.com/cortex-lab/phy) | GUI to inspect and manually curate sorting results (Kilosort output) | Python | 433 | 2026-10 | BSD-3-Clause |
| [SpikeInterface/probeinterface](https://github.com/SpikeInterface/probeinterface) | Describes probe geometry and wiring (Neuropixels, Cambridge NeuroTech, NeuroNexus...) | Python | 86 | 2026-10 | MIT |
| [flatironinstitute/spikeforest](https://github.com/flatironinstitute/spikeforest) | Benchmark of sorters against ground-truth recordings | Python | 33 | 2026-10 | Apache-2.0 |
| [AllenInstitute/ecephys_spike_sorting](https://github.com/AllenInstitute/ecephys_spike_sorting) | Allen's Neuropixels processing pipeline around Kilosort | Python | 130 | 2024-08 | Custom |

**Data tools and acquisition**

| Repo | What it does | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [NeurodataWithoutBorders/pynwb](https://github.com/NeurodataWithoutBorders/pynwb) | Read and write NWB files in Python | Python | 225 | 2026-10 | Custom |
| [NeurodataWithoutBorders/matnwb](https://github.com/NeurodataWithoutBorders/matnwb) | NWB for MATLAB | MATLAB | 62 | 2026-10 | BSD-2-Clause |
| [NeurodataWithoutBorders/nwbinspector](https://github.com/NeurodataWithoutBorders/nwbinspector) | Checks NWB files against best practices before upload | Python | 24 | 2026-10 | Custom |
| [catalystneuro/neuroconv](https://github.com/catalystneuro/neuroconv) | Converts proprietary formats (Blackrock, SpikeGLX, Open Ephys, ...) to NWB | Python | 81 | 2026-10 | BSD-3-Clause |
| [dandi/dandi-cli](https://github.com/dandi/dandi-cli) | Download and upload DANDI datasets (`dandi download DANDI:000128`) | Python | 29 | 2026-10 | Apache-2.0 |
| [NeuralEnsemble/python-neo](https://github.com/NeuralEnsemble/python-neo) | Readers for dozens of ephys formats; used by SpikeInterface | Python | 363 | 2026-10 | BSD-3-Clause |
| [open-ephys/plugin-GUI](https://github.com/open-ephys/plugin-GUI) | Open Ephys acquisition GUI | C++ | 246 | 2026-09 | GPL-3.0 |
| [open-ephys/open-ephys-python-tools](https://github.com/open-ephys/open-ephys-python-tools) | Load Open Ephys recordings in Python | Python | 48 | 2025-11 | MIT |
| [billkarsh/SpikeGLX](https://github.com/billkarsh/SpikeGLX) | SpikeGLX acquisition software for Neuropixels | HTML | 112 | 2026-10 | Custom |
| [jenniferColonell/SpikeGLX_Datafile_Tools](https://github.com/jenniferColonell/SpikeGLX_Datafile_Tools) | Example readers for SpikeGLX `.bin`/`.meta` (MATLAB and Python) | MATLAB | 16 | 2026-06 | — |
| [BlackrockNeurotech/NPMK](https://github.com/BlackrockNeurotech/NPMK) | Official MATLAB toolkit for `.nev`/`.nsX` files | MATLAB | 54 | 2025-12 | — |
| [BlackrockNeurotech/Python-Utilities](https://github.com/BlackrockNeurotech/Python-Utilities) | Python scripts to load Blackrock files | Python | 42 | 2025-10 | — |
| [int-brain-lab/ibllib](https://github.com/int-brain-lab/ibllib) | Access and process IBL Brain-Wide Map data | Python | 69 | 2026-10 | MIT |
| [AllenInstitute/AllenSDK](https://github.com/AllenInstitute/AllenSDK) | Access Allen Brain Observatory data, including Visual Coding Neuropixels | Jupyter Notebook | 399 | 2026-07 | Custom |
| [brandbci/brand](https://github.com/brandbci/brand) | BRAND: real-time asynchronous decoding framework used in UC Davis speech BCIs | Python | 50 | 2026-09 | MIT |

**Models and papers with code**

| Repo | What it does | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [arsedler9/lfads-torch](https://github.com/arsedler9/lfads-torch) | PyTorch LFADS and AutoLFADS; the practical way to run LFADS today | Jupyter Notebook | 143 | 2026-03 | Custom |
| [google-research/computation-thru-dynamics](https://github.com/google-research/computation-thru-dynamics) | JAX LFADS and dynamical-systems tutorials. Archived | Jupyter Notebook | 394 | 2021-05 | Apache-2.0, archived |
| [lfads/lfads-run-manager](https://github.com/lfads/lfads-run-manager) | MATLAB interface for original LFADS | MATLAB | 52 | 2021-12 | Apache-2.0 |
| [snel-repo/neural-data-transformers](https://github.com/snel-repo/neural-data-transformers) | Original NDT (Transformer for spiking activity) | Python | 87 | 2022-02 | Unlicense |
| [joel99/context_general_bci](https://github.com/joel99/context_general_bci) | NDT2 multi-context pretraining | Python | 36 | 2025-07 | MIT |
| [joel99/ndt3](https://github.com/joel99/ndt3) | NDT3 pretrained generalist motor decoder | Python | 37 | 2026-01 | MIT |
| [trungle93/STNDT](https://github.com/trungle93/STNDT) | Spatiotemporal NDT with contrastive loss (NLB entry) | Python | 15 | 2023-09 | Custom |
| [neuro-galaxy/torch_brain](https://github.com/neuro-galaxy/torch_brain) | Library for POYO/POYO+-style models on neural data | Python | 101 | 2026-10 | Apache-2.0 |
| [neuro-galaxy/brainsets](https://github.com/neuro-galaxy/brainsets) | Preprocessing pipelines that turn public datasets into training-ready form for torch_brain | Python | 43 | 2026-06 | Apache-2.0 |
| [AdaptiveMotorControlLab/CEBRA](https://github.com/AdaptiveMotorControlLab/CEBRA) | Contrastive joint behaviour-neural embeddings | Python | 1123 | 2026-09 | Custom |
| [fwillett/speechBCI](https://github.com/fwillett/speechBCI) | Willett 2023 RNN + language-model decoder; 18.8% WER (3-gram) and 13.7% (5-gram + OPT) on its test split | Roff | 218 | 2025-06 | — |
| [cffan/neural_seq_decoder](https://github.com/cffan/neural_seq_decoder) | PyTorch port of the speechBCI RNN decoder | Jupyter Notebook | 46 | 2024-08 | — |
| [Neuroprosthetics-Lab/nejm-brain-to-text](https://github.com/Neuroprosthetics-Lab/nejm-brain-to-text) | Card 2024 code, data loaders and Brain-to-Text '25 baseline | Roff | 130 | 2025-07 | — |
| [fwillett/handwritingBCI](https://github.com/fwillett/handwritingBCI) | Willett 2021 handwriting decoder | Jupyter Notebook | 387 | 2023-06 | Custom |

**Benchmarks**

| Repo | What it does | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [neurallatents/nlb_tools](https://github.com/neurallatents/nlb_tools) | Loading, splitting and scoring for the Neural Latents Benchmark | Python | 72 | 2026-01 | MIT |
| [snel-repo/falcon-challenge](https://github.com/snel-repo/falcon-challenge) | FALCON evaluation package (`pip install falcon-challenge`) and Docker submission | Jupyter Notebook | 28 | 2025-11 | MIT |

**Curated lists**

| Repo | What it does | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [NeuroTechX/awesome-bci](https://github.com/NeuroTechX/awesome-bci) | Curated BCI resources (papers, datasets, software) | — | 1551 | 2026-10 | — |
| [analyticalmonk/awesome-neuroscience](https://github.com/analyticalmonk/awesome-neuroscience) | Curated neuroscience libraries and software | — | 1732 | 2026-06 | — |
