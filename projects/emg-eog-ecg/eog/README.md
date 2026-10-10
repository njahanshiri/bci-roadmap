# EOG (Electrooculography)

EOG records the small voltage changes on the skin around the eyes that happen when the eyes move or blink. Today it is used most heavily as a **standard channel in clinical sleep studies (polysomnography)**, as a **reference signal for removing eye artifacts from EEG**, and in **vestibular testing (electronystagmography)**. It is also used as a low-power, camera-free way to detect eye gestures in assistive tech, glasses and earbuds, although consumer products in that space are still few ([Chang 2019 review](https://pmc.ncbi.nlm.nih.gov/articles/PMC6630230/); [AASM manual](https://learn.aasm.org/AssetListing/The-AASM-Manual-for-the-Scoring-of-Sleep-and-Associated-Events-4265/The-AASM-Manual-for-the-Scoring-of-Sleep-and-Associated-Events-6697); [ENG vs VNG](https://hearinghealthmatters.org/dizzinessdepot/2014/eng-versus-vng-part/)).

## 1. The data

**What is measured.** The eye carries a standing potential between the cornea (positive) and the retina (negative), so it behaves like an electrical dipole. When the eye rotates, the dipole rotates too, and electrodes near the eye see the voltage rise as the cornea approaches and fall as it moves away ([Chang 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6630230/); [López et al. 2018](https://ciencia.iscte-iul.pt/publications/development-of-an-eog-based-system-to-control-a-serious-game/53597)). Because EOG measures this potential and not an image, it **works with the eyes closed and during sleep** ([FAU eye-movement notes](https://www4.cs.fau.de/~wosch/fb/eye-movement.html)).

**Channels and montages.**
- **Horizontal EOG (hEOG):** electrodes at the outer corners (canthi) of the eyes, to the left and right. **Vertical EOG (vEOG):** electrodes above and below one eye. The classic setup uses four electrodes. The minimum workable setup uses three: one on the nose bridge and one between the eyebrows ([Chang 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6630230/)).
- **Sleep (PSG):** the AASM recommends E1-M2 and E2-M2. E1 sits about 1 cm below the left outer canthus and E2 about 1 cm above the right one, both referenced to the mastoid ([AASM manual](https://learn.aasm.org/AssetListing/The-AASM-Manual-for-the-Scoring-of-Sleep-and-Associated-Events-4265/The-AASM-Manual-for-the-Scoring-of-Sleep-and-Associated-Events-6697); exact placement confirmed only through secondary sources, *unverified* against the manual itself).
- **Forehead EOG:** 4 forehead channels in the SEED-VIG driving dataset ([SEED-VIG](https://bcmi.sjtu.edu.cn/home/seed/seed-vig.html)).
- **Glasses nose pads:** JINS MEME uses a 3-point EOG with electrodes on the nose bridge and both nose pads ([IEEE DataPort](https://ieee-dataport.org/keywords/eog-smartglasses-driving-wearable-sensors-driving-simulator); [JINS patent US9433369B2](https://patents.google.com/patent/US9433369)).
- **In-ear / around-ear:** OpenEarable ExG ([arXiv 2410.06533](https://arxiv.org/abs/2410.06533)); 14 electrodes around the ears in earEOG ([arXiv 2506.07193](https://arxiv.org/abs/2506.07193)).

**Signal types:** saccades (fast jumps), fixations (flat segments), smooth pursuit (slow ramps), blinks (large vertical spikes), and in sleep, rapid eye movements (REM) and slow eye movements. The 90 features in Bulling et al. are built from saccades, fixations and blinks ([Bulling 2011](https://perceptualui.org/publications/bulling11_pami/)). Slow eye movements are used as vigilance features ([SEED-VIG](https://bcmi.sjtu.edu.cn/home/seed/seed-vig.html)).

| Property | Typical value | Source |
|---|---|---|
| Sensitivity | ~5–20 µV per degree of rotation | [Cornell ECE course page](https://people.ece.cornell.edu/land/courses/ece4760/FinalProjects/s2005/dcc34/finalsite/design.html) (course project, weak source) |
| Amplitude | usually < 500 µV | [Chang 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6630230/) |
| Linear range | about ±20° (naso-temporal) to ±30° (bi-temporal) | [FAU](https://www4.cs.fau.de/~wosch/fb/eye-movement.html) |
| Useful band | DC/0.01 Hz to ~30 Hz; common filters: high-pass 0.05–0.1 Hz, low-pass 10–60 Hz | [Cornell](https://people.ece.cornell.edu/land/courses/ece4760/FinalProjects/s2005/dcc34/finalsite/design.html), [Chang 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6630230/) |
| Coupling | Must be DC-coupled to hold a steady fixation; AC-coupled amplifiers lose it | [ADInstruments KB](https://www.adinstruments.com/support/knowledge-base/can-i-use-bio-amp-teaching-powerlab-record-electrooculography-eog-signals) |
| Sampling rates seen in practice | 100 Hz (Sleep-EDF), 128 Hz (Bulling dataset), 200 Hz (JINS MEME) | [Sleep-EDF](https://physionet.org/content/sleep-edfx/1.0.0/), [Bulling dataset](https://perceptualui.org/research/datasets/RecognitionActivity), [IEEE DataPort](https://ieee-dataport.org/keywords/eog-smartglasses-driving-wearable-sensors-driving-simulator) |
| Electrodes | Wet Ag/AgCl (clinical); dry gold, textile, contactless (wearables) | [FAU](https://www4.cs.fau.de/~wosch/fb/eye-movement.html), [Ban 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC9979786/), [ElectraSight](https://arxiv.org/abs/2412.14848) |
| Main noise | Baseline drift, facial and jaw EMG, eyelid artifacts, motion, changes in the standing potential with lighting | [Chang 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6630230/), [FAU](https://www4.cs.fau.de/~wosch/fb/eye-movement.html) |

**Formats.** In sleep, EOG ships inside EDF files alongside EEG and EMG ([Sleep-EDF](https://physionet.org/content/sleep-edfx/1.0.0/)). In EEG research it is stored as extra channels in the EEG file (for example hEOG and vEOG in DEAP, [DEAP readme](https://www.eecs.qmul.ac.uk/mmv/datasets/deap/readme.html)). Wearables usually stream CSV or BLE packets through vendor apps or SDKs.

## 2. Devices and specifications

Only specs I could source are listed; "–" means not found.

**Research and lab amplifiers**

| Device | Company | Type | Channels | Sampling rate | Resolution | Connectivity | Typical use | Status/price |
|---|---|---|---|---|---|---|---|---|
| [EOG100C](https://biopac.com/?p=15771) | BIOPAC | Dedicated EOG amplifier module, DC to 100 Hz, can output eye velocity directly | 1 per module | set by the MP data-acquisition unit | – | MP system | Saccade and nystagmus research | Sold |
| [g.USBamp](https://www.gtec.at/product/g-usbamp-research/) | g.tec | General biosignal amplifier, DC-coupled, < 0.4 µV RMS noise | 16 monopolar / 8 bipolar | up to 38.4 kHz | 24-bit | USB 2.0 | EEG+EOG BCI | Sold |
| [ActiveTwo](https://www.biosemi.com/faq/adjust_samplerate.htm) | BioSemi | EEG system with 8 external "EX" channels (often used for EOG) | up to 256 + 8 EX | 2–16 kHz | *unverified* | – | EEG with EOG references | Sold |
| [BrainAmp ExG](https://www.brainproducts.com/solutions/brainamp/) | Brain Products | Bipolar ExG amplifier, DC–1000 Hz | *unverified* | up to 5 kHz | – | Fiber optic | EOG, EMG and ECG alongside EEG | Sold |
| [Bio Amp (DC mode) / EOG Pod](https://www.adinstruments.com/support/knowledge-base/can-i-use-bio-amp-teaching-powerlab-record-electrooculography-eog-signals) | ADInstruments | Isolated bio amplifier with DC mode; the EOG Pod is for teaching | 1–8 | set by PowerLab | – | PowerLab | Teaching and physiology labs | Sold |

**Clinical systems**

| Device | Company | Type | Channels | Sampling rate | Resolution | Connectivity | Typical use | Status |
|---|---|---|---|---|---|---|---|---|
| [Grael PSG](https://www.compumedics.com.au/products/grael-psg) | Compumedics | Lab PSG amplifier | 29 total (13 referential + 6 differential + others) | up to 2048 Hz | 24-bit | Power over Ethernet | In-lab sleep studies | Sold |
| [Nox A1s](https://www.medi-shop.gr/en/sleep-diagnostic-systems/nox-a1s-c1s-sleep-diagnostic-system-kit) | Nox Medical | Portable PSG, 10 unipolar inputs for EEG and EOG | 13 unipolar + 4 bipolar | output rate *unverified* (the vendor quotes a very high internal rate) | 24-bit (bipolar) | BLE 5.0, USB-C | Home and hospital PSG | Sold |
| ENG systems | various | EOG electrodes around the eyes for caloric, positional and oculomotor tests | 2–4 | – | – | – | Vestibular testing; video-based VNG is the camera alternative | Both ENG and VNG are in clinical use ([source](https://hearinghealthmatters.org/dizzinessdepot/2014/eng-versus-vng-part/)) |

**Wearable / consumer / research prototypes**

| Device | Company | Type | Channels | Sampling rate | Resolution | Connectivity | Typical use | Status |
|---|---|---|---|---|---|---|---|---|
| JINS MEME ES_R | JINS | Glasses with 3-point EOG and IMU | 4 EOG channels in the dataset | 200 Hz | – | Bluetooth | Fatigue, focus, driving research | General sales ended Mar 2024; business-only; app support to Aug 2025 ([IEEE DataPort](https://ieee-dataport.org/keywords/eog-smartglasses-driving-wearable-sensors-driving-simulator), [Fashionsnap](https://www.fashionsnap.com/article/2024-03-13/jins-meme-close/)) |
| Naqi Neural Earbuds | Naqi Logix | Earbuds controlled by blinks, jaw and brow gestures | – | – | – | – | Accessibility control | CES 2026 Best of Innovation; sensing modality not disclosed ([CES](https://www.ces.tech/ces-innovation-awards/2026/naqi-neural-earbuds-with-invisible-user-interface/)) |
| AAVAA glasses and earbuds | AAVAA | Fabric/polymer biosignal sensors for eye, face and head control | – | – | – | – | Assistive device control | Launched 2024 ([Rehab Pub](https://rehabpub.com/mobility/aavaa-launches-bci-technology-for-smart-glasses/)) |
| OpenEarable ExG | KIT (academic) | Open-source ear ExG | up to 7 | – | – | – | Research | MIT license ([arXiv](https://arxiv.org/abs/2410.06533)) |
| ElectraSight | ETH Zürich (academic) | Glasses with contact and contactless EOG, onboard tinyML | – | – | – | – | Research | 7.75 mW ([arXiv](https://arxiv.org/abs/2412.14848)) |

**Low-cost / DIY**

| Device | Company | Type | Channels | Sampling rate | Resolution | Connectivity | Typical use | Price |
|---|---|---|---|---|---|---|---|---|
| [Cyton](https://shop.openbci.com/products/cyton-biosensing-board-8-channel) | OpenBCI | ADS1299 board; EOG listed among supported signals | 8 | 250 Hz | 24-bit | RF dongle | Hobby and research BCI | $1,249 |
| [Ganglion](https://docs.openbci.com/Ganglion/GanglionSpecs/) | OpenBCI | MCP3912 board | 4 | 200 Hz | 0.1788 µV/bit | BLE | Low-cost ExG | – |
| [EOG sensor for BITalino](https://www.pluxbiosignals.com/products/electrooculography-eog-for-bitalino) | PLUX | Analog EOG sensor; datasheet values (gain 2040, 0.05–41 Hz) *unverified* | 1 | 1–1000 Hz (BITalino) | 10-bit (BITalino ADC, *unverified*) | BITalino BT/BLE | Teaching | €60 |
| [AD8232](https://www-cce.cldnet.analog.com/media/en/technical-documentation/data-sheets/ad8232.pdf) | Analog Devices | Single-lead ECG front-end chip (gain 100, 170 µA) that hobbyists repurpose for EOG | 1 | MCU-dependent | MCU-dependent | – | DIY | Its DC blocking removes slow EOG (fixations) |

## 3. Applications (domains)

| Domain | How EOG is used | Examples | Maturity |
|---|---|---|---|
| Sleep staging | Two EOG leads are standard in PSG for detecting REM, since R&K 1968 and the AASM 2007 manual | Compumedics, Nox; EOG-only staging reaches macro-F1 ~0.70–0.75 ([Maiti 2023](https://arxiv.org/abs/2310.03757)) | **Clinical standard** |
| EEG artifact removal | The EOG channel serves as a regression reference or helps label ICA components; deep models are trained on EOG-contaminated EEG | Gratton 1983, ICA (Jung 2000), ART, D4PM | **Standard in research** |
| Vestibular testing | Electronystagmography records nystagmus during caloric and positional tests | ENG vs VNG ([source](https://hearinghealthmatters.org/dizzinessdepot/2014/eng-versus-vng-part/)) | **Clinical**, increasingly replaced by video |
| Clinical ophthalmology | Light-peak to dark-trough (Arden) ratio measures retinal pigment epithelium function; ≥1.80 is normal; used to confirm Best disease | [EyeWiki](https://eyewiki.org/Electrooculogram), [ISCEV 2017](https://link.springer.com/10.1007/s10633-017-9573-2) | **Clinical, niche** |
| Assistive communication (ALS/LIS) | Eye-movement spellers, including auditory spellers for patients who can no longer use cameras | [Sci Rep 2020](https://www.nature.com/articles/s41598-020-65333-1) | Research |
| Wheelchair / robot control | Eye gestures mapped to motion commands | [Barea 2002](https://portalcientifico.uah.es/documentos/614e76ac68c341284de7859b?lang=en) | Research |
| HCI, smart glasses, earables | Calibration-free eye gestures at milliwatt power | JINS MEME, [VergeIO](https://arxiv.org/abs/2507.02187), Wisear/Naqi | Early commercial |
| VR/AR | EOG added to SSVEP inside VR headsets to raise bit rate | [Ha, Park, Im 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8908008/) | Research |
| Hybrid BCI | EOG narrows the SSVEP target set, or adds blink/brow commands to motor-imagery BCI | [Zhang 2023](https://www.frontiersin.org/journals/human-neuroscience/articles/10.3389/fnhum.2023.1103935/full) | Research |
| Drowsiness / vigilance | Blink and slow-eye-movement features from forehead EOG, regressed against PERCLOS | [SEED-VIG](https://bcmi.sjtu.edu.cn/home/seed/seed-vig.html), JINS MEME | Research; JINS sold fatigue features commercially |
| Reading / activity / cognitive state | Saccade, fixation and blink statistics | [Bulling 2011](https://perceptualui.org/publications/bulling11_pami/) | Research |
| Gaming | Games controlled by eye movements, often for motor rehab | [López et al. 2018](https://ciencia.iscte-iul.pt/publications/development-of-an-eog-based-system-to-control-a-serious-game/53597) | Research |
| Emotion | hEOG and vEOG used as peripheral channels for affect recognition | [DEAP](https://www.eecs.qmul.ac.uk/mmv/datasets/deap/readme.html) | Research |

## 4. Companies

| Company | Country | Focus | Key product | Status 2025–2026 |
|---|---|---|---|---|
| JINS | Japan | EOG glasses | JINS MEME | Business-only since 2024; app support ended Aug 2025 ([source](https://www.fashionsnap.com/article/2024-03-13/jins-meme-close/)) |
| Wisear → Naqi Logix | France → Canada | Earbud neural interface (Wisear demoed EOG) | Wisearphones / Naqi Neural Earbuds | Acquired by Naqi on 5 Jan 2026 ([source](https://www.trysignalbase.com/news/acquisitions/wisear-acquired-by-naqi-acquisition)); EOG prototype noted by [TechCrunch](https://techcrunch.com/2022/01/20/wisear/) |
| AAVAA | Canada | Assistive biosignal control | Glasses and earbuds | On sale ([source](https://rehabpub.com/mobility/aavaa-launches-bci-technology-for-smart-glasses/)) |
| Emteq Labs | UK | Facial sensing; **optical (OCO), not EOG** | OCOsense / Sense | Dev kit from Dec 2024 ([IEEE Spectrum](https://spectrum.ieee.org/glasses-health-tech)) |
| Beacon Biosignals | USA | Sleep; the Dreem 3S is a **dry-EEG** headband | Dreem 3S | FDA 510(k) 2023 ([source](https://www.medtechdive.com/news/beacon-biosignals-fda-clearance-sleep-tracking-headband/693901/)) |
| Compumedics / Nox Medical | Australia / Iceland | PSG with EOG | Grael, Nox A1s | Sold |
| BIOPAC, g.tec, Brain Products, ADInstruments, OpenBCI, PLUX | various | EOG-capable amplifiers | see §2 | Sold |
| Oticon, Starkey | Denmark, USA | Ear-level EOG patents for hearing aids | – | Patents only (§5) |
| Tobii, Pupil Labs | Sweden, Germany | **Camera** eye tracking, the main competitor | Glasses X, Neon (1.8° calibration-free) | Active ([Tobii](https://www.tipranks.com/news/company-announcements/tobii-ab-reports-strong-growth-and-profitability-in-2025), [Neon validation](https://zenodo.org/records/18504792)) |

## 5. Patents

| Patent | Holder | Topic | Year (grant) | Why it matters |
|---|---|---|---|---|
| [US9433369B2](https://patents.google.com/patent/US9433369) | JINS | EOG electrodes on glasses nose pads | 2016 | The basis of JINS MEME's form factor |
| [US11237411B2](https://patents.google.com/patent/US11237411) | JINS | Nose pad with electrodes and electronics | 2022 | Self-contained EOG module |
| [US11874958B2](https://patents.google.com/patent/US11874958B2/en) | Apple | EOG on a head-mounted device, elastomer electrode contact | 2024 | Big-tech interest in EOG for headsets |
| [US11954249B1](https://patents.google.com/patent/US11954249B1/en) | Apple | Eye-monitoring electrodes on a head-mounted device | 2024 | Same |
| [US11992324B2](https://patents.google.com/patent/US11992324B2/en) | Oticon | Beamformed ear-level EOG for gaze | 2024 | Gaze-steered hearing aids |
| [US11223915B2](https://patents.google.com/patent/US11223915B2/en) | Starkey | In-ear EOG combined with EMREO | 2022 | Eye sensing from inside the ear |
| [US11507185B1](https://patents.google.com/patent/US11507185B1/en) | Lenovo | EOG and IMU fusion for headset eye tracking | 2022 | A drift-correction approach |
| [EP4173567B1](https://patents.google.com/patent/EP4173567B1/en) | STMicroelectronics | Charge-variation electrodes in the glasses frame | 2025 | Non-contact EOG at the chip-vendor level |
| [US9955895B2](https://patents.google.com/patent/US9955895B2/en) | SUNY Research Foundation | EOG in eyeglass temples | 2018 | Early smart-glasses EOG HCI |

I found no confirmed EOG patents assigned to Meta or Google (*unverified*).

## 6. Most-cited papers

These are foundational papers; I did not verify citation counts.

| Paper | Authors | Venue/year | Why it matters |
|---|---|---|---|
| [New clinical test of retinal function based upon the standing potential of the eye](https://pmc.ncbi.nlm.nih.gov/articles/PMC510228) | Arden, Barrada, Kelsey | Br J Ophthalmol 1962 | Introduced the Arden ratio and clinical EOG |
| [A Manual of Standardized Terminology… Sleep Stages](https://search.worldcat.org/oclc/2518321) | Rechtschaffen, Kales | 1968 | Made two EOG leads standard in sleep scoring |
| [Survey of eye movement recording methods](https://link.springer.com/article/10.3758/BF03201553) | Young, Sheena | Behav Res Methods 1975 | Classic comparison of EOG with other eye-tracking methods |
| [A new method for off-line removal of ocular artifact](https://pubmed.ncbi.nlm.nih.gov/6187540/) | Gratton, Coles, Donchin | EEG Clin Neurophysiol 1983 | Regression-based EOG correction (EMCP) |
| [Removal of ocular artifact from the EEG: a review](https://busqueda.bvsalud.org/portal/resource/es/mdl-11018488) | Croft, Barry | Neurophysiol Clin 2000 | The standard review of EOG correction |
| [Removing EEG artifacts by blind source separation](https://www.cambridge.org/core/journals/psychophysiology/article/abs/removing-electroencephalographic-artifacts-by-blind-source-separation/2548D35629CAE17E6956C2FFF1B6C8AB) | Jung, Makeig et al. | Psychophysiology 2000 | ICA for eye artifacts, the basis of EEGLAB practice |
| [System for assisted mobility using eye movements based on EOG](https://portalcientifico.uah.es/documentos/614e76ac68c341284de7859b?lang=en) | Barea, Boquete, Mazo, López | IEEE TNSRE 2002 | Landmark EOG wheelchair |
| [AASM Manual for the Scoring of Sleep](https://learn.aasm.org/AssetListing/The-AASM-Manual-for-the-Scoring-of-Sleep-and-Associated-Events-4265/The-AASM-Manual-for-the-Scoring-of-Sleep-and-Associated-Events-6697) | AASM | 2007 → current | The current PSG EOG standard |
| [Eye movement analysis for activity recognition using EOG](https://perceptualui.org/publications/bulling11_pami/) | Bulling, Ward, Gellersen, Tröster | IEEE TPAMI 2011 | Wearable EOG for activity recognition |
| [A multimodal approach to estimating vigilance using EEG and forehead EOG](https://bcmi.sjtu.edu.cn/home/seed/seed-vig.html) | Zheng, Lu | J Neural Eng 2017 | SEED-VIG, the standard vigilance benchmark |
| [ISCEV standard for clinical EOG, 2017 update](https://link.springer.com/10.1007/s10633-017-9573-2) | ISCEV | Doc Ophthalmol 2017 | Current clinical EOG protocol |

## 7. New achievements (2023–2026)

- **SleepFM** (Nature Medicine 2026) is trained on 585k hours of PSG, with EOG included as part of brain activity. It predicts 130 conditions with C-index ≥ 0.75 ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12920147/)).
- **VergeIO** (2025): depth (vergence) eye gestures on glasses, 97% accuracy on unseen users, no calibration, 3 mW ([arXiv](https://arxiv.org/abs/2507.02187)).
- **ElectraSight** (2024): 92% on 6 classes and 81% on 10 classes, 7.75 mW, more than 3 days on a 175 mAh battery ([arXiv](https://arxiv.org/abs/2412.14848)).
- **earEOG** (2025): around-ear EOG reaches saccade r=0.99 horizontally, but vertical tracking is poor ([arXiv](https://arxiv.org/abs/2506.07193)).
- **SSVEP+EOG speller** (2023): 94.75% accuracy and 108.6 bits/min ([Frontiers](https://www.frontiersin.org/journals/human-neuroscience/articles/10.3389/fnhum.2023.1103935/full)).
- **Soft headband** (2023): 4 dry electrodes plus a CNN, 98.3% on 6 classes ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC9979786/)).
- **Artifact removal:** ART, a transformer ([arXiv 2024](https://arxiv.org/abs/2409.07326)); D4PM, a diffusion model that claims state of the art on EOG ([arXiv 2025](https://arxiv.org/abs/2509.14302)); EEGPARnet, CC 0.967 on EEGdenoiseNet EOG ([project page](https://lmerin.owlstown.net/projects/6870-eegparnet)).
- **Industry:** Naqi wins CES 2026 Best of Innovation and acquires Wisear (Jan 2026). STMicroelectronics is granted EP4173567B1 (Dec 2025).

## 8. Current state of the field

**Where EOG is used today.**
- *Clinical and standard:* PSG sleep staging, ENG vestibular testing (losing ground to video), clinical EOG for Best disease (niche), and as the EOG reference channel in EEG labs.
- *Early commercial:* assistive and gesture earbuds and glasses (AAVAA, Naqi). The best-known consumer device, JINS MEME, retreated to business-only sales in 2024.
- *Research:* ALS spellers, wheelchairs, hybrid BCI, VR, vigilance, activity and emotion recognition.

**Open problems.**
- **Drift and absolute gaze:** DC drift and electrode-contact changes mean wearable EOG mostly classifies gestures; it does not deliver absolute gaze the way cameras do (about 1.8° for Neon).
- **Placement:** vertical EOG from ear and around-ear placements is weak (earEOG).
- **Benchmarks:** artifact-removal results come mostly from semi-synthetic mixes (EEGdenoiseNet), and some vigilance results look like subject leakage (*unverified*).
- **Clinical evidence:** ALS evidence comes from tiny cohorts (n=4, [Sci Data 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC7801642/)).

**Where an AI engineer can contribute.**
- Calibration-free, cross-user models for dry and contactless electrodes.
- Drift-robust sequence models, for example fusing EOG with an IMU as Lenovo's patent does.
- tinyML on milliwatt budgets.
- Honest cross-subject benchmarks for vigilance and artifact removal.
- EOG inside biosignal foundation models (SleepFM shows the way).

## 9. Public datasets

| Dataset | Content | Size | Link |
|---|---|---|---|
| Sleep-EDF Expanded | PSG with EEG, EOG and chin EMG at 100 Hz, plus hypnograms | 197 nights | [PhysioNet](https://physionet.org/content/sleep-edfx/1.0.0/) |
| SEED-VIG | 17-channel EEG, 4-channel forehead EOG, PERCLOS labels, simulated driving | 23 subjects, ~2 h each ([arXiv 2408.13929](https://arxiv.org/abs/2408.13929)) | [BCMI](https://bcmi.sjtu.edu.cn/home/seed/seed-vig.html) |
| EEGdenoiseNet | Clean EEG, EOG and EMG segments for building synthetic mixtures | 4,514 EEG / 3,400 EOG / 5,598 EMG segments | [G-Node](https://gin.g-node.org/NCClab/EEGdenoiseNet) |
| ALS locked-in EEG+EOG | Auditory EOG speller sessions | 4 patients | [Sci Data 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC7801642/) |
| Bulling EOG activity | hEOG and vEOG at 128 Hz, 5 office activities | 8 people, ~8 h | [perceptualui.org](https://perceptualui.org/research/datasets/RecognitionActivity) |
| Real & simulated driving | JINS MEME ES_R, 4-channel EOG at 200 Hz | 51 people | [IEEE DataPort](https://ieee-dataport.org/keywords/eog-smartglasses-driving-wearable-sensors-driving-simulator) |
| DEAP | 32-channel EEG plus hEOG, vEOG and other peripheral signals; emotion ratings | 32 people × 40 videos | [QMUL](https://www.eecs.qmul.ac.uk/mmv/datasets/deap/readme.html) |
| EEGEyeNet | 128-channel EEG plus video eye tracking (not EOG; useful for gaze from EEG and EOG-like signals) | 356 people, 47+ h | [NeurIPS 2021](https://neurips.cc/virtual/2021/22756) |

## 10. GitHub repositories

Stars and dates checked via the GitHub API on 2026-10-10.

**Toolkits and libraries**

| Repo | What it does / when to use it | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [neuropsychology/NeuroKit](https://github.com/neuropsychology/NeuroKit) | NeuroKit2. Has EOG functions for cleaning and blink detection next to ECG/EMG/EDA. The quickest way to get started with EOG in Python | Python | 2,392 | 2026-10 | MIT |
| [mne-tools/mne-python](https://github.com/mne-tools/mne-python) | The standard M/EEG library. Its EOG tools find blink and saccade events, build EOG epochs and flag ICA components that match the EOG channel | Python | 3,540 | 2026-10 | BSD-3-Clause |
| [scientisst/BioSPPy](https://github.com/scientisst/BioSPPy) | General biosignal toolbox, maintained fork of the original BioSPPy ([PIA-Group/BioSPPy](https://github.com/PIA-Group/BioSPPy), archived, 645 stars) | Python | 124 | 2026-09 | NOASSERTION |
| [brainflow-dev/brainflow](https://github.com/brainflow-dev/brainflow) | One API for streaming data from many biosensor boards (OpenBCI and others). Use it to acquire EOG from low-cost hardware | C++ | 1,770 | 2026-10 | NOASSERTION |
| [sccn/eeglab](https://github.com/sccn/eeglab) | MATLAB environment where ICA-based removal of eye artifacts became standard practice | MATLAB | 800 | 2026-09 | NOASSERTION |

**EEG ocular-artifact removal**

| Repo | What it does / when to use it | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [ncclabsustech/EEGdenoiseNet](https://github.com/ncclabsustech/EEGdenoiseNet) | Benchmark of clean EEG, EOG and EMG segments plus baseline networks. The usual starting point for deep-learning EOG removal | Jupyter Notebook | 257 | 2023-07 | MIT |
| [CNElab-Plus/ArtifactRemovalTransformer](https://github.com/CNElab-Plus/ArtifactRemovalTransformer) | Official code for ART, the transformer for multichannel EEG denoising (see §7) | Python | 12 | 2024-11 | none listed |
| [sccn/ICLabel](https://github.com/sccn/ICLabel) | EEGLAB plugin that labels ICA components, including an "eye" class | MATLAB | 76 | 2026-10 | BSD-2-Clause |
| [mne-tools/mne-icalabel](https://github.com/mne-tools/mne-icalabel) | Python port of ICLabel for MNE | Python | 124 | 2026-10 | BSD-3-Clause |
| [nbara/python-meegkit](https://github.com/nbara/python-meegkit) | Denoising toolkit (ASR, DSS and others). Use it for artifact removal without training a model | Python | 230 | 2026-08 | BSD-3-Clause |
| [DiGyt/asrpy](https://github.com/DiGyt/asrpy) | Artifact Subspace Reconstruction for MNE data | Jupyter Notebook | 66 | 2026-08 | BSD-3-Clause |
| [autoreject/autoreject](https://github.com/autoreject/autoreject) | Automatically rejects or repairs bad trials and sensors; usually paired with ICA for eye artifacts | Python | 162 | 2026-10 | BSD-3-Clause |

**Sleep staging with EOG**

| Repo | What it does / when to use it | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [zou-group/sleepfm-clinical](https://github.com/zou-group/sleepfm-clinical) | Official SleepFM (Nature Medicine) code and checkpoints. The PSG foundation model takes EEG+EOG as "brain activity" input | Python | 736 | 2026-03 | NOASSERTION |
| [rthapa84/sleepfm-codebase](https://github.com/rthapa84/sleepfm-codebase) | Earlier SleepFM version (ICML 2024) | Python | 179 | 2024-06 | MIT |
| [perslev/U-Time](https://github.com/perslev/U-Time) | U-Time and U-Sleep, fully convolutional sleep stagers that run on PSG channels including EOG | Python | 319 | 2026-06 | MIT |
| [raphaelvallat/yasa](https://github.com/raphaelvallat/yasa) | PSG analysis: automatic staging (optional EOG input), REM detection, spindles | Python | 589 | 2026-10 | BSD-3-Clause |
| [KiranKGR/ScoreREMGUI](https://github.com/KiranKGR/ScoreREMGUI) | MATLAB GUI for annotating and quantifying rapid eye movements in REM sleep | MATLAB | 3 | 2026-06 | GPL-3.0 |

**Eye-gesture / HCI / hardware**

| Repo | What it does / when to use it | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [OpenEarable/open-earable-ExG](https://github.com/OpenEarable/open-earable-ExG) | Hardware (CAD, EasyEDA) and code for the OpenEarable ExG ear biopotential board (UbiComp '24) | C | 7 | 2024-07 | none listed |
| [zx-explorer/VergeIO](https://github.com/zx-explorer/VergeIO) | Official code for VergeIO, the depth-aware EOG eye gestures on glasses | none listed | 0 | 2026-07 | none listed |
| [OpenBCI/OpenBCI_GUI](https://github.com/OpenBCI/OpenBCI_GUI) | Desktop app for Cyton and Ganglion boards. The easiest way to view raw EOG from DIY hardware | HTML | 965 | 2026-04 | MIT |
| [jins-meme/ES_R-Development-Kit](https://github.com/jins-meme/ES_R-Development-Kit) | Official JINS MEME ES_R academic development kit (Windows, Android, Mac) | C# | 19 | 2026-10 | NOASSERTION |
| [jins-meme/JinsMemeSDK-Sample-Android](https://github.com/jins-meme/JinsMemeSDK-Sample-Android) | Consumer-SDK sample app for JINS MEME (archived) | Java | 12 | 2021-10 | MIT |

**Vigilance / emotion / datasets**

| Repo | What it does / when to use it | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [ardkastrati/EEGEyeNet](https://github.com/ardkastrati/EEGEyeNet) | Benchmark code for predicting gaze from EEG (NeurIPS 2021 dataset) | Python | 49 | 2021-11 | MIT |
| [dttutty/SEED-VIG-CNN](https://github.com/dttutty/SEED-VIG-CNN) | Community (unofficial) model fusing EEG and forehead-EOG features to regress PERCLOS on SEED-VIG | Python | 30 | 2026-07 | none listed |

**Curated lists**

| Repo | What it does / when to use it | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [NeuroTechX/awesome-bci](https://github.com/NeuroTechX/awesome-bci) | Broad BCI resource list | – | 1,548 | 2026-10 | none listed |
| [guxiao0822/Awesome-Biosignal-Foundation-Model](https://github.com/guxiao0822/Awesome-Biosignal-Foundation-Model) | Foundation models, datasets and tools for biosignals | – | 145 | 2026-03 | none listed |
| [BosonHwang/awesome-biosignals](https://github.com/BosonHwang/awesome-biosignals) | AI papers on physiological signals | – | 90 | 2026-08 | none listed |
| [eyes-on-disabilities/awesome-eye-tracking](https://github.com/eyes-on-disabilities/awesome-eye-tracking) | Eye- and head-tracking software and products with an accessibility focus (mirror of a Codeberg repo) | – | 26 | 2026-04 | none listed |
