# MEG (Magnetoencephalography)

Magnetoencephalography records the tiny magnetic fields (around 100 fT, about a billion times weaker than the Earth's field) produced by synchronized currents in the cortex. It gives millisecond timing and better source localization than EEG ([Brookes et al. 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC10465236/), [Baillet 2017](https://doi.org/10.1038/nn.4504)). Its one well-established clinical job is finding where seizures start before epilepsy surgery, plus mapping eloquent cortex ([Aetna policy](https://www.aetna.com/cpb/medical/data/200_299/0279.html)). It is also the main non-invasive testbed for deep-learning brain decoding: speech perception, typed sentences and images ([Défossez et al. 2023](https://arxiv.org/abs/2208.12266), [Brain2Qwerty](https://github.com/facebookresearch/brain2qwerty)). Meanwhile, wearable sensors called optically pumped magnetometers (OPMs) are moving MEG out of the fixed, helium-cooled helmet.

Items marked *unverified* could not be confirmed from a source. Cells marked "—" mean the manufacturer did not publish the spec, or I could not find it.

## 1. The data

**Where the field comes from.** When many cortical pyramidal neurons are active at the same moment, the currents flowing inside them add up. Those currents produce a magnetic field outside the head. MEG sensors measure that field, which is about 100 fT ([Brookes 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC10465236/), [Hämäläinen et al. 1993](https://doi.org/10.1103/RevModPhys.65.413)). Unlike EEG, the skull and scalp barely smear the field. The cost is that MEG is blind to some source orientations: "MEG is mainly sensitive to tangential source components only, whereas EEG is sensitive to all components" ([Ahlfors et al. 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2914866/)). For a typical cortical location, the orientation MEG sees least gives only about 6% (median) of the signal of the best orientation. In practice this means sulcal walls (tangential) are seen well, while gyral crowns and deep radial sources are seen poorly.

**Sensor types**

| Term | What it is | Used in |
|---|---|---|
| Magnetometer | A single pickup loop that measures the field component normal to it. It is the most sensitive type, and also picks up the most distant noise | MEGIN TRIUX neo (102 per system) ([Yale](https://research.yale.edu/cores/brainworks/megin-truix-neo-meg)); all OPMs |
| Planar gradiometer | Two side-by-side loops wound in opposite directions. It measures the spatial derivative of the field, so it rejects distant sources and peaks right above a source | MEGIN TRIUX neo (204 per system) |
| Axial gradiometer | Two loops stacked along the radial axis. A set of reference sensors lets the software build "synthetic" higher-order gradiometers ([Gross et al. 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC3925794/)) | CTF (275 + 29 references, [McGill](https://www.mcgill.ca/bic/meg-unit/meg-bic/equipment)), Ricoh ([FDA K210199](https://fda.innolitics.com/device/K210199)), Compumedics ([FDA K191785](https://fda.innolitics.com/device/K191785)) |
| SQUID | Superconducting sensor kept at about 4 K (−269 °C) in a liquid-helium dewar. Noise is about 2–5 fT/√Hz. Because of the dewar, sensors sit about 2 cm or more from the scalp | All conventional MEG ([Brookes 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC10465236/)) |
| OPM | A heated alkali-vapour cell (about 150 °C) read by a laser. Noise is about 7–10 fT/√Hz. Sensors sit a few mm from the scalp, which gives 4–5× more signal in many cortical areas | QuSpin, FieldLine, Mag4Health (helium-4), Cerca systems ([Brookes 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC10465236/), [Alem 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10303922/), [Bonnet 2025](https://www.frontiersin.org/articles/10.3389/fmedt.2025.1548260/full)) |

**Shielding and head position.** MEG is recorded inside a magnetically shielded room (MSR). Passive mu-metal layers bring the Earth's field from about 60 µT down to about 5 nT. Adding active coils brings it to about 200 pT ([Brookes 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC10465236/)). OPMs need this extra step: they stop working if the field at the sensor changes by more than about 3 nT, so a head rotation of about 4° in an uncompensated room can take them offline (same source). Boto et al. used bi-planar nulling coils to cut the remnant field 50-fold, and subjects could then nod, stretch and drink while being scanned ([Boto 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6063354/)). With SQUIDs the head moves *relative to fixed sensors*. Small coils on the head driven at known frequencies (continuous head-position indicators, cHPI) let the software track that motion and correct for it ([MNE tutorial](https://mne.tools/stable/auto_tutorials/preprocessing/60_maxwell_filtering_sss.html)). Gross et al. recommend recording head position continuously and reporting the maximum movement ([Gross 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC3925794/)).

**Signal characteristics**

| Property | Typical value | Source |
|---|---|---|
| Brain field strength | About 100 fT; about 10⁹ times smaller than the Earth's field | [Brookes 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC10465236/) |
| Sensor noise floor | SQUID 2–5 fT/√Hz (Ricoh and Compumedics specify 10 fT/√Hz). OPM: QuSpin Gen-3 <15 fT/√Hz dual-axis and <23 fT/√Hz triaxial; FieldLine about 10 fT/√Hz per sensor; Mag4Health <40 fT/√Hz (typically 30) | [Brookes 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC10465236/), [FDA K210199](https://fda.innolitics.com/device/K210199), [FDA K191785](https://fda.innolitics.com/device/K191785), [QuSpin](https://quspin.com/qzfm-gen-3), [Alem 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10303922/), [Mag4Health](https://mag4health.com/product) |
| Bandwidth | SQUID (CTF): typically 0–300 Hz. OPM: QuSpin specifies 3–100 Hz (flat from 1 Hz); FieldLine 350 Hz in closed loop; Mag4Health helium-4 OPM DC–2 kHz | [Frankfurt CoBIC](https://www.rhein-main-universitaeten.de/en/rmu-facilities/coquitlam-ctf-275-kanal-whole-head-meg-system), [QuSpin](https://quspin.com/qzfm-gen-3), [Alem 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10303922/), [Bonnet 2025](https://www.frontiersin.org/articles/10.3389/fmedt.2025.1548260/full) |
| Sampling rate | Research datasets usually use 1 kHz (LibriBrain, Brain2Qwerty, MEGBCI2020). Hardware allows 1–5 kHz (TRIUX neo) and up to 12 kHz (CTF). Rule of thumb: sample at 3–4× the highest frequency of interest | [LibriBrain](https://arxiv.org/html/2506.02098v1), [Brain2Qwerty](https://arxiv.org/html/2502.17480v1), [Rathee 2021](https://doi.org/10.1038/s41597-021-00899-7), [Yale](https://research.yale.edu/cores/brainworks/megin-truix-neo-meg), [McGill](https://www.mcgill.ca/bic/meg-unit/meg-bic/equipment), [Gross 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC3925794/) |
| Channel count | SQUID: 306 (MEGIN), 275 + 29 references (CTF), 64–320 (Ricoh), 186 adult / 138 child (Compumedics). OPM: 128 (FieldLine), 192 (Cerca, 64 triaxial), 48–288 (Mag4Health), 384 (Nottingham research array) | Section 2 |
| Dynamic range | OPM: ±5 nT (QuSpin), ±15 nT closed-loop (FieldLine), ±200 nT (helium-4) | [QuSpin Neuro-1](https://quspin.com/products/neuro-1/), [Alem 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10303922/), [Bonnet 2025](https://www.frontiersin.org/articles/10.3389/fmedt.2025.1548260/full) |
| Main noise sources | Environmental fields (power line, traffic, lifts). Heart, eye and muscle artifacts (record ECG/EOG/EMG alongside). Head movement. Magnetic contamination on the subject, e.g. residual magnetization after an MRI scan, which can take up to about 3 days to fade. Sensor noise. For OPMs, motion through background field gradients | [Gross 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC3925794/), [Brookes 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC10465236/) |

**Preprocessing basics.**
- **Signal space separation (SSS) / Maxwell filtering.** Expands the measured field in spherical harmonics, keeps the "internal" part (sources inside the sensor array) and drops the "external" part (environment) ([Taulu & Kajola 2005](https://doi.org/10.1063/1.1935742), [MNE tutorial](https://mne.tools/stable/auto_tutorials/preprocessing/60_maxwell_filtering_sss.html)).
- **Temporal SSS (tSSS).** Also removes nearby interference, such as implants and dental work, by projecting out time courses shared by the internal and external subspaces ([Taulu & Simola 2006](https://doi.org/10.1088/0031-9155/51/7/008)). The same machinery corrects head movement using cHPI.
- **ICA.** Removes heartbeat and blink components, and [mne-icalabel](https://github.com/mne-tools/mne-icalabel) can label them automatically.
- **Other steps.** Bad-channel detection, notch and band-pass filtering, and epoching. Gross et al. warn that IIR filters distort phase, while FIR filters can keep it linear ([Gross 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC3925794/)).

The LibriBrain release is a typical deep-learning pipeline: head position from HPI, bad-channel interpolation, Maxwell filtering, 50 Hz notch, 0.1–125 Hz band-pass, then downsampling to 250 Hz ([LibriBrain](https://arxiv.org/html/2506.02098v1)).

**Source imaging.** Estimating the sources inside the head from fields measured outside (the inverse problem) has no unique solution, so every method adds a prior ([Hämäläinen 1993](https://doi.org/10.1103/RevModPhys.65.413)).
- **Equivalent current dipole (ECD).** One or a few point sources. This is the clinical standard for epileptic spikes ([FDA K210199](https://fda.innolitics.com/device/K210199)).
- **Minimum-norm estimates (MNE, dSPM, sLORETA).** Distributed sources on the cortex ([Hämäläinen & Ilmoniemi 1994](https://doi.org/10.1007/BF02512476)).
- **Beamformers.** LCMV ([Van Veen 1997](https://doi.org/10.1109/10.623056)) and DICS in the frequency domain ([Gross 2001](https://doi.org/10.1073/pnas.98.2.694)).

All three need a forward model (head geometry from MRI) and accurate MEG–MRI coregistration. Coregistration errors feed straight into the source estimates ([Gross 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC3925794/)). Spatial resolution is roughly centimetre-level, versus millimetres for 7T fMRI ([Benchetrit et al. 2024](https://arxiv.org/html/2310.19812v3)).

**File formats.** There is no single MEG standard ([Niso et al. 2018](https://doi.org/10.1038/sdata.2018.110)). The main ones, all readable by MNE-Python ([MNE docs](https://mne.tools/stable/auto_tutorials/io/10_reading_meg_data.html)):
- **FIF** (`.fif`): MEGIN/Elekta Neuromag, and MNE's native format. Mag4Health also exports FIFF ([Mag4Health](https://mag4health.com/product)).
- **CTF** `.ds`: a directory.
- **BTi/4D Neuroimaging**: a directory. Used by the HCP MEG data (Magnes 3600).
- **KIT / Ricoh** `.sqd` / `.con`.
- **FIL OPM** `.bin` and **Artemis123** `.bin`.
- **FieldTrip** `.mat`.

**BIDS-MEG** is the community folder and metadata standard that sits on top of these ([Niso 2018](https://doi.org/10.1038/sdata.2018.110), [mne-bids](https://github.com/mne-tools/mne-bids)).

## 2. Devices and specifications

**SQUID (cryogenic) systems**

| System | Company | Sensor type | Channels | Sampling rate | Noise floor | Shielding needs | Typical use | Status/price |
|---|---|---|---|---|---|---|---|---|
| TRIUX neo | MEGIN (owned by York Instruments) | SQUID: 102 magnetometers + 204 planar gradiometers | 306 MEG + 64 EEG (Yale config) | 1–5 kHz | — | MSR; internal helium recycler; tSSS + movement compensation | Clinical epilepsy and mapping, research | FDA 510(k) [K233985](https://fda.innolitics.com/device/K233985), May 2024; price not published ([Yale](https://research.yale.edu/cores/brainworks/megin-truix-neo-meg)) |
| CTF 275 (Omega/2005 series) | CTF MEG Neuro Innovations | SQUID axial gradiometers + 29 reference channels | 275 | Up to 12 kHz (6 kHz at Frankfurt) | — | MSR; optional helium recovery | Research, clinical | Selling new and refurbished; FDA [K030737](https://fda.innolitics.com/device/K030737) (2003, CTF Systems) ([CTF](https://www.ctf.com/), [McGill](https://www.mcgill.ca/bic/meg-unit/meg-bic/equipment)) |
| RICOH MEG | Ricoh (ex-Yokogawa/KIT line) | SQUID axial first-order gradiometers | 64–320 | — | 10 fT/√Hz | MSR, liquid helium | Epilepsy, evoked fields | FDA 2017 and [K210199](https://fda.innolitics.com/device/K210199) (Jul 2021); Ricoh bought the Yokogawa business in 2016 ([BioSpace](https://www.biospace.com/ricoh-meg-receives-fda-510-k-clearance)) |
| Orion LifeSpan MEG | Compumedics | DROS SQUID, axial gradiometers | 186 (adult) / 138 (child) helmets, dual-helmet dewar; up to 256 EEG | — | 10 fT/√Hz | MSR; 100% helium recycling | Clinical, pediatric, hyperscanning | FDA [K191785](https://fda.innolitics.com/device/K191785) (Feb 2020) ([product](https://www.compumedics.com.au/en/products/orionlifespanmeg/)) |
| MEGSCAN | York Instruments | SQUID | — | — | — | — | — | Described in 2018 ([Magnetics](https://magneticsmag.com/york-instruments-expands-its-magnetoencephalography-business-with-megin-acquisition/)); current status *unverified* (site unreachable on 2026-10-11) |

**OPM (wearable) systems**

| System | Company | Sensor type | Channels | Sampling rate | Noise floor | Shielding needs | Typical use | Status/price |
|---|---|---|---|---|---|---|---|---|
| QZFM Gen-3 sensor / Neuro-1 system | QuSpin | Rubidium zero-field OPM, dual-axis or triaxial | 64 sensors per backpack, 1–2 backpacks | — | Dual-axis <15 fT/√Hz (typ. 10–15 in dual-axis mode); triaxial <23 (typ. 15–20) | MSR; ±5 nT dynamic range | Sensors inside most academic OPM systems | Selling; price not published ([Gen-3](https://quspin.com/qzfm-gen-3), [Neuro-1](https://quspin.com/products/neuro-1/)) |
| HEDscan | FieldLine | Rubidium zero-field OPM | 128 (up to 512 supported) | 1 kHz used in validation | About 10 fT/√Hz per sensor; 20 ± 5 system | 4-layer MSR plus field coils (<30 nT); ±15 nT closed loop; 350 Hz bandwidth | Research, epilepsy research | Selling. No FDA clearance found in openFDA (checked 2026-10-11) ([FieldLine](https://fieldlineinc.com/), [Alem 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10303922/)) |
| Cerca OPM-MEG | Cerca Magnetics | QuSpin QZFM Gen-3 triaxial in a wearable helmet | 192 (64 triaxial) at Yale; matrix coils up to 128 elements at Zurich | — | Set by sensor (above) | MSR with active (matrix-coil) shielding | Pediatric, dementia, epilepsy research | Research system with no regulatory approval in any jurisdiction ([Cerca](https://www.cercamagnetics.com/), [Yale OPM](https://research.yale.edu/cores/optically-pumped-magnetoencephalography), [news](https://www.cercamagnetics.com/news)) |
| FYNA | Mag4Health | Helium-4 OPM, triaxial, room temperature | 16–96 sensors (48–288 channels) | 1,003.2 Hz standard, 3 kHz tested | <40 fT/√Hz on 2 axes (typ. 30); 200 on the third axis | Standard MSR, no field nulling needed (±200 nT) | Epilepsy (HFOs), research | Research system, not yet approved ([product](https://mag4health.com/product), [Bonnet 2025](https://www.frontiersin.org/articles/10.3389/fmedt.2025.1548260/full)) |
| Kernel Flux | Kernel | OPM modules | 432 magnetometers (title of 2021 paper) | — | — | Wearable shielding/compensation | Research, "natural experiences" | 2021 SPIE paper ([Pratt et al.](https://doi.org/10.1117/12.2581794)); current availability *unverified* |
| 384-channel array | University of Nottingham / Cerca / QuSpin authors | Triaxial OPMs | 384 | — | — | MSR | Research prototype | Dipole localization error <1 mm in phantom ([Schofield 2025](https://arxiv.org/abs/2509.03107)) |

## 3. Applications (domains)

| Domain | How MEG is used | Examples | Maturity |
|---|---|---|---|
| Epilepsy presurgical localization | Interictal spikes are localized with dipoles or distributed models and overlaid on MRI to guide surgery or electrode implantation | Erlangen series of 1,000 cases: 72% sensitivity. Completely resecting the MEG focus predicted seizure freedom, and diagnostic odds ratios were 41.6 extra-temporal vs 4.4 temporal ([Rampp 2019](https://doi.org/10.1093/brain/awz231)). US code CPT 95965 ([AuntMinnie](https://www.auntminnie.com/industry-news/regulatory/article/15566466/cms-hikes-meg-reimbursement)); payers cover intractable focal epilepsy ([Aetna](https://www.aetna.com/cpb/medical/data/200_299/0279.html)); [ACMEGS guideline 1](https://doi.org/10.1097/wnp.0b013e3182272fed) | Clinical, reimbursed |
| Presurgical functional mapping | Evoked fields localize somatosensory, motor, auditory, visual and language cortex before resection | [ACMEGS guideline 2](https://doi.org/10.1097/wnp.0b013e3182272ffe); CPT 95966/95967; UF Health uses it for brain tumours ([MEGIN news](https://megin.com/news/)) | Clinical |
| Cognitive neuroscience | Millisecond dynamics of perception, language and memory; time-resolved decoding (temporal generalization) | [King & Dehaene 2014](https://doi.org/10.1016/j.tics.2014.01.002); MOUS, THINGS-MEG datasets | Mature research |
| Developmental / pediatric (OPM) | Helmets that fit any head and tolerate movement allow scanning infants and children | 192-channel OPM-MEG across ages 2–34 ([Rier 2024](https://doi.org/10.7554/eLife.94561)); children with epilepsy had 2.3–4.6× higher spike amplitudes with OPM than SQUID ([Feys 2022](https://doi.org/10.1148/radiol.212453)); Aston study comparing OPM with SQUID MEG for localizing epileptiform activity in 20 children ([HRA](https://www.hra.nhs.uk/planning-and-improving-research/application-summaries/research-summaries/opm-meg-in-pre-surgical-mapping-for-patients-with-epilepsy/)) | Research to early clinical trials |
| Dementia, TBI, psychiatry | Resting-state spectra and connectivity as biomarkers | BioFIND MCI dataset ([Vaghari 2021](https://doi.org/10.1101/2021.05.19.21257330)); Cerca system at Oxford OHBA for dementia, £3.1M grant on blast exposure ([Cerca news](https://www.cercamagnetics.com/news)). Payers class Alzheimer's, TBI, autism and schizophrenia as investigational ([Aetna](https://www.aetna.com/cpb/medical/data/200_299/0279.html)) | Research |
| BCI and brain decoding | Deep networks map MEG to speech segments, typed characters, words or image embeddings | Speech perception: up to 41% accuracy among >1,000 segments ([Défossez 2023](https://arxiv.org/abs/2208.12266)). Typing: 32% CER ([Brain2Qwerty](https://arxiv.org/abs/2502.17480v1)). Images: 7× better retrieval than linear ([Benchetrit 2024](https://arxiv.org/abs/2310.19812v1)). Motor-imagery data: [MEGBCI2020](https://doi.org/10.1038/s41597-021-00899-7) | Research (fast-moving) |
| Neurofeedback / closed-loop rehab | Real-time sensorimotor-rhythm feedback drives a device | Six of 8 chronic stroke patients learned to drive a hand orthosis, with no significant change in clinical hand scores ([Buch 2008](https://doi.org/10.1161/strokeaha.107.505313)); real-time MEG review ([Parkkonen 2014](https://doi.org/10.1007/978-4-431-55037-2_17)); [mne-lsl](https://github.com/mne-tools/mne-lsl) | Research |
| Connectivity and networks | Band-limited amplitude envelopes and HMM state models describe resting networks | [Brookes 2011](https://doi.org/10.1073/pnas.1112685108); HCP MEG ([Larson-Prior 2013](https://doi.org/10.1016/j.neuroimage.2013.05.056)); [osl-dynamics](https://github.com/OHBA-analysis/osl-dynamics) | Research |
| Hyperscanning | Two MEG systems record two people interacting | Compumedics dual-helmet dewar ([product](https://www.compumedics.com.au/en/products/orionlifespanmeg/)); MEGIN dual-MEG at Tsinghua, Jul 2026 ([MEGIN news](https://megin.com/news/)) | Research |

## 4. Companies

| Company | Country | Focus | Key product | Status 2025–2026 |
|---|---|---|---|---|
| MEGIN / York Instruments | Finland / UK | SQUID MEG | TRIUX neo, MEG Maps | York bought MEGIN from Elekta in Jul 2018 ([Magnetics](https://magneticsmag.com/york-instruments-expands-its-magnetoencephalography-business-with-megin-acquisition/)). TRIUX neo FDA-cleared May 2024. Installations: Shanghai (Jun 2025), first MEG Maps system in Japan (May 2026), dual-MEG at Tsinghua (Jul 2026); BESA AI partnership (May 2026) ([MEGIN news](https://megin.com/news/)) |
| CTF MEG Neuro Innovations | Canada | SQUID MEG | CTF 275 | Selling new and refurbished systems, MSRs, helium recovery ([CTF](https://www.ctf.com/)); no 2025–26 news found |
| Ricoh | Japan | SQUID MEG | RICOH MEG | FDA 2017, re-cleared 2021 (K210199); 2025–26 activity *unverified* |
| Compumedics | Australia | SQUID MEG + EEG software (CURRY) | Orion LifeSpan | Five MEG orders worth about $25M (Chinese universities); Beijing Normal University $4.9M order, Nov 2025 ([Compumedics](https://www.compumedics.com.au/en/?p=16187)) |
| QuSpin | US | OPM sensors and systems | QZFM Gen-3, Neuro-1 | Supplies the sensors used by many academic OPM systems; "An Atomic Devices Company" ([QuSpin](https://quspin.com/)) |
| FieldLine | US (Boulder, CO) | OPM MEG | HEDscan | Selling; no FDA clearance found ([FieldLine](https://fieldlineinc.com/)) |
| Cerca Magnetics | UK | OPM MEG systems (Nottingham spin-out) | Cerca OPM-MEG | £3.8M Series A (Apr 2026). Share of £14M Innovate UK quantum funding (Nov 2025). UKRI-funded NHS clinical implementation with the Epilepsy Research Institute: installs from Jun 2027, aimed at UKCA/MHRA/NICE ([Cerca news](https://www.cercamagnetics.com/news), [ERI](https://epilepsy-institute.org.uk/?p=479685)) |
| Mag4Health | France | Helium-4 OPM MEG | FYNA | €5.3M raised (2023) ([Le Journal des Entreprises](https://www.lejournaldesentreprises.com/breve/la-medtech-iseroise-mag4health-leve-53-millions-deuros-2061574)). Lyon epilepsy trial of FYNA, 70 patients, from Sep 2026 ([NCT07281222](https://clinicaltrials.gov/study/NCT07281222)) |
| Kernel | US | Consumer/research neurotech | Flux (OPM), Flow (fNIRS) | Flux status *unverified* ([kernel.com](https://www.kernel.com/)) |
| Meta FAIR (Brain & AI) | France / US | Decoding research | Brain2Qwerty, brainmagick | Brain2Qwerty published in *Nature Neuroscience* 2026; v2 preprint ([repo](https://github.com/facebookresearch/brain2qwerty)) |

## 5. Patents

Status as listed on Google Patents on 2026-10-11. "Pending" means an application, not a granted patent.

| Patent number | Holder | Title/topic | Year | Why it matters |
|---|---|---|---|---|
| [US 7,463,024 B2](https://patents.google.com/patent/US7463024) | Elekta Neuromag Oy (Simola, Kajola, Taulu) | Processing a multi-channel magnetic measurement: the SSS method | Priority 2003, granted 2008; expired | The basis of MaxFilter/SSS, now free to implement (MNE has an open implementation) |
| [US 7,933,727 B2](https://patents.google.com/patent/US7933727) | Elekta AB (Taulu, Simola); Canadian family now held by Megin Oy (*unverified*) | Interference suppression using three volumes (tSSS) | Priority 2005, granted 2011; listed active | Removes nearby artifacts such as implants and dental work |
| [US 8,838,225 B2](https://patents.google.com/patent/US8838225) | Elekta AB | Orthogonal virtual channels for multi-channel data | Priority 2007, granted 2014 | Extends the SSS framework |
| [US 9,116,201 B2](https://patents.google.com/patent/US9116201) | QuSpin (Shah, Hughes) | Detecting zero-field resonance | Priority 2014, granted 2015 | Core zero-field OPM readout, the sensor type behind most OPM-MEG |
| [US 10,775,450 B1](https://patents.google.com/patent/US10775450) | QuSpin | Zero-field parametric resonance magnetometer with triaxial sensitivity | Priority 2020, granted 2020 | Measuring all three field components helps with motion and interference |
| [US 2021/0015427 A1](https://patents.google.com/patent/US20210015427A1) | QuSpin | Easily customizable multi-shell MEG helmet | Priority 2019 | Helmet design for wearable arrays |
| [US 12,564,331 B2](https://patents.google.com/patent/US12564331B2) | FieldLine (Park, Alem, Knappe, Holloway) | Sensor localization in an MEG system using coils | Priority 2021, granted Mar 2026 | Co-registration of flexible OPM arrays |
| [US 11,867,776 B2](https://patents.google.com/patent/US11867776B2) | FieldLine Industries | Laser-bonded glass-silicon vapour cell | Priority 2021, granted 2024 | Manufacturable OPM cells |
| [US 2024/0000359 A1](https://patents.google.com/patent/US20240000359A1) (also [EP 4221592](https://patents.google.com/patent/EP4221592A1), *unverified*) | University of Nottingham (Brookes, Boto) | Reducing MEG error from non-neuromagnetic fields | Priority 2020; pending | Interference modelling for OPM-MEG |
| [GB 2607881 A](https://patents.google.com/patent/GB2607881A) (*unverified*) | University of Nottingham (Brookes, Boto, Bowtell, Sims) | Helmet whose sensors slide toward/away from the head | Priority 2021; pending (EP version withdrawn) | One-size helmet for any head |
| [GB 2643046 A](https://patents.google.com/patent/GB2643046A) (*unverified*) | Cerca Magnetics + University of Nottingham | Linked array of sensor holders worn on the head | Priority 2024; pending | Cerca's next-generation flexible array |
| [FR 3147007 A1](https://patents.google.com/patent/FR3147007A1) (*unverified*) | Mag4Health | Optically pumped magnetometer cell | Priority 2023 | Helium-4 OPM hardware |
| [US 11,839,474 B2](https://patents.google.com/patent/US11839474B2) | HI LLC (link to Kernel *unverified*) | MEG phantoms simulating neural activity | Priority 2019, granted 2023 | One of a large HI LLC OPM/MEG portfolio |

## 6. Most-cited papers

Citation counts are from Crossref ("is-referenced-by-count"), checked on 2026-10-11. Crossref counts lower than Google Scholar does.

| Paper | Authors | Venue/year | Crossref cites | Why it matters |
|---|---|---|---|---|
| [Magnetoencephalography: evidence of magnetic fields produced by alpha-rhythm currents](https://doi.org/10.1126/science.161.3843.784) | Cohen | Science 1968 | 607 | First MEG recording |
| [Magnetoencephalography: detection of the brain's electrical activity with a superconducting magnetometer](https://doi.org/10.1126/science.175.4022.664) | Cohen | Science 1972 | 652 | First SQUID MEG |
| [Magnetoencephalography — theory, instrumentation, and applications](https://doi.org/10.1103/RevModPhys.65.413) | Hämäläinen, Hari, Ilmoniemi, Knuutila, Lounasmaa | Rev. Mod. Phys. 1993 | 4,030 | The standard physics reference |
| [Interpreting magnetic fields of the brain: minimum norm estimates](https://doi.org/10.1007/BF02512476) | Hämäläinen, Ilmoniemi | Med. Biol. Eng. Comput. 1994 | 1,887 | The minimum-norm inverse used in MNE |
| [Localization of brain electrical activity via LCMV spatial filtering](https://doi.org/10.1109/10.623056) | Van Veen et al. | IEEE TBME 1997 | 2,504 | The LCMV beamformer |
| [Dynamic imaging of coherent sources (DICS)](https://doi.org/10.1073/pnas.98.2.694) | Gross et al. | PNAS 2001 | 1,754 | Frequency-domain beamformer for oscillations and coherence |
| [Spatiotemporal signal space separation (tSSS)](https://doi.org/10.1088/0031-9155/51/7/008) | Taulu, Simola | Phys. Med. Biol. 2006 | 1,594 | Standard interference suppression (SSS itself: [Taulu & Kajola 2005](https://doi.org/10.1063/1.1935742)) |
| [FieldTrip](https://doi.org/10.1155/2011/156869) | Oostenveld, Fries, Maris, Schoffelen | Comput. Intell. Neurosci. 2011 | 9,857 | Main MATLAB toolbox |
| [Brainstorm](https://doi.org/10.1155/2011/879716) | Tadel et al. | Comput. Intell. Neurosci. 2011 | 3,540 | GUI toolbox |
| [Good practice for conducting and reporting MEG research](https://doi.org/10.1016/j.neuroimage.2012.10.001) | Gross et al. | NeuroImage 2013 | 727 | Community guidelines; read before your first study |
| [MEG and EEG data analysis with MNE-Python](https://doi.org/10.3389/fnins.2013.00267) / [MNE software](https://doi.org/10.1016/j.neuroimage.2013.10.027) | Gramfort et al. | Front. Neurosci. 2013 / NeuroImage 2014 | 3,845 / 2,084 | The Python stack most ML work builds on |
| [Characterizing the dynamics of mental representations: temporal generalization](https://doi.org/10.1016/j.tics.2014.01.002) | King, Dehaene | TICS 2014 | 1,071 | Time-resolved decoding method |
| [Magnetoencephalography for brain electrophysiology and imaging](https://doi.org/10.1038/nn.4504) | Baillet | Nat. Neurosci. 2017 | 1,032 | Modern review |
| [Moving MEG towards real-world applications with a wearable system](https://doi.org/10.1038/nature26147) | Boto et al. | Nature 2018 | 1,370 | First wearable OPM-MEG with free head movement |

## 7. New achievements (2023–2026)

- **Speech perception decoding.** A contrastive model trained on 175 volunteers (4 public M/EEG datasets) identifies which 3 s speech segment a person heard. It reaches up to 41% accuracy among more than 1,000 candidates on average, and over 80% in the best participants ([Défossez et al., *Nat. Mach. Intell.* 2023](https://arxiv.org/abs/2208.12266)).
- **Images from MEG.** On THINGS-MEG (4 participants, 22,448 images, 272 channels), retrieval is 7× better than linear decoders. Late responses are best explained by DINOv2 features. Generated images keep high-level content but little low-level detail ([Benchetrit, Banville, King, ICLR 2024](https://arxiv.org/html/2310.19812v3)).
- **Words at scale.** Words were decoded across 723 participants. MEG beats EEG and reading beats listening, and more data per participant helps more than more participants ([d'Ascoli et al. 2024](https://arxiv.org/abs/2412.17829)).
- **Typing from MEG (Brain2Qwerty).**
  - v1: 35 volunteers typed memorized sentences. Character error rate was 32% with MEG versus 67% with EEG, and 19% for the best participant ([arXiv Feb 2025](https://arxiv.org/abs/2502.17480v1)); published in *Nature Neuroscience* in 2026 ([paper](https://www.nature.com/articles/s41593-026-02303-2)).
  - v2: 9 participants, about 10 h of MEG each and about 22,000 sentences. Word accuracy was 61% on average and 78% for the best participant, and accuracy rises log-linearly with data ([Meta blog](https://ai.meta.com/blog/brain2qwerty-brain-ai-human-communication/)). The v2 data is embargoed ([repo](https://github.com/facebookresearch/brain2qwerty)).
- **Self-supervised scaling.** Pretraining on nearly 400 h of MEG from 900 subjects improves speech decoding by 15–27% over prior models ([Jayalath et al., ICML 2025](https://www.arxiv.org/abs/2406.04328v5)).
- **Foundation models.**
  - BrainOmni pretrains on 1,997 h of EEG plus 656 h of MEG and transfers to unseen devices ([NeurIPS 2025](https://arxiv.org/abs/2505.18185)).
  - MEG-GPT, trained on 612 Cam-CAN subjects, raises zero-shot cross-subject accuracy from 0.41 to 0.49 ([arXiv Oct 2025](https://arxiv.org/abs/2510.18080)).
- **LibriBrain.** Over 52 h from one participant across 95 sessions (MEGIN 306 channels, 1 kHz). Baselines: speech-detection F1 0.899, and 39-class phoneme micro-F1 0.117 ([NeurIPS 2025 D&B](https://arxiv.org/html/2506.02098v1)).
- **PNPL 2025 competition (NeurIPS 2025).** $10,000 prize pool ([prizes](https://libribrain.com/editions/2025/prizes/)). The team that won the Phoneme Standard track reported 65.8% F1-macro on phonemes, and its speech-detection system scored 88.9% ([MEGConformer](https://arxiv.org/abs/2512.01443)).
- **PNPL 2026 edition.** The 2026 edition classifies 50 heard words on LibriBrain100: more than 100 h, 33 subjects, with "Deep" (single subject) and "Broad" (32 subjects) tracks. Submissions close 15 Oct 2026 ([libribrain.com](https://libribrain.com/)).
- **OPM milestones.**
  - First OPM system with more channels than SQUID MEG: 384 channels, dipole error <1 mm ([Schofield 2025](https://arxiv.org/abs/2509.03107)).
  - Whole-head helium-4 OPM with 288 channels benchmarked against cryogenic MEG ([Bonnet 2025](https://www.frontiersin.org/articles/10.3389/fmedt.2025.1548260/full)).
  - Development tracked from age 2 to 34 ([Rier 2024](https://doi.org/10.7554/eLife.94561)).
- **OPM clinical trials.** Aston University's pediatric epilepsy trial began 17 Jun 2025 (20 children; [NCT07378397](https://clinicaltrials.gov/study/NCT07378397)). Lyon's FYNA trial (70 patients) is planned for Sep 2026 ([NCT07281222](https://clinicaltrials.gov/study/NCT07281222)). A UKRI-funded NHS implementation is planned for 2027–28 ([ERI](https://epilepsy-institute.org.uk/?p=479685)).

## 8. Current state of the field

**Where MEG is used today, and where it is still research**

| Maturity | Applications |
|---|---|
| Established clinical | Epilepsy focus localization and presurgical functional mapping with SQUID MEG (FDA-cleared MEGIN, Ricoh, Compumedics, CTF systems) |
| Commercial, growing | OPM research systems (Cerca, FieldLine, QuSpin, Mag4Health); SQUID sales in China |
| Trials / early | OPM-MEG for pediatric epilepsy (Aston, Lyon, NHS plan); no OPM-MEG FDA clearance found |
| Research | Speech, word, typing and image decoding; foundation models; biomarkers for dementia, TBI and psychiatry; neurofeedback; hyperscanning |

**Open problems**
- **Hardware access.** SQUID systems need a shielded room and cryogenics, and payers still treat most non-epilepsy uses as investigational ([Aetna](https://www.aetna.com/cpb/medical/data/200_299/0279.html)). That keeps data scarce and limits practical BCIs to the lab.
- **Generalization across subjects and devices.** The 2026 PNPL "Broad" track and BrainOmni exist because models trained on one person or one scanner transfer poorly. Brain2Qwerty v2 gains came from about 10× more data *per participant*.
- **Typing is not yet communication.** Brain2Qwerty decodes typing *while people really type*, and part of the signal is motor ([arXiv](https://arxiv.org/abs/2502.17480v1)). Showing that it works for people who cannot move is still open.
- **OPM practicalities.** OPMs stop working if the field changes by more than about 3 nT ([Brookes 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC10465236/)). Other open issues are noise (7–23 fT/√Hz vs 2–5 fT/√Hz for SQUIDs), sensor co-registration, and cross-talk in dense arrays.
- **Phoneme-level decoding is hard.** The LibriBrain 39-class baseline micro-F1 is 0.117 even with 52 h of data from one subject.
- **Licensing.** Brain2Qwerty code and data are CC BY-NC 4.0, and LibriBrain is CC BY-NC 4.0 on Hugging Face ([HF](https://huggingface.co/datasets/pnpl/LibriBrain)).

**Where an AI engineer can contribute.** Self-supervised pretraining over heterogeneous MEG (sensor-layout-aware tokenizers such as BrainOmni's, or MEG-GPT). Subject and device adaptation. Contrastive alignment to speech, text and vision models. CTC and language-model fusion for sentence decoding. Learned denoising and artifact removal that could replace or extend tSSS and ICA. Motion-robust OPM processing. Real-time inference for neurofeedback. Honest held-out-subject benchmarks. Entering the PNPL competition with `pnpl` loaders is the quickest start.

## 9. Public datasets

| Dataset | Content | Size | Link |
|---|---|---|---|
| LibriBrain / LibriBrain100 | Listening to audiobooks (Sherlock Holmes); speech, phoneme and word labels | 52 h from 1 subject; LibriBrain100 >100 h, 33 subjects | [arXiv](https://arxiv.org/abs/2506.02098), [HF](https://huggingface.co/datasets/pnpl/LibriBrain), [site](https://libribrain.com/) |
| MEG-MASC | Naturalistic English stories with word and phoneme timings | 27 participants × 2 h | [Sci. Data 2023](https://doi.org/10.1038/s41597-023-02752-5) |
| MOUS | Reading or listening to sentences, plus rest | 204 subjects (MEG + MRI) | [Sci. Data 2019](https://doi.org/10.1038/s41597-019-0020-y) |
| Armeni 2022 | Audiobook listening, head casts | 3 participants × 10 h | [Sci. Data 2022](https://doi.org/10.1038/s41597-022-01382-7) |
| THINGS-MEG | Object images | 4 participants, 22,448 images, 272 ch | [eLife 2023](https://doi.org/10.7554/eLife.82580) |
| Brain2Qwerty v1 (Spanish BCBL) | Typing memorized sentences, MEG + EEG | 35 volunteers; MEG 21.5 h | [HF](https://huggingface.co/datasets/bcbl190626/SpanishBCBL) |
| Cam-CAN | Lifespan rest and tasks | About 700 adults, 18–87 years | [NeuroImage 2017](https://doi.org/10.1016/j.neuroimage.2015.09.018) |
| HCP MEG | Rest and motor, working-memory and language tasks | 50 twin pairs planned | [NeuroImage 2013](https://doi.org/10.1016/j.neuroimage.2013.05.056) |
| OMEGA | Open resting-state archive | Multi-site | [NeuroImage 2016](https://doi.org/10.1016/j.neuroimage.2015.04.028) |
| Wakeman & Henson | Faces; MEG + EEG + fMRI | 19 volunteers | [Sci. Data 2015](https://doi.org/10.1038/sdata.2015.1) |
| MEGBCI2020 | Hand, feet, subtraction and word imagery | 17 participants × 2 sessions, 306 ch @ 1 kHz | [Sci. Data 2021](https://doi.org/10.1038/s41597-021-00899-7) |

Full specifications for each dataset, and tables of published results on them, are in [DATASETS.md](DATASETS.md).

## 10. GitHub repositories

Stars and dates checked via the GitHub API on 2026-10-11.

"Custom" means GitHub could not detect a standard license (`NOASSERTION`), so read the repo's LICENSE file before reusing the code. "—" means no license file or no detected language.

**Toolkits and libraries**

| Repo | What it does / when to use it | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [mne-tools/mne-python](https://github.com/mne-tools/mne-python) | Full MEG/EEG pipeline: I/O for all formats, Maxwell filtering, ICA, source imaging, decoding. Start here | Python | 3542 | 2026-10 | BSD-3-Clause |
| [fieldtrip/fieldtrip](https://github.com/fieldtrip/fieldtrip) | MATLAB toolbox for MEG/EEG/iEEG: beamformers, connectivity, cluster statistics | MATLAB | 990 | 2026-10 | GPL-3.0 |
| [brainstorm-tools/brainstorm3](https://github.com/brainstorm-tools/brainstorm3) | GUI-driven MEG/EEG analysis and source imaging | MATLAB | 488 | 2026-10 | GPL-3.0 |
| [spm/spm](https://github.com/spm/spm) | SPM development version: M/EEG source inversion, DCM, OPM support | MATLAB | 219 | 2026-10 | GPL-2.0 |
| [OHBA-analysis/osl-ephys](https://github.com/OHBA-analysis/osl-ephys) | Oxford's batch preprocessing and source-recon pipeline built on MNE (the old `osl` repo redirects here) | Python | 64 | 2026-10 | Custom |
| [OHBA-analysis/osl-dynamics](https://github.com/OHBA-analysis/osl-dynamics) | HMM and dynamic network models of brain states | Python | 92 | 2026-10 | Apache-2.0 |
| [mne-tools/mne-bids](https://github.com/mne-tools/mne-bids) | Read and write BIDS-MEG datasets | Python | 182 | 2026-10 | BSD-3-Clause |
| [mne-tools/mne-bids-pipeline](https://github.com/mne-tools/mne-bids-pipeline) | Configurable end-to-end processing of whole BIDS datasets | Python | 172 | 2026-10 | BSD-3-Clause |
| [bids-standard/bids-specification](https://github.com/bids-standard/bids-specification) | The BIDS standard, including MEG | Python | 370 | 2026-10 | CC-BY-4.0 |
| [mne-tools/mne-connectivity](https://github.com/mne-tools/mne-connectivity) | Spectral and time-resolved connectivity | Python | 92 | 2026-10 | BSD-3-Clause |
| [AaltoImagingLanguage/conpy](https://github.com/AaltoImagingLanguage/conpy) | DICS power mapping and all-to-all connectivity | Python | 41 | 2026-09 | BSD-3-Clause |
| [mne-tools/mne-rsa](https://github.com/mne-tools/mne-rsa) | Representational similarity analysis on MEG/EEG | Python | 88 | 2026-10 | BSD-3-Clause |
| [autoreject/autoreject](https://github.com/autoreject/autoreject) | Automatic bad-trial and bad-sensor rejection and repair | Python | 162 | 2026-10 | BSD-3-Clause |
| [mne-tools/mne-icalabel](https://github.com/mne-tools/mne-icalabel) | Automatic labelling of ICA components | Python | 124 | 2026-10 | BSD-3-Clause |
| [Neuronal-Oscillations/FLUX](https://github.com/Neuronal-Oscillations/FLUX) | Documented, opinionated MEG analysis pipeline with MNE | HTML | 65 | 2025-01 | BSD-3-Clause |
| [mne-tools/mne-hcp](https://github.com/mne-tools/mne-hcp) | Load HCP MEG data into MNE | Python | 28 | 2024-07 | BSD-3-Clause |
| [mne-tools/mne-cpp](https://github.com/mne-tools/mne-cpp) | C++ framework for real-time acquisition and processing | C++ | 177 | 2026-10 | BSD-3-Clause |
| [mne-tools/mne-lsl](https://github.com/mne-tools/mne-lsl) | Real-time streaming (LSL) for closed-loop and neurofeedback | Python | 91 | 2026-10 | BSD-3-Clause |
| [mne-tools/mne-realtime](https://github.com/mne-tools/mne-realtime) | Older real-time client for MEGIN/FieldTrip buffers | Python | 58 | 2026-09 | BSD-3-Clause |

**Decoding models and papers with code**

| Repo | What it does / when to use it | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [facebookresearch/brain2qwerty](https://github.com/facebookresearch/brain2qwerty) | Brain2Qwerty v1 and v2: conv encoder + transformer + character LM for typed-sentence decoding | Python | 1102 | 2026-09 | Custom (README: CC BY-NC 4.0) |
| [facebookresearch/brainmagick](https://github.com/facebookresearch/brainmagick) | Code for Défossez 2023 speech-perception decoding. Archived | Python | 474 | 2024-03 | Custom, archived |
| [facebookresearch/neuroai](https://github.com/facebookresearch/neuroai) | Meta's NeuralSet/NeuralTrain data and training suite used by Brain2Qwerty | Python | 323 | 2026-10 | MIT |
| [braindecode/braindecode](https://github.com/braindecode/braindecode) | PyTorch deep-learning models for EEG/MEG decoding | Python | 1323 | 2026-10 | BSD-3-Clause |
| [OpenTSLab/BrainOmni](https://github.com/OpenTSLab/BrainOmni) | BrainOmni EEG+MEG foundation model (NeurIPS 2025) | Jupyter Notebook | 78 | 2025-12 | Custom |
| [pyRiemann/pyRiemann](https://github.com/pyRiemann/pyRiemann) | Covariance and Riemannian classifiers, a strong classic baseline | Python | 779 | 2026-10 | BSD-3-Clause |
| [zubara/mneflow](https://github.com/zubara/mneflow) | Compact CNN decoders for MEG on top of MNE (TensorFlow) | Python | 46 | 2026-09 | BSD-3-Clause |
| [ricsinaruto/MEG-transfer-decoding](https://github.com/ricsinaruto/MEG-transfer-decoding) | Sliding-window vs full-epoch MEG decoders, with permutation feature importance | Jupyter Notebook | 18 | 2024-05 | MIT |
| [ivsemenkov/LISA](https://github.com/ivsemenkov/LISA) | Compact, interpretable MEG-to-audio retrieval | Python | 19 | 2026-09 | MIT |
| [kingjr/meg-masc](https://github.com/kingjr/meg-masc) | Validation and decoding code for the MEG-MASC dataset | Python | 49 | 2023-09 | BSD-3-Clause |

**Benchmarks and dataset loaders**

| Repo | What it does / when to use it | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [neural-processing-lab/pnpl](https://github.com/neural-processing-lab/pnpl) | `pip install pnpl`: PyTorch loaders for LibriBrain, LibriBrain100, MEG-MASC, Armeni, MOUS and more, plus task objects | Python | 15 | 2026-09 | BSD-3-Clause |
| [neural-processing-lab/libribrain-experiments](https://github.com/neural-processing-lab/libribrain-experiments) | Official LibriBrain baselines | Python | 4 | 2025-05 | BSD-3-Clause |
| [neural-processing-lab/2025-libribrain-competition](https://github.com/neural-processing-lab/2025-libribrain-competition) | Competition website source | TypeScript | 6 | 2026-10 | — |
| [kovalalvi/alvi-libribrain-2025](https://github.com/kovalalvi/alvi-libribrain-2025) | 3rd-place LibriBrain 2025 solution | Jupyter Notebook | 4 | 2025-12 | — |
| [OpenTSLab/MEG-to-Speech-Detection-for-the-LibriBrain-Competition-NeurIPS-2025](https://github.com/OpenTSLab/MEG-to-Speech-Detection-for-the-LibriBrain-Competition-NeurIPS-2025) | Speech-detection Standard-track model (Parameter Team, track winner) | Python | 4 | 2025-12 | — |
| [eegdash/EEGDash](https://github.com/eegdash/EEGDash) | Catalog and PyTorch loaders for 700+ BIDS EEG/MEG/iEEG datasets | Python | 89 | 2026-10 | BSD-3-Clause |
| [sagihaider/MEGBCI2020](https://github.com/sagihaider/MEGBCI2020) | Code for the MEG motor/cognitive imagery BCI dataset | MATLAB | 18 | 2021-10 | MIT |

**OPM tools**

| Repo | What it does / when to use it | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [tierneytim/OPM](https://github.com/tierneytim/OPM) | OPM processing in SPM (UCL FIL) | MATLAB | 18 | 2024-06 | GPL-2.0 |
| [FIL-OPMEG/optitrack](https://github.com/FIL-OPMEG/optitrack) | Scripts and SOPs for motion capture during OPM recordings | MATLAB | 3 | 2025-07 | Custom |
| [FLUX-pipeline/FieldLine](https://github.com/FLUX-pipeline/FieldLine) | FLUX pipeline adapted to FieldLine OPM data | Jupyter Notebook | 2 | 2026-06 | — |
| [laurabpaulsen/OPM_lab](https://github.com/laurabpaulsen/OPM_lab) | Collection and analysis code for FieldLine semi-rigid helmet data | Python | 3 | 2025-01 | — |
| [HollySchofield/Towards-a-384-channel-magnetoencephalography-system-based-on-optically-pumped-magnetometers](https://github.com/HollySchofield/Towards-a-384-channel-magnetoencephalography-system-based-on-optically-pumped-magnetometers) | Repo named after the Schofield 2025 384-channel paper (no description) | Python | 1 | 2025-12 | — |
| [peterjhobson/fields_in_shields](https://github.com/peterjhobson/fields_in_shields) | Design coils inside shielded cylinders to null background fields | Python | 8 | 2021-01 | Custom |
| [juangpc/fieldline-opm-client](https://github.com/juangpc/fieldline-opm-client) | Client for streaming from FieldLine OPMs (no description) | Python | 5 | 2022-02 | — |

**Curated lists**

| Repo | What it does / when to use it | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [openlists/ElectrophysiologyData](https://github.com/openlists/ElectrophysiologyData) | List of open electrophysiology datasets, including MEG | — | 551 | 2026-06 | — |
| [analyticalmonk/awesome-neuroscience](https://github.com/analyticalmonk/awesome-neuroscience) | General neuroscience software list | — | 1732 | 2026-06 | — |
