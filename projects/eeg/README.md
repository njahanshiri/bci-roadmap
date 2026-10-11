# EEG (Electroencephalography)

Electroencephalography records the brain's electrical activity with electrodes on the scalp. It is the oldest and most widely used way to measure brain activity non-invasively, first reported in humans by Hans Berger in 1929 ([Berger 1929](https://doi.org/10.1007/BF01797193)). Today it is a clinical standard for epilepsy, ICU seizure monitoring and sleep studies, the main signal for non-invasive brain-computer interfaces (BCIs), and a growing consumer wearable category. Since 2024 it has also become a target for large pretrained "foundation models" ([LaBraM, ICLR 2024](https://arxiv.org/abs/2405.18765), [EEG Foundation Challenge, NeurIPS 2025](https://arxiv.org/abs/2506.19141)).

Starter notebook: [01_load_and_explore_eeg.ipynb](01_load_and_explore_eeg.ipynb) loads PhysioNet motor-imagery EEG with MNE, plots the spectrum, filters, epochs, and shows mu/beta desynchronization over C3/C4.

Items marked *unverified* could not be confirmed from a source. Cells marked "—" mean the manufacturer did not publish the spec, or I could not find it.

## 1. The data

**What is measured.** Scalp EEG is mostly the sum of synaptic (postsynaptic) currents in large populations of cortical pyramidal neurons. These neurons are lined up in parallel, so when many of them are active together their small current dipoles add up into a field strong enough to reach the scalp. Single spikes contribute little. On the way out, the fields spread through brain, cerebrospinal fluid, skull and scalp. This *volume conduction* smears them, so every electrode picks up a mix of many sources, and EEG has good timing (milliseconds) but poor spatial resolution ([Buzsáki, Anastassiou & Koch 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC4907333/)).

**Rhythms.** Band edges below follow the International Federation of Clinical Neurophysiology (IFCN) glossary ([Kane et al. 2017](https://discovery.ucl.ac.uk/id/eprint/10076640/)).

| Band | Range | Notes |
|---|---|---|
| Delta | 0.1 to <4 Hz (in practice from 0.5 Hz) | Slow waves; widespread delta grows in Alzheimer's disease ([Babiloni 2021](https://doi.org/10.1002/alz.12311)) |
| Theta | 4 to <8 Hz | Theta/beta ratio is the basis of the NEBA ADHD aid ([Healio](https://www.healio.com/news/psychiatry/20130725/fda-approved-device-testing-brain-function-to-assess-for-adhd)) |
| Alpha | 8–13 Hz | Posterior, best seen with eyes closed; mostly below 50 µV in adults ([Kane 2017](https://discovery.ucl.ac.uk/id/eprint/10076640/)) |
| Mu | 7–11 Hz | Central/centro-parietal; blocked by contralateral movement or even the thought of moving. This is the motor-imagery BCI signal |
| Beta | 14–30 Hz | Fronto-central; desynchronizes (drops) during movement and motor imagery ([Pfurtscheller & Lopes da Silva 1999](https://doi.org/10.1016/S1388-2457(99)00141-8)) |
| Gamma | >30 to 80 Hz | The glossary warns not to cut high frequencies too aggressively when displaying EEG |

**Event-related signals.** Averaging EEG time-locked to an event gives an *event-related potential* (ERP). The best known is the P300, a positive wave about 300 ms after a rare, relevant stimulus ([Polich 2007](https://doi.org/10.1016/j.clinph.2007.04.019)). It drives the P300 speller ([Farwell & Donchin 1988](https://doi.org/10.1016/0013-4694(88)90149-6)). Other BCI signals are event-related desynchronization/synchronization (ERD/ERS), a drop or rise in band power during movement or imagery ([Pfurtscheller & Lopes da Silva 1999](https://doi.org/10.1016/S1388-2457(99)00141-8)); steady-state visual evoked potentials (SSVEP) at the frequency of a flickering target ([Chen et al. 2015](https://doi.org/10.1073/pnas.1508080112)); code-modulated VEPs (c-VEP), driven by pseudo-random flicker codes ([Martínez-Cagigal 2021](https://doi.org/10.1088/1741-2552/ac38cf)); and error-related potentials (ErrP), which appear when the user sees the system make a mistake ([Chavarriaga 2014](https://doi.org/10.3389/fnins.2014.00208)).

**Montages and electrode systems**

| System | What it is | Source |
|---|---|---|
| 10-20 | Electrodes at 10% and 20% of skull distances between nasion, inion and preauricular points. Clinical standard | [Jasper 1958](https://doi.org/10.1016/0013-4694(58)90053-1), [CBRET 2016 standard](https://cbret.org/wp-content/uploads/2020/06/Minimal-Technical-Standards-Routine-Adult-2016.pdf) |
| 10-10 | 10% spacing extension proposed in 1985; used by 64-channel research caps (e.g. PhysioNet EEGMMIDB) | [Oostenveld & Praamstra 2001](https://doi.org/10.1016/S1388-2457(00)00527-7), [PhysioNet](https://physionet.org/content/eegmmidb/1.0.0/) |
| 10-5 | 5% spacing, up to 345 named positions, for high-density EEG | [Oostenveld & Praamstra 2001](https://pubmed.ncbi.nlm.nih.gov/11275545/), [FieldTrip guide](https://www.fieldtriptoolbox.org/getting_started/1020/) |
| Referential vs bipolar | Clinical reading uses both; bipolar chains run anterior to posterior | [CBRET 2016](https://cbret.org/wp-content/uploads/2020/06/Minimal-Technical-Standards-Routine-Adult-2016.pdf) |

**Electrodes**

| Type | How | Trade-off | Examples |
|---|---|---|---|
| Wet (gel) | Ag/AgCl or gold cups with conductive gel; skin often abraded | Best signal and lowest impedance; slow to set up and needs a technician | Clinical standard ([CBRET 2016](https://cbret.org/wp-content/uploads/2020/06/Minimal-Technical-Standards-Routine-Adult-2016.pdf)); Ceribell disposable headband with gel reservoirs ([FDA K232052](https://fda.innolitics.com/device/K232052)) |
| Saline | Felt pads soaked in saline | Quick, but pads dry out over hours | Emotiv EPOC X ([Emotiv](https://www.emotiv.com/epoc-x)) |
| Semi-dry | Hydrophilic semi-dry polymer wetted with a few drops of solution | Between wet and dry | Emotiv Insight ([Emotiv](https://www.emotiv.com/insight)) |
| Dry | Pins, pads or flexible polymer contacts, usually with active (buffered) electronics | Fast, no gel; higher contact impedance and more motion artifact ([Lopez-Gordo 2014](https://doi.org/10.3390/s140712847)) | Zeto, DSI-24, CGX, Neurosity Crown (section 2) |
| In-ear / around-ear | Electrodes in earbuds or headphone ear pads | Very wearable; few channels far from most cortex | IDUN Guardian, Emotiv MN8, Neurable MW75 Neuro (section 2) |
| Active vs passive | Active electrodes put an amplifier at the electrode, so they tolerate higher impedance | — | BioSemi active electrodes have 300 MΩ input impedance ([BioSemi](https://www.biosemi.com/activetwo_full_specs.htm)) |

**Signal characteristics**

| Property | Typical value | Source |
|---|---|---|
| Amplitude | Tens of microvolts; adult alpha and mu mostly below 50 µV | [Kane 2017](https://discovery.ucl.ac.uk/id/eprint/10076640/) |
| Frequency band | Clinical display filter 1–70 Hz or higher; gamma defined up to 80 Hz | [CBRET 2016](https://cbret.org/wp-content/uploads/2020/06/Minimal-Technical-Standards-Routine-Adult-2016.pdf), [Kane 2017](https://discovery.ucl.ac.uk/id/eprint/10076640/) |
| Sampling rate | Clinical minimum 200 samples/s per channel at ≥12 bits. Common datasets: 160 Hz (EEGMMIDB), 250 Hz (BCI IV 2a), 256 Hz (CHB-MIT). Consumer: 128–256 Hz. Research amplifiers: 16 kHz (BioSemi) to 100 kHz (actiCHamp Plus, 32 ch) | [CBRET 2016](https://cbret.org/wp-content/uploads/2020/06/Minimal-Technical-Standards-Routine-Adult-2016.pdf), section 9, section 2 |
| Channels | Clinical amplifiers: at least 24, preferably 32 channels. Research: 32–256 | [CBRET 2016](https://cbret.org/wp-content/uploads/2020/06/Minimal-Technical-Standards-Routine-Adult-2016.pdf), [eego mylab](https://www.ant-neuro.com/eegomylab) |
| Impedance | Balanced, 100–5000 Ω; up to 10 kΩ acceptable for prolonged recordings (EMU, cEEG), if balanced | [CBRET 2016](https://cbret.org/wp-content/uploads/2020/06/Minimal-Technical-Standards-Routine-Adult-2016.pdf) |
| Main noise and artifacts | Eye blinks and movements (EOG), muscle (EMG, e.g. chewing, jaw), heartbeat (ECG), electrode pops, shivering and motion, power-line noise. The TUH artifact corpus labels eye movement, chewing, shivering, electrode and muscle artifacts. Clinical standards discourage the 60 Hz notch in routine recording | [TUH EEG](https://isip.piconepress.com/projects/nedc/html/tuh_eeg/), [CBRET 2016](https://cbret.org/wp-content/uploads/2020/06/Minimal-Technical-Standards-Routine-Adult-2016.pdf) |
| Artifact removal | Independent component analysis (ICA) separates eye and muscle sources; ICLabel/mne-icalabel classify components; autoreject sets rejection thresholds automatically | [Jung 2000](https://doi.org/10.1111/1469-8986.3720163), [Jas 2017](https://doi.org/10.1016/j.neuroimage.2017.06.030) |

**Features.** Classic pipelines compute band power and band ratios per channel, ERP amplitudes and latencies, and connectivity between channels. For motor imagery, Common Spatial Patterns (CSP) learns spatial filters that maximize the variance difference between two classes ([Blankertz 2008](https://doi.org/10.1109/MSP.2008.4408441)). Riemannian methods classify channel covariance matrices directly and are a strong, simple baseline ([Barachant 2012](https://doi.org/10.1109/TBME.2011.2172210)). Sleep pipelines add spindle and slow-wave features ([YASA, Vallat & Walker 2021](https://doi.org/10.7554/eLife.70092)). Deep learning works on the raw multichannel signal with compact CNNs ([Schirrmeister 2017](https://doi.org/10.1002/hbm.23730), [EEGNet](https://doi.org/10.1088/1741-2552/aace8c)) and, since 2023, transformers pretrained on thousands of hours (section 7). Reviews: [Lotte 2018](https://doi.org/10.1088/1741-2552/aab2f2) (classifiers), [Roy 2019](https://doi.org/10.1088/1741-2552/ab260c) (deep learning).

**File formats**

| Format | Extension | Notes | Source |
|---|---|---|---|
| EDF / EDF+ | `.edf` | European Data Format, 1992; EDF+ (2003) adds annotations. Clinical and PhysioNet default | [Kemp 1992](https://doi.org/10.1016/0013-4694(92)90009-7), [Kemp & Olivan 2003](https://doi.org/10.1016/S1388-2457(03)00123-8), [edfplus.info](https://www.edfplus.info/) |
| BDF | `.bdf` | BioSemi's 24-bit version of EDF | [BioSemi](https://www.biosemi.com/faq/file_format.htm) |
| BrainVision | `.vhdr` + `.vmrk` + `.eeg` | Header, marker and binary data files (Brain Products) | [Brain Products](https://www.brainproducts.com/support-resources/brainvision-core-data-format-1-0/) |
| FIF | `.fif` | Native MNE-Python / Neuromag format | [MNE](https://mne.tools/stable/auto_tutorials/io/20_reading_eeg_data.html) |
| XDF | `.xdf` | Lab Streaming Layer recordings: many streams (EEG, markers, eye tracking) with timestamps | [XDF spec](https://github.com/sccn/xdf/wiki/Specifications) |
| EEGLAB SET | `.set` (+ `.fdt`) | MATLAB structure used by EEGLAB | [EEGLAB](https://eeglab.org/tutorials/ConceptsGuide/Data_Structures.html) |
| BIDS-EEG | folder layout + sidecar JSON/TSV | A dataset standard, not a binary format; data files are EDF, BDF, BrainVision or SET. Used by the NeurIPS 2025 challenge | [Pernet 2019](https://doi.org/10.1038/s41597-019-0104-8), [BIDS spec](https://bids-specification.readthedocs.io/en/stable/modality-specific-files/electroencephalography.html) |

## 2. Devices and specifications

**Research-grade**

| Device | Company | Type | Channels | Sampling rate | Resolution | Electrodes | Connectivity | Typical use | Status/price |
|---|---|---|---|---|---|---|---|---|---|
| ActiveTwo Mk2 | BioSemi | Wired amplifier | Up to 280 (152 at 16 kHz) | 2048–16384 Hz | 24-bit | Active Ag/AgCl | USB2, optical triggers | High-density ERP, EEG+EMG | Current ([BioSemi](https://www.biosemi.com/activetwo_full_specs.htm)) |
| actiCHamp Plus | Brain Products | Wired modular amplifier | 32–160 + 8 AUX | Up to 100 kHz (32 ch), 50 kHz (64 ch), 25 kHz (96–160 ch) | 24-bit | — | — | High-density ERP | Current ([Brain Products](https://www.brainproducts.com/solutions/actichamp/)) |
| LiveAmp 8/16/32/64 | Brain Products | Wireless mobile amplifier | 8 / 16 / 32 / 64 | 250 / 500 / 1000 Hz (1 kHz up to 32 ch) | 24-bit | — | Wireless (10 m indoor), memory card | Mobile EEG | Current ([Brain Products](https://www.brainproducts.com/solutions/liveamp/)) |
| g.USBamp RESEARCH | g.tec | Wired biosignal amplifier | 16 | Up to 38.4 kHz | 24-bit | — | USB | BCI and invasive research | Current ([g.tec](https://www.gtec.at/product/gusbamp-research-16-channel-biosignal-amplifier/)) |
| g.Nautilus Research | g.tec | Wireless headset | 8 / 16 / 32 / 64 | 250 or 500 Hz (64 ch: 250 Hz) | 24-bit | g.SAHARA hybrid dry/gel, or gel | 2.4 GHz | Mobile BCI | Current ([g.tec](https://www.gtec.at/product/g-nautilus-research/)) |
| eego mylab | ANT Neuro | Wired high-density amplifier | 32–256 + up to 24 bipolar | Up to 16,384 Hz | 24-bit | — | USB-C 3.0 | High-density research | Current ([ANT Neuro](https://www.ant-neuro.com/eegomylab)) |
| Enobio 20 / 32 | Neuroelectrics | Wireless | 20 / 32 | 500 SPS | 24-bit | — | Wi-Fi or USB, microSD | Mobile research | Current ([datasheet](https://neuroelectrics.com/_files/ugd/408c5c_646fbb4757984993abbbe9ff1ca1f47f.pdf)) |
| Starstim 8 / 20 / 32 | Neuroelectrics | Brain stimulation (tES) + EEG | Models 8, 20, 32 | — | — | — | Wireless | Stimulation with simultaneous EEG | Current ([Neuroelectrics](https://www.neuroelectrics.com/solutions/starstim)) |
| DSI-24 | Wearable Sensing | Dry wireless headset | 19 scalp + 2 ear clips + 3 aux | 300 Hz (600 Hz upgrade) | 16-bit | Active dry | Bluetooth, 10 m | Fast research EEG | Quote only ([Wearable Sensing](https://wearablesensing.com/dsi-24/)) |
| Smarting PRO / PRO X | mBrainTrain | Mobile amplifier | 32 / 64 | Up to 2000 Hz / 250–4000 Hz | 24-bit (PRO) | — | Bluetooth 5.0, SD card | Mobile EEG, hyperscanning | Current ([mBrainTrain](https://support.mbraintrain.com/faq/supported-sampling-rates), [Circuit Cellar](https://circuitcellar.com/newsletter/next-generation-innovation-smartingpro-portable-eeg-uses-bluetooth-5-0/)) |
| Quick-32r | CGX (Cognionics) | Dry wireless headset | 32 EEG + 2 ExG | 500 Hz | 24-bit | Dry (Drypad or Flex) | BLE, 10 m; 8 h on AA batteries | Fast research EEG | Quote only; sold with Brain Products ([CGX](https://cgxcrunchbox.com/store/product/quick-32r-quick-32r), [Brain Products](https://www.brainproducts.com/solutions/cgx-quick/)) |
| Galea | OpenBCI | VR/XR headset with EEG, EMG, EDA, PPG, eye tracking | — | — | — | — | — | Neuro-VR research | $42,980, listed as sold out ([OpenBCI shop](https://shop.openbci.com/products/galea)) |

**Clinical**

| Device | Company | Type | Channels | Sampling rate | Resolution | Electrodes | Connectivity | Typical use | Status/price |
|---|---|---|---|---|---|---|---|---|---|
| EEG-1200 Neurofax | Nihon Kohden | Clinical EEG system | 32; up to 256 with JE-120A junction box | Up to 10 kHz | 16-bit *unverified* | — | — | Routine EEG, long-term epilepsy monitoring, ICU, sleep | FDA K080546 ([FDA data](https://fda.innolitics.com/device/K080546); 256 ch and 10 kHz via JE-120A: [Wang 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11175507/)) |
| Quantum | Natus | Long-term monitoring amplifier | 128–256 | Up to 16,384 Hz | 24-bit | — | — | Epilepsy monitoring units | FDA K143440 ([FDA data](https://fda.innolitics.com/device/K143440)) |
| BrainWatch | Natus | Point-of-care EEG; Persyst seizure detection *unverified* (510(k) summary says no automated alerts) | 10 | — | — | — | — | ED/ICU seizure and status epilepticus | Cleared Nov 2024, FDA K242930 ([FDA data](https://fda.innolitics.com/device/K242930), [Practical Neurology](https://practicalneurology.com/news/the-fda-clears-an-eeg-decision-support-tool-that-identifies-seizure-and-status-epilepticus)) |
| Grael 4K | Compumedics | EEG/PSG amplifier | 32 referential + 16 differential, plus PSG sensor inputs | 16,384 sps internal; saved at 256–4096 sps | 24-bit | — | Power-over-Ethernet | EEG and sleep labs | Current ([spec sheet](https://www.compumedics.com.au/wp-content/uploads/2016/08/AI936-01-Grael-4K-specs-2023.pdf)) |
| Ceribell System (Pocket EEG + Instant EEG Headband) | Ceribell | Rapid-response EEG with Clarity AI | 10 electrodes | — | — | Disposable passive Ag/AgCl with gel reservoirs | — | ICU/ED seizure detection, from preterm neonates to adults | Setup under 10 minutes; first cleared 2017; neonatal Clarity cleared Nov 2025 ([FDA K232052](https://fda.innolitics.com/device/K232052), [Medical Device Network](https://www.medicaldevice-network.com/news/ceribell-monitoring-alerting-system/), [Contemporary Pediatrics](https://www.contemporarypediatrics.com/view/fda-grants-510-k-clearance-for-clarity-algorithm-to-detect-electrographic-seizures-in-newborns)) |
| WR19 (zEEG) / Zeto ONE | Zeto | Dry wireless clinical headset | 19 | 500 Hz | 24-bit | Active dry Ag/AgCl | Wi-Fi | Routine and ICU EEG | WR19 cleared Apr 2018 (K172735); Zeto ONE cleared 2024 ([FDA data](https://fda.innolitics.com/device/K172735), [Medical Device Network](https://www.medicaldevice-network.com/news/zeto-wins-fda-clearance-for-one-eeg-system/)) |
| REMI | Epitel | Wearable wireless EEG with Vigilenz AI | — | — | — | — | Wireless | Ambulatory and bedside seizure detection | Four FDA 510(k)s by Oct 2024 ([BusinessWire](https://www.businesswire.com/news/home/20241021071646/en/Epitel-Expands-AI-Portfolio-With-A-Fourth-FDA-510k-Clearance-for-REMI)) |

**Consumer / wearable**

| Device | Company | Type | Channels | Sampling rate | Resolution | Electrodes | Connectivity | Typical use | Status/price |
|---|---|---|---|---|---|---|---|---|---|
| EPOC X | Emotiv | Headset | 14 + 2 references | 128 or 256 SPS (2048 Hz internal) | 14 or 16-bit | Saline felt pads | BLE 5.0 or USB receiver | Research, BCI | Current; price on shop ([Emotiv](https://www.emotiv.com/epoc-x)) |
| Insight | Emotiv | Headset | 5 (AF3, AF4, T7, T8, Pz) | 128 SPS | 16-bit | Semi-dry polymer | BLE | Research, wellness | Current ([Emotiv](https://www.emotiv.com/insight)) |
| MN8 | Emotiv | EEG earbuds | 2 | 128 Hz (8 kHz internal) | 14-bit | Dry elastomer earbuds | — | — | Current ([manual](https://emotiv.gitbook.io/mn8-user-manual/introduction/introduction-to-mn8)) |
| Muse 2 / Muse S (classic firmware) | Interaxon | Headband | 4 (TP9, AF7, AF8, TP10) | 256 Hz | 12-bit | — | — | Meditation, sleep | Current ([spec sheet](https://ifelldh.tec.mx/sites/g/files/vgjovo1101/files/Muse_2_Specifications.pdf), citing [Acta IMEKO](https://doi.org/10.21014/acta_imeko.v10i4.1180)) |
| Muse S Athena | Interaxon | Headband, EEG + fNIRS + PPG | 7 EEG sensors | — | — | — | — | Sleep, focus, meditation | $474.99 sale price on product page, Oct 2026 ([Muse](https://choosemuse.com/products/muse-s-athena)) |
| Crown | Neurosity | Headset | 8 (CP3, C3, F5, PO3, PO4, F6, C4, CP4) | 256 Hz | — | Flexible dry Ag/AgCl | BLE 4.2, Wi-Fi | Focus tracking, developer SDK | Current ([Neurosity](https://neurosity.co/tech-specs)) |
| Dreem 3S (now Waveband) | Beacon Biosignals | Sleep headband | 6 electrodes | — | — | — | — | Home sleep staging for clinical trials | FDA 510(k) Aug 2023, K223539; announced Sep 2023 ([AASM](https://aasm.org/fda-clears-ai-assisted-sleep-monitoring-device-dreem-3s/), [Sleep Review](https://sleepreviewmag.com/sleep-diagnostics/connected-care/remote-monitoring/beacon-biosignals-bolsters-sleep-medicine-research-acquisition-dreem/)) |
| Guardian 4 | IDUN | In-ear EEG earbuds | Dual-channel per earpiece | — | — | Dry "Dryode" | Wireless (Snapdragon S7 Sound) | Sleep, focus, developer platform | Shipping 2026 ([audioXpress](https://audioxpress.com/article/idun-technologies-from-concept-to-real-world-brain-sensing-platform)) |
| MW75 Neuro / Neuro LT | Neurable + Master & Dynamic | EEG headphones | 12 | — (bandwidth 0–131 Hz) | — | Soft fabric sensors in ear pads | — | Focus, mental fatigue | $699 (Sep 2024); LT $499 ([Master & Dynamic](https://www.masterdynamic.com/blogs/news-culture/introducing-the-mw75-neuro-smart-eeg-active-noise-cancelling-wireless-headphones-for-neurable-inc), [Wareable](https://www.wareable.com/wearable-tech/neurable-debuts-lighter-more-affordable-mw75-neuro-brain-sensing-headphones)) |

**Low-cost / DIY**

| Device | Company | Type | Channels | Sampling rate | Resolution | Electrodes | Connectivity | Typical use | Status/price |
|---|---|---|---|---|---|---|---|---|---|
| Cyton (+ Daisy) | OpenBCI | Open-source ExG board (ADS1299) | 8 (16 with Daisy) | 250 Hz | 24-bit | Any (user-supplied) | BLE dongle, SD card | Hobby and research BCI | Current ([specs](https://docs.openbci.com/Cyton/CytonSpecs/), [data format](https://docs.openbci.com/Cyton/CytonDataFormat/)) |
| Ganglion | OpenBCI | Open-source board (MCP3912) | 4 | 200 Hz (BLE limit) | 24-bit | Any (user-supplied) | BLE | Teaching, simple BCI | Current ([specs](https://docs.openbci.com/Ganglion/GanglionSpecs/), [data format](https://docs.openbci.com/Ganglion/GanglionDataFormat/)) |
| Unicorn Hybrid Black | g.tec | Headset | 8 | 250 Hz | 24-bit | Hybrid wet/dry | Bluetooth | BCI education, art | Current ([g.tec](https://www.gtec.at/product/unicorn-hybrid-black/)) |

## 3. Applications (domains)

| Domain | How EEG is used | Examples | Maturity |
|---|---|---|---|
| Epilepsy diagnosis and monitoring | Routine EEG and multi-day video-EEG find interictal spikes and capture seizures | Nihon Kohden, Natus systems (section 2); SCORE-AI reads routine EEGs at expert level, AUC 0.89–0.96 on independent test sets after development on 30,493 EEGs ([Tveit 2023](https://doi.org/10.1001/jamaneurol.2023.1645)) | Clinical standard |
| ICU seizure detection | Continuous EEG finds non-convulsive seizures that the bedside exam misses | ACNS consensus ([Herman 2015](https://doi.org/10.1097/WNP.0000000000000166)); rapid-response EEG from Ceribell, Natus BrainWatch, Epitel REMI | Clinical, growing fast |
| Sleep (polysomnography) | EEG, EOG and chin EMG are scored into sleep stages | AASM scoring manual ([AASM](https://aasm.org/clinical-resources/scoring-manual/)); YASA open-source auto-staging ([Vallat & Walker 2021](https://doi.org/10.7554/eLife.70092)); Dreem 3S home headband | Clinical standard |
| Anesthesia depth | Frontal EEG reduced to an index; BIS runs 0 (silence) to 100 (awake), 40–60 is the manufacturer's target for general anesthesia | BIS, introduced by Aspect Medical in 1994 ([WikiAnesthesia](https://wikianesthesia.org/wiki/BIS); commercial use since 1994: [PMC11323923](https://pmc.ncbi.nlm.nih.gov/articles/PMC11323923/)) | Clinical |
| Brain death | Historically an ancillary test for "electrocerebral silence". The 2023 AAN/AAP/CNS/SCCM guideline no longer accepts EEG as an ancillary test | [Guideline Central](https://www.guidelinecentral.com/guideline/3303590), [Munson Healthcare](https://www.munsonhealthcare.org/about-the-system/news-media-relations/news/updated-brain-death-criteria-eeg-no-longer-acceptable) | Declining |
| Neonatal | Continuous EEG for neonatal seizures, which are often subclinical | ACNS neonatal guideline ([Shellhaas 2011](https://doi.org/10.1097/WNP.0b013e31823e96d7)); Ceribell neonatal clearance with more than 700 patients (Nov 2025) | Clinical |
| ADHD (NEBA) | Theta/beta power ratio as an aid to clinical diagnosis | NEBA, FDA de novo July 2013, based on 275 children aged 6–17 ([Healio](https://www.healio.com/news/psychiatry/20130725/fda-approved-device-testing-brain-function-to-assess-for-adhd)) | Cleared, limited use |
| Dementia research | Resting-state alpha slowing and more delta/theta in Alzheimer's disease; proposed for trial stratification | Expert recommendations ([Babiloni 2021](https://doi.org/10.1002/alz.12311)) | Research |
| BCI: motor imagery | ERD of mu/beta over motor cortex when imagining movement | IpsiHand stroke rehabilitation system, FDA de novo Apr 2021 ([WashU](https://source.washu.edu/2021/04/stroke-recovery-device-using-brain-computer-interface-receives-fda-market-authorization/)); mean accuracy only 71.1% in a 54-person study ([Lee 2019](https://doi.org/10.1093/gigascience/giz002)) | Early commercial (rehab) / research |
| BCI: P300 | Rare-target flashes evoke a P300; the speller picks the letter | [Farwell & Donchin 1988](https://doi.org/10.1016/0013-4694(88)90149-6); 96.7% mean accuracy in Lee 2019 | Research / assistive niche |
| BCI: SSVEP and c-VEP | Targets flicker at different frequencies or codes; the classifier finds which one the user looks at | Up to 5.32 bits/s and 60 characters/min ([Chen 2015](https://doi.org/10.1073/pnas.1508080112)); c-VEP review ([Martínez-Cagigal 2021](https://doi.org/10.1088/1741-2552/ac38cf)) | Research (fastest non-invasive BCIs) |
| BCI: error potentials | ErrPs flag mistakes so the system can correct or learn | [Chavarriaga 2014](https://doi.org/10.3389/fnins.2014.00208) | Research |
| Neurofeedback | Users see their own EEG (e.g. theta/beta) and try to change it | Meta-analysis: no significant effect on ADHD when ratings were probably blinded ([Cortese 2016](https://doi.org/10.1016/j.jaac.2016.03.007)) | Commercial, weak evidence |
| Neuromarketing | Attention, engagement and frontal alpha asymmetry while watching ads or products | Systematic review ([2024](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11153447/)) | Commercial services, research-grade evidence |
| Cognitive workload / neuroergonomics | Passive BCI estimates mental workload; EEG+fNIRS beats either alone | [Aghajani 2017](https://doi.org/10.3389/fnhum.2017.00359) | Research / pilots |
| Driver drowsiness | EEG changes as drivers become fatigued | Review ([Lal & Craig 2001](https://doi.org/10.1016/S0301-0511(00)00085-5)) | Research |
| Consumer wellness and meditation | Headbands and earbuds turn band power into feedback and sleep or focus scores | Muse, Neurosity Crown, Neurable, IDUN, Emotiv MN8 (section 2) | Commercial |
| Gaming | Focus and cognitive-state signals for players and e-sports | Neurable plans gaming and e-sports products *unverified*, not in the cited article ([Built In Boston](https://www.builtinboston.com/articles/neurable-raises-35m-to-expandbrain-computer-technology-20251219)) | Early commercial |
| Emotion recognition | Classify valence/arousal or discrete emotions from EEG during video or music | DEAP ([Koelstra 2012](https://doi.org/10.1109/T-AFFC.2011.15)), SEED ([Zheng & Lu 2015](https://doi.org/10.1109/TAMD.2015.2431497)) | Research |
| Speech and imagined-speech decoding | Decode heard or imagined words | Contrastive model picks the right 3 s speech segment among more than 1,000 with up to 41% accuracy from MEG; same work used EEG datasets ([Défossez 2023](https://doi.org/10.1038/s42256-023-00714-5)); imagined-speech review ([2025](https://doi.org/10.1016/j.asoc.2025.113563)); EEG-to-text models score about the same on noise as on EEG ([Jo 2024](https://arxiv.org/abs/2405.06459)) | Research (early, hype risk) |
| EEG foundation models | Self-supervised pretraining on thousands of hours, then fine-tuning on downstream tasks | LaBraM, CBraMod, EEGPT, NeuroLM (section 7) | Research |

## 4. Companies

| Company | Country | Focus | Key product | Status 2025–2026 |
|---|---|---|---|---|
| Ceribell | US | Point-of-care EEG + AI | Ceribell System, Clarity | IPO on Nasdaq (CBLL) Oct 2024: 12,196,969 shares at $17, net proceeds about $187.8M ([10-K](https://www.sec.gov/Archives/edgar/data/1861107/000095017025026773/cbll-20241231.htm)). 2025 revenue $89.1M (+36%); 2026 guidance $111–115M ([Q4 2025 results](https://www.santelog.com/actualites-sante-nasdaq/ceribell-reports-fourth-quarter-and-full-year-2025-financial-results)). Neonatal clearance Nov 2025 |
| Natus | US | Clinical neurodiagnostics | NeuroWorks, Quantum, BrainWatch | Taken private by ArchiMed, July 2022, $1.2B equity value ([BioSpace](https://www.biospace.com/archimed-completes-acquisition-of-natus-medical-incorporated-for-1-2-billion-total-equity-value)); BrainWatch cleared Nov 2024 |
| Nihon Kohden | Japan | Clinical EEG | Neurofax EEG-1200 | Selling ([FDA data](https://fda.innolitics.com/device/K080546)) |
| Compumedics | Australia | EEG and sleep | Grael | Selling |
| Zeto | US | Dry clinical EEG + cloud | WR19, Zeto ONE | $31M Series B, Jan 2025, led by MindWorks Global ([MedTech Innovator](https://medtechinnovator.org/zeto-inc-secures-31-million-in-series-b-funding-to-redefine-the-future-of-eeg-brain-monitoring/)) |
| Epitel | US | Wearable seizure EEG | REMI + Vigilenz AI | Fourth FDA 510(k) in Oct 2024, with an authorized Predetermined Change Control Plan (PCCP) ([BusinessWire](https://www.businesswire.com/news/home/20241021071646/en/Epitel-Expands-AI-Portfolio-With-A-Fourth-FDA-510k-Clearance-for-REMI), [HLTH](https://hlth.com/insights/news/fda-clears-epitel-remote-monitoring-tech-ai-detection-platform-2024-04-25)) |
| Beacon Biosignals | US | EEG analytics for trials, sleep | Dreem 3S / Waveband | Bought Dreem's R&D arm July 2023; Dreem 3S cleared Aug 2023 ([Sleep Review](https://sleepreviewmag.com/sleep-diagnostics/connected-care/remote-monitoring/beacon-biosignals-bolsters-sleep-medicine-research-acquisition-dreem/), [BioSpace](https://www.biospace.com/beacon-biosignals-receives-fda-clearance-for-ai-assisted-sleep-monitoring-device-dreem-3s)) |
| Neurolutions | US | EEG BCI for stroke rehab | IpsiHand | FDA de novo Apr 2021 ([FDAnews](https://www.fdanews.com/articles/202479-fda-gives-de-novo-approval-for-stroke-rehabilitation-device)) |
| Emotiv | — | Consumer/research headsets | EPOC X, Insight, MN8 | Selling |
| Interaxon (Muse) | Canada | Consumer EEG | Muse 2, Muse S Athena | $9.5M Series C in 2022 ([BusinessWire](https://www.businesswire.com/news/home/20220811005493/en/Interaxon-Inc.-Muse-Announces-%25249.5M-Series-C-Funding-Round-To-Expand-Brain-Health-and-Wellness-Offerings)); Muse S Athena (EEG + fNIRS) on sale ([Muse](https://choosemuse.com/products/muse-s-athena)) |
| Neurable | US | EEG headphones | MW75 Neuro, Neuro LT | $35M Series A Dec 2025 led by Spectrum Moonshot Fund, $65M total ([Built In Boston](https://www.builtinboston.com/articles/neurable-raises-35m-to-expandbrain-computer-technology-20251219)) |
| Neurosity | US | Developer headset | Crown | Selling |
| IDUN Technologies | Switzerland | In-ear EEG | Guardian 4 | Shipping 2026; raised $2.5M for a true-wireless version ([audioXpress](https://audioxpress.com/article/idun-technologies-from-concept-to-real-world-brain-sensing-platform)) |
| OpenBCI | US | Open-source hardware | Cyton, Ganglion, Galea | Selling; Galea listed at $42,980, sold out |
| g.tec | Austria | Research and BCI | g.USBamp, g.Nautilus, Unicorn | Selling |
| Brain Products | Germany | Research EEG | actiCHamp, LiveAmp | Selling; offers CGX dry headsets through a partnership ([Brain Products](https://pressrelease.brainproducts.com/tag/cgx/)) |
| BioSemi / ANT Neuro / Neuroelectrics / Wearable Sensing / mBrainTrain / CGX | Netherlands / Netherlands / Spain / US / Serbia / US | Research hardware | See section 2 | Selling |

## 5. Patents

| Patent number | Holder | Title/topic | Year | Why it matters |
|---|---|---|---|---|
| [US 4,907,597](https://patents.google.com/patent/US4907597A/en) | Biometrak Corp (inventor N. Chamoun) | Cerebral biopotential analysis (bispectral EEG) | 1990 | Bispectral analysis of EEG, the approach behind BIS-style anesthesia monitoring |
| [US 5,363,858](https://patents.google.com/patent/US5363858A/en) | Francis Luca Conte (assignee; inventor L. Farwell) | Multifaceted EEG response analysis (MERA) | 1994 | P300-based "brain fingerprinting" for recognition detection; scientifically contested |
| [US 6,097,980](https://patents.google.com/patent/US6097980A/en) | V. Monastra, J. Lubar (individuals) | QEEG process for assessing attention deficit | 2000 | Theta/beta-type QEEG for ADHD, the idea later cleared as NEBA (2013) |
| [US 7,551,952](https://patents.google.com/patent/US7551952B2/en) | Sam Technology (A. Gevins) | EEG electrode headset | 2009 | Early quick-application headset design |
| [US D565,735](https://patents.justia.com/patent/D565735) | Emotiv Systems | Electrode headset (design) | 2008 | Emotiv's consumer headset design |
| [US 9,820,670](https://patents.google.com/patent/US9820670B2/en) | Ceribell | Electrode placement and tracking | 2017 | Asserted against Natus in 2025 |
| [US 10,433,756](https://patents.google.com/patent/US10433756B1/en) | Ceribell | Adjustable-geometry wearable electrodes | 2019 | Asserted against Natus in 2025 |
| [US 11,471,088](https://patents.google.com/patent/US11471088B1/en) | Stanford + Ceribell (Parvizi, Chafe, Chao) | Handheld or wearable device for recording or sonifying brain signals | 2022 | The "brain stethoscope": seizures turned into sound for non-experts |
| [US 10,213,157](https://patents.google.com/patent/US10213157B2/en) | Bose | Active dry-electrode open-ear headset and BCI | 2019 | A large audio company claiming ear-EEG headphones |
| [US 10,321,842](https://patents.google.com/patent/US10321842B2/en) | Interaxon (Muse) | Associating music with brain-state data | 2019 | Consumer EEG tied to content |
| [US 2019/0107888 A1](https://patents.google.com/patent/US20190107888A1/en) | Holland Bloorview Kids Rehabilitation Hospital | BCI for classifying covert (imagined) speech | Filed 2018 (application) | Imagined-speech BCI claim |

**Litigation.** On 7 July 2025, Ceribell sued Natus Medical, Natus Neurology and Excel-Tech (XLTEK) at the US International Trade Commission and in the US District Court for Delaware. It asserted six patents (US 9,820,670; 10,433,756; 11,357,434; 12,150,769; 12,324,670; 12,336,826) covering its EEG headband and electrode design. Natus's BrainWatch clearance had named Ceribell's Pocket EEG Device and Instant EEG Headband as predicates ([FDA K242930](https://fda.innolitics.com/device/K242930), [Bloomberg Law](https://news.bloomberglaw.com/ip-law/ceribell-hits-competitor-with-patent-lawsuit-over-wearable-eeg), [Barchart](https://www.barchart.com/story/news/33255459/ceribell-files-complaints-against-natus-medical-incorporated-with-the-u-s-international-trade-commission-and-federal-court-in-delaware)). The ITC opened investigation 337-TA-1458 in August 2025 ([USITC](https://www.usitc.gov/press_room/news_release/2025/er0806_67388.htm), [Federal Register](https://www.federalregister.gov/documents/2025/08/11/2025-15179/certain-wearable-electroencephalogram-devices-and-systems-and-components-thereof-notice-of)). In May 2026 the Commission declined to review an initial determination terminating the investigation as to certain patent claims ([USITC notice](https://www.usitc.gov/fed_reg_notices/section_337_notices/certain_wearable_electroencephalogram_devices_and_052226.htm)); a further Commission notice followed in July 2026 ([USITC notice](https://www.usitc.gov/fed_reg_notices/section_337_notices/certain_wearable_electroencephalogram_devices_and_071726.htm); its content *unverified*). The case was not over: Ceribell's 10-Q filed 10 August 2026 says the ITC hearing ended 12 June 2026, an initial determination is expected by 19 November 2026 and a final determination by March 2027, and the Delaware case was stayed on 12 August 2025 until the ITC's final determination ([10-Q](https://www.sec.gov/Archives/edgar/data/1861107/000119312526342574/cbll-20260630.htm)).

## 6. Most-cited papers

Citation counts are Crossref "cited-by" numbers, checked on 2026-10-11. They undercount compared with Google Scholar, but they are reproducible.

| Paper | Authors | Venue/year | Crossref citations | Why it matters |
|---|---|---|---|---|
| [Über das Elektrenkephalogramm des Menschen](https://doi.org/10.1007/BF01797193) | Berger | Arch. Psychiatr. Nervenkr. 1929 | 3,205 | First human EEG; alpha rhythm |
| [The ten-twenty electrode system of the International Federation](https://doi.org/10.1016/0013-4694(58)90053-1) | Jasper | EEG Clin. Neurophysiol. 1958 | 1,800 | The 10-20 placement standard |
| [Talking off the top of your head: toward a mental prosthesis utilizing event-related brain potentials](https://doi.org/10.1016/0013-4694(88)90149-6) | Farwell, Donchin | EEG Clin. Neurophysiol. 1988 | 2,681 | The P300 speller |
| [Event-related EEG/MEG synchronization and desynchronization: basic principles](https://doi.org/10.1016/S1388-2457(99)00141-8) | Pfurtscheller, Lopes da Silva | Clin. Neurophysiol. 1999 | 6,476 | ERD/ERS, the basis of motor-imagery BCI |
| [Removing electroencephalographic artifacts by blind source separation](https://doi.org/10.1111/1469-8986.3720163) | Jung, Makeig, Humphries, Lee et al. | Psychophysiology 2000 | 2,919 | ICA for artifact removal |
| [Brain–computer interfaces for communication and control](https://doi.org/10.1016/S1388-2457(02)00057-3) | Wolpaw, Birbaumer, McFarland, Pfurtscheller, Vaughan | Clin. Neurophysiol. 2002 | 6,499 | Defined the BCI field and its vocabulary |
| [EEGLAB: an open source toolbox for analysis of single-trial EEG dynamics including independent component analysis](https://doi.org/10.1016/j.jneumeth.2003.10.009) | Delorme, Makeig | J. Neurosci. Methods 2004 | 23,720 | The most used EEG toolbox |
| [Updating P300: an integrative theory of P3a and P3b](https://doi.org/10.1016/j.clinph.2007.04.019) | Polich | Clin. Neurophysiol. 2007 | 7,104 | Standard P300 reference |
| [Optimizing spatial filters for robust EEG single-trial analysis](https://doi.org/10.1109/MSP.2008.4408441) | Blankertz, Tomioka, Lemm, Kawanabe, Müller | IEEE Signal Process. Mag. 2008 | 1,884 | CSP tutorial |
| [FieldTrip: open source software for advanced analysis of MEG, EEG, and invasive electrophysiological data](https://doi.org/10.1155/2011/156869) | Oostenveld, Fries, Maris, Schoffelen | Comput. Intell. Neurosci. 2011 | 9,857 | Major MATLAB toolbox |
| [Multiclass brain–computer interface classification by Riemannian geometry](https://doi.org/10.1109/TBME.2011.2172210) | Barachant, Bonnet, Congedo, Jutten | IEEE TBME 2012 | 842 | Covariance-matrix classifiers (pyRiemann) |
| [MEG and EEG data analysis with MNE-Python](https://doi.org/10.3389/fnins.2013.00267) | Gramfort et al. | Front. Neurosci. 2013 | 3,845 | The standard Python stack |
| [Deep learning with convolutional neural networks for EEG decoding and visualization](https://doi.org/10.1002/hbm.23730) | Schirrmeister et al. | Hum. Brain Mapp. 2017 | 3,634 | ShallowConvNet/DeepConvNet; Braindecode |
| [EEGNet: a compact convolutional neural network for EEG-based BCIs](https://doi.org/10.1088/1741-2552/aace8c) | Lawhern, Solon, Waytowich, Gordon, Hung, Lance | J. Neural Eng. 2018 | 4,886 | The default deep-learning baseline |

## 7. New achievements (2023–2026)

- **Foundation models arrive.** LaBraM (ICLR 2024) pretrained on about 2,500 hours from about 20 datasets and beat prior methods on abnormality detection, event classification, emotion and gait ([arXiv](https://arxiv.org/abs/2405.18765)). EEGPT (NeurIPS 2024) is a 10M-parameter transformer that is strong under linear probing ([NeurIPS](https://proceedings.neurips.cc/paper_files/paper/2024/hash/4540d267eeec4e5dbd9dae9448f0b739-Abstract.html)). CBraMod (ICLR 2025) pretrained on the TUH corpus and was tested on up to 10 tasks across 12 datasets ([arXiv](https://arxiv.org/abs/2412.07236)). NeuroLM (ICLR 2025) reached 1.7B parameters on about 25,000 hours ([arXiv](https://arxiv.org/abs/2409.00101)). BIOT (2023) handles mismatched channels across datasets and added about 3% balanced accuracy on CHB-MIT ([arXiv](https://arxiv.org/abs/2305.10351)).
- **A reality check.** Fine-tuned foundation models beat compact deep models by only 0.9–1.2% while using millions instead of thousands of parameters ([Lee et al. 2025](https://arxiv.org/abs/2507.01196)). EEG-FM-Bench (ICML 2026) compares seven EEG foundation models (BIOT, BENDR, LaBraM, EEGPT, CBraMod, CSBrain, REVE) and two general time-series models on 14 datasets across 10 paradigms ([arXiv](https://arxiv.org/abs/2508.17742), [ICML](https://icml.cc/virtual/2026/poster/60932)).
- **NeurIPS 2025 EEG Foundation Challenge.** Built on HBN-EEG: more than 3,000 children and young adults, 128 channels, six tasks, in BIDS ([challenge](https://eeg2025.github.io/), [arXiv](https://arxiv.org/abs/2506.19141), [HBN-EEG](https://www.biorxiv.org/content/10.1101/2024.10.03.615261v2)). Challenge 1 predicts response time across tasks; challenge 2 predicts an externalizing psychopathology score across subjects. Top teams: KU Leuven won challenge 1 and MBZUAI won challenge 2; weights are on Hugging Face ([hall of fame](https://github.com/eeg2025/hall-of-fame-2025)).
- **Clinical AI.** SCORE-AI matched experts on routine EEG (developed on 30,493 recordings; AUC 0.89–0.96 on independent test sets) ([JAMA Neurol 2023](https://doi.org/10.1001/jamaneurol.2023.1645)). Ceribell's Clarity algorithm was cleared for neonates in Nov 2025, validated on more than 700 patients ([Contemporary Pediatrics](https://www.contemporarypediatrics.com/view/fda-grants-510-k-clearance-for-clarity-algorithm-to-detect-electrographic-seizures-in-newborns)). Natus BrainWatch (Persyst algorithms *unverified*) was cleared in Nov 2024. Epitel's REMI Vigilenz AI got bedside seizure notifications with a PCCP, so the model can be updated without a new submission (Oct 2024).
- **Speech.** From MEG, a contrastive model identifies the right 3 s speech segment among more than 1,000 with up to 41% accuracy ([Défossez 2023](https://doi.org/10.1038/s42256-023-00714-5)). For EEG-to-text, Jo et al. (2024) showed published models score about the same on pure noise, because of teacher forcing in evaluation ([arXiv](https://arxiv.org/abs/2405.06459)).
- **Data infrastructure.** EEGDash catalogs 700+ BIDS datasets as PyTorch-ready loaders ([GitHub](https://github.com/eegdash/EEGDash)).
- **Market signals.** Ceribell went public (2024) and grew revenue 36% in 2025; Zeto raised $31M; Neurable raised $35M; Muse added fNIRS to a consumer headband; IDUN began shipping in-ear EEG (section 4).

## 8. Current state of the field

**Where EEG is used today, and where it is still research**

| Maturity | Applications |
|---|---|
| Established clinical | Epilepsy diagnosis and long-term monitoring, ICU continuous EEG, polysomnography, anesthesia depth (BIS), neonatal monitoring |
| Commercial, growing | Rapid-response point-of-care EEG (Ceribell and Epitel with seizure-detection AI; Natus BrainWatch without automated alerts per its 510(k)), dry clinical headsets (Zeto), consumer wellness wearables (Muse, Neurable, IDUN) |
| Cleared but niche | NEBA for ADHD, IpsiHand stroke BCI, P300/SSVEP spellers for assistive use |
| Research | Foundation models, imagined-speech decoding, emotion recognition, workload and drowsiness monitoring, dementia biomarkers |
| Declining | EEG as an ancillary test for brain death (dropped in the 2023 guideline) |

**Open problems**
- **Subject and session variability.** In a 54-person study, motor-imagery accuracy averaged 71.1% and 53.7% of users were "BCI illiterate", against 96.7% for ERP and 95.1% for SSVEP ([Lee 2019](https://doi.org/10.1093/gigascience/giz002)). Most decoders still need calibration for each user.
- **Low signal-to-noise ratio and artifacts.** Signals of tens of µV sit under eye, muscle and motion artifacts, and dry and in-ear electrodes make this worse.
- **Foundation models are not yet clearly better.** Gains over small CNNs are about 1% ([Lee et al. 2025](https://arxiv.org/abs/2507.01196)), and benchmarks are only now being standardized ([EEG-FM-Bench](https://arxiv.org/abs/2508.17742)).
- **Evaluation pitfalls.** Teacher forcing and missing noise baselines inflated EEG-to-text results ([Jo 2024](https://arxiv.org/abs/2405.06459)). Report results on held-out subjects, with subject-wise splits, if a model is meant to work on new users.
- **Heterogeneous data.** Channel counts, montages, sampling rates and file formats differ between datasets, and labels (seizure, sleep stage) differ between expert raters.
- **Weak evidence in consumer and wellness claims.** Neurofeedback for ADHD showed no significant effect when outcomes were probably blinded ([Cortese 2016](https://doi.org/10.1016/j.jaac.2016.03.007)).
- **IP and regulation.** Point-of-care EEG is now contested in patent court (section 5), and clinical AI needs FDA clearance; PCCPs are the emerging path for updating models.

**Where an AI engineer can contribute.** Self-supervised pretraining that actually beats small baselines, with honest subject-wise evaluation. Channel-agnostic architectures that handle any montage. Few-shot calibration and domain adaptation across subjects and sessions. Robust seizure and sleep models for dry and in-ear headsets. Artifact handling learned end-to-end. Distilled models for on-device inference in earbuds and headbands. Reproducible pipelines in BIDS with MNE, Braindecode and MOABB. The datasets below are a good starting point.

## 9. Public datasets

| Dataset | Content | Size | Link |
|---|---|---|---|
| TUH EEG Corpus (TUEG + TUAB, TUSZ, TUAR, TUEV, TUSL, TUEP subsets) | Clinical hospital EEG with abnormal, seizure, artifact and event labels in the subsets | TUEG: 26,846 sessions, 2002–2017 | [TUH](https://isip.piconepress.com/projects/nedc/html/tuh_eeg/), [Obeid & Picone 2016](https://doi.org/10.3389/fnins.2016.00196) |
| CHB-MIT Scalp EEG | Pediatric intractable seizures | 22 subjects / 23 cases; 256 Hz, 16-bit, mostly 23 channels | [PhysioNet](https://physionet.org/content/chbmit/1.0.0/) |
| EEG Motor Movement/Imagery (EEGMMIDB) | Real and imagined fist/feet movements (used in the starter notebook) | 109 subjects, 64 ch, 160 Hz, EDF+ | [PhysioNet](https://physionet.org/content/eegmmidb/1.0.0/), [BCI2000](https://doi.org/10.1109/TBME.2004.827072) |
| BCI Competition IV 2a | 4-class motor imagery (left hand, right hand, feet, tongue) | 9 subjects, 22 ch, 250 Hz, 2 sessions × 288 trials | [BBCI](https://www.bbci.de/competition/iv/) |
| OpenBMI (Lee 2019) | MI, ERP and SSVEP from the same users | 54 subjects, multiple sessions | [GigaScience](https://doi.org/10.1093/gigascience/giz002) |
| Sleep-EDF Expanded | Whole-night PSG with sleep-stage labels | 197 recordings | [PhysioNet](https://physionet.org/content/sleep-edfx/1.0.0/) |
| HBN-EEG | Six tasks plus psychopathology scores (NeurIPS 2025 challenge) | 3,000+ participants (bioRxiv v2 counted 2,600+), 128 ch, BIDS | [bioRxiv](https://www.biorxiv.org/content/10.1101/2024.10.03.615261v2), [challenge](https://arxiv.org/abs/2506.19141) |
| DEAP | Emotion (valence/arousal) while watching music videos | 32 participants | [Koelstra 2012](https://doi.org/10.1109/T-AFFC.2011.15) |
| SEED | Emotion while watching film clips | 15 subjects, 62 ch | [SJTU](https://bcmi.sjtu.edu.cn/home/seed/seed.html) |
| THINGS-EEG | Visual object recognition | 10 participants × 82,160 trials, 16,740 image conditions | [Gifford 2022](https://doi.org/10.1016/j.neuroimage.2022.119754) |

Full specifications for each dataset, and tables of published results on them, are in [DATASETS.md](DATASETS.md).

## 10. GitHub repositories

Stars and dates checked via the GitHub API on 2026-10-11.

"Custom" means GitHub could not detect a standard license (`NOASSERTION`), so read the repo's LICENSE file before reusing the code. "—" means no license file or no detected language. None of the repos below is archived.

**Toolkits and libraries**

| Repo | What it does / when to use it | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [mne-tools/mne-python](https://github.com/mne-tools/mne-python) | The standard Python library for EEG/MEG: I/O, filtering, ICA, epochs, source analysis. Start here | Python | 3542 | 2026-10 | BSD-3-Clause |
| [sccn/eeglab](https://github.com/sccn/eeglab) | The most cited MATLAB EEG toolbox, with a GUI and many plugins | MATLAB | 800 | 2026-09 | Custom |
| [fieldtrip/fieldtrip](https://github.com/fieldtrip/fieldtrip) | MATLAB toolbox for EEG/MEG time-frequency, connectivity and source analysis | MATLAB | 990 | 2026-10 | GPL-3.0 |
| [cbrnr/mnelab](https://github.com/cbrnr/mnelab) | GUI on top of MNE for quick inspection | Python | 294 | 2026-10 | BSD-3-Clause |
| [braindecode/braindecode](https://github.com/braindecode/braindecode) | PyTorch deep learning for EEG (ShallowConvNet, Deep4, EEGNet and more), dataset loaders | Python | 1324 | 2026-10 | BSD-3-Clause |
| [NeuroTechX/moabb](https://github.com/NeuroTechX/moabb) | Mother of All BCI Benchmarks: dozens of BCI datasets and fair cross-session/cross-subject evaluation | Python | 1067 | 2026-10 | BSD-3-Clause |
| [pyRiemann/pyRiemann](https://github.com/pyRiemann/pyRiemann) | Covariance-matrix (Riemannian) classifiers in scikit-learn style. Strong small-data baseline | Python | 779 | 2026-10 | BSD-3-Clause |
| [torcheeg/torcheeg](https://github.com/torcheeg/torcheeg) | PyTorch library for EEG signal analysis | Python | 581 | 2026-09 | Custom |
| [autoreject/autoreject](https://github.com/autoreject/autoreject) | Automatic bad-epoch and bad-channel rejection for MNE | Python | 162 | 2026-10 | BSD-3-Clause |
| [mne-tools/mne-icalabel](https://github.com/mne-tools/mne-icalabel) | Automatic labeling of ICA components (eye, muscle, brain) for MNE | Python | 124 | 2026-10 | BSD-3-Clause |
| [sccn/ICLabel](https://github.com/sccn/ICLabel) | The original ICLabel classifier for EEGLAB | MATLAB | 76 | 2026-10 | BSD-2-Clause |
| [sappelhoff/pyprep](https://github.com/sappelhoff/pyprep) | Python version of the PREP pipeline (bad channels, robust referencing) | Python | 185 | 2026-10 | MIT |
| [sccn/clean_rawdata](https://github.com/sccn/clean_rawdata) | EEGLAB plugin for Artifact Subspace Reconstruction (ASR) | MATLAB | 55 | 2026-09 | GPL-3.0 |
| [raphaelvallat/yasa](https://github.com/raphaelvallat/yasa) | Automatic sleep staging, spindle and slow-wave detection | Python | 589 | 2026-10 | BSD-3-Clause |
| [mne-tools/mne-bids](https://github.com/mne-tools/mne-bids) | Read and write BIDS-EEG datasets with MNE | Python | 182 | 2026-10 | BSD-3-Clause |
| [mne-tools/mne-connectivity](https://github.com/mne-tools/mne-connectivity) | Connectivity measures (coherence, PLV, etc.) | Python | 92 | 2026-10 | BSD-3-Clause |
| [mne-tools/mne-features](https://github.com/mne-tools/mne-features) | Classic hand-crafted EEG features in scikit-learn style | Python | 161 | 2026-03 | BSD-3-Clause |
| [neuropsychology/NeuroKit](https://github.com/neuropsychology/NeuroKit) | General physiological toolbox with some EEG utilities | Python | 2392 | 2026-10 | MIT |
| [brainflow-dev/brainflow](https://github.com/brainflow-dev/brainflow) | One device-agnostic API to stream EEG from many boards, including OpenBCI | C++ | 1770 | 2026-10 | Custom |
| [labstreaminglayer/pylsl](https://github.com/labstreaminglayer/pylsl) | Python bindings for Lab Streaming Layer: synchronized real-time streams | Python | 201 | 2026-09 | MIT |
| [sccn/liblsl](https://github.com/sccn/liblsl) | The LSL core C/C++ library | C++ | 179 | 2026-09 | Custom |
| [sccn/labstreaminglayer](https://github.com/sccn/labstreaminglayer) | LSL super-repository with apps for many amplifiers | HTML | 785 | 2026-09 | Custom |
| [mne-tools/mne-lsl](https://github.com/mne-tools/mne-lsl) | Real-time LSL streams as MNE objects | Python | 91 | 2026-10 | BSD-3-Clause |
| [xdf-modules/pyxdf](https://github.com/xdf-modules/pyxdf) | Read XDF files recorded with LSL | Python | 57 | 2026-09 | BSD-2-Clause |

**Models and papers with code**

| Repo | What it does / when to use it | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [vlawhern/arl-eegmodels](https://github.com/vlawhern/arl-eegmodels) | Official EEGNet (plus ShallowConvNet, DeepConvNet) in Keras. Not updated since 2022; Braindecode has PyTorch versions | Python | 1570 | 2022-05 | Custom |
| [eeyhsong/EEG-Conformer](https://github.com/eeyhsong/EEG-Conformer) | CNN + transformer decoder (IEEE TNSRE 2023) | Python | 765 | 2024-07 | GPL-3.0 |
| [935963004/LaBraM](https://github.com/935963004/LaBraM) | Official LaBraM (ICLR 2024 spotlight) | Python | 668 | 2025-09 | MIT |
| [wjq-learning/CBraMod](https://github.com/wjq-learning/CBraMod) | Official CBraMod criss-cross transformer (ICLR 2025) | Python | 354 | 2026-08 | MIT |
| [BINE022/EEGPT](https://github.com/BINE022/EEGPT) | Official EEGPT (NeurIPS 2024) | Python | 316 | 2026-09 | Apache-2.0 |
| [ycq091044/BIOT](https://github.com/ycq091044/BIOT) | BIOT biosignal transformer with pretrained EEG models | Python | 215 | 2023-12 | MIT |
| [SPOClab-ca/BENDR](https://github.com/SPOClab-ca/BENDR) | BENDR, an early contrastive transformer for EEG ([Kostas 2021](https://doi.org/10.3389/fnhum.2021.653659)) | Python | 213 | 2022-08 | — |
| [935963004/NeuroLM](https://github.com/935963004/NeuroLM) | NeuroLM, EEG + language multi-task model up to 1.7B parameters (ICLR 2025) | Python | 170 | 2025-09 | MIT |

**Benchmarks and dataset loaders**

| Repo | What it does / when to use it | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [xw1216/EEG-FM-Bench](https://github.com/xw1216/EEG-FM-Bench) | Official EEG-FM-Bench code: 14 datasets, 10 paradigms, 6 foundation models listed in the README | Python | 68 | 2026-06 | Custom |
| [eeg2025/startkit](https://github.com/eeg2025/startkit) | Starter kit for the NeurIPS 2025 EEG Foundation Challenge (HBN-EEG) | Jupyter Notebook | 80 | 2025-10 | — |
| [eeg2025/hall-of-fame-2025](https://github.com/eeg2025/hall-of-fame-2025) | Code and weights of the top challenge submissions | Python | 8 | 2026-01 | BSD-3-Clause |
| [eegdash/EEGDash](https://github.com/eegdash/EEGDash) | Catalog and PyTorch loaders for 700+ BIDS EEG/MEG/fNIRS/EMG/iEEG datasets | Python | 89 | 2026-10 | BSD-3-Clause |
| [NeuroTechX/EEG-ExPy](https://github.com/NeuroTechX/EEG-ExPy) | EEG experiments in Python (formerly eeg-notebooks) | Python | 579 | 2026-10 | BSD-3-Clause |
| [bids-standard/bids-specification](https://github.com/bids-standard/bids-specification) | The BIDS standard, including the EEG extension | Python | 370 | 2026-10 | CC-BY-4.0 |

**Hardware and firmware**

| Repo | What it does / when to use it | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [OpenBCI/OpenBCI_GUI](https://github.com/OpenBCI/OpenBCI_GUI) | Cross-platform desktop app to view and record Cyton and Ganglion data | HTML | 965 | 2026-04 | MIT |
| [OpenBCI/OpenBCI_Cyton_Library](https://github.com/OpenBCI/OpenBCI_Cyton_Library) | Firmware for the Cyton (ADS1299) board | C++ | 126 | 2025-07 | MIT |
| [OpenBCI/OpenBCI_Ganglion_Library](https://github.com/OpenBCI/OpenBCI_Ganglion_Library) | Firmware for the Ganglion board | C++ | 32 | 2026-01 | MIT |
| [openbci-archive/OpenBCI_Python](https://github.com/openbci-archive/OpenBCI_Python) | Old Python driver, moved to OpenBCI's archive organization; use BrainFlow instead | Python | 541 | 2022-12 | MIT |
| [alexandrebarachant/muse-lsl](https://github.com/alexandrebarachant/muse-lsl) | Stream Muse headband EEG to LSL | Python | 780 | 2026-09 | BSD-3-Clause |
| [DominiqueMakowski/OpenMuse](https://github.com/DominiqueMakowski/OpenMuse) | Record and stream Muse S Athena signals | Python | 97 | 2026-01 | — |
| [neurosity/neurosity-sdk-js](https://github.com/neurosity/neurosity-sdk-js) | Official SDK for the Neurosity Crown | TypeScript | 373 | 2026-06 | MIT |
| [Emotiv/cortex-example](https://github.com/Emotiv/cortex-example) | Official examples for Emotiv's Cortex API | C# | 265 | 2026-08 | MIT |

**Curated lists**

| Repo | What it does / when to use it | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [meagmohit/EEG-Datasets](https://github.com/meagmohit/EEG-Datasets) | Large list of public EEG datasets by task | — | 3120 | 2025-10 | — |
| [NeuroTechX/awesome-bci](https://github.com/NeuroTechX/awesome-bci) | Curated BCI resources: papers, software, hardware | — | 1551 | 2026-10 | — |
| [openlists/ElectrophysiologyData](https://github.com/openlists/ElectrophysiologyData) | Open electrophysiology datasets (EEG, MEG, iEEG) | — | 551 | 2026-06 | — |
