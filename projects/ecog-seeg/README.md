# ECoG and sEEG (Intracranial EEG)

Intracranial EEG (iEEG) records the brain's electrical field potentials from electrodes placed on the cortex (electrocorticography, ECoG), inside the brain on depth shafts (stereo-EEG, sEEG), or, more recently, from inside a blood vessel next to the cortex (the endovascular Stentrode). Because the electrodes sit past the skull, the signal is 10 to 100 times larger than scalp EEG and carries usable activity up to and above 150 Hz ([Mercier et al. 2022](https://doi.org/10.1016/j.neuroimage.2022.119438), [Metzger et al. 2023](https://doi.org/10.1038/s41586-023-06443-4)). Today it is used most in epilepsy surgery workups, in implanted closed-loop therapies for epilepsy and Parkinson's disease, and in some of the best-performing speech and motor BCIs that do not penetrate the brain ([Morrell 2011](https://doi.org/10.1212/WNL.0b013e3182302056), [Medtronic 2025](https://news.medtronic.com/2025-02-24-Medtronic-earns-U-S-FDA-approval-for-the-worlds-first-Adaptive-deep-brain-stimulation-system-for-people-with-Parkinsons)).

Items marked *unverified* could not be confirmed from a source. Cells marked "—" mean the manufacturer did not publish the spec, or I could not find it.

## 1. The data

**What is measured.** Each electrode picks up the summed extracellular field potential of the large population of neurons near it. Above about 80 Hz there is a broadband "high-gamma" signal that tracks the firing rate of the neurons under the electrode rather than an oscillation ([Ray & Maunsell 2011](https://doi.org/10.1371/journal.pbio.1000610), [Miller et al. 2009](https://doi.org/10.1371/journal.pcbi.1000609)). High-gamma power (most decoders use 70–150 Hz) is the main feature behind ECoG speech and motor BCIs and behind passive functional mapping ([Crone et al. 1998](https://doi.org/10.1093/brain/121.12.2301), [Moses et al. 2021](https://doi.org/10.1056/NEJMoa2027540), [Metzger et al. 2023](https://doi.org/10.1038/s41586-023-06443-4)).

**How it differs from scalp EEG.** iEEG signals range from 0.05 to 2 mV, about 10 to 100 times larger than scalp EEG ([Mercier et al. 2022](https://doi.org/10.1016/j.neuroimage.2022.119438)). Skull and scalp blur and low-pass filter scalp EEG, so iEEG gives millimetre-scale spatial detail and keeps high frequencies that scalp EEG largely loses ([Parvizi & Kastner 2018](https://doi.org/10.1038/s41593-018-0108-2)). The trade-off is coverage: electrodes go only where the clinical team needs them, so every patient has a different, sparse layout. That is the central problem for machine learning on iEEG (section 8).

**Recording types**

| Type | How | Used for |
|---|---|---|
| Subdural ECoG (grids and strips) | Silicone sheets with platinum or stainless-steel discs, placed on the cortex through a craniotomy. Ad-Tech's current 510(k) covers up to 256 contacts at 1–20 mm spacing ([K191186](https://fda.innolitics.com/device/K191186)) | Epilepsy monitoring, intraoperative mapping, research BCIs |
| High-density ECoG | Same idea, smaller and denser discs: 128 contacts at 4 mm ([Moses 2021](https://doi.org/10.1056/NEJMoa2027540)), 253 contacts at 3 mm ([Metzger 2023](https://doi.org/10.1038/s41586-023-06443-4)) | Speech BCIs |
| Thin-film micro-ECoG | Microfabricated polymer films with hundreds to thousands of small electrodes. Precision's Layer 7 has 1,024 electrodes per array ([Fierce Biotech](https://www.fiercebiotech.com/medtech/precision-neuroscience-deploys-4096-electrodes-brain-computer-interface-procedure)); NeuroOne makes thin-film cortical and sEEG electrodes ([K192764](https://fda.innolitics.com/device/K192764), [K222404](https://fda.innolitics.com/device/K222404)) | Intraoperative mapping, high-resolution BCI research |
| Epidural ECoG | Electrodes on top of the dura, so the brain's covering is not opened. WIMAGINE: 64 electrodes, 2.3 mm diameter, 4–4.5 mm pitch, built into a wireless implant that replaces a piece of skull ([Moly et al. 2022](https://arxiv.org/abs/2201.10449), [Lorach 2023](https://doi.org/10.1038/s41586-023-06094-5)) | Long-term motor BCIs (exoskeleton, brain–spine interface) |
| Stereo-EEG (depth) | Thin shafts inserted through small drill holes. Contacts are about 2 mm long and 0.8–2 mm wide, 2.5–10 mm apart; a typical implant has 8–20 shafts with 5–20 contacts each ([Mercier 2022](https://doi.org/10.1016/j.neuroimage.2022.119438)) | Epilepsy localization, especially deep or bilateral foci; cognitive research (hippocampus, insula) |
| Endovascular | Electrodes on a stent placed in the superior sagittal sinus through the jugular vein. Stentrode: 16 electrodes, 3 mm spacing ([Mitchell et al. 2023](https://doi.org/10.1001/jamaneurol.2022.4847)) | Motor BCI for paralysis without opening the skull |
| Chronic sensing neurostimulators | Implanted stimulators that also record a few channels for months to years: NeuroPace RNS (4 channels), Medtronic Percept (DBS local field potentials) | Closed-loop epilepsy and Parkinson's therapy; long-term "ambulatory" iEEG data |

**Clinical recording context.** Almost all human iEEG comes from people with drug-resistant epilepsy who are monitored in an epilepsy monitoring unit (EMU) to find where seizures start before surgery. Standard grids, strips and depth electrodes are cleared for temporary use of less than 30 days ([Ad-Tech K191186](https://fda.innolitics.com/device/K191186), [NeuroOne K222404](https://fda.innolitics.com/device/K222404)). While patients wait for seizures, many volunteer for research tasks, which is where most iEEG datasets come from. Electrode placement is set by clinical need, not research needs ([Parvizi & Kastner 2018](https://doi.org/10.1038/s41593-018-0108-2)).

**Electrode localization.** To know where each contact sits, the post-implant CT (or MRI) is co-registered to the pre-implant MRI. Contacts are then labelled (grey vs white matter, gyrus, atlas region) and can be warped to a template brain for group analysis ([Mercier 2022](https://doi.org/10.1016/j.neuroimage.2022.119438)). Grids also need correction for brain shift caused by the craniotomy. Tools: iELVis (brain-shift correction, FreeSurfer atlases; [Groppe et al. 2017](https://doi.org/10.1016/j.jneumeth.2017.01.022)), img_pipe (from a pre-op T1 and post-op CT; [Hamilton et al. 2017](https://doi.org/10.3389/fninf.2017.00062)), MNE-Python, and SEEG Assistant for 3D Slicer (section 10).

**Signal characteristics**

| Property | Typical value | Source |
|---|---|---|
| Amplitude | 0.05–2 mV, about 10–100× scalp EEG | [Mercier 2022](https://doi.org/10.1016/j.neuroimage.2022.119438) |
| Useful bandwidth | Clinical recordings are typically sampled around 1 kHz. High-gamma features are taken from 70–150 Hz; low-frequency features from 0.3–17 Hz in the UCSF speech work | [Mercier 2022](https://doi.org/10.1016/j.neuroimage.2022.119438), [Metzger 2023](https://doi.org/10.1038/s41586-023-06443-4) |
| Sampling rates in practice | Clinical amplifiers: up to 10 kHz (Nihon Kohden JE-120A) or 16 kHz (Natus Quantum). Research systems: 30 kHz (Blackrock NeuroPort), 38.4 kHz internal (g.HIamp). Chronic implants are much lower: 250 Hz (NeuroPace RNS, Medtronic Percept), 586 Hz (WIMAGINE) | Section 2 |
| ECoG contact size and spacing | Exposed diameter 1–4.5 mm; spacing typically 3–10 mm (clinical grids usually 10 mm) | [Mercier 2022](https://doi.org/10.1016/j.neuroimage.2022.119438) |
| sEEG contact size and spacing | About 2 mm long, 0.8–2 mm diameter, 2.5–10 mm apart. Example: PMT 2102 series: 0.8 mm lead, 2.0 mm contacts, 1.5 mm gaps, 8–16 contacts | [Mercier 2022](https://doi.org/10.1016/j.neuroimage.2022.119438), [OSS-DBS electrode docs](https://oss-dbsv2.readthedocs.io/en/stable/electrode_files/PMTsEEG.html) |
| Channel counts | Clinical: often more than 100 contacts per patient (≥128 channels in EMU monitoring); Brain Treebank averages 168 electrodes per subject. High-density research arrays: 128–253; thin-film: 1,024 per array, up to 4,096 in one procedure | [Quigg et al. 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC5008166), [Brain Treebank](https://arxiv.org/abs/2411.08343), [Precision](https://precisionneuro.io/), [Fierce Biotech](https://www.fiercebiotech.com/medtech/precision-neuroscience-deploys-4096-electrodes-brain-computer-interface-procedure) |
| Noise and artifacts | Eye blinks and movements, cardiac and muscle activity still leak in; the choice of reference matters (e.g. a pair of white-matter contacts as reference; bipolar or common-average re-referencing). | [Mercier 2022](https://doi.org/10.1016/j.neuroimage.2022.119438) |
| Long-term stability | Vansteensel's home-use ECoG BCI worked for about 6 years before signals faded with ALS-related atrophy; Stentrode signal bandwidth stayed at 233 ± 16 Hz over 12 months | [Vansteensel 2024](https://doi.org/10.1056/NEJMoa2314598), [Mitchell 2023](https://doi.org/10.1001/jamaneurol.2022.4847) |

**Formats.** Clinical systems export EDF/EDF+ ([edfplus.info](https://www.edfplus.info/)) or vendor formats. The research standard is iEEG-BIDS, which adds electrode coordinates, channel status and event files to a BIDS folder ([Holdgraf et al. 2019](https://doi.org/10.1038/s41597-019-0105-7), [spec](https://bids-specification.readthedocs.io/en/stable/modality-specific-files/intracranial-electroencephalography.html)); OpenNeuro hosts iEEG datasets in this form. Neurodata Without Borders (NWB, HDF5-based; [nwb.org](https://www.nwb.org/)) is used by the UCSF ECoG group's tools (ecogVIS). MNE-Python and MNE-BIDS read all of these.

## 2. Devices and specifications

**Electrodes (acute, under 30 days)**

| Device | Company | Type | Contacts/channels | Sampling rate | Implant duration | Regulatory | Typical use | Status |
|---|---|---|---|---|---|---|---|---|
| Subdural strip / grid / interhemispheric / mapping grid | Ad-Tech Medical | ECoG | Up to 256 contacts; discs 1.96–6.35 mm; spacing 1–20 mm; Pt/Ir or stainless steel | Set by amplifier | < 30 days | FDA 510(k) [K191186](https://fda.innolitics.com/device/K191186) (Jan 2020) | EMU monitoring, intraoperative mapping | Current |
| Spencer Probe depth electrodes | Ad-Tech Medical | sEEG / depth | — | Set by amplifier | — | 510(k) [K223269](https://fda.innolitics.com/device/K223269) (May 2023) | sEEG | Current |
| Depthalon / sEEG 2102 series | PMT Corporation | sEEG / depth | 8–16 contacts; 2.0 mm contacts, 1.5 mm gaps, 0.8 mm diameter | Set by amplifier | — | Listed in FDA GUDID ([example](https://accessgudid.nlm.nih.gov/devices/00650551147343)); PMT subdural electrodes 510(k) [K082474](https://fda.innolitics.com/device/K082474) | sEEG; PMT also built the 128-ch array in [Moses 2021](https://doi.org/10.1056/NEJMoa2027540) | Current |
| Microdeep | DIXI Medical | sEEG / depth | 5–18 Pt/Ir contacts, 2 mm long, 0.8 mm diameter | Set by amplifier | — | 510(k) [K170959](https://fda.innolitics.com/device/K170959) (2017); micro-macro version [K202087](https://fda.innolitics.com/device/K202087) (2021) | sEEG; micro-macro adds single-unit microwires | Current |
| AuraGen cortical surface electrodes | Integra | ECoG | — | Set by amplifier | — | 510(k) [K082250](https://fda.innolitics.com/device/K082250) (2008) | ECoG monitoring | Current status *unverified* |
| Evo Cortical | NeuroOne | Thin-film ECoG | — | Set by amplifier | — | 510(k) [K192764](https://fda.innolitics.com/device/K192764) (Nov 2019) | ECoG monitoring | Current ([NeuroOne](https://nmtc1.com/)) |
| Evo sEEG | NeuroOne | Thin-film sEEG | — | Set by amplifier | < 30 days | 510(k) [K211367](https://fda.innolitics.com/device/K211367) (2021, < 24 h); [K222404](https://fda.innolitics.com/device/K222404) (Oct 2022, < 30 days) | sEEG | Current; distributed with Zimmer Biomet ([NeuroOne](https://nmtc1.com/)) |
| Layer 7-T Cortical Interface | Precision Neuroscience | Thin-film micro-ECoG | 1,024 electrodes per array | — | Up to 30 days | 510(k) [K242618](https://fda.innolitics.com/device/K242618) (decision 30 Mar 2025, announced 17 Apr 2025) | Intraoperative mapping, BCI research | Current ([BioSpace](https://www.biospace.com/press-releases/precision-neuroscience-receives-fda-clearance-for-high-resolution-cortical-electrode-array)) |
| NeuroCoG strips and grids | Blackrock | ECoG | — | Set by amplifier | — | 510(k) [K191346](https://fda.innolitics.com/device/K191346) (2020) | ECoG monitoring | Current *unverified* |

**Recording systems**

| Device | Company | Type | Contacts/channels | Sampling rate | Implant duration | Regulatory | Typical use | Status |
|---|---|---|---|---|---|---|---|---|
| Quantum LTM amplifier | Natus | Clinical EEG/iEEG amplifier | 256 + 16 DC inputs | Up to 16 kHz; 0.01 Hz–4 kHz bandwidth | n/a | 510(k) [K143440](https://fda.innolitics.com/device/K143440), [K180181](https://fda.innolitics.com/device/K180181) | EMU scalp and intracranial monitoring, cortical stimulation | Current ([Natus](https://natus.com/neuro/natus-quantum-ltm-amplifier/), [Hospimedica](https://hospimedica.com/expo/product/18383/eeg-electrophysiology-amplifier-model-quantum-ltm-amplifier)) |
| EEG-1200A with JE-120A | Nihon Kohden | Clinical EEG/iEEG amplifier | Up to 256 | Up to 10 kHz clinical; 40 kHz for research with Neuralynx ATLAS | n/a | 510(k) [K113117](https://fda.innolitics.com/device/K113117) (2012) | EMU monitoring | Current ([Sleep Review](https://sleepreviewmag.com/uncategorized/nihon-kohden-america-neuralynx-partnership-clinical-eeg-research/)) |
| NeuroPort Biopotential Signal Processing System | Blackrock Neurotech | Research/clinical acquisition | 32–512 | 30 kS/s, 16-bit | n/a | 510(k) [K202174](https://fda.innolitics.com/device/K202174) (Digital NeuroPort, 2021) | ECoG and spike BCIs; used in [Moses 2021](https://doi.org/10.1056/NEJMoa2027540) | Current ([Blackrock](https://blackrockneurotech.com/products/neuroport/)) |
| Grapevine Neural Interface Processor | Ripple Neuro | Research acquisition and stimulation | Up to 512 | — | n/a | No 510(k) found in openFDA | Research iEEG, spikes | Current ([SciCrunch](https://scicrunch.org/resolver/SCR_018897), [MathWorks listing](https://www.mathworks.com/products/connections/product_detail/grapevine-nip.html)) |
| g.HIamp | g.tec | Research/clinical biosignal amplifier | 256 | 38.4 kHz internal per channel, 24-bit | n/a | 510(k) [K123255](https://fda.innolitics.com/device/K123255) (2012); companion cortiQ PRO mapping software [K191432](https://fda.innolitics.com/device/K191432) | Real-time ECoG mapping and BCI research | Current ([g.tec](https://www.gtec.at/product-configurator/g-hiamp/)) |

**Chronic implants that record field potentials**

| Device | Company | Type | Contacts/channels | Sampling rate | Implant duration | Regulatory | Typical use | Status |
|---|---|---|---|---|---|---|---|---|
| RNS System | NeuroPace | Responsive neurostimulator, cranially mounted | 2 leads (depth and/or cortical strip) × 4 contacts; 4 bipolar sensing channels; stores about 7.5 min of 4-ch ECoG | 250 Hz, 4–90 Hz band, 10-bit | Years; RNS-300M battery replaced every 3–5 years | PMA [P100026](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpma/pma.cfm?id=P100026), approved 14 Nov 2013 | Drug-resistant focal epilepsy | Commercial ([Quigg et al. 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC5008166), [Meisenhelter et al. 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6439470), [Constantino et al. 2021](https://doi.org/10.3389/fneur.2021.603868)) |
| Percept PC / RC with BrainSense | Medtronic | DBS with local field potential sensing | DBS leads; sensing on a bipolar contact pair per hemisphere *unverified* | 250 Hz streaming; chronic mode stores 5 Hz-wide band power every 10 min for up to 60 days | Years | PMA P960009/S361 (Percept PC, 24 Jun 2020); BrainSense Adaptive DBS approved 24 Feb 2025 | Parkinson's disease; adaptive DBS | Commercial ([Cummins et al. 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8382799), [Medtronic](https://news.medtronic.com/2025-02-24-Medtronic-earns-U-S-FDA-approval-for-the-worlds-first-Adaptive-deep-brain-stimulation-system-for-people-with-Parkinsons)) |
| WIMAGINE | CEA-Clinatec | Wireless epidural ECoG | 64 electrodes (8×8); 32 used at 586 Hz in the brain–spine interface | 586 Hz; 0.5–300 Hz | 24+ months reported | Investigational ([NCT02550522](https://clinicaltrials.gov/study/NCT02550522)) | Exoskeleton and brain–spine interface for tetraplegia | Clinical research ([Benabid 2019](https://doi.org/10.1016/S1474-4422(19)30321-7), [Lorach 2023](https://doi.org/10.1038/s41586-023-06094-5), [Moly 2022](https://arxiv.org/abs/2201.10449)) |
| Stentrode | Synchron | Endovascular stent-electrode array | 16 electrodes, 0.3 mm² each, 3 mm spacing; implanted chest telemetry unit (first generation) | — (signal bandwidth 233 Hz) | Permanent; 12-month follow-ups reported | FDA IDE early feasibility ([COMMAND, NCT05035823](https://clinicaltrials.gov/study/NCT05035823)) | Computer control for severe paralysis | Trials; next-generation device in [FOCUS-AU](https://clinicaltrials.gov/study/NCT07533903) ([Mitchell 2023](https://doi.org/10.1001/jamaneurol.2022.4847)) |

## 3. Applications (domains)

| Domain | How iEEG is used | Examples | Maturity |
|---|---|---|---|
| Epilepsy localization and monitoring | Grids or sEEG record spontaneous seizures in the EMU to find the seizure-onset zone before resection; interictal spikes and high-frequency oscillations are extra markers | Standard of care ([Parvizi & Kastner 2018](https://doi.org/10.1038/s41593-018-0108-2)); computational onset-zone markers such as neural fragility ([Wang et al. 2026](https://doi.org/10.1523/ENEURO.0340-25.2026)) | Clinical standard; ML markers are research |
| Functional mapping | Electrical stimulation mapping is the classic method ([Penfield & Boldrey 1937](https://doi.org/10.1093/brain/60.4.389)). Passive high-gamma mapping during tasks is faster and needs no stimulation ([Crone 1998](https://doi.org/10.1093/brain/121.12.2301)) | g.tec cortiQ PRO (FDA 510(k) [K191432](https://fda.innolitics.com/device/K191432)); Precision Layer 7 for intraoperative mapping ([BioSpace](https://www.biospace.com/press-releases/precision-neuroscience-receives-fda-clearance-for-high-resolution-cortical-electrode-array)) | Clinical (stimulation) / commercial, early (passive) |
| Responsive neurostimulation | Implant detects seizure patterns in 4 channels of ECoG and stimulates to stop them | NeuroPace RNS pivotal trial ([Morrell 2011](https://doi.org/10.1212/WNL.0b013e3182302056)); NAUTILUS for generalized epilepsy: 77% median reduction of tonic-clonic seizures at 18 months ([BusinessWire](https://www.businesswire.com/news/home/20251208932472/en/NeuroPace-Announces-Positive-18-Month-NAUTILUS-Trial-Results-in-Idiopathic-Generalized-Epilepsy)) | Commercial |
| Adaptive DBS | Beta-band LFP from the DBS lead sets stimulation amplitude | Medtronic BrainSense Adaptive DBS, FDA-approved Feb 2025; ADAPT-PD: 68 participants, primary endpoint met by 91% (dual threshold) and 79% (single threshold) ([Bronte-Stewart 2025](https://doi.org/10.1001/jamaneurol.2025.2781)); gamma-driven aDBS pilot ([Oehrn 2024](https://doi.org/10.1038/s41591-024-03196-z)) | Commercial (new) |
| Seizure prediction and forecasting | Long-term implanted recordings show daily and multi-day seizure cycles that can be used to forecast risk | NeuroVista advisory system ([Cook 2013](https://doi.org/10.1016/S1474-4422(13)70075-9)); multi-day rhythms in RNS data ([Baud 2018](https://doi.org/10.1038/s41467-017-02577-y)); next-day forecasts better than chance in 66% of 157 validation patients ([Proix 2021](https://doi.org/10.1016/S1474-4422(20)30396-3)) | Research / trials |
| Speech BCI | High-gamma from high-density ECoG over speech motor cortex decoded to text, audio and avatar | 15.2 words/min ([Moses 2021](https://doi.org/10.1056/NEJMoa2027540)); 78 words/min ([Metzger 2023](https://doi.org/10.1038/s41586-023-06443-4)); streaming voice ([Littlejohn 2025](https://doi.org/10.1038/s41593-025-01905-6)); ALS command decoding at JHU ([Luo 2023](https://doi.org/10.1002/advs.202304853)) | Clinical trials |
| Motor BCI (ALS home use, exoskeleton, walking) | Attempted movement detected from motor-cortex ECoG, epidural ECoG or endovascular signals | Utrecht home-use typing ([Vansteensel 2016](https://doi.org/10.1056/NEJMoa1608085), 7-year follow-up [2024](https://doi.org/10.1056/NEJMoa2314598)); WIMAGINE exoskeleton ([Benabid 2019](https://doi.org/10.1016/S1474-4422(19)30321-7)) and brain–spine interface ([Lorach 2023](https://doi.org/10.1038/s41586-023-06094-5)); Stentrode ([Mitchell 2023](https://doi.org/10.1001/jamaneurol.2022.4847)) | Clinical trials |
| Memory and cognition research | Hippocampal and cortical sEEG during memory tasks; closed-loop stimulation when the decoder predicts poor encoding | Closed-loop lateral temporal stimulation improved recall ([Ezzyat 2018](https://doi.org/10.1038/s41467-017-02753-0)) | Research |
| Language and semantic decoding | Align iEEG to word embeddings or language-model states during natural listening | The brain and autoregressive language models share next-word prediction and contextual embeddings during a podcast ([Goldstein 2022](https://doi.org/10.1038/s41593-022-01026-4)); Brain Treebank (movies, 223,000 words; [Wang 2024](https://arxiv.org/abs/2411.08343)); music reconstruction ([Bellier 2023](https://doi.org/10.1371/journal.pbio.3002176)) | Research |
| Sleep | Physiology of sleep stages, spindles and slow waves measured directly in cortex; sleep-related HFO markers for epilepsy | MNI normal iEEG atlas, wake ([Frauscher 2018](https://doi.org/10.1093/brain/awy035)) and sleep ([von Ellenrieder 2020](https://doi.org/10.1002/ana.25651)); HFOs in slow-wave sleep ([OpenNeuro ds003498](https://openneuro.org/datasets/ds003498)) | Research |
| Psychiatric closed-loop therapy | Find a personal mood biomarker with days of sEEG, then implant a sensing stimulator that fires when the biomarker appears | Mood decoded from multi-site iEEG in 7 patients ([Sani 2018](https://doi.org/10.1038/nbt.4200)); closed-loop DBS for depression, n=1 ([Scangos 2021](https://doi.org/10.1038/s41591-021-01480-w)); closed-loop DBS trial for major depression recruiting, target 12 ([NCT04004169](https://clinicaltrials.gov/study/NCT04004169)); cingulate LFP tracks recovery ([Alagapan 2023](https://doi.org/10.1038/s41586-023-06541-3)) | Early trials |

## 4. Companies

| Company | Country | Focus | Key product | Status 2025–2026 |
|---|---|---|---|---|
| NeuroPace | US | Responsive neurostimulation | RNS System | 2025 revenue $100.0M, up 25% ([NeuroPace](https://investors.neuropace.com/news/news-details/2026/NeuroPace-Reports-Fourth-Quarter-and-Full-Year-2025-Financial-Results-and-Reiterates-2026-Outlook)); PMA supplement for generalized epilepsy filed Dec 2025 ([BusinessWire](https://www.businesswire.com/news/home/20251217370604/en/NeuroPace-Files-PMA-Supplement-to-FDA-Seeking-Expanded-RNS-System-Indication-for-Idiopathic-Generalized-Epilepsy)); on 28 Jul 2026 FDA said it was not approvable in its current form ([NeuroPace](https://investors.neuropace.com/news/news-details/2026/NeuroPace-Receives-FDA-Guidance-on-PMA-Supplement-for-Indication-Expansion-into-Idiopathic-Generalized-Epilepsy/default.aspx)) |
| Medtronic | US/Ireland | DBS with sensing | Percept PC/RC, BrainSense | Adaptive DBS approved 24 Feb 2025; more than 40,000 patients have Percept devices ([Medtronic](https://news.medtronic.com/2025-02-24-Medtronic-earns-U-S-FDA-approval-for-the-worlds-first-Adaptive-deep-brain-stimulation-system-for-people-with-Parkinsons)) |
| Synchron | US/Australia | Endovascular BCI | Stentrode | COMMAND met its primary safety endpoint in 6 patients ([BioSpace](https://www.biospace.com/news/synchron-announces-positive-results-from-u-s-command-study-of-endovascular-brain-computer-interface)); $200M Series D led by Double Point Ventures, Nov 2025 ([AlleyWatch](https://www.alleywatch.com/2025/11/the-alleywatch-startup-daily-funding-report-11-10-2025/)); FOCUS-AU next-gen trial started 22 May 2026, 10 patients planned ([NCT07533903](https://clinicaltrials.gov/study/NCT07533903)); iPad control through Apple's BCI HID protocol shown Aug 2025 ([MacTech](https://www.mactech.com/2025/08/04/synchron-debuts-first-thought-controlled-ipad-experience)) |
| Precision Neuroscience | US | Thin-film cortical BCI | Layer 7 | 510(k) K242618 (Mar 2025); 100+ implanted study patients at 18+ hospitals ([Precision](https://precisionneuro.io/)); $250M Series D, Sep 2026, total $430M ([Pulse 2.0](https://pulse2.com/precision-neuroscience-raises-250-million-series-d-to-advance-brain-computer-interface-technology/)) |
| NeuroOne | US | Thin-film electrodes, RF ablation | Evo Cortical, Evo sEEG, OneRF | Most recent 510(k): OneRF trigeminal probes, Aug 2025 ([K251243](https://fda.innolitics.com/device/K251243)); Zimmer Biomet listed as distribution partner ([NeuroOne](https://nmtc1.com/)) |
| Ad-Tech Medical | US | Grids, strips, depth electrodes | Subdural and Spencer depth electrodes | Latest clearances May 2023 ([K223269](https://fda.innolitics.com/device/K223269)) |
| DIXI Medical | France | sEEG electrodes | Microdeep | Micro-macro electrodes cleared 2021 ([K202087](https://fda.innolitics.com/device/K202087)) |
| PMT Corporation | US | Depth and cortical electrodes | Depthalon | Selling (GUDID listings) |
| Natus / Nihon Kohden | US / Japan | Clinical EEG/iEEG systems | Quantum / EEG-1200 | Selling; Nihon Kohden cleared EEG-1260A Neurofax Oct 2025 ([K251366](https://fda.innolitics.com/device/K251366)) |
| Blackrock Neurotech / Ripple Neuro / g.tec | US / US / Austria | Research acquisition | NeuroPort / Grapevine / g.HIamp | Selling (section 2) |
| CEA-Clinatec | France | Wireless epidural ECoG | WIMAGINE | Academic clinical trial ([NCT02550522](https://clinicaltrials.gov/study/NCT02550522)), partner in brain–spine interface work ([Lorach 2023](https://doi.org/10.1038/s41586-023-06094-5)) |
| INBRAIN Neuroelectronics | Spain | Graphene cortical interfaces | Graphene BCI | FDA Breakthrough designation (Parkinson's) Aug 2023; first human procedure Sep 2024; first-in-human study recruitment completed Apr 2026; $50M raised Oct 2024 ([INBRAIN](https://inbrain.tech/)) |
| CorTec | Germany | Implantable ECoG recording/stimulation | Brain Interchange | Second FDA Breakthrough designation for Brain Interchange, Aug 2026 ([CorTec](https://www.cortec-neuro.com/news/)) |

## 5. Patents

| Patent number | Holder | Title/topic | Year | Why it matters |
|---|---|---|---|---|
| [US 6,016,449](https://patents.google.com/patent/US6016449A) | NeuroPace | System for treatment of neurological disorders | 2000 (priority 1997) | Fischell and Upton's founding claim on an implant that detects abnormal brain activity and responds with stimulation, the basis of RNS |
| [US 6,810,285](https://patents.google.com/patent/US6810285B2) | NeuroPace | Seizure sensing and detection using an implantable device | 2004 | Seizure detection running inside the implant, the sensing half of a responsive stimulator |
| [US 8,036,736](https://patents.google.com/patent/US8036736B2) | NeuroVista (later LivaNova) | Implantable systems for identifying a contra-ictal (low-risk) condition | 2011 | Seizure-advisory concept tested in [Cook 2013](https://doi.org/10.1016/S1474-4422(13)70075-9) |
| [US 7,847,628](https://patents.google.com/patent/US7847628B2) | Medtronic | Chopper-stabilized instrumentation amplifier | 2010 | Timothy Denison's chopper-stabilized front end, a method for amplifying small low-frequency signals with low noise in implants; Denison also co-authored the Utrecht ECoG BCI paper ([Vansteensel 2016](https://doi.org/10.1056/NEJMoa1608085)) |
| [US 9,888,861](https://patents.google.com/patent/US9888861B2) | Medtronic | Detecting a biomarker in the presence of electrical stimulation | 2018 (priority 2011) | Sensing while stimulating, the core problem behind BrainSense and adaptive DBS |
| [US 10,575,783](https://patents.google.com/patent/US10575783B2) | Synchron | Methods for sensing or stimulating brain tissue from within a vessel | 2020 (priority 2011) | Oxley's claim on recording the brain from inside a blood vessel to control a device |
| [US 10,485,968](https://patents.google.com/patent/US10485968B2) | University of Melbourne | Medical device for sensing and/or stimulating tissue (stent-electrode) | 2019 (priority 2015) | The Stentrode design (Opie, Oxley, Rind) |
| [US 11,755,110](https://patents.google.com/patent/US11755110B2) | Synchron | Generic control using a neural signal | 2023 | "Universal switch": mapping a trained thought to any digital command |
| [US 10,918,857](https://patents.google.com/patent/US10918857B2) | Precision Neuroscience | Conformal electrode arrays for electrophysiologic recording and neural stimulation within the cerebral ventricles | 2021 (priority 2016) | Flexible arrays that fold to pass through a narrow channel for placement in the brain's ventricles; an early form of the minimally invasive approach behind Layer 7 |
| [US 12,508,079](https://patents.google.com/patent/US12508079B2) | Precision Neuroscience | High-bandwidth minimally invasive BCIs | 2025 (priority 2021) | Cortical-surface, ventricular and endovascular delivery of high-density arrays |
| [US 12,548,570](https://patents.google.com/patent/US12548570B1) | Precision Neuroscience | Neural foundation models for BCI | 2026 (priority 2025) | Claims a pipeline of feature embeddings and encoders for speech decoding; shows that foundation-model methods are now being patented |
| [US 10,438,603](https://patents.google.com/patent/US10438603B2) | University of California | Methods of decoding speech from the brain | 2019 (priority 2013) | Chang lab speech-decoding claims, upstream of the UCSF speech neuroprostheses |
| [US 11,478,179](https://patents.google.com/patent/US11478179B2) | NeuroOne | Neural depth probes | 2022 | Thin-film sEEG probe construction |

## 6. Most-cited papers

Citation counts are from the Crossref API on 2026-10-11. They are lower than Google Scholar counts, but are useful for comparing papers with each other.

| Paper | Authors | Venue/year | Crossref citations | Why it matters |
|---|---|---|---|---|
| [Somatic motor and sensory representation in the cerebral cortex of man as studied by electrical stimulation](https://doi.org/10.1093/brain/60.4.389) | Penfield, Boldrey | Brain 1937 | 3,575 | The "homunculus"; the basis of stimulation mapping |
| [Functional mapping of human sensorimotor cortex with ECoG spectral analysis. II. Event-related synchronization in the gamma band](https://doi.org/10.1093/brain/121.12.2301) | Crone et al. | Brain 1998 | 940 | Showed task-locked gamma/high-gamma increases in ECoG, the field's main feature |
| [A brain–computer interface using electrocorticographic signals in humans](https://doi.org/10.1088/1741-2560/1/2/001) | Leuthardt, Schalk, Wolpaw, Ojemann, Moran | J. Neural Eng. 2004 | 991 | Early online ECoG BCI: EMU patients controlled a 1D cursor |
| [Decoding two-dimensional movement trajectories using electrocorticographic signals in humans](https://doi.org/10.1088/1741-2560/4/3/012) | Schalk et al. | J. Neural Eng. 2007 | 451 | Continuous kinematics from ECoG; online 2D control followed in [Schalk 2008](https://doi.org/10.1088/1741-2560/5/1/008) |
| [Spectral changes in cortical surface potentials during motor movement](https://doi.org/10.1523/JNEUROSCI.3886-06.2007) | Miller et al. | J. Neurosci. 2007 | 696 | Separated focal broadband high-gamma from diffuse low-frequency changes; the broadband/power-law view in [Miller 2009](https://doi.org/10.1371/journal.pcbi.1000609) |
| [Decoding flexion of individual fingers using electrocorticographic signals in humans](https://doi.org/10.1088/1741-2560/6/6/066001) | Kubánek et al. | J. Neural Eng. 2009 | 256 | Individual finger decoding from ECoG; BCI Competition IV dataset 4 (Miller and Schalk) offers the same kind of finger-flexion data |
| [Responsive cortical stimulation for the treatment of medically intractable partial epilepsy](https://doi.org/10.1212/WNL.0b013e3182302056) | Morrell et al. | Neurology 2011 | 1,153 | RNS pivotal trial, which led to FDA approval of the RNS System in 2013 |
| [Prediction of seizure likelihood with a long-term, implanted seizure advisory system](https://doi.org/10.1016/S1474-4422(13)70075-9) | Cook et al. | Lancet Neurol. 2013 | 855 | Seizure prediction from long-term ambulatory iEEG in 15 patients; sensitivity 65–100% in the 11 who qualified |
| [Brain-to-text: decoding spoken phrases from phone representations in the brain](https://doi.org/10.3389/fnins.2015.00217) | Herff et al. | Front. Neurosci. 2015 | 268 | Continuous speech decoded to text from ECoG through phone (speech sound) models |
| [Minimally invasive endovascular stent-electrode array for high-fidelity, chronic recordings of cortical neural activity](https://doi.org/10.1038/nbt.3428) | Oxley et al. | Nat. Biotechnol. 2016 | 336 | The Stentrode concept, shown in sheep |
| [Fully implanted brain–computer interface in a locked-in patient with ALS](https://doi.org/10.1056/NEJMoa1608085) | Vansteensel et al. | NEJM 2016 | 563 | Fully implanted ECoG BCI that a person with late-stage ALS used on her own; about two letters per minute |
| [Speech synthesis from neural decoding of spoken sentences](https://doi.org/10.1038/s41586-019-1119-1) | Anumanchipalli, Chartier, Chang | Nature 2019 | 846 | Decoded ECoG first into vocal-tract movements, then into audio |
| [An exoskeleton controlled by an epidural wireless brain–machine interface in a tetraplegic patient](https://doi.org/10.1016/S1474-4422(19)30321-7) | Benabid et al. | Lancet Neurol. 2019 | 375 | 24 months of WIMAGINE epidural ECoG controlling up to 8 degrees of freedom |
| [Neuroprosthesis for decoding speech in a paralyzed person with anarthria](https://doi.org/10.1056/NEJMoa2027540) | Moses et al. | NEJM 2021 | 573 | Decoded sentences from a person with anarthria (unable to speak): 15.2 words/min, 25.6% median word error rate, 50-word vocabulary |

## 7. New achievements (2023–2026)

- **Speech at conversational speed.** With a 253-channel ECoG array, Metzger et al. reached a median 78 words per minute and 25% word error rate on a 1,024-word vocabulary, plus voice synthesis and a talking avatar (*Nature* 2023, [paper](https://doi.org/10.1038/s41586-023-06443-4)). The same group later streamed speech in 80 ms steps instead of waiting for the end of a sentence ([Littlejohn 2025](https://doi.org/10.1038/s41593-025-01905-6)), and decoded both Spanish and English with one shared model ([Silva 2024](https://doi.org/10.1038/s41551-024-01207-5)).
- **Decoders across many patients.** NYU's ECoG-to-speech framework works across 48 epilepsy patients, still decodes with causal (real-time-compatible) models, and works with right-hemisphere coverage ([Chen 2024](https://doi.org/10.1038/s42256-024-00824-8)).
- **ALS at home.** At Johns Hopkins, a man with ALS issued 6 spoken commands with 90.59% median accuracy for 3 months without recalibration ([Luo 2023](https://doi.org/10.1002/advs.202304853)); synthesized words were 80% intelligible to listeners ([Angrick 2024](https://doi.org/10.1038/s41598-024-60277-2)). The Utrecht patient used her ECoG BCI at home for 7 years; it stopped working when signals faded with brain atrophy, not because of device failure ([Vansteensel 2024](https://doi.org/10.1056/NEJMoa2314598)).
- **Walking.** WIMAGINE epidural ECoG drove spinal-cord stimulation so a man with tetraplegia could stand, walk and climb stairs; the brain–spine interface stayed reliable for over a year, including at home ([Lorach 2023](https://doi.org/10.1038/s41586-023-06094-5)).
- **Thin-film scale.** Precision placed 4,096 electrodes on a human brain in one procedure in 2024, twice the earlier record of 2,048 ([Precision](https://precisionneuro.io/), [HumanProgress/Ars Technica](https://humanprogress.org/neuralink-rival-sets-brain-chip-record-with-4096-electrodes/)). Its Layer 7-T got 510(k) clearance for up to 30 days of implantation, after 37 study patients ([K242618](https://fda.innolitics.com/device/K242618), [BioSpace](https://www.biospace.com/press-releases/precision-neuroscience-receives-fda-clearance-for-high-resolution-cortical-electrode-array)).
- **Endovascular BCI.** In SWITCH, 4 patients typed with 93.9% selection accuracy at 16.6 correct characters per minute, with no serious adverse events in 12 months ([Mitchell 2023](https://doi.org/10.1001/jamaneurol.2022.4847)). The US COMMAND study (6 patients) met its primary safety endpoint ([BioSpace](https://www.biospace.com/news/synchron-announces-positive-results-from-u-s-command-study-of-endovascular-brain-computer-interface)). The next-generation Stentrode trial FOCUS-AU began enrolling in May 2026 ([NCT07533903](https://clinicaltrials.gov/study/NCT07533903)).
- **Foundation models for sEEG.** BrainBERT pretrained a transformer on unlabelled iEEG spectrograms and transfers to new subjects (ICLR 2023, [arXiv](https://arxiv.org/abs/2302.14367)). Brant, a model of more than 500M parameters, is pretrained on intracranial data (NeurIPS 2023, [DOI](https://doi.org/10.52202/075280-1144), [repo](https://github.com/yzz673/Brant)). The Brain Treebank provides 43 h of sEEG from 10 subjects watching movies, with 38,000 parsed sentences (NeurIPS 2024, [arXiv](https://arxiv.org/abs/2411.08343)). The Population Transformer learns to combine channels across subjects with different electrode layouts (ICLR 2025, [arXiv](https://arxiv.org/abs/2406.03044)). Neuroprobe turns the Brain Treebank into a standard benchmark for iEEG foundation models ([arXiv](https://arxiv.org/abs/2509.21671)). BrainWave pretrains on more than 40,000 hours of invasive and non-invasive recordings from about 16,000 people ([arXiv](https://arxiv.org/abs/2402.10251)).
- **Closed loop goes commercial.** Medtronic's adaptive DBS was approved in February 2025 ([Medtronic](https://news.medtronic.com/2025-02-24-Medtronic-earns-U-S-FDA-approval-for-the-worlds-first-Adaptive-deep-brain-stimulation-system-for-people-with-Parkinsons)); in the 68-patient ADAPT-PD trial, 91% (dual threshold) and 79% (single threshold) met the primary endpoint ([Bronte-Stewart 2025](https://doi.org/10.1001/jamaneurol.2025.2781)). NeuroPace's NAUTILUS trial reported a 77% median drop in generalized tonic-clonic seizures at 18 months ([BusinessWire](https://www.businesswire.com/news/home/20251208932472/en/NeuroPace-Announces-Positive-18-Month-NAUTILUS-Trial-Results-in-Idiopathic-Generalized-Epilepsy)).
- **Psychiatry.** With DBS of the subcallosal cingulate, 90% of 10 participants with depression responded and 70% were in remission at 24 weeks; cingulate LFPs tracked recovery ([Alagapan 2023](https://doi.org/10.1038/s41586-023-06541-3)). A closed-loop DBS trial for major depression is recruiting, with a target of 12 participants ([NCT04004169](https://clinicaltrials.gov/study/NCT04004169)).
- **Money.** Synchron raised a $200M Series D (Nov 2025) and Precision a $250M Series D (Sep 2026); NeuroPace passed $100M in annual revenue in 2025 (section 4).

## 8. Current state of the field

**Where iEEG is used today, and where it is still research**

| Maturity | Applications |
|---|---|
| Established clinical | EMU seizure localization with grids, strips and sEEG; electrical stimulation mapping |
| Commercial, growing | NeuroPace RNS; Medtronic Percept sensing and adaptive DBS; thin-film electrodes (NeuroOne Evo, Precision Layer 7-T); passive high-gamma mapping (cortiQ PRO) |
| Trials / early | Speech and motor BCIs with ECoG (UCSF, JHU, Utrecht); endovascular BCI (Synchron COMMAND, FOCUS-AU); epidural ECoG (WIMAGINE); closed-loop psychiatric DBS; RNS for generalized epilepsy |
| Research | Seizure forecasting in daily use; iEEG foundation models; semantic and language decoding; memory enhancement; sleep physiology |

**Open problems**
- **Every patient has a different electrode layout.** sEEG positions vary from patient to patient, and channel counts range from a few dozen to hundreds. Models must handle variable, sparse inputs. That is the motivation for BrainBERT, PopT and Neuroprobe, and none of them has solved it yet ([PopT](https://arxiv.org/abs/2406.03044)).
- **Small, biased data.** Research iEEG comes from epilepsy patients over days to weeks, with medication changes, epileptic activity and electrodes placed for clinical reasons ([Parvizi & Kastner 2018](https://doi.org/10.1038/s41593-018-0108-2)). Chronic implants record only 4 channels at 250 Hz (RNS) or a single band-power value every 10 minutes (Percept chronic mode).
- **Going from acute to chronic.** The best decoders run on percutaneous research arrays connected to NeuroPort-class systems. Fully implanted systems have lower bandwidth (16 Stentrode electrodes; 32 of 64 WIMAGINE contacts at 586 Hz in the brain–spine interface).
- **Stability over years.** Signals can fade with disease progression ([Vansteensel 2024](https://doi.org/10.1056/NEJMoa2314598)). Recalibration-free decoding has been shown for months, not years ([Luo 2023](https://doi.org/10.1002/advs.202304853); WIMAGINE models were reusable for about 7 weeks in [Benabid 2019](https://doi.org/10.1016/S1474-4422(19)30321-7)).
- **Benchmarks.** Results are mostly reported on private, single-patient data; Neuroprobe and the Epilepsyecosystem are rare exceptions ([Kuhlmann 2018](https://doi.org/10.1093/brain/awy210)).
- **Regulation and IP.** New indications can stall at FDA (NeuroPace IGE, section 4), and patents now cover foundation-model decoders (Precision US 12,548,570).

**Where an AI engineer can contribute.** Self-supervised pretraining that handles variable electrode sets (set and graph models, learned positional encodings from MNI coordinates). Cross-subject transfer and few-shot calibration for speech and motor decoders. Streaming sequence models (RNN-T, CTC with language-model fusion) with low latency. Seizure detection and forecasting that runs on low-power implants at 250 Hz. Automatic electrode localization and labelling from CT/MRI. Artifact and epileptic-activity rejection. Neural compression for wireless implants ([BrainCodec](https://github.com/IBM/eeg-ieeg-brain-compressor)). Honest benchmarks on held-out subjects. The datasets below are a good starting point.

## 9. Public datasets

Full specifications for each dataset, and tables of published results on them, are in [DATASETS.md](DATASETS.md).

| Dataset | Content | Size | Link |
|---|---|---|---|
| Brain Treebank | sEEG while watching Hollywood movies; words aligned and parsed | 10 subjects, 43 h, 223,000 words, about 168 electrodes per subject | [braintreebank.dev](https://braintreebank.dev/), [arXiv](https://arxiv.org/abs/2411.08343) |
| Miller ECoG library | 16 behavioural tasks (motor, imagery, faces/houses, etc.), same amplifiers and settings | 34 patients, 204 datasets, with MATLAB analysis code | [Stanford Digital Repository](https://searchworks.stanford.edu/view/zk881ps0522), [paper](https://doi.org/10.1038/s41562-019-0678-3) |
| BCI Competition IV, dataset 4 | ECoG during individual finger flexions, with data-glove kinematics | 3 subjects, 48–64 channels at 1000 Hz | [bbci.de](https://www.bbci.de/competition/iv/) |
| Single-word production (Dutch) | sEEG while reading words aloud, with audio | 10 participants, 1,103 electrodes | [OSF](https://osf.io/nrgx6/), [paper](https://doi.org/10.1038/s41597-022-01542-9) |
| Open multimodal iEEG-fMRI | iEEG and fMRI while watching a short film | 63 subjects, 16.3 GB, CC0 | [OpenNeuro ds003688](https://openneuro.org/datasets/ds003688) |
| HUP iEEG Epilepsy | Clinical iEEG from epilepsy surgery candidates | 57 subjects, 14.2 GB, CC0 | [OpenNeuro ds004100](https://openneuro.org/datasets/ds004100) |
| Epilepsy iEEG multicenter | Clinical iEEG from several epilepsy centres | 35 subjects, 11.1 GB, CC0 | [OpenNeuro ds003029](https://openneuro.org/datasets/ds003029) |
| Open pediatric iEEG (Wayne State, UCLA) | Clinical pediatric iEEG | 185 subjects, 109.7 GB, CC0 | [OpenNeuro ds005398](https://openneuro.org/datasets/ds005398) |
| CCEP ECoG across age | Cortico-cortical evoked potentials, ages 4–51 | 74 subjects, 289 GB, CC0 | [OpenNeuro ds004080](https://openneuro.org/datasets/ds004080) |
| Zurich HFO sleep dataset | Interictal iEEG in slow-wave sleep with HFO markings | 20 subjects, 48 GB, CC0 | [OpenNeuro ds003498](https://openneuro.org/datasets/ds003498) |
| Mayo Clinic / FNUSA iEEG clips | Labelled clips: physiological, pathological, artifact; two centres | See paper | [paper](https://doi.org/10.1038/s41597-020-0532-5) |
| Melbourne seizure prediction (Epilepsyecosystem) | Long-term NeuroVista iEEG; interictal vs preictal 10-min clips | 3 patients, 442 days of recordings per patient on average; 478 Kaggle teams competed | [Epilepsyecosystem](https://www.epilepsyecosystem.org/), [Kaggle](https://www.kaggle.com/c/melbourne-university-seizure-prediction), [paper](https://doi.org/10.1093/brain/awy210) |

## 10. GitHub repositories

Stars and dates checked via the GitHub API on 2026-10-11.

"Custom" means GitHub could not detect a standard license (`NOASSERTION`), so read the repo's LICENSE file before reusing the code. "—" means no license file or no detected language. Papers with Code shut down in 2025, so leaderboards are no longer tracked there; use the official repos and Neuroprobe instead.

**Toolkits and libraries**

| Repo | What it does / when to use it | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [mne-tools/mne-python](https://github.com/mne-tools/mne-python) | General MEG/EEG/ECoG/sEEG analysis and 3D plotting of electrodes. Start here in Python | Python | 3542 | 2026-10 | BSD-3-Clause |
| [mne-tools/mne-bids](https://github.com/mne-tools/mne-bids) | Read and write iEEG-BIDS datasets (electrodes.tsv, coordinate systems) | Python | 182 | 2026-10 | BSD-3-Clause |
| [fieldtrip/fieldtrip](https://github.com/fieldtrip/fieldtrip) | MATLAB toolbox for MEG, EEG and iEEG analysis | MATLAB | 990 | 2026-10 | GPL-3.0 |
| [brainstorm-tools/brainstorm3](https://github.com/brainstorm-tools/brainstorm3) | GUI-based analysis of MEG, EEG, fNIRS, ECoG and sEEG | MATLAB | 488 | 2026-10 | GPL-3.0 |
| [iELVis/iELVis](https://github.com/iELVis/iELVis) | Electrode localization with brain-shift correction, atlas labelling and visualization on FreeSurfer surfaces | MATLAB | 36 | 2026-02 | GPL-3.0 |
| [ChangLabUcsf/img_pipe](https://github.com/ChangLabUcsf/img_pipe) | UCSF pipeline: from a pre-op T1 MRI and post-op CT to labelled, atlas-warped ECoG/sEEG contacts | Jupyter Notebook | 68 | 2024-06 | — |
| [mnarizzano/SEEGA](https://github.com/mnarizzano/SEEGA) | SEEG Assistant: 3D Slicer extension for automatic segmentation and labelling of depth contacts in CT | Python | 32 | 2023-10 | GPL-3.0 |
| [beauchamplab/rave](https://github.com/beauchamplab/rave) | RAVE: reproducible analysis and visualization of iEEG (R, with Python parts) | R | 26 | 2026-08 | — |
| [dipterix/threeBrain](https://github.com/dipterix/threeBrain) | WebGL 3D brain and electrode viewer used by RAVE | R | 52 | 2026-10 | — |
| [wonambi-python/wonambi](https://github.com/wonambi-python/wonambi) | Reads EEG/ECoG in many formats (EDF, Blackrock, Micromed, BIDS); GUI sleep scoring; spindle and slow-wave detectors | Python | 101 | 2026-04 | BSD-3-Clause |
| [catalystneuro/ecogVIS](https://github.com/catalystneuro/ecogVIS) | Viewer and preprocessing for ECoG stored in NWB (with the Chang lab) | Python | 31 | 2024-06 | BSD-3-Clause |
| [NeurodataWithoutBorders/pynwb](https://github.com/NeurodataWithoutBorders/pynwb) | Read and write NWB files | Python | 225 | 2026-10 | Custom |
| [bids-standard/bids-specification](https://github.com/bids-standard/bids-specification) | The BIDS standard, including the iEEG chapter | Python | 370 | 2026-10 | CC-BY-4.0 |
| [bids-standard/bids-validator](https://github.com/bids-standard/bids-validator) | Check that an iEEG-BIDS folder is valid before sharing | TypeScript | 51 | 2026-10 | MIT |
| [neuromodulation/py_neuromodulation](https://github.com/neuromodulation/py_neuromodulation) | Real-time feature extraction and decoding from ECoG/LFP, aimed at adaptive DBS | Python | 81 | 2026-02 | MIT |
| [fooof-tools/fooof](https://github.com/fooof-tools/fooof) | Separates periodic peaks from the aperiodic (1/f, broadband) part of a power spectrum | Python | 450 | 2026-09 | Apache-2.0 |
| [mne-tools/mne-hfo](https://github.com/mne-tools/mne-hfo) | High-frequency oscillation detectors for BIDS iEEG | Python | 15 | 2023-12 | BSD-3-Clause |
| [ZurichNCH/Automatic-High-Frequency-Oscillation-Detector](https://github.com/ZurichNCH/Automatic-High-Frequency-Oscillation-Detector) | Zurich automatic HFO detector (goes with the ds003498 sleep dataset) | MATLAB | 16 | 2026-06 | Apache-2.0 |
| [ieeg-portal/ieegpy](https://github.com/ieeg-portal/ieegpy) | Python API to stream data from the IEEG.org portal. Old (Python 2.7+ era) | Python | 25 | 2020-02 | Apache-2.0 |
| [MultimodalNeuroimagingLab/mnl_ieegBasics](https://github.com/MultimodalNeuroimagingLab/mnl_ieegBasics) | Basic iEEG analysis code from the Mayo Multimodal Neuroimaging Lab | MATLAB | 6 | 2026-08 | GPL-3.0 |

**Models and papers with code**

| Repo | What it does / when to use it | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [czlwang/BrainBERT](https://github.com/czlwang/BrainBERT) | Official BrainBERT (ICLR 2023): self-supervised transformer on iEEG spectrograms | Jupyter Notebook | 77 | 2025-11 | — |
| [czlwang/PopulationTransformer](https://github.com/czlwang/PopulationTransformer) | Official PopT (ICLR 2025): pools channel embeddings across variable electrode layouts | Python | 19 | 2026-09 | MIT |
| [yzz673/Brant](https://github.com/yzz673/Brant) | Brant (NeurIPS 2023), more than 500M-parameter intracranial foundation model; code now on Hugging Face | — | 44 | 2025-12 | Apache-2.0 |
| [flinkerlab/neural_speech_decoding](https://github.com/flinkerlab/neural_speech_decoding) | ECoG-to-speech with a differentiable synthesizer, 48 participants ([Chen 2024](https://doi.org/10.1038/s42256-024-00824-8)) | Jupyter Notebook | 122 | 2024-04 | GPL-3.0 |
| [neuralinterfacinglab/SingleWordProductionDutch](https://github.com/neuralinterfacinglab/SingleWordProductionDutch) | Loaders and baseline spectrogram reconstruction for the Dutch sEEG speech dataset | Python | 29 | 2025-01 | MIT |
| [jonaskohler/stereoEEG2speech](https://github.com/jonaskohler/stereoEEG2speech) | Seq2seq model with attention mapping sEEG to speech | Python | 34 | 2022-09 | — |
| [ludovicbellier/PF_HFAdecoding](https://github.com/ludovicbellier/PF_HFAdecoding) | Code for music reconstruction from high-frequency activity ([Bellier 2023](https://doi.org/10.1371/journal.pbio.3002176)) | MATLAB | 16 | 2023-10 | — |
| [SiavashShams/neuro2semantic](https://github.com/SiavashShams/neuro2semantic) | Neuro2Semantic (Interspeech 2025): aligns high-gamma iEEG with text embeddings, then inverts them to sentences. Marked "under construction" | Python | 13 | 2025-06 | — |
| [hassonlab/podcast-ecog-tutorials](https://github.com/hassonlab/podcast-ecog-tutorials) | Tutorials for the Hasson lab podcast ECoG dataset (language-model encoding) | Jupyter Notebook | 11 | 2025-02 | — |
| [IBM/eeg-ieeg-brain-compressor](https://github.com/IBM/eeg-ieeg-brain-compressor) | BrainCodec: neural compressor for EEG/iEEG; transfer from cleaner iEEG to EEG | Python | 23 | 2025-09 | Apache-2.0 |
| [NeuroSyd/seizure-prediction-GAN](https://github.com/NeuroSyd/seizure-prediction-GAN) | Seizure forecasting with GAN features | Python | 30 | 2023-12 | AGPL-3.0 |
| [ICRC-BME/machine_learn_module](https://github.com/ICRC-BME/machine_learn_module) | Code and data for multi-feature localization of epileptic foci from interictal iEEG | Python | 7 | 2019-02 | Apache-2.0 |
| [braindecode/braindecode](https://github.com/braindecode/braindecode) | Deep-learning models and training utilities for EEG/ECoG/MEG; good baselines | Python | 1324 | 2026-10 | BSD-3-Clause |

**Benchmarks and dataset loaders**

| Repo | What it does / when to use it | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [insight-neuro/neuroprobe](https://github.com/insight-neuro/neuroprobe) | Neuroprobe: benchmark of decoding tasks for iEEG foundation models, built on the Brain Treebank ([neuroprobe.dev](https://neuroprobe.dev)) | Python | 15 | 2026-10 | MIT |
| [czlwang/brain_treebank_code_release](https://github.com/czlwang/brain_treebank_code_release) | Official Brain Treebank code (NeurIPS 2024): loading, alignment, baselines | Python | 6 | 2025-01 | — |
| [michal-nahlik/kaggle-melbourne-seizure-prediction](https://github.com/michal-nahlik/kaggle-melbourne-seizure-prediction) | One entry to the Melbourne/AES Kaggle seizure prediction challenge | Matlab | 4 | 2018-06 | — |

**Curated lists**

| Repo | What it does / when to use it | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [openlists/ElectrophysiologyData](https://github.com/openlists/ElectrophysiologyData) | List of open (mostly human) electrophysiology datasets, including iEEG | — | 551 | 2026-06 | — |
| [openlists/ElectrophysiologySoftware](https://github.com/openlists/ElectrophysiologySoftware) | List of open electrophysiology software | — | 134 | 2025-02 | — |
| [LBCN-Stanford/awesome-ieeg](https://github.com/LBCN-Stanford/awesome-ieeg) | Curated iEEG resources from the Stanford LBCN lab | — | 4 | 2025-12 | MIT |
