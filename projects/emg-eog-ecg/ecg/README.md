# ECG (Electrocardiography)

ECG records the heart's electrical activity from electrodes on the skin. It is one of the most common medical tests. Most use today falls into three groups: hospital 12-lead machines for diagnosis, patches and Holters worn for days to catch arrhythmias, and smartwatches that check for atrial fibrillation (AF). AI now reads ECGs for conditions a cardiologist cannot see on the trace, and several of these tools have FDA clearance ([Anumana LEF](https://www.biospace.com/anumana-receives-u-s-fda-510-k-clearance-for-ecg-ai-algorithm-to-detect-low-ejection-fraction), [Anumana amyloidosis](https://www.dicardiology.com/content/anumana-receives-fda-clearance-ecg-ai-cardiac-amyloidosis-algorithm-using-standard-12-lead), [Tempus ECG-Low EF and ECG-AF](https://investors.tempus.com/news-releases/news-release-details/tempus-receives-us-fda-510k-clearance-tempus-ecg-low-ef-software)).

Reading the tables: *n/s* means no source was found for that value, and *unverified* means a value was seen but could not be confirmed.

## 1. The data

**What it measures.** Each heartbeat is a wave of depolarization (cells firing) and repolarization (cells recovering). Electrodes on the skin pick up the voltage this produces. The **P wave** is atrial depolarization, the **QRS complex** is ventricular depolarization, and the **T wave** is ventricular repolarization. Clinicians measure the PR, QRS, QT and RR intervals. The RR interval is the time between beats; heart rate and HRV are derived from it.

**Lead systems.**
- **12-lead**: 10 electrodes give 12 views of the heart. This is the diagnostic standard.
- **3/5-lead**: used for bedside and ICU monitoring.
- **Holter**: usually 3 channels, worn for 1–7 days ([Philips DigiTrak XT](https://www.documents.philips.com/assets/20181128/e4b717caff5245278b96a9a60143a6c8.pdf)).
- **Patch**: a single channel worn for up to 14 days ([Zio XT manual](https://go.irhythmtech.com/hubfs/Instructions%20for%20Use%20(IFUs)/US/N100A4010.06%20ZIO%20XT%20CLINICAL%20REFERENCE%20MANUAL.pdf)).
- **Single-lead "Lead I"**: you touch a watch or card with both hands for 30 s ([Apple IFU](https://www.apple.com/legal/ifu/ecg/ecg-ifu-1-en_US.pdf)).

| Characteristic | Typical value | Source |
|---|---|---|
| Amplitude | A few mV. Devices are built for a ±10 mV differential input (GE MAC 5500) or ±1.65 mV (Zio XT). Electrode DC offsets reach ±300 mV. | [GE MAC 5500 via reseller](https://www.somatechnology.com/ekg-machines/ge-mac-5500), [Zio XT](https://go.irhythmtech.com/hubfs/Instructions%20for%20Use%20(IFUs)/US/N100A4010.06%20ZIO%20XT%20CLINICAL%20REFERENCE%20MANUAL.pdf), [AD8232](https://www.radiolocman.com/datasheet/data.html?di=523629) |
| Diagnostic bandwidth | 0.05–150 Hz (AHA). At least 250 Hz is recommended for children. | [Rijnbeek 2001, Circulation](https://repub.eur.nl/pub/9806/11748105.pdf) |
| Monitoring bandwidth | About 0.5–40 Hz (KardiaMobile 6L, Movesense under IEC 60601-2-47). Zio XT uses 0.5–30 Hz. | [KardiaMobile 6L](https://fda.innolitics.com/device/K210753), [Movesense](https://www.movesense.com/wp-content/uploads/2020/12/Movesense-Medical-Spec-Sheet-2020-12-v1.0.pdf) |
| Sampling rate | AHA minimum is 500 Hz for diagnostic ECG (*unverified*; Rijnbeek derives 500 Hz from a 250 Hz pediatric bandwidth). Wearables use 130–512 Hz. | [Rijnbeek 2001](https://repub.eur.nl/pub/9806/11748105.pdf), Section 2 |
| Electrodes | Wet Ag/AgCl gel electrodes are the gold standard. Dry electrodes (metal, polymer, textile) are used in wearables. | [Arrow](https://arrow.com/en/research-and-events/articles/cardiac-monitoring-ecg-electrodes) |
| Noise | Baseline wander (below ~0.5 Hz, from breathing and movement), powerline (50/60 Hz), electrode motion, muscle (EMG) | [Denoising review](https://arxiv.org/abs/2108.08376v1), [GE HealthCare](https://www.gehealthcare.com/en-gb/insights/article/a-guide-to-ecg-signal-filtering) |

**Derived signals.** The main derived signals are heart rate and heart-rate variability (HRV). HRV time-domain measures include SDNN and RMSSD. Frequency-domain measures include the LF and HF power bands. Definitions follow the [Task Force 1996](https://pubmed.ncbi.nlm.nih.gov/8598068/). Norms for 24-h, 5-min and shorter recordings are not interchangeable ([Shaffer & Ginsberg 2017](https://www.frontiersin.org/journals/public-health/articles/10.3389/fpubh.2017.00258)).

**Formats.**
- **WFDB**: PhysioNet's format ([PhysioNet](https://www.physionet.org/content/ptb-xl/1.0.3/)).
- **SCP-ECG** (EN 1064) and **DICOM waveform**: used for resting ECGs and hospital systems ([CinC 2006](https://www.cinc.org/archives/2006/pdf/0413.pdf)).
- **HL7 aECG**: XML, required for FDA QT submissions ([FDA](https://www.fda.gov/media/150173/download)).
- **EDF**: common in sleep studies. *I did not check a separate source for this.*

## 2. Devices and specifications

**Clinical 12-lead**

| Device | Company | Type | Leads/ch | Sampling rate | Resolution | Duration | Connectivity | Regulatory | Typical use |
|---|---|---|---|---|---|---|---|---|---|
| [MAC 5500](https://www.somatechnology.com/ekg-machines/ge-mac-5500) | GE HealthCare | Resting cart | 12 | 4,000 sps/ch acquisition, 500 sps analysis | 1.22 µV/LSB @ 500 sps (4.88 @ 250 sps) | n/s | n/s | n/s | Hospital ECG |
| [MAC 2000](https://www.somatechnology.com/blog/products/ge-mac-2000/) | GE HealthCare | Resting cart | 12 | 16,000 sps/ch acquisition, 500/1000 analysis | 4.88 µV/LSB | n/s | n/s | n/s | Clinic ECG |
| [PageWriter TC50](https://www.somatechnology.com/ekg-machines/philips-pagewriter-tc50) | Philips | Resting cart | 12 | n/s | 5 µV | n/s | n/s | n/s | Hospital ECG |
| [CARDIOVIT FT-1](https://schillerindia.com/product/cardiovit-ft-1/) | Schiller | Portable cart | 12 | 32,000 Hz | n/s | Stores 350 ECGs | HL7/DICOM (optional) | n/s | Portable ECG |
| [Cardiofax S 1250A](https://mesm.resonantclinical.com/products/ecgs/nihon-kohden-cardiofax-s-1250a/) | Nihon Kohden | Resting cart | 12 | 8,000 acquisition, 500 analysis | n/s | n/s | n/s | n/s | Hospital ECG |

The GE and Philips specs come from reseller pages, not manufacturer datasheets.

**Ambulatory and patch**

| Device | Company | Type | Leads/ch | Sampling rate | Resolution | Duration | Connectivity | Regulatory | Typical use |
|---|---|---|---|---|---|---|---|---|---|
| [Zio XT](https://go.irhythmtech.com/hubfs/Instructions%20for%20Use%20(IFUs)/US/N100A4010.06%20ZIO%20XT%20CLINICAL%20REFERENCE%20MANUAL.pdf) | iRhythm | Patch | 1 | 200 Hz | 10-bit | Up to 14 days | None (mailed back for analysis) | FDA, prescription only | Arrhythmia diagnosis |
| [Zio AT](https://irhythmtech.gcs-web.com/news-releases/news-release-details/irhythm-technologies-receives-fda-510k-clearance-design-updates) | iRhythm | Patch (mobile telemetry) | n/s | n/s | n/s | n/s | Transmits data | FDA 510(k), Oct 2024 | Near-real-time monitoring |
| [CAM](https://www.biospace.com/bardy-diagnostics-announces-commercial-launch-of-the-14-day-carnation-ambulatory-monitor-cam-patch) | Bardy (Baxter) | Sternal patch focused on P waves | n/s | n/s | n/s | 2, 7 or 14 days | n/s | FDA (14-day version, 2019) | Arrhythmia diagnosis |
| [ePatch](https://www.gobio.com/wp-content/uploads/2024/03/ePatch-Brochure-NEW-MAR2023-220-0730-01-Rev.-H-3.13.24-PAL-410704-approved93.pdf) | Philips / BioTelemetry | Patch | 1 (or 3 with lead wires) | n/s | n/s | 14 days (3–5 days with lead wires) | n/s | n/s | Extended Holter |
| [DigiTrak XT](https://www.documents.philips.com/assets/20181128/e4b717caff5245278b96a9a60143a6c8.pdf) | Philips | Holter | 3 | 175 sps | 10-bit | 24 h to 7 days | USB dock | n/s | Holter monitoring |

**Consumer and wearable**

| Device | Company | Type | Leads/ch | Sampling rate | Resolution | Duration | Connectivity | Regulatory | Typical use |
|---|---|---|---|---|---|---|---|---|---|
| [Apple Watch ECG](https://fda.innolitics.com/device/DEN180044) | Apple | Watch | 1 (Lead I) | 512 Hz ([Data in Brief 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC12855598/)) | n/s | 30 s | iPhone | FDA De Novo 2018, over the counter | AF check |
| [Galaxy Watch ECG](https://fda.innolitics.com/device/K201168) | Samsung | Watch | 1 | 500 Hz ([Samsung dev](https://developer.samsung.com/health/sensor/sample/ecg-monitor.html)) | n/s | 30 s | Phone | FDA K201168 (2020); IHRN K230292 | AF check |
| [ScanWatch 2](https://support.withings.com/hc/en-us/articles/16780197080209-ScanWatch-2-ECG-Frequently-Asked-Questions-FAQ-U-S-Only) | Withings | Watch | 1 | n/s | n/s | 30 s ([product sheet](https://media.withings.com/press/product-sheets/Product_sheet_SW_RG_EN.pdf)) | Phone | FDA, over the counter | AF check |
| [BPM Core](https://support.withings.com/hc/en-us/articles/360014212353-BPM-Core-Frequently-asked-questions) | Withings | Blood-pressure cuff with ECG and stethoscope | 1 | n/s | n/s | n/s | Phone | CE; FDA status *unverified* | Home cardio check |
| [Fitbit Sense ECG](https://blog.google/products/fitbit/fitbit-sense-ecg/) | Google / Fitbit | Watch | 1 | n/s | n/s | 30 s | Phone | FDA 510(k) and CE, 2020 | AF check |
| [KardiaMobile 6L](https://fda.innolitics.com/device/K210753) | AliveCor | Handheld | 6 leads | 300 Hz | 16-bit | 30 s to 5 min | Phone | FDA | Home and clinic AF/QT |
| [Kardia 12L](https://cdn.alivecor.com/ifus/k12l/27LB07_k12l.pdf) | AliveCor | Handheld, 5 electrodes | 4 measured channels (12 leads synthesized) | 750 Hz | 22-bit data (24-bit ADC) | About 10 s | Bluetooth 5.1 | FDA, 39 AI findings | Point-of-care 12-lead |
| [HeartBeam](https://www.dicardiology.com/content/heartbeam-earns-fda-clearance-12-lead-synthesis-software) | HeartBeam | Cable-free card that synthesizes 12 leads | 3D vector | n/s | n/s | n/s | Phone | FDA 510(k), Dec 2025 | Home arrhythmia assessment |
| [Polar H10](https://github.com/polarofficial/polar-ble-sdk/blob/master/documentation/products/PolarH10.md) | Polar | Chest strap | 1 | 130 Hz | n/s | Continuous | BLE | Not a medical device | Sports, HRV research |
| [Movesense MD](https://www.movesense.com/wp-content/uploads/2020/12/Movesense-Medical-Spec-Sheet-2020-12-v1.0.pdf) | Movesense | Chest strap/patch | 1 | 128/256/512 Hz | 15-bit | Logging to memory | BLE | CE Class IIa | Remote monitoring, research |

**Research**

| Device | Company | Type | Leads/ch | Sampling rate | Resolution | Duration | Connectivity | Regulatory | Typical use |
|---|---|---|---|---|---|---|---|---|---|
| [ECG100C + MP160](https://imotions.com/de/products/hardware/biopac-ecg100c/) | BIOPAC | Lab amplifier | Up to 16 system channels | Up to 400 kHz aggregate ([BIOPAC](https://www.biopac.com/application-note/mp-system-data-sampling-reference/)) | n/s | Lab sessions | Wired | Research use | Psychophysiology |
| [PowerLab + Bio Amp](https://www.adinstruments.com/products/powerlab/details) | ADInstruments | Lab DAQ | Varies by model | Up to 100 kS/s | 16-bit | Lab sessions | USB | Research use | Physiology labs |
| [Shimmer3 ECG](https://shimmersensing.com/wp-content/docs/support/documentation/Shimmer3_ECG_EMG_Specification_Sheet_Revision_1.7.pdf) | Shimmer | Wearable | 4 ch (5-wire) | 125–8,000 SPS | 24-bit (ADS1292R; [user guide](https://shimmersensing.com/wp-content/docs/support/documentation/ECG_User_Guide_Rev1.12.pdf)) | microSD (8 GB) | Bluetooth | n/s | Ambulatory research |
| [BITalino ECG](https://www.pluxbiosignals.com/products/electrocardiography-ecg-sensor) | PLUX | DIY/education kit | 1 | 1/10/100/1000 Hz | 10-bit | Streaming | Bluetooth | Not medical | Teaching, prototyping |

**Low-cost and DIY**

| Device | Company | Type | Leads/ch | Sampling rate | Resolution | Duration | Connectivity | Regulatory | Typical use |
|---|---|---|---|---|---|---|---|---|---|
| [AD8232](https://www.radiolocman.com/datasheet/data.html?di=523629) | Analog Devices | Analog front-end chip | 1 | Set by your own ADC | Set by your own ADC | n/a | n/a | Not medical | Hobby heart-rate boards |
| [Cyton](https://shop.openbci.com/products/cyton-biosensing-board-8-channel) | OpenBCI | ADS1299 board | 8 | 250 Hz | 24-bit | Streaming | RF dongle | Not medical | EEG+ECG research ([ECG setup](https://docs.openbci.com/GettingStarted/Biosensing-Setups/ECGSetup/)) |

## 3. Applications (domains)

| Domain | How ECG is used | Examples | Maturity |
|---|---|---|---|
| AF detection and screening | 30-s Lead I checks. PPG alerts followed by a confirming ECG. | Apple Heart Study (419,297 people, 0.52% notified) ([NEJM summary](https://www.healio.com/news/cardiology/20191113/apple-heart-study-publication-offers-further-insights-on-af-detection-from-wearables)); Apple, Samsung, Withings, Kardia | Commercial |
| MI and ischemia | 12-lead ST/T analysis; reduced-lead AI | Kardia 12L detects acute MI from a reduced lead set ([AliveCor](https://alivecor.com/press/press_release/alivecor-launches-kardia-12l-a-first-of-its-kind-ai-powered-12-lead-ecg-system)) | Clinical |
| AI-ECG for hidden disease | A neural net on a normal-looking 12-lead ECG predicts low EF, amyloidosis, potassium, age/sex or mortality | Anumana LEF (AUROC 0.932) and amyloidosis (2026); hyperkalemia AUC 0.853–0.883 ([Galloway 2019](https://mayoclinic.elsevierpure.com/en/publications/development-and-validation-of-a-deep-learning-model-to-screen-for)); sex AUC 0.97 and age MAE 6.9 y ([Attia 2019](https://pubmed.ncbi.nlm.nih.gov/31450977/)) | Clinical (LEF, amyloidosis); others in research or Breakthrough designation |
| Remote and ambulatory | 1–14-day Holters and patches; mobile cardiac telemetry | Zio, CAM, ePatch; BioTelemetry serves more than 1M patients a year ([Philips](https://www.philips.com/a-w/about/news/archive/standard/news/press/2021/20210209-philips-completes-the-acquisition-of-biotelemetry-inc.html)) | Commercial |
| ICU and perioperative | Continuous 3/5-lead arrhythmia alarms; false-alarm rates up to 86% reported | PhysioNet 2015 false-alarm challenge ([PhysioNet](https://physionet.org/content/challenge-2015/)) | Clinical; alarm AI is research |
| Drug safety (QT) | Annotated ECGs used to assess QT prolongation under ICH E14 | FDA warehouse of ~6.1M ECGs and 250+ thorough QT studies, as of 2012 ([AMPS](https://www.amps-llc.com/uploads/2017-12-7/AMPS-QT_1q12.pdf)) | Regulatory standard |
| Sports and fitness | Chest straps stream heart rate and RR intervals | Polar H10, Movesense | Commercial |
| Sleep | ECG is a polysomnography (PSG) channel; apnea can be detected from ECG alone | Apnea-ECG: 85–93% per-minute accuracy ([PhysioNet](https://physionet.org/content/challenge-2000/1.0.0/)); PhysioNet 2026 uses PSG ECG ([PhysioNet](https://physionet.org/news/post/moody-challenge-2026/)) | Research to clinical |
| Stress, workload, emotion (passive BCI) | HRV features or raw ECG fed to classifiers, often fused with EEG | HRV findings for pilot workload are inconsistent ([review](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11207491/)); WESAD dataset | Research |
| Driver monitoring | Steering-wheel or seat (capacitive) ECG used to detect drowsiness | CardioWheel ([summary](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12845553/)); textile seat ECG F1 69.7%, rising to 78.2% when fused with vehicle data ([ÉTS thesis 2025](https://espace.etsmtl.ca/id/eprint/3652/1/Renaud-Dumoulin_Geordi-Gabriel.pdf)) | Research and prototypes |
| Biometrics | The ECG waveform used as an identity credential | Nymi band ([TechCrunch](https://techcrunch.com/2014/09/24/bionym-raises-14m-series-a-for-its-heartbeat-authentication-wristband/)); survey ([Sensors 2025](https://oa.upm.es/95017/)) | Niche commercial and research |
| Fetal ECG | Fetal ECG extracted from abdominal leads | PhysioNet 2013 challenge (4-channel, 1 kHz) ([PhysioNet](https://moody-challenge.physionet.org/2013)) | Research |
| Population screening and insurance | Mass single-lead AF screening | STROKESTOP (28,768 people aged 75–76; HR 0.96) ([TCTMD](https://www.tctmd.com/news/strokestop-small-clinical-benefit-seen-systematic-af-screening)); use by insurers *unverified* | Trials |
| Brain–heart and EEG artifacts | Heartbeat-evoked potentials; removing the cardiac field artifact from EEG | Methods review of 132 studies ([bioRxiv 2025](https://www.biorxiv.org/content/10.1101/2025.08.08.668923.full.pdf)); deep-learning removal ([SPMB 2025](https://isip.piconepress.com/conferences/ieee_spmb/2025/papers/10_spmb_l03_05.pdf)) | Research |

## 4. Companies

Countries are as commonly reported; I did not check each against a separate source.

| Company | Country | Focus | Key product | Status 2025–2026 |
|---|---|---|---|---|
| Apple | US | Watch ECG and PPG | ECG app, IRN | Hypertension notification (PPG) cleared Sep 2025 ([Engadget](https://engadget.com/wearables/apple-watch-series-11-receives-fda-clearance-for-hypertension-alerts-120046138.html)); won AliveCor appeals |
| AliveCor | US | Personal and point-of-care ECG with AI | Kardia 6L, Kardia 12L | 39 cleared findings, Jan 2026 ([BioSpace](https://www.biospace.com/press-releases/alivecor-announces-fda-clearance-of-new-cardiac-determinations-for-kardia-12l-ecg-system-bringing-total-to-39)) |
| Samsung | South Korea | Watch ECG | Galaxy Watch | LVSD (heart-failure) AI approved in Korea only ([Android Authority](https://www.androidauthority.com/samsung-galaxy-watch-lvsd-ecg-3602963), [SamMobile](https://www.sammobile.com/news/samsung-bringing-potentially-life-saving-feature-galaxy-watches/)) |
| Withings | France | Consumer medical devices | ScanWatch 2, BPM Core | ECG cleared for over-the-counter use in the US ([Withings](https://support.withings.com/hc/en-us/articles/16780197080209-ScanWatch-2-ECG-Frequently-Asked-Questions-FAQ-U-S-Only)) |
| iRhythm | US | Patches and AI services | Zio monitor/XT/AT | Zio MCT 510(k) submitted Q3 2025, not cleared as of Jan 2026 ([SEC](https://www.sec.gov/Archives/edgar/data/1388658/000110465926002755/tm262849d1_ex99-2.htm)); third-generation algorithm cleared ([SEC Q2 2026](https://www.sec.gov/Archives/edgar/data/0001388658/000138865826000070/irtcq22026ex991pressrelease.htm)); Baxter patent settlement 31 Jul 2026 ([10-Q](https://www.sec.gov/Archives/edgar/data/0001388658/000138865826000072/irtc-20260630.htm)) |
| Anumana | US | 12-lead AI-ECG (Mayo-licensed) | ECG-AI LEF, amyloidosis | Amyloidosis cleared Apr 2026; on the Philips AI Marketplace ([Philips](https://www.usa.philips.com/about/news-and-insights/press-release/philips-launches-ecg-ai-marketplace-to-enhance-early-cardiac-diagnosis)) |
| Eko | US | Stethoscope with ECG | Low EF AI | Cleared 2024; no clearances found for 2025–26 ([Eko](https://www.ekohealth.com/blogs/newsroom/fda-clears-low-ejection-fraction-ai)) |
| HeartBeam | US | Synthesized 12-lead ECG | HeartBeam system | Cleared Dec 2025 after appeal; limited launch in 2026 |
| Philips (BioTelemetry, Cardiologs) | Netherlands | Monitoring, Holter, AI | ePatch, MCT, Cardiologs | BioTelemetry bought for $2.8B (2021); ECG AI Marketplace (2025) |
| Baxter (Bardy, Welch Allyn) | US | Patches, carts | CAM | Settled patent dispute with iRhythm, 2026 |
| Idoven | Spain | AI ECG platform | Willem | CE IIa (22 patterns); no FDA clearance found ([Idoven](https://idoven.ai/regulatory-compliance), [22 patterns](https://idoven.ai/)) |
| Medical AI | South Korea | Single-lead AI | AiTiA LVSD-1L | Korean MFDS approval |
| Movesense | Finland | Open sensor | Movesense MD | EU MDR Class IIa ([MedTech Dive](https://www.medtechdive.com/press-release/20230420-movesense-medical-receives-eu-mdr-clearance-as-the-first-chest-strap-ecg-mo)) |

## 5. Patents

| Patent | Holder | Topic | Year granted | Why it matters |
|---|---|---|---|---|
| [US 8,509,882](https://patents.google.com/patent/US8509882B2/en) | AliveCor | Smartphone ECG using a frequency-modulated audio link (6–20 kHz carrier) | 2013 | Foundation of the smartphone ECG category |
| [US 9,572,499](https://patents.google.com/patent/US9572499B2/en) | AliveCor | Arrhythmia tracking and scoring | 2017 | Asserted against Apple; later held unpatentable |
| US 10,595,731 / 10,638,941 | AliveCor | PPG-triggered ECG confirmation | — | Asserted against Apple; held unpatentable ([iClarified](https://www.iclarified.com/96659/apple-defeats-alivecors-bid-to-block-us-watch-imports)) |
| [US 10,076,257](https://patents.google.com/patent/US10076257B2/en) | Apple | Leads embedded in the device housing (priority 2008) | 2018 | Apple's early ECG-in-device claim; asserted against AliveCor |
| US 10,610,157 / [12,259,690](https://patents.google.com/patent/US12259690B2/en) | Apple | Watch electrodes; conductive crown | 2025 (12,259,690) | Watch ECG hardware |
| [US 12,121,326](https://patents.google.com/patent/US12121326B2/en) | Mayo Foundation | ECG-based ejection-fraction screening | 2024 | Core AI-ECG low-EF patent (Attia, Friedman) |
| [US 9,700,227](https://patents.google.com/patent/US9700227B2/en) | Bardy Diagnostics | Sternal patch tuned for P waves | 2017 | The CAM design; Bardy later sued iRhythm |

**AliveCor vs. Apple.**
- AliveCor filed at the ITC (337-TA-1266). An administrative judge found infringement in 2022.
- The PTAB ruled all three AliveCor patents unpatentable in December 2022.
- The Federal Circuit affirmed on 7 Mar 2025, so no Apple Watch import ban followed ([9to5Mac](https://9to5mac.com/2025/03/07/apple-alivecor-itc-case-patents)).
- AliveCor's separate antitrust claim lost at the Ninth Circuit on 8 Jan 2026 ([9to5Mac](https://9to5mac.com/2026/01/08/apple-shuts-down-alivecor-antitrust-claims-after-earlier-apple-watch-patent-win)).
- Apple's own countersuit was filed in 2022 ([Knobbe](https://www.knobbe.com/blog/developments-patent-disputes-between-apple-and-alivecor/)). Its outcome is *unverified*.

## 6. Most-cited papers

I could not verify citation counts, so none are given.

| Paper | Authors | Venue/year | Why it matters |
|---|---|---|---|
| String galvanometer ECG | Einthoven | 1901–1903; Nobel Prize 1924 ([Nobel](https://www.nobelprize.org/prizes/medicine/1924/einthoven/biographical/)) | Invented the clinical ECG |
| [A real-time QRS detection algorithm](https://doi.org/10.1109/TBME.1985.325532) | Pan, Tompkins | IEEE TBME 1985 | 99.3% QRS detection on MIT-BIH; still the default R-peak detector |
| [HRV standards](https://pubmed.ncbi.nlm.nih.gov/8598068/) | Task Force ESC/NASPE | Circulation 1996 | Defines the HRV metrics |
| [PhysioBank, PhysioToolkit, PhysioNet](https://archive.physionet.org/publications/citations/article000018.html) | Goldberger et al. | Circulation 2000 | Open biosignal data infrastructure |
| [Impact of the MIT-BIH Arrhythmia DB](https://archive.physionet.org/physiobank/database/mitdb/) | Moody, Mark | IEEE EMB Mag 2001 | The classic arrhythmia benchmark |
| [Recommendations for ECG standardization, Part I](https://www.hrsonline.org/resource/2007-ahaacchrs-scientific-statement-recommendations-standardization-and-interpretation/) | Kligfield et al. | Heart Rhythm/Circulation 2007 | Technical standards for digital ECG |
| [Cardiologist-level arrhythmia detection](https://pmc.ncbi.nlm.nih.gov/articles/PMC6784839/) | Hannun, Rajpurkar, …, Ng | Nat Med 2019 | 91,232 single-lead ECGs; F1 0.837 vs 0.780 for cardiologists |
| [Screening for contractile dysfunction](https://mayoclinic.elsevierpure.com/en/publications/screening-for-cardiac-contractile-dysfunction-using-an-artificial) | Attia et al. | Nat Med 2019 | Low EF from ECG, AUC 0.93; launched AI-ECG |
| [AF signature during sinus rhythm](https://www.healio.com/news/cardiology/20190802/ai-may-identify-af-in-patients-during-normal-sinus-rhythm) | Attia et al. | Lancet 2019 | Detects past or future AF from a normal-rhythm ECG; 79.4% accuracy from one ECG, 83.3% using all ECGs in the first month |
| [Automatic diagnosis of the 12-lead ECG](https://doi.org/10.1038/s41467-020-15432-4) | Ribeiro et al. | Nat Commun 2020 | Trained on 2M+ CODE exams; beat residents |
| [PTB-XL](https://publica.fraunhofer.de/handle/publica/264664) | Wagner et al. | Sci Data 2020 | Standard open 12-lead benchmark |

## 7. New achievements (2023–2026)

- **Outcome trial**: AI-ECG alerts cut 90-day mortality from 4.3% to 3.6% (HR 0.83) in 15,965 inpatients (Lin et al., *Nat Med* 2024) ([HCPLive](https://hcplive.com/view/ai-electrocardiogram-alert-intervention-reduces-all-cause-mortality)).
- **EAGLE trial**: AI-ECG raised low-EF diagnoses by 32% in primary care ([TCTMD](https://www.tctmd.com/news/ai-ecg-allows-early-diagnosis-low-ef)).
- **EchoNext** (*Nature* 2025): detected 77% of structural heart disease against 64% for cardiologists; Mini-Model weights and data released, data under a DUA ([NYP](https://www.nyp.org/news/can-ai-detect-hidden-heart-disease), [PhysioNet](https://physionet.org/content/echonext/)).
- **Foundation models**:
  - ECGFounder: 10.8M ECGs, AUROC above 0.95 on 80 diagnoses ([arXiv](https://arxiv.org/abs/2410.04133v3)).
  - ECG-FM: AF AUROC 0.996 ([JAMIA Open](https://pubmed.ncbi.nlm.nih.gov/41113504/)).
  - HuBERT-ECG: 9.1M ECGs, still a preprint ([medRxiv](https://www.medrxiv.org/content/10.1101/2024.11.14.24317328v4.full-text)).
  - AnyECG: AUROC above 0.7 on 306 diseases, still a preprint ([arXiv](https://arxiv.org/abs/2601.10748v1)).
- **New clearances**: Anumana amyloidosis (Apr 2026), HeartBeam synthesized 12-lead (Dec 2025), and Kardia 12L reaching 39 AI findings (Jan 2026).
- **PhysioNet 2025**: Chagas detection from ECG, with 111 teams ([arXiv](https://arxiv.org/pdf/2510.02202)).

## 8. Current state of the field

**Where ECG is in routine practice.**
- AF detection on watches and handheld devices.
- Automated arrhythmia reading of patch and Holter data.
- 12-lead interpretation software.
- QT analysis in drug trials.
- Cleared AI-ECG for low EF and amyloidosis, though adoption is still early.

**Where it is still research.** Stress, workload and emotion detection, driver monitoring, fetal ECG, biometrics, and brain–heart markers. Foundation models are also not yet in clinical products.

**Open problems.**
- Generalizing across hospitals, devices and lead sets.
- Noisy single-lead wearable data.
- Too few randomized outcome trials.
- Large datasets are proprietary or embargoed; CODE in full and Mayo's data are not open.
- HRV workload markers are inconsistent between people ([review](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11207491/)).
- Removing the cardiac field artifact from EEG without losing heartbeat-evoked signals.

**Where an AI engineer can contribute.**
- Self-supervised pretraining that transfers to wearables.
- Benchmarks that test under distribution shift (PhysioNet 2021 tested reduced-lead ECGs from multiple sites).
- Calibrated, explainable risk scores.
- On-device models.
- Multimodal EEG+ECG models for passive BCI that handle the cardiac artifact explicitly.

## 9. Public datasets

Full specifications for each dataset, and tables of published results on them, are in [DATASETS.md](DATASETS.md).

| Dataset | Content | Size | Link |
|---|---|---|---|
| MIT-BIH Arrhythmia | 2-channel Holter, 360 Hz, 11-bit; ~110k beat labels | 48 half-hour records / 47 subjects | [PhysioNet](https://archive.physionet.org/physiobank/database/mitdb/) |
| PTB-XL | 12-lead, 10 s, 500 Hz, SCP labels | 21,799 ECGs / 18,869 patients | [PhysioNet](https://www.physionet.org/content/ptb-xl/1.0.3/) |
| MIMIC-IV-ECG | 12-lead, 10 s, 500 Hz, linked to the MIMIC-IV clinical database | ~800k ECGs / ~160k patients | [PhysioNet](https://physionet.org/news/post/422/) |
| CODE-15% | 12-lead, 400 Hz, Brazilian telehealth | 345,779 exams / 233,770 patients | [Zenodo](https://zenodo.org/records/4916206) |
| Harvard-Emory ECG Database (HEEDB) | 12-lead, 10 s, 250/500 Hz | 10.6M (MGH) + ~1.0–1.45M (Emory; sources disagree) | [AWS/BDSP](https://registry.opendata.aws/bdsp-heedb) |
| PhysioNet 2017 | Single-lead AliveCor, 300 Hz, AF/normal/other/noisy | 8,528 public | [PhysioNet](https://moody-challenge.physionet.org/2017) |
| PhysioNet 2021 | 12/6/4/3/2-lead, multi-site | 88,253 public | [PhysioNet](https://moody-challenge.physionet.org/2021) |
| PhysioNet 2025 | Chagas, weak and strong labels | Multi-source | [PhysioNet](https://moody-challenge.physionet.org/2025/) |
| Apnea-ECG | Overnight ECG with apnea labels | 70 recordings (~8 h each) | [PhysioNet](https://archive.physionet.org/physiobank/database/apnea-ecg) |
| PhysioNet 2013 | Abdominal fetal ECG, 4 channels, 1 kHz | 1-min records | [PhysioNet](https://moody-challenge.physionet.org/2013) |
| PhysioNet 2015 | ICU multi-signal alarm segments | 1,250 alarms | [PhysioNet](https://physionet.org/content/challenge-2015/) |
| WESAD | Chest ECG at 700 Hz plus wrist signals; stress and amusement | 15 subjects | [UCI](https://archive.ics.uci.edu/dataset/465/wesad+wearable+stress+and+affect+detection) |
| EchoNext | ECGs paired with echo-derived labels | Released with the *Nature* 2025 paper | [NYP](https://www.nyp.org/news/can-ai-detect-hidden-heart-disease) |

## 10. GitHub repositories

Stars and dates checked via the GitHub API on 2026-10-10. "Other" means GitHub could not identify the license; check the repo before reusing code.

**Toolkits and libraries**

| Repo | What it does / when to use it | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [MIT-LCP/wfdb-python](https://github.com/MIT-LCP/wfdb-python) | Reads and writes PhysioNet WFDB files and annotations. Use it first for any PhysioNet dataset. | Jupyter Notebook | 853 | 2026-06 | MIT |
| [neuropsychology/NeuroKit](https://github.com/neuropsychology/NeuroKit) | NeuroKit2: ECG cleaning, R-peaks, delineation and HRV, plus EDA, EMG, EOG and RSP. The best general starting point for multimodal biosignals. | Python | 2,392 | 2026-10 | MIT |
| [scientisst/BioSPPy](https://github.com/scientisst/BioSPPy) | Maintained fork of BioSPPy: filtering, R-peaks and heart rate for ECG, PPG, EDA and EMG. The original [PIA-Group/BioSPPy](https://github.com/PIA-Group/BioSPPy) is archived. | Python | 124 | 2026-09 | Other |
| [paulvangentcom/heartrate_analysis_python](https://github.com/paulvangentcom/heartrate_analysis_python) | HeartPy: heart rate and HRV from noisy PPG or ECG, including wearable data | Python | 1,151 | 2025-12 | MIT |
| [berndporr/py-ecg-detectors](https://github.com/berndporr/py-ecg-detectors) | Reference QRS detectors (Pan-Tompkins, Hamilton, Christov, wavelet and others) for benchmarking R-peak detection | Python | 391 | 2024-02 | GPL-3.0 |
| [PGomes92/pyhrv](https://github.com/PGomes92/pyhrv) | Full HRV toolbox: time, frequency and nonlinear measures, with reports | Python | 341 | 2026-06 | BSD-3-Clause |
| [Aura-healthcare/hrv-analysis](https://github.com/Aura-healthcare/hrv-analysis) | Lightweight HRV feature extraction from RR intervals, for example from chest-strap data | Python | 460 | 2026-10 | GPL-3.0 |
| [embodied-computation-group/systole](https://github.com/embodied-computation-group/systole) | Cardiac signal analysis and synchrony for psychophysiology and brain–heart (interoception) experiments | Python | 94 | 2026-10 | Apache-2.0 |
| [marianux/ecg-kit](https://github.com/marianux/ecg-kit) | MATLAB toolbox for ECG delineation and beat classification; dated but still cited | MATLAB | 295 | 2020-02 | GPL-2.0 |
| [DeepPSP/torch_ecg](https://github.com/DeepPSP/torch_ecg) | PyTorch ECG models, preprocessing and dataset readers for many PhysioNet challenges | Python | 272 | 2026-10 | MIT |
| [alphanumericslab/ecg-image-kit](https://github.com/alphanumericslab/ecg-image-kit) | Synthesizes and digitizes ECG images, for turning paper and scanned ECGs into signals | Jupyter Notebook | 165 | 2024-10 | BSD-3-Clause |

**Foundation models and papers with code**

| Repo | What it does / when to use it | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [bowang-lab/ecg-fm](https://github.com/bowang-lab/ecg-fm) | ECG-FM open-weight transformer, pretrained on 1.5M ECGs (JAMIA Open 2025). Fine-tune it on small labeled sets. | Python | 320 | 2026-01 | MIT |
| [PKUDigitalHealth/ECGFounder](https://github.com/PKUDigitalHealth/ECGFounder) | ECGFounder (NEJM AI 2025): 10M+ ECGs, 150 labels, 12-lead and single-lead checkpoints | Python | 158 | 2026-02 | MIT |
| [Edoar-do/HuBERT-ECG](https://github.com/Edoar-do/HuBERT-ECG) | HuBERT-ECG self-supervised model pretrained on 9.1M ECGs | Shell | 82 | 2026-10 | Other |
| [antonior92/automatic-ecg-diagnosis](https://github.com/antonior92/automatic-ecg-diagnosis) | Ribeiro et al., Nat Commun 2020: ResNet trained on CODE, with weights. A strong 12-lead baseline. | Python | 456 | 2023-03 | MIT |
| [antonior92/ecg-age-prediction](https://github.com/antonior92/ecg-age-prediction) | ECG-age model from the same group; ECG-estimated age predicts mortality | Python | 99 | 2023-09 | MIT |
| [awni/ecg](https://github.com/awni/ecg) | Hannun et al., Nat Med 2019: the single-lead arrhythmia deep network | Python | 821 | 2023-03 | GPL-3.0 |

EchoNext's dataset is on [PhysioNet](https://physionet.org/content/echonext/) under restricted access. PhysioNet links [PierreElias/IntroECG](https://github.com/PierreElias/IntroECG) for the code; I found no separate EchoNext repo. AnyECG had no public repo at the time of checking.

**Benchmarks and dataset loaders**

| Repo | What it does / when to use it | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [helme/ecg_ptbxl_benchmarking](https://github.com/helme/ecg_ptbxl_benchmarking) | Official PTB-XL benchmark (Strodthoff et al.): splits, tasks and baselines. Use it to compare 12-lead models. | Python | 317 | 2025-06 | GPL-3.0 |
| [AI4HealthUOL/ecg-fm-benchmarking](https://github.com/AI4HealthUOL/ecg-fm-benchmarking) | Benchmarks ECG foundation models on 12 public datasets and 26 tasks | Python | 56 | 2026-06 | None stated |
| [physionetchallenges/python-example-2025](https://github.com/physionetchallenges/python-example-2025) | Official starter code for the 2025 Chagas challenge: data loading, scoring, submission format | Python | 33 | 2025-06 | BSD-2-Clause |
| [physionetchallenges/python-classifier-2021](https://github.com/physionetchallenges/python-classifier-2021) | Official starter code for the 2021 reduced-lead (12/6/4/3/2-lead) challenge | Python | 33 | 2021-08 | BSD-2-Clause |
| [MIT-LCP/mimic-code](https://github.com/MIT-LCP/mimic-code) | Community code for MIMIC databases; use it to link MIMIC-IV-ECG to clinical labels | Jupyter Notebook | 3,407 | 2026-09 | MIT |

**Wearable, hardware and open devices**

| Repo | What it does / when to use it | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [polarofficial/polar-ble-sdk](https://github.com/polarofficial/polar-ble-sdk) | Official SDK for streaming raw ECG (130 Hz) and RR intervals from the Polar H10 | Swift | 751 | 2026-10 | Other |
| [brainflow-dev/brainflow](https://github.com/brainflow-dev/brainflow) | One API to stream EEG, EMG and ECG from many boards (OpenBCI and others). Good for multimodal passive-BCI rigs. | C++ | 1,770 | 2026-10 | Other |
| [OpenBCI/OpenBCI_GUI](https://github.com/OpenBCI/OpenBCI_GUI) | Acquisition GUI for Cyton and Ganglion, which can record ECG ([setup guide](https://docs.openbci.com/GettingStarted/Biosensing-Setups/ECGSetup/)) | HTML | 965 | 2026-04 | MIT |
| [sparkfun/AD8232_Heart_Rate_Monitor](https://github.com/sparkfun/AD8232_Heart_Rate_Monitor) | Arduino and Processing examples and hardware files for the AD8232 single-lead board | Processing | 224 | 2024-11 | Other |

The Movesense device and mobile libraries are hosted on [Bitbucket](https://www.movesense.com/news/2017/10/movesense-device-library-now-public-bitbucket/), not GitHub, so they are not listed here.

**Curated lists**

| Repo | What it does / when to use it | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [PierreElias/IntroECG](https://github.com/PierreElias/IntroECG) | Starter resource library and notebooks for deep learning on ECGs, from an EchoNext author | Jupyter Notebook | 188 | 2026-04 | None stated |
| [ShijianXu/awesome-ECG](https://github.com/ShijianXu/awesome-ECG) | Small paper list; I found no large, well-maintained "awesome-ECG" list | n/a | 5 | 2024-06 | None stated |
