# EMG (Electromyography)

Electromyography records the electrical activity that skeletal muscles produce when the nervous system tells them to contract. Today it is used most in clinical neuromuscular diagnosis (needle EMG with nerve conduction studies), in myoelectric prosthesis and orthosis control, and in sports and rehabilitation research. Since September 2025 it has also been a mass-market input device: Meta's sEMG wristband ships with its display glasses ([AANEM](https://education.aanem.org/AssetListing/Medical-Student-Nerve-Conduction-Study-Basics-6162/2022-Basics-of-NCS-and-Needle-EMG-Part-1-28668), [Auganix](https://www.auganix.org/?p=17578)).

Items marked *unverified* could not be confirmed from a source. Cells marked "—" mean the manufacturer did not publish the spec, or I could not find it.

## 1. The data

**What is measured.** A *motor unit* is one motor neuron plus all the muscle fibres it controls. Each time the neuron fires, every fibre in the unit produces an action potential. These add up into a *motor unit action potential* (MUAP), and the repeated firing produces a MUAP train. The EMG you record is the sum of all active MUAP trains, filtered by tissue and electrodes. With needle electrodes MUAPs reach millivolts; at the skin they are microvolts ([ISEK glossary](https://cede.isek.org/glossary/?page=6), [DEMUSE](https://demuse.feri.um.si/?p=14)). Because EMG is a filtered copy of spinal motor-neuron spikes, it can be "decomposed" back into individual neuron firings ([Farina et al. 2004](https://vivo-cub.colorado.edu/display/pubid_11885)).

**Recording types**

| Type | How | Used for |
|---|---|---|
| Surface EMG (sEMG) | A few bipolar electrodes on the skin | Prosthetics, sports, biofeedback, consumer wristbands |
| High-density sEMG (HD-sEMG) | Grids of 32–400+ electrodes | Motor-unit decomposition, research decoders ([Hyser: 256 ch](https://physionet.org/content/hd-semg/)) |
| Intramuscular / needle EMG | Needle or fine wire in the muscle | Clinical diagnosis of neuropathy, myopathy, ALS ([AANEM](https://education.aanem.org/AssetListing/Medical-Student-Nerve-Conduction-Study-Basics-6162/2022-Basics-of-NCS-and-Needle-EMG-Part-1-28668)) |
| Implanted EMG | Wireless sensors left inside muscle | Prosthesis control: Össur/AMF IMES ([Rehab Management](https://rehabpub.com/orthotics-prosthetics/prosthetics/ossur-and-alfred-mann-foundation-extend-agreement-to-explore-mind-controlled-prosthetics/)), Phantom Neuro ([TechCrunch](https://techcrunch.com/2025/04/15/phantom-neuro-grabs-19m-to-help-amputees-gain-control-of-their-phantom-limbs)) |

**Signal characteristics**

| Property | Typical value | Source |
|---|---|---|
| Amplitude (surface) | 0–10 mV peak-to-peak, 0–1.5 mV RMS | [De Luca 2002, Delsys](https://www.delsys.com/downloads/TUTORIAL/semg-detection-and-recording.pdf) |
| Frequency band | Usable 0–500 Hz, dominant 50–150 Hz | same |
| Recommended high-pass | 20 Hz Butterworth, 12 dB/oct, to remove motion artifact | [De Luca et al. 2010](https://www.bu.edu/nmrc/files/2010/06/103.pdf) |
| Sampling rate | About 2 kHz is standard (Ninapro DB2, Hyser, GRABMyo, Meta datasets); consumer bands go lower (Myo: 200 Hz); research amplifiers reach 10,240 Hz for intramuscular EMG | [Ninapro](https://ninapro.hevs.ch/), [Hyser](https://physionet.org/content/hd-semg/), [Myo](https://pmc.ncbi.nlm.nih.gov/articles/PMC10222313), [Quattrocento](https://otbioelettronica.it/en/quattrocento/) |
| Electrodes / placement | Ag/AgCl or silver bars (De Luca: 1 cm × 1 mm); SENIAM placement guidelines | [De Luca 2002](https://www.delsys.com/downloads/TUTORIAL/semg-detection-and-recording.pdf), [Hermens 2000](https://www.doi.org/10.1016/S1050-6411(00)00027-4) |
| Main noise sources | Power-line and ambient EM noise, motion artifact (skin interface and cable), electronics noise, baseline noise. Electrode shift and sweat matter for wearables | [De Luca 2002](https://www.delsys.com/downloads/TUTORIAL/semg-detection-and-recording.pdf), [emg2pose](https://arxiv.org/html/2412.02725v1) |

**Features and formats.** Classic decoders use time-domain features computed over sliding windows: mean absolute value (MAV), zero crossings, slope sign changes and waveform length (the "Hudgins set"), plus RMS, autoregressive coefficients and spectral features ([Hudgins 1993](https://scinapse.io/papers/2123167643), [Phinyomark 2012](https://doi.org/10.1016/j.eswa.2012.01.102)). Mean and median frequency fall as a muscle fatigues ([fatigue review](https://journals.utm.my/jurnalteknologi/article/view/4676)). Modern work instead feeds raw multichannel signals into CNNs or transformers (section 7). Common file formats are MATLAB `.mat` (Ninapro, [Atzori 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC4421935)), WFDB `.dat`/`.hea` (Hyser, GRABMyo on PhysioNet) and HDF5 (Meta's [generic-neuromotor-interface](https://github.com/facebookresearch/generic-neuromotor-interface) data).

## 2. Devices and specifications

**Research-grade**

| Device | Company | Type | Channels | Sampling rate | Bits | Connectivity | Typical use | Status/price |
|---|---|---|---|---|---|---|---|---|
| Trigno (original system) | Delsys | Wireless sEMG | Up to 16 sensors per base | Up to 4000 Hz; bandwidth 20–450 Hz | 16 | Wireless, 40 m range | Biomechanics, gait | Older system ([user guide](https://biomedicale.u-paris.fr/wp-content/uploads/2020/01/Trigno-Users-Guide.pdf)) |
| Trigno Avanti | Delsys | Wireless sEMG + IMU | 1 EMG per sensor | Up to 4370 Hz; bandwidth 10–850 Hz selectable | 16 | Wireless | Biomechanics | Current ([product](https://delsys.com/trigno-avanti/), specs from [ADInstruments](https://adinstruments.com/products/trigno-emg-sensors)) |
| Trigno Galileo | Delsys | HD/decomposition sensor | — | — | — | Wireless | Motor-unit analysis with NeuroMap | Current ([Delsys](https://delsys.com/trigno-galileo/)) |
| Quattrocento | OT Bioelettronica | HD-EMG amplifier | 96–384 + 16 aux | 512 / 2048 / 5120 / 10240 Hz | — | Ethernet, USB2 | HD-sEMG, intramuscular EMG, EEG | Current ([OTB](https://otbioelettronica.it/en/quattrocento/)) |
| Sessantaquattro+ | OT Bioelettronica | Portable HD-EMG | 64 + 2 aux | — | — | Wi-Fi, SD card (>11 h) | Mobile HD-sEMG | Current ([OTB](https://otbioelettronica.it/en/sessantaquattro/)) |
| Muovi / MuoviPro | OT Bioelettronica | Wearable HD-EMG probe | 32 per probe (Pro: up to 4×32) | — | — | Wi-Fi / Ethernet via SyncStation | Wearable HD-sEMG with IMU | Current ([OTB](https://otbioelettronica.it/en/muovi/)) |
| Ultium EMG | Noraxon | Wireless sEMG | Up to 32 (analog out) | Up to 4000 Hz | 24 | Wireless, >8 h onboard memory | Sports, clinical gait | Current ([spec](https://www.praiston.pl/en/catalog/view/12716/noraxon-ultium-emg-surface-electromyography-with-myomuscle-module)) |
| WaveX | Cometa | Wireless sEMG + IMU | Up to 36 transmitters | Up to 2000 Hz | — | Wi-Fi | Gait, clinical (MDR IIa) | Current ([Prophysics](https://www.prophysics.ch/en/our-products/emg-imu-sensors/wavex-receiver)) |
| ActiveTwo Mk2 | BioSemi | Wired EEG/EMG amplifier | Up to 280 (≤8 kHz; 152 at 16 kHz) | 2048–16384 Hz | 24 | USB2, optical | HD-EMG, EEG+EMG | Current ([BioSemi](https://www.biosemi.com/activetwo_full_specs.htm)) |

**Clinical / diagnostic**

| Device | Company | Type | Channels | Sampling rate | Bits | Connectivity | Typical use | Status |
|---|---|---|---|---|---|---|---|---|
| Sierra Summit | Cadwell | Needle EMG / NCS / EP / neuromuscular ultrasound | 1–2 or 3–12 amplifier | — | — | USB-C peripherals | Electrodiagnosis | Current ([Cadwell](https://www.cadwell.com/emg-summit/)) |
| UltraPro S100 | Natus | EMG / NCS / EP | — | — | — | — | Electrodiagnosis | Current ([Hospimedica](https://hospimedica.com/expo/product/18385/emg-ncs-ep-neurodiagnostic-system)) |

**Consumer / wearable**

| Device | Company | Type | Channels | Sampling rate | Bits | Connectivity | Typical use | Status/price |
|---|---|---|---|---|---|---|---|---|
| Meta Neural Band | Meta | sEMG wristband | Not published (the research band is 16 ch @ 2 kHz, per [emg2pose](https://arxiv.org/abs/2412.02725)) | — | — | Bluetooth 5.3; 18 h battery; IPX7 | Input for Ray-Ban Display glasses | Shipping since 30 Sep 2025, bundled at $799, US only ([Techpoint](https://techpoint.africa/guide/meta-ray-ban-display-glasses/), [Meta](https://www.meta.com/blog/ces-2026-meta-ray-ban-display-teleprompter-emg-handwriting-garmin-unified-cabin-university-of-utah-tetraski/)) |
| Mudra Band / Mudra Link | Wearable Devices | "Surface Nerve Conductance" (SNC) wristband | — | — | — | Bluetooth (Apple Watch; Link: Android/PC/XR) | Gestures for watch, XR, glasses | Shipping; Band $199 *unverified* ([Wearable Technologies](https://wearable-technologies.com/news/mudra-the-worlds-first-neural-input-wristband)) |
| gForce Pro / Pro+ | OYMotion | sEMG armband | 8 | 1 kHz @ 8-bit or 500 Hz @ 12-bit | 8 / 12 | BLE 4.0 | Research, robotics | Status *unverified* ([Humanoid Guide](https://humanoid.guide/product/gforce-pro/)) |
| Myo | Thalmic Labs | sEMG armband | 8 | 200 Hz | 8 | BLE | Gestures; Ninapro DB5 | Discontinued Oct 2018 ([myo-bluetooth README](https://github.com/thalmiclabs/myo-bluetooth), [specs](https://pmc.ncbi.nlm.nih.gov/articles/PMC10222313)) |

**Prosthetic control**

| Device | Company | Type | Channels | Sampling rate | Bits | Connectivity | Typical use | Status |
|---|---|---|---|---|---|---|---|---|
| Myo Plus TR | Ottobock | Pattern recognition | *unverified* | — | — | Bluetooth | Transradial prosthesis | FDA-cleared Sep 2019 ([Ottobock](https://www.ottobock.com/en-us/b2b-product/13E520)) |
| Complete Control Gen2 | Coapt | Pattern recognition | — | — | — | Bluetooth | Upper-limb prostheses, TMR users | FDA K191083 ([FDA](https://fda.innolitics.com/device/K191083), [GUDID](https://accessgudid.nlm.nih.gov/devices/B618N1)) |
| Phantom X | Phantom Neuro | Minimally invasive implant | — | — | — | — | Prosthesis/robot control | Breakthrough + TAP designations; first-in-human trial NCT07325708 from 2026 ([Hoodline](https://hoodline.com/2026/02/austin-implant-lets-amputees-work-robot-hands-by-sheer-will/)) |
| IMES | Össur / Alfred Mann Foundation | Implanted sensors (5×3 mm) | — | — | — | Wireless | Prosthesis control | Research (first in humans 2014–15) ([ODT](https://www.odtmag.com/contents/view_breaking-news/2019-11-04/ossur-and-amf-extend-exploration-of-mind-controlled-prosthetics/)) |

**Low-cost / DIY**

| Device | Company | Type | Channels | Sampling rate | Bits | Connectivity | Typical use | Price |
|---|---|---|---|---|---|---|---|---|
| Cyton (+Daisy) | OpenBCI | ExG board (ADS1299) | 8 (16 with Daisy) | 250 Hz | 24 | BLE dongle, SD card | EEG/EMG hacking | — ([docs](https://docs.openbci.com/Cyton/CytonSpecs/), [data format](https://docs.openbci.com/Cyton/CytonDataFormat/)) |
| MyoWare 2.0 | SparkFun / Advancer | Analog sensor | 1 (raw, rectified, envelope outputs) | Set by host ADC; 20.8–498.4 Hz band | Analog | Wired to MCU | Maker projects | $42.95 ([SparkFun](https://learn.sparkfun.com/tutorials/getting-started-with-the-myoware-20-muscle-sensor-ecosystem/all)) |
| BITalino (r)evolution | PLUX | Multi-sensor board | 6 analog in | Up to 1000 Hz; EMG 25–480 Hz | 10 (4 ch) / 6 (2 ch) | — | Teaching, prototyping | — ([BITalino paper](https://scitepress.org/Papers/2014/47278/pdf/index.html), [(r)evolution EMG band](https://pmc.ncbi.nlm.nih.gov/articles/PMC6498399)) |
| Shimmer3 ExG | Shimmer | Wearable ECG/EMG | 2 EMG | 125–8000 SPS | — | Bluetooth (RN4678) | Ambulatory research | — ([spec sheet](https://shimmersensing.com/wp-content/docs/support/documentation/Shimmer3_ECG_EMG_Specification_Sheet_Revision_1.7.pdf)) |

## 3. Applications (domains)

| Domain | How EMG is used | Examples | Maturity |
|---|---|---|---|
| Prosthetics control | Residual-limb sEMG drives the hand, wrist or elbow, either directly (2 sites) or by pattern recognition | Ottobock Myo Plus, Coapt Gen2, Open Bionics Hero, Psyonic; TMR surgery creates extra signal sites ([Kuiken 2009](https://pmc.ncbi.nlm.nih.gov/articles/PMC3036162)) | Commercial |
| Implanted myoelectric control | Sensors inside muscle give stable signals | Phantom Neuro, Össur IMES | Clinical trials |
| Rehabilitation, stroke and SCI | EMG-triggered powered orthoses; decoding of spared motor units after injury | Myomo MyoPro (Medicare-covered since Apr 2024, [BusinessWire](https://www.businesswire.com/news/home/20250507851091/en), [HomeCare](https://www.homecaremag.com/news/cms-posts-final-medicare-dmepos-fee-schedule-rate-myopro)); MyoGestic ([Sci. Adv. 2025](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11980827/)) | Commercial / research |
| Clinical neuromuscular diagnosis | Needle EMG plus nerve conduction studies for neuropathy, ALS, myopathy | Natus, Cadwell ([AANEM](https://education.aanem.org/AssetListing/Medical-Student-Nerve-Conduction-Study-Basics-6162/2022-Basics-of-NCS-and-Needle-EMG-Part-1-28668)) | Clinical standard |
| Consumer HCI / AR-VR input | Wrist sEMG decoded into clicks, swipes and handwriting | Meta Neural Band, Mudra Link (works with Rokid, RayNeo, Viture glasses, [press](https://business.minstercommunitypost.com/minstercommunitypost/article/nnwire-2026-3-2-techmediabreaks-wearable-devices-ltd-nasdaq-wlds-to-debut-mudra-experience-studio-at-mwc-barcelona-2026)) | Commercial (early) |
| Silent speech | Face and throat EMG during internal speech, decoded to words | AlterEgo: 92% median word accuracy in 2018 ([MIT](https://www.media.mit.edu/publications/alterego-IUI/)); startup launched Sep 2025 ([Decrypt](https://decrypt.co/338527/near-telepathic-wearable-communicate-silently-devices)) | Research / early commercial |
| Sports science and ergonomics | Activation timing, force estimation, fatigue from the drop in median frequency | Noraxon, Delsys ([review](https://journals.utm.my/jurnalteknologi/article/view/4676)) | Commercial (research tools) |
| Exoskeletons and robot teleoperation | sEMG triggers or scales assistance; EMG-decoded teleoperation | Cyberdyne HAL (FDA-cleared 2017, [Exoskeleton Report](https://exoskeletonreport.com/2017/12/cyberdynes-medical-hal-obtains-fda-marketing-clearance-class-ii-medical-device/)); EMG telemanipulation ([FAU 2023](https://cris.fau.de/publications/332559390)) | Commercial (HAL) / research |
| Gait analysis | Muscle on/off timing across the gait cycle, e.g. cerebral palsy | [Prosser 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2897131); Cometa, Noraxon | Clinical |
| Biofeedback | Shows the patient their own muscle activity to retrain it | Meta-analysis: short-term limb gains after stroke ([PMC10783731](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10783731/)) | Clinical |
| Functional stimulation wearables | EMG sensing plus FES to retrain gait | Cionic Neural Sleeve 2 (FDA-cleared Sep 2025, [Medical Economics](https://www.medicaleconomics.com/view/cionic-s-neural-sleeve-2-wins-fda-clearance-expands-mobility-options-for-neurological-patients)) | Commercial |
| Sleep | Chin EMG atonia for REM scoring and REM behaviour disorder; masseter EMG for bruxism | AASM scoring rules ([RBD review](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8699681/), [bruxism](https://doaj.org/article/471ab39255c6464bafb7e619f47d1e71)) | Clinical standard |
| Emotion / affect | Corrugator (frown) and zygomaticus (smile) facial EMG track valence | [Larsen et al. 2003](https://imotions.com/blog/zygomaticus-major/) | Research |
| Hybrid BCIs | EEG + EMG fusion; cortico-muscular coherence for stroke | [Frontiers 2023](https://www.frontiersin.org/articles/10.3389/fnins.2023.1125230/pdf), [hybrid BCI-FES trial](https://clinicaltrials.gov/study/NCT05511207) | Research |
| Accessibility | Custom gestures for people with limited hand mobility | Meta + University of Utah (TetraSki, smart home), Jan 2026 ([Meta](https://www.meta.com/blog/ces-2026-meta-ray-ban-display-teleprompter-emg-handwriting-garmin-unified-cabin-university-of-utah-tetraski/)) | Research / pilot |
| Gaming | Serious games train prosthesis control; consumer bands control games | [Serious-games review](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8663510/), Mudra ([Nasdaq](https://www.nasdaq.com/articles/wearable-devices-ltd-showcases-award-winning-mudra-link-neural-gesture-control-wristband)) | Research / niche commercial |
| Automotive | Wristband gestures for in-car infotainment | Meta + Garmin proof of concept, CES 2026 ([Meta](https://www.meta.com/blog/ces-2026-meta-ray-ban-display-teleprompter-emg-handwriting-garmin-unified-cabin-university-of-utah-tetraski/)) | Prototype |

## 4. Companies

| Company | Country | Focus | Key product | Status 2025–2026 |
|---|---|---|---|---|
| Meta (CTRL-labs) | US | Consumer wrist sEMG | Neural Band | CTRL-labs bought 2019 for a reported $500M–1B ([SiliconANGLE](https://siliconangle.com/2019/09/23/fb-buys-brain-reading-neural-interface-startup-ctrl-labs-500m-1b/)); shipping since Sep 2025; international rollout paused Jan 2026 ([Meta](https://www.meta.com/blog/ces-2026-meta-ray-ban-display-teleprompter-emg-handwriting-garmin-unified-cabin-university-of-utah-tetraski/)) |
| Wearable Devices Ltd (WLDS) | Israel | Consumer neural wristband | Mudra Band / Link | Mudra Link launched H1 2025 ([Barchart](https://www.barchart.com/story/news/34725716/wearable-devices-nasdaq-wlds-reports-first-half-2025-results-marks-commercial-debut-of-mudra-link)); developer studio at MWC 2026 |
| Thalmic Labs / North | Canada | Consumer armband | Myo | Myo ended 2018; patents sold to CTRL-labs 2019; North acquired by Google Jun 2020 ([CNBC](https://www.cnbc.com/2020/06/30/google-acquires-north-augmented-reality-glasses-start-up.html)) |
| Ottobock | Germany | Prosthetics | Myo Plus | IPO in Frankfurt 9 Oct 2025, about €4.2B market cap at the €66 offer price ([press release](https://app.boersengefluester.de/de/newswire/DE000BCK2223/ottobock-se-co-kgaa/ottobock-celebrates-successful-ipo-in-frankfurt-2211374)); led Phantom Neuro's Series A |
| Össur (Embla Medical) | Iceland | Prosthetics | i-Limb Quantum, IMES research | Parent renamed Embla Medical 2024 ([Össur](https://www.ossur.com/global/about-ossur/newsroom/ossur-establishes-new-parent-organization-embla-medical)) |
| Coapt | US | Pattern-recognition control | Complete Control Gen2 | Hanger agreed to acquire, Feb 2025 ([Hanger](https://corporate.hanger.com/?p=3207)) |
| Psyonic | US | Bionic hand | Ability Hand | Integration with NVIDIA Isaac Lab (Mar 2026) and ABB arms; based in San Diego since 2023 ([Humanoids Daily](https://www.humanoidsdaily.com/feed/from-prosthetics-to-pixels-psyonic-and-nvidia-bridge-the-robotics-data-gap-with-real-to-real-transfer), [Monoist](https://monoist.itmedia.co.jp/mn/articles/2602/06/news052.html), [San Diego Magazine](https://sandiegomagazine.com/partner-content/psyonic-creator-of-the-worlds-most-powerful-bionic-hand-now-calls-san-diego-home/)) |
| Phantom Neuro | US | Implanted EMG interface | Phantom X | $19M Series A (Apr 2025), FDA Breakthrough + TAP; trial from 2026 ([TechCrunch](https://techcrunch.com/2025/04/15/phantom-neuro-grabs-19m-to-help-amputees-gain-control-of-their-phantom-limbs)) |
| Atom Limbs | US | Non-invasive sEMG arm | Atom Touch | 2025–26 FDA/shipping status *unverified* ([Wefunder](https://wefunder.com/feed/168612.md)) |
| Open Bionics | UK | 3D-printed bionic arm | Hero PRO / Hero RGD | Launched 15 Apr 2025 ([Open Bionics](https://openbionics.com/open-bionics-sets-new-benchmark-with-launch-of-hero-rgd-and-hero-pro/)) |
| Cionic | US | EMG + FES sleeve | Neural Sleeve 2 | FDA-cleared Sep 2025 |
| Myomo | US | EMG-powered arm orthosis | MyoPro | 2025 revenue $40.9M, up 26% ([BusinessWire](https://www.businesswire.com/news/home/20260309467133/en)) |
| Cyberdyne | Japan | EMG-driven exoskeleton | HAL | FDA-cleared 2017 |
| AlterEgo | US | Silent speech | AlterEgo wearable | Unveiled Sep 2025 ([Decrypt](https://decrypt.co/338527/near-telepathic-wearable-communicate-silently-devices)) |
| Delsys / OT Bioelettronica / Noraxon / Cometa / BioSemi | US / Italy / US / Italy / Netherlands | Research hardware | See section 2 | Selling |
| OpenBCI | US | Open-source biosignal hardware | Cyton | Selling |

## 5. Patents

| Patent number | Holder | Title/topic | Year | Why it matters |
|---|---|---|---|---|
| [US 10,409,371](https://patents.google.com/patent/US10409371) | CTRL-labs, now Meta | Inferring user intent from neuromuscular signals | Granted 2019 (priority 2016) | Core claim on predicting movement from wristband EMG with ML; inventors include Kaifosh and Reardon |
| [US 11,000,211](https://patents.google.com/patent/US11000211) | Meta | Adaptive system for control signals from neuromuscular activity | 2021 | Adaptive, personalized EMG control |
| [US 10,496,168](https://patents.google.com/patent/US10496168) | CTRL-labs, now Meta | Calibration for hand-state modeling from neuromuscular signals | 2019 | EMG-to-hand-pose calibration (cf. emg2pose) |
| [US 10,937,414](https://patents.google.com/patent/US10937414) | Meta | Text input using neuromuscular information | 2021 | EMG typing and text entry (cf. emg2qwerty) |
| [US 7,596,393](https://patents.google.com/patent/US7596393) | ETRI (Korea), asserted by Perceptix | Wearable phone using wrist EMG to interpret hand motions | 2009 (expires 2028) | Asserted against Meta's Neural Band |
| Myo patent portfolio (numbers not confirmed) | Thalmic/North, then CTRL-labs, then Meta | Armband gesture control | Sold 2019 | Consolidated early consumer-EMG IP at Meta ([BetaKit](https://betakit.com/ctrl-labs-acquires-norths-patents-for-myo-armband-technology/)) |

**Litigation.** On 22 Oct 2025, Perceptix Technologies sued Meta in the US District Court for the Central District of California. The suit claims that Orion, Ray-Ban Display and the Neural Band infringe US 7,596,393 ([Bloomberg Law](https://news.bloomberglaw.com/ip-law/meta-ar-glasses-prompt-patent-suit-over-muscle-signal-technology)). I found no confirmed suit between Wearable Devices and Meta.

## 6. Most-cited papers

These are field-defining works. Citation counts are left out because I could not verify them.

| Paper | Authors | Venue/year | Why it matters |
|---|---|---|---|
| [A new strategy for multifunction myoelectric control](https://scinapse.io/papers/2123167643) | Hudgins, Parker, Scott | IEEE TBME 1993 | Pattern-recognition prosthesis control; the "Hudgins" time-domain features |
| [The use of surface electromyography in biomechanics](https://www.bisp-surf.de/Record/PU199804301575) | De Luca | J. Appl. Biomech. 1997 | Standard reference on sEMG timing, force and fatigue |
| [Development of recommendations for SEMG sensors and sensor placement procedures](https://www.doi.org/10.1016/S1050-6411(00)00027-4) | Hermens, Freriks, Disselhorst-Klug, Rau | J. Electromyogr. Kinesiol. 2000 | SENIAM electrode and placement standard |
| [A robust, real-time control scheme for multifunction myoelectric control](https://scinapse.io/papers/2165619603) | Englehart, Hudgins | IEEE TBME 2003 | Continuous windowed classification, the template for clinical pattern recognition |
| [The extraction of neural strategies from the surface EMG](https://vivo-cub.colorado.edu/display/pubid_11885) | Farina, Merletti, Enoka | J. Appl. Physiol. 2004 | Limits of reading neural drive from sEMG amplitude |
| [Multichannel blind source separation using convolution kernel compensation](https://www.academia.edu/49664588/Multichannel_Blind_Source_Separation_Using_Convolution_Kernel_Compensation) | Holobar, Zazula | IEEE TSP 2007 | Core HD-EMG motor-unit decomposition algorithm |
| [Targeted muscle reinnervation for real-time myoelectric control of multifunction artificial arms](https://pmc.ncbi.nlm.nih.gov/articles/PMC3036162) | Kuiken et al. | JAMA 2009 | Surgery that creates new EMG sites for prosthesis control |
| [Filtering the surface EMG signal: movement artifact and baseline noise contamination](https://www.bu.edu/nmrc/files/2010/06/103.pdf) | De Luca, Gilmore, Kuznetsov, Roy | J. Biomech. 2010 | The 20 Hz high-pass recommendation |
| [Feature reduction and selection for EMG signal classification](https://doi.org/10.1016/j.eswa.2012.01.102) | Phinyomark, Phukpattaranont, Limsakul | Expert Syst. Appl. 2012 | Standard EMG feature comparison |
| [Electromyography data for non-invasive naturally-controlled robotic hand prostheses](https://pmc.ncbi.nlm.nih.gov/articles/PMC4421935) | Atzori et al. | Scientific Data 2014 | Ninapro, the field's main benchmark |
| [The extraction of neural information from the surface EMG for the control of upper-limb prostheses](https://ieeexplore.ieee.org/document/6737308) | Farina, Jiang, Rehbaum, Holobar, Graimann, Dietl, Aszmann | IEEE TNSRE 2014 | Why academic decoders had not reached commercial prostheses |
| [Deep learning for electromyographic hand gesture signal classification using transfer learning](https://arxiv.org/abs/1801.07756v3) | Côté-Allard et al. | IEEE TNSRE 2019 | Early cross-user deep learning for EMG |

## 7. New achievements (2023–2026)

- **A generic wrist interface.** Kaifosh, Reardon et al. (*Nature*, 2025) trained on data from thousands of people. New users get, without calibration, 0.66 target acquisitions/s, 0.88 gesture detections/s and 20.9 words per minute of handwriting. Personalizing the handwriting model adds 16% ([paper](https://ideas.repec.org/a/nat/nature/v645y2025i8081d10.1038_s41586-025-09255-w.html)).
- **It shipped.** The Neural Band went on sale 30 Sep 2025, and neural handwriting entered early access in January 2026 ([Meta](https://www.meta.com/blog/ces-2026-meta-ray-ban-display-teleprompter-emg-handwriting-garmin-unified-cabin-university-of-utah-tetraski/)).
- **Typing from EMG (emg2qwerty, NeurIPS 2024).** The generic model's character error rate (CER) is 51.8% with a language model; a personalized model gets 6.95%; the best user reaches 3.16% ([arXiv](https://arxiv.org/html/2410.20081v1)).
- **Hand pose from EMG (emg2pose, NeurIPS 2024).** The best model's error is 12.2° and 15.8 mm on unseen users ([arXiv](https://arxiv.org/html/2412.02725v1)).
- **Scaling.** Transformers grow to 110M parameters, then distill 50x smaller while losing less than 1.5 points ([TMLR 2025](https://arxiv.org/abs/2507.22094)). TinyMyo (3.6M parameters) gets 89.4% on Ninapro DB5 and runs on a GAP9 microcontroller at about 57 mW ([arXiv](https://arxiv.org/pdf/2512.15729v2)).
- **Decomposition.** Swarm-Contrastive Decomposition finds about 26 motor units versus about 14 for the baseline ([J. Physiol. 2025](https://research.chalmers.se/en/publication/545684)).
- **Clinical HD-EMG.** MyoGestic gives 7 people with spinal cord injury (including spinal stroke) or amputation working control within minutes ([Sci. Adv. 2025](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11980827/)).
- **Market signals.** Coapt went to Hanger, Ottobock had its IPO, Phantom Neuro got FDA Breakthrough designation, Cionic's Neural Sleeve 2 was cleared, and Myomo grew 26% (section 4).

## 8. Current state of the field

**Where EMG is used today, and where it is still research**

| Maturity | Applications |
|---|---|
| Established clinical | Needle EMG/NCS diagnosis, PSG sleep scoring, gait labs, biofeedback |
| Commercial, growing | Myoelectric prostheses with pattern recognition, EMG orthoses (MyoPro), consumer wristbands (Neural Band, Mudra) |
| Trials / early | Implanted EMG (Phantom X), silent speech (AlterEgo), accessibility pilots |
| Research | Cross-user foundation models, motor-unit-level interfaces, hybrid EEG+EMG BCIs, emotion sensing, automotive |

**Open problems**
- **Generalizing across people and sessions.** On emg2qwerty, the generic model's error (~52% CER) is far above the personalized one (~7%). EMGBench measures this out-of-distribution gap across 9 datasets ([EMGBench](https://arxiv.org/pdf/2410.23625)).
- **Robustness.** Electrode shift, posture, sweat and fatigue all degrade decoders; emg2pose error rises from 12.2° to 15.2° on unseen task stages.
- **Clinical data is scarce.** The big datasets come from able-bodied wrist wearers, while amputee data stays small (Ninapro DB3 has 11 amputees). Farina et al. 2014 noted that academic decoders rarely reach commercial prostheses.
- **Running on the device.** Models must fit milliwatt microcontrollers with low latency.
- **IP and licensing.** Meta's patent portfolio and the Perceptix suit affect commercial freedom to operate. Meta's datasets are CC-BY-NC.

**Where an AI engineer can contribute.** Self-supervised pretraining across heterogeneous datasets. Domain adaptation and few-shot personalization. Sequence models (CTC, language-model fusion) for typing and handwriting. Pose regression with velocity targets. Distillation and quantization for wearables. Learned motor-unit decomposition. Honest benchmarks on held-out users. The datasets below are a good starting point.

## 9. Public datasets

Full specifications for each dataset, and tables of published results on them, are in [DATASETS.md](DATASETS.md).

| Dataset | Content | Size | Link |
|---|---|---|---|
| Ninapro DB1–DB10 | Hand gestures, sEMG + kinematics/force; includes amputees | DB2: 40 subjects, 49 movements, 12 Delsys at 2 kHz; DB9: 77 subjects (hand kinematics only, no EMG) | [ninapro.hevs.ch](https://ninapro.hevs.ch/) |
| emg2qwerty | Wrist sEMG during touch typing | 108 users, 1,135 sessions, 346 h | [arXiv](https://arxiv.org/abs/2410.20081) |
| emg2pose | Wrist sEMG + 26-camera hand pose | 193 users, 370 h, 16 ch @ 2 kHz | [arXiv](https://arxiv.org/abs/2412.02725) |
| Meta Generic Neuromotor Interface | Discrete gestures, handwriting, wrist | 100 participants; about 64 h / 141 h / 77 h; CC-BY-NC | [GitHub](https://github.com/facebookresearch/generic-neuromotor-interface) |
| Hyser | HD-sEMG, 34 gestures + finger forces | 20 subjects × 2 days, 256 ch @ 2048 Hz, 142.8 GB | [PhysioNet](https://physionet.org/content/hd-semg/) |
| GRABMyo | Forearm + wrist sEMG, 16 gestures, 3 days | 43 subjects, 28 used ch @ 2048 Hz, 9.4 GB | [PhysioNet](https://physionet.org/content/grabmyo/1.1.0/) |
| EMG-EPN-612 | Myo armband, 5 gestures + rest | 612 users (306 train / 306 test) | [Zenodo](https://zenodo.org/record/4023305) |
| EMGBench | Cross-subject benchmark over 9 datasets + new HD-EMG set | 9 datasets | [emgbench.github.io / arXiv](https://arxiv.org/pdf/2410.23625) |

## 10. GitHub repositories

Stars and dates checked via the GitHub API on 2026-10-10.

"Custom" means GitHub could not detect a standard license (`NOASSERTION`), so read the repo's LICENSE file before reusing the code. "—" means no license file or no detected language.

**Toolkits and libraries**

| Repo | What it does / when to use it | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [libemg/libemg](https://github.com/libemg/libemg) | API for building real-time EMG interactions and running offline analysis (from the Scheme/Phinyomark group). Start here for gesture-control prototypes | Python | 80 | 2026-10 | MIT |
| [neuropsychology/NeuroKit](https://github.com/neuropsychology/NeuroKit) | NeuroKit2: general physiological signal toolbox with EMG cleaning, amplitude and activation detection, alongside ECG/EOG/EDA | Python | 2392 | 2026-10 | MIT |
| [scientisst/BioSPPy](https://github.com/scientisst/BioSPPy) | Biosignal processing (EMG onset detection, filtering). Maintained fork of the original, now archived [PIA-Group/BioSPPy](https://github.com/PIA-Group/BioSPPy) (645 stars) | Python | 124 | 2026-09 | Custom |
| [pluxbiosignals/biosignalsnotebooks](https://github.com/pluxbiosignals/biosignalsnotebooks) | Tutorial notebooks and helpers for EMG/ECG processing, built around PLUX/BITalino hardware | Jupyter Notebook | 95 | 2026-05 | MIT |
| [aalhossary/pyemgpipeline](https://github.com/aalhossary/pyemgpipeline) | Classic biomechanics EMG pipeline: DC removal, band-pass, rectification, envelope, amplitude normalization | Python | 12 | 2022-04 | GPL-3.0 |
| [GiacomoValliPhD/openhdemg](https://github.com/GiacomoValliPhD/openhdemg) | Analysis of HD-sEMG and decomposed motor units (firing properties, MU tracking across sessions) | Python | 67 | 2026-10 | BSD-3-Clause |
| [simonavrillon/MUedit](https://github.com/simonavrillon/MUedit) | App to decompose HD-EMG into motor units and manually edit the pulse trains | MATLAB | 52 | 2026-04 | GPL-3.0 |
| [The-Motor-Unit/EMGdecomPy](https://github.com/The-Motor-Unit/EMGdecomPy) | Python package for blind-source-separation decomposition of multichannel EMG into motor units | Jupyter Notebook | 33 | 2022-06 | GPL-3.0 |
| [neuromechanist/emg2mu](https://github.com/neuromechanist/emg2mu) | GPU-accelerated (PyTorch) HD-EMG motor-unit decomposition | Jupyter Notebook | 17 | 2025-02 | Custom |
| [CEINMS/CEINMS](https://github.com/CEINMS/CEINMS) | Calibrated EMG-informed neuromusculoskeletal modelling: estimates muscle forces and joint moments from EMG with OpenSim models | C++ | 33 | 2026-08 | Apache-2.0 |

**Models and papers with code**

| Repo | What it does / when to use it | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [facebookresearch/emg2qwerty](https://github.com/facebookresearch/emg2qwerty) | Official emg2qwerty dataset and CTC typing baselines (NeurIPS 2024). Archived, so no further updates | Python | 142 | 2025-06 | Custom, archived |
| [facebookresearch/emg2pose](https://github.com/facebookresearch/emg2pose) | Official emg2pose dataset and pose-regression baselines (vemg2pose, NeuroPose) | Python | 281 | 2024-12 | Custom |
| [facebookresearch/generic-neuromotor-interface](https://github.com/facebookresearch/generic-neuromotor-interface) | Data and training code for Meta's Nature 2025 wristband paper (discrete gestures, handwriting, wrist) | Jupyter Notebook | 266 | 2025-08 | Custom (data CC-BY-NC-4.0) |
| [pulp-bio/BioFoundation](https://github.com/pulp-bio/BioFoundation) | Biosignal foundation models, including TinyMyo (3.6M-parameter sEMG transformer, arXiv 2512.15729) | Python | 142 | 2026-09 | Apache-2.0 |
| [UlysseCoteAllard/MyoArmbandDataset](https://github.com/UlysseCoteAllard/MyoArmbandDataset) | Dataset and code for Côté-Allard et al. 2019 transfer-learning paper (Myo armband). Older Theano stack | Python (GitHub detects "OpenEdge ABL") | 98 | 2022-02 | GPL-3.0 |
| [NsquaredLab/MyoGestic](https://github.com/NsquaredLab/MyoGestic) | Official MyoGestic framework (Sci. Adv. 2025) for training and testing real-time myocontrol decoders | Python | 32 | 2026-08 | GPL-3.0 |

**Benchmarks and dataset loaders**

| Repo | What it does / when to use it | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [jehanyang/emgbench](https://github.com/jehanyang/emgbench) | Official EMGBench (NeurIPS 2024): cross-subject generalization and adaptation benchmark over 9 datasets | Python | 24 | 2025-09 | MIT |
| [Lif3line/nina_helper_package_mk2](https://github.com/Lif3line/nina_helper_package_mk2) | Helpers for loading and windowing Ninapro DB1/DB2 | Python | 21 | 2022-12 | MIT |
| [Zeng-Jia/Ninapro-dataset-processing](https://github.com/Zeng-Jia/Ninapro-dataset-processing) | Ninapro preprocessing flow plus a PyTorch dataloader | Jupyter Notebook | 35 | 2021-09 | — |

**Hardware and firmware**

| Repo | What it does / when to use it | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [brainflow-dev/brainflow](https://github.com/brainflow-dev/brainflow) | Device-agnostic API to stream EEG/EMG/ECG from many boards (OpenBCI and others), with bindings for many languages | C++ | 1770 | 2026-10 | Custom |
| [OpenBCI/OpenBCI_GUI](https://github.com/OpenBCI/OpenBCI_GUI) | Desktop app for Cyton/Ganglion, including an EMG widget | HTML | 965 | 2026-04 | MIT |
| [OpenBCI/OpenBCI_Cyton_Library](https://github.com/OpenBCI/OpenBCI_Cyton_Library) | Firmware libraries for the Cyton (ADS1299) board | C++ | 126 | 2025-07 | MIT |
| [PerlinWarp/pyomyo](https://github.com/PerlinWarp/pyomyo) | Python driver for the discontinued Myo armband, giving raw 200 Hz EMG without the official SDK | Python | 189 | 2026-07 | MIT |
| [thalmiclabs/myo-bluetooth](https://github.com/thalmiclabs/myo-bluetooth) | Official BLE protocol specification for the Myo | C | 145 | 2020-09 | Apache-2.0, archived |
| [AdvancerTechnologies/MyoWare_v1_MuscleSensor](https://github.com/AdvancerTechnologies/MyoWare_v1_MuscleSensor) | Example code and docs for the MyoWare 1.0 sensor. Old; no MyoWare 2.0 repo found | Processing | 93 | 2016-07 | Apache-2.0 |
| [OpenBionics/Prosthetic-Hands](https://github.com/OpenBionics/Prosthetic-Hands) | Open-source low-cost (<$200) 3D-printable prosthetic hand designs from the academic OpenBionics initiative (not the UK company Open Bionics) | TeX | 189 | 2018-02 | Custom |
| [grablab/openhand-hardware](https://github.com/grablab/openhand-hardware) | Yale OpenHand CAD designs. A robot-hand platform, useful as an EMG-teleoperation target | Python | 237 | 2025-03 | Custom |

**Curated lists**

| Repo | What it does / when to use it | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [x-labs-xyz/awesome-emg-data](https://github.com/x-labs-xyz/awesome-emg-data) | List of public raw-EMG datasets with their papers. A good way to find data beyond section 9 | — | 102 | 2024-02 | — |
