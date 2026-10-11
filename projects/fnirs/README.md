# fNIRS (Functional near-infrared spectroscopy)

Functional near-infrared spectroscopy shines red and near-infrared light (about 650–950 nm) through the scalp and measures how much comes back. From that it estimates changes in oxygenated and deoxygenated haemoglobin in the outer 1.5–2 cm of cortex, which follow neural activity with a delay of several seconds ([Pinti et al. 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC6367070)). Today it is used most in cognitive and developmental neuroscience (it is silent, portable and tolerates movement), in bedside cerebral oximetry during surgery and intensive care, and as a slow but motion-tolerant BCI signal. Since March 2025 it has also been in a mass-market headband that combines it with EEG ([Muse S Athena](https://athletechnews.com/muse-s-athena-brain-wearable/)).

Items marked *unverified* could not be confirmed from a source. Cells marked "—" mean the manufacturer did not publish the spec, or I could not find it.

## 1. The data

**What is measured.** Active neurons trigger a local increase in blood flow that overshoots their oxygen use. This is *neurovascular coupling*. In the activated patch of cortex, oxygenated haemoglobin (HbO, or HbO₂) goes up and deoxygenated haemoglobin (HbR, or HHb) goes down. fMRI's BOLD signal comes mainly from the same HbR change. A typical evoked response peaks about 5–6 s after stimulus onset and takes about 16 s to return to baseline. The shape varies with brain region, task and age ([Pinti 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC6367070)).

**From light to haemoglobin.** Light in the near-infrared "optical window" is scattered much more than it is absorbed, so photons take a banana-shaped path from source to detector. The deeper that path reaches, the further apart the source and detector are. The *modified Beer–Lambert law* (MBLL) turns a change in detected light at each wavelength into a change in HbO and HbR concentration. It uses each chromophore's extinction coefficient, the source–detector distance, and a *differential pathlength factor* (DPF) that accounts for the extra distance scattered photons travel ([Pinti 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC6367070); DPF measured by time of flight in [Delpy et al. 1988](https://doi.org/10.1088/0031-9155/33/12/008)). Because continuous-wave systems only see changes, the result is relative. Best practice is to report units and the DPF used. The same channel can read "40 µM·mm" uncorrected or "0.22 µM" with DPF 6 and a 30 mm separation ([Yücel et al. 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC7793571)).

**Measurement types**

| Type | How | What you get | Used for |
|---|---|---|---|
| Continuous wave (CW) | Constant or slowly modulated light; measure intensity only | Relative ΔHbO/ΔHbR via MBLL. Cheapest and most common | Almost all research and consumer fNIRS ([Pinti 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC6367070)) |
| Frequency domain (FD) | Light intensity-modulated at radio frequencies; measure amplitude and phase | Separates absorption from scattering, so absolute concentrations | ISS Imagent (110 MHz) ([ISS](https://iss.com/biomedical/imagent)) |
| Time domain (TD) | Picosecond pulses; build a histogram of photon arrival times | Absolute values plus depth information from late photons | Kernel Flow ([Ban et al. 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8765296)) |
| Spatially resolved spectroscopy (SRS) | CW at several distances from one source | Absolute tissue saturation index (TOI/rSO₂, %) | Clinical cerebral oximeters ([Hamamatsu NIRO](https://www.hamamatsu.com/jp/ja/product/life-science-and-medical-systems/medical_related_products/brain-and-tissue-oxygen-monitors/C10448-10.html)) |
| High-density diffuse optical tomography (HD-DOT) | Dense, overlapping grid of sources and detectors at many distances, then image reconstruction | 3D images with resolution approaching fMRI | Visual, language and naturalistic mapping ([Eggebrecht et al. 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC4114252)) |

Sparse fNIRS arrays usually space optodes about 30 mm apart. HD-DOT grids use about 13 mm, which gives several source–detector distances (13–40 mm) and roughly half the spatial resolution of fMRI ([Markow et al. 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11762274)).

**Short channels.** A long channel (about 30 mm) sees both the brain and the scalp, and scalp blood flow changes with heart rate, breathing and blood pressure, often in step with the task. A *short-separation channel* (under 15 mm; about 8 mm is best in adults and 4–5 mm in infants) sees mostly the scalp. Its signal is regressed out of the long channels ([Yücel 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC7793571), [Brigadoi & Cooper 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4478880)). Ignoring this is a leading cause of false positives ([Tachtsidis & Scholkmann 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4791590)).

**Signal characteristics**

| Property | Typical value | Source |
|---|---|---|
| Wavelengths | 650–950 nm window; usually 2–3 wavelengths, e.g. 760/850 nm LEDs (NIRx), 690/830 nm lasers (ISS), 735/810/850 nm (Hamamatsu) | [Pinti 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC6367070), section 2 |
| Hemodynamic delay | Peak about 5–6 s after onset; back to baseline about 16 s | [Pinti 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC6367070) |
| Sampling rate | Commonly up to 10 Hz; research systems reach 100–240 Hz (NIRScout 100 Hz, NIRSport2 240 Hz); whole-head TD and HD-DOT frame rates are lower (Kernel Flow 2: 4.75 Hz; LUMO: up to 12.5 Hz) | [Pinti 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC6367070), [NIRx](https://nirx.net/nirsport), [Kernel](https://www.kernel.com/specs/Flow%202%20Spec%20Sheet.pdf), [Gowerlabs](https://www.gowerlabs.co.uk/lumospecs) |
| Depth | Outer cortex only, about 1.5–2 cm below the scalp | [Pinti 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC6367070) |
| Spatial resolution | 2–3 cm for sparse fNIRS; HD-DOT about half that of fMRI | [Pinti 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC6367070), [Markow 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11762274) |
| Source–detector separation | About 30 mm for brain channels; under 15 mm (8 mm optimum in adults) for short channels | [Yücel 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC7793571) |
| Noise: cardiac | About 1 Hz | [Pinti 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC6367070) |
| Noise: respiration | Period about 3 s (about 0.3 Hz) | [Kirilina et al. 2013](https://www.frontiersin.org/articles/10.3389/fnhum.2013.00864/full) |
| Noise: Mayer waves | Blood-pressure oscillations with a period of about 10 s (about 0.1 Hz). They overlap the task band, so a band-pass filter cannot remove them | [Kirilina 2013](https://www.frontiersin.org/articles/10.3389/fnhum.2013.00864/full), [Yücel 2016](https://doi.org/10.1364/BOE.7.003078), [Yücel 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC7793571) |
| Noise: motion | Optode slips cause spikes and baseline shifts; corrected with methods such as TDDR, spline or wavelet filtering | [Yücel 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC7793571), [TDDR code](https://github.com/frankfishburn/TDDR) |
| Noise: extracerebral | Scalp blood flow changes with the task; affects HbO more than HbR | [Kirilina 2013](https://www.frontiersin.org/articles/10.3389/fnhum.2013.00864/full), [Tachtsidis & Scholkmann 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4791590) |

**Features and formats.** Classic fNIRS BCIs band-pass filter the signal and then take window statistics of ΔHbO and ΔHbR: mean, variance, peak, slope, skewness and kurtosis. They classify with LDA or SVM, with LDA usually "simple but good" ([Naseer & Hong 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4309034)). Neuroscience studies instead fit a general linear model (GLM) with HRF regressors, drift terms and short-channel regressors ([Yücel 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC7793571)). Deep-learning work feeds the raw or lightly filtered multichannel time series to CNNs, LSTMs or transformers (section 7).

File formats:
- **SNIRF** is the community standard: an HDF5 file that holds data, probe geometry, stimuli and metadata for CW, FD, TD and DOT. Artinis, NIRx, Kernel, Gowerlabs, OBELAB and Cortivision export it, and Homer3, MNE, FieldTrip, AnalyzIR, Satori and Brainstorm read it ([Tucker et al. 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC9732807), [spec](https://github.com/fNIRS/snirf)).
- **`.nirs`** is the older MATLAB format from HOMER2. Homer3 ships a `Nirs2Snirf` converter ([Homer3](https://github.com/BUNPC/Homer3/blob/master/DataTree/AcquiredData/DataFiles/Nirs2Snirf.m)).
- **NIRS-BIDS** is the Brain Imaging Data Structure extension for organizing whole studies, published in 2025 ([Luke et al. 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11772744)).
- MNE-Python also reads vendor formats directly (`read_raw_nirx`, `read_raw_hitachi`, `read_raw_boxy` for ISS Imagent) ([MNE](https://mne.tools/stable/api/reading_raw_data.html)).

## 2. Devices and specifications

Channels are source–detector pairs, so the channel count depends on the montage. Vendors usually quote a maximum.

**Research-grade**

| Device | Company | Type | Sources / detectors / channels | Sampling rate | Wavelengths | Wearable? | Connectivity | Typical use | Status/price |
|---|---|---|---|---|---|---|---|---|---|
| NIRSport2 | NIRx | CW | 8 or 16 sources, 8–16 detectors; up to 16 short detectors; ~25–50 typical 3 cm channels (max 256); multi-device up to 80+80 | Up to 240 Hz | 760 / 850 nm (LED) | Yes (2–4.5 h battery) | USB, Wi-Fi, standalone; LSL or cabled triggers | Mobile, hyperscanning, EEG-fNIRS | Current ([NIRx](https://nirx.net/nirsport)) |
| NIRScout | NIRx | CW | Up to 64 LED or 32 laser sources and 32 detectors (double in tandem); up to 2048 channels (4096 tandem) | 2.5–100 Hz | LED 760 / 850; lasers 785, 808, 830, 850 nm | No (lab) | 255 trigger in/out; EEG, fMRI, TMS integration | Lab fNIRS, fMRI co-recording | Current ([NIRx](https://nirx.net/nirscout)) |
| Brite (MKIV) | Artinis | CW | Up to 27 channels; 10–55 mm separations | — | Multi-wavelength (not listed) | Yes (300 g) | Bluetooth or Wi-Fi; offline recording | Mobile cognitive studies | Current ([Artinis](https://artinis.com/brite)) |
| Brite Lite (the old OctaMon URL now redirects here) | Artinis | CW | 8 channels (10 with upgrade) | Up to 150 Hz | — | Yes (<250 g) | Bluetooth or offline | Prefrontal, field studies | Current ([Artinis](https://artinis.com/brite-lite)) |
| PortaLite MKII | Artinis | CW + SRS | 3 channels + 3 short channels per sensor; 1–2 sensors | Up to 100 Hz | — | Yes | Real-time or offline; mobile app | Forehead or muscle, TSI | Current ([Artinis](https://artinis.com/portalite)) |
| LABNIRS | Shimadzu | CW | 4–40 sets (10–142 channels); photomultiplier detectors | 6 ms per sample (about 167 Hz) | 3 laser wavelengths (values not listed) | No (lab) | — | Lab mapping | Current ([specs](https://www.shimadzu.com/an/products/life-science-lab-instruments/imaging/labnirs/spec.html), [features](https://www.shimadzu.com/an/products/life-science-lab-instruments/imaging/labnirs/features.html)) |
| LIGHTNIRS | Shimadzu | CW | 8 pairs, up to 22 channels; APD detectors | — | 3 laser wavelengths | Portable (~1.6 kg) | Battery; 3 digital + 10 analog inputs | Portable studies (used for the Bak 2019 dataset) | Current ([Shimadzu](https://www.shimadzu.com/an/products/life-science-lab-instruments/imaging/lightnirs/spec.html)) |
| ETG-4000 | Hitachi Medical | CW (frequency-modulated lasers) | 24–52 channels (ETG-4100 figure) | 10 Hz used in studies | 695 / 830 nm | No | — | Optical topography, Japanese psychiatry | Legacy; FDA 510(k) K042501 (2004) ([FDA](https://fda.innolitics.com/device/K042501), [ETG-4100](https://labonline.com.au/content/analytical-instrumentation/product/hitachi-medical-systems-etg-4100-optical-topography-system-1172943690), [study](https://arxiv.org/pdf/1507.07422)); current availability not reported |
| LUMO | Gowerlabs | HD-DOT (CW) | Tiles of 3 dual-wavelength sources + 4 detectors; up to 54 docks (162 sources, 216 detectors); >7000 channels; 10–70 mm separations | Up to 12.5 frames/s | 735 / 850 nm | Yes, fibreless (tile <6 g; adult whole-head cap 810 g) | 2 m cable; IMU per tile | Whole-head HD-DOT, infants | Current, research use ([Gowerlabs](https://www.gowerlabs.co.uk/lumospecs), wavelengths from [Vidal-Rosas 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8033536)) |
| Photon Cap C20 | Cortivision | CW | 16 sources, 10 detectors (light version 4 + 2); up to 37 channels | Up to 86 Hz *unverified* | 760 / 850 nm *unverified* | Yes (230 g, 6 h) | Wireless (Bluetooth *unverified*) | Entry-level, paediatric | Current ([Cortivision](https://www.cortivision.com/products/photon); rate, wavelengths and Bluetooth from a [UNSW listing](https://www.unsw.edu.au/research/facilities-and-infrastructure/find-an-instrument/rinsw-instruments/cortivision-photon-cap-c20)) |
| Spectrum C23 | Cortivision | CW | 8×12 to 32×48 optodes; up to 150 channels | Up to 250 Hz | — | — | — | Scalable lab/mobile | Current ([Cortivision](https://www.cortivision.com/)) |
| Imagent | ISS | FD (110 MHz) | 16–960 channels; up to 128 source fibres and 60 detector bundles (3,840 channels); PMT detectors | 15 ms minimum (~67 Hz) | 690 / 830 nm | No | — | Absolute oximetry, fast optical signals (EROS) | Current ([ISS](https://iss.com/biomedical/imagent)) |
| Flow (v1) | Kernel | TD | 52 modules, each 1 source + 6 detectors at 10 mm | 200 Hz histograms, 100 Hz per wavelength pair | 690 / 850 nm | Yes (2.05 kg, USB-C power) | USB-C | Whole-head TD-fNIRS research | Superseded by Flow 2 ([Ban et al. 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8765296)) |
| Flow 2 | Kernel | TD + 6 EEG electrodes | 40 modules × (3 sources + 6 detectors) = 120 sources, 240 detectors; up to 3,500 channels; 8.5–60 mm | Whole cortex at 4.75 Hz (heart rate at 9.5 Hz); EEG 500 Hz | 753 / 905 nm | Yes (2.5 kg) | USB 2.0 over 10 ft cable; real-time SDK; SNIRF export | Clinical-research and pharma studies | Research use only ([spec sheet](https://www.kernel.com/specs/Flow%202%20Spec%20Sheet.pdf)) |
| fNIR 2000 / 1200 | Biopac (fNIR Devices) | CW | 16-channel forehead pad: 4 emitters, 10 detectors, 25 mm; 2000C/2000M up to 18 optodes | 2 Hz (E series) | 730 / 850 nm | 2000M wireless | — | Prefrontal workload, education | Current ([Biopac sensors](https://biopac.com/product/fnir-sensors-2000), [2000M](https://www.biopac.com/product/fnir-2000m-systems/)) |
| ninjaNIRS 2022 | Boston University (open hardware) | CW HD | 56 sources, up to 192 detectors (144 for whole head); 18 mm nearest neighbour | — | Dual-wavelength | Yes (4.7 kg without batteries) | — | Open whole-head HD research | Designs released ([O'Brien et al. 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11482177)) |

**Clinical cerebral oximetry**

These report an absolute regional saturation (rSO₂ or TOI, %) rather than task responses.

| Device | Company | Type | Sources / detectors / channels | Sampling rate | Wavelengths | Wearable? | Connectivity | Typical use | Status/price |
|---|---|---|---|---|---|---|---|---|---|
| INVOS 7100 | Medtronic (ex-Somanetics, Covidien) | CW multi-distance | 2 or 4 sensor channels *unverified* | — | 730 / 810 nm for trending, plus 2 for sensor-off detection | Bedside monitor + adhesive sensors | USB 3.0/2.0, docking port | Cardiac surgery, ICU, neonates | Current ([Medtronic](https://www.medtronic.com/en-us/healthcare-professionals/products/patient-monitoring/regional-oximetry/regional-oximeters/invos-7100-regional-oximeter.html), [sensor](https://www.medtronic.com/en-us/healthcare-professionals/products/patient-monitoring/regional-oximetry/sensors/invos-regional-oximetry-adult-sensor.html)); Somanetics sold to Covidien in 2010 for $250M ([Wikipedia](https://en.wikipedia.org/wiki/Somanetics)) |
| O3 | Masimo | CW multi-distance | Sensor = 1 emitter + 2 detectors | — | Multi-wavelength (values not listed) | Module on Root monitor | — | Cerebral and somatic oximetry | Expanded FDA clearance K201432 (decision 29 Aug 2020, announced 31 Aug 2020) (somatic, all ages; relative Hb changes in adult brain); trend accuracy 3% ARMS ([BioSpace](https://www.biospace.com/masimo-o3-regional-oximetry-receives-fda-clearance-for-somatic-applications-and-measurement-of-relative-changes-in-cerebral-hemoglobin), [FDA K201432](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm?ID=K201432); sensor and accuracy also in the 2017 clearance [FDA K162603](https://www.accessdata.fda.gov/cdrh_docs/pdf16/K162603.pdf)) |
| SenSmart X-100 + 8004C sensors | Nonin | CW multi-distance | Dual emitters, dual detectors per sensor; up to 6 sites | rSO₂ display refreshes every 1.5 s | 4 wavelengths (730 / 760 / 810 / 880 nm) | Bedside | — | Surgery, ICU | Current ([Nonin](https://www.nonin.com/products/8004c/), [wavelengths](https://www.nonin.com/support/8004c/), [X-100](https://www.nonin.com/support/x100/)) |
| NIRO-200NX | Hamamatsu | SRS + MBLL | 2 channels (4 optional); 1 source + 2 photodiodes per probe | 0.05–30 s interval | 735 / 810 / 850 nm | Bedside | — | TOI, nTHI and ΔHb; neonates, research | Japanese Class III approval 30600BZX00183000 ([Hamamatsu JP](https://www.hamamatsu.com/jp/ja/product/life-science-and-medical-systems/medical_related_products/brain-and-tissue-oxygen-monitors/C10448-10.html)) |

**Consumer / wellness**

| Device | Company | Type | Sources / detectors / channels | Sampling rate | Wavelengths | Wearable? | Connectivity | Typical use | Status/price |
|---|---|---|---|---|---|---|---|---|---|
| Mendi | Mendi Innovations AB | CW, prefrontal | — | — | — | Headband (~55 g, up to 5 h) | Bluetooth, USB-C | Neurofeedback games for focus | Selling; $379 list, $284.25 on sale ([Mendi](https://www.mendi.io/); weight and battery from a [review](https://wellnesspulse.com/reviews/mendi-headset-review/)) |
| Muse S Athena | Interaxon | EEG + fNIRS | "5-optode fNIRS" *unverified*; EEG channel count reported as 4 or 7 *unverified* | — | — | Headband (up to 10 h *unverified*) | Wireless, USB-C | Meditation, sleep, focus | Launched 18 Mar 2025 at $475 ([Athletech News](https://athletechnews.com/muse-s-athena-brain-wearable/), [Muse](https://choosemuse.com/blogs/news/the-future-of-mental-fitness-starts-now-meet-muse-s-athena)) |

## 3. Applications (domains)

| Domain | How fNIRS is used | Examples | Maturity |
|---|---|---|---|
| Cognitive neuroscience | Block or event designs with GLM analysis in settings fMRI cannot reach: walking, talking, real objects | Prefrontal executive function, naturalistic tasks ([Pinti 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC6367070)) | Established research tool |
| Hyperscanning | Record two or more people at once and measure inter-brain coherence | Right superior frontal coherence rises during cooperation but not competition ([Cui, Bryant, Reiss 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3254802)); [HyPyP](https://github.com/ppsp-team/HyPyP) | Research, growing |
| Infant and developmental | Silent, tolerant of movement, no sedation; short channels at 4–5 mm | Methods consortium ([Gervain et al. 2011](https://pmc.ncbi.nlm.nih.gov/articles/PMC6987576)); review ([Lloyd-Fox et al. 2010](https://doi.org/10.1016/j.neubiorev.2009.07.008)); whole-head infant HD-DOT, N = 16 ([Collins-Jones 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC12272203)) | Established research |
| BCI | Classify mental arithmetic, motor imagery, music imagery or emotion induction from prefrontal or motor cortex, usually in 5–15 s windows | Review ([Naseer & Hong 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4309034)); open MI/MA data ([Shin 2017](https://doi.org/10.1109/TNSRE.2016.2628057)). A widely cited fNIRS "yes/no" communication study in completely locked-in patients ([Chaudhary 2017](https://doi.org/10.1371/journal.pbio.1002593)) was retracted in 2019 ([retraction](https://pmc.ncbi.nlm.nih.gov/articles/PMC6913924)) | Research |
| Hybrid EEG-fNIRS | EEG gives speed, fNIRS gives robustness; fuse features or decisions | EEG+fNIRS is one of the two most common hybrid combinations ([Hong & Khan 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5522881)); datasets in section 9; Kernel Flow 2 and Muse Athena build both into one headset | Research; first commercial headsets |
| Neurofeedback | Show the user their own prefrontal or motor ΔHbO in real time | Systematic review and best-practice recommendations ([Kohl et al. 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7396619)); Mendi at home | Research / consumer |
| Stroke rehabilitation | fNIRS neurofeedback during motor-imagery practice | Sham-controlled pilot with 20 patients: greater Fugl-Meyer hand/finger gain with real feedback ([Mihara et al. 2013](https://doi.org/10.1161/STROKEAHA.111.674507)) | Clinical research |
| Disorders of consciousness | Look for command-following (motor imagery) in unresponsive patients | 16 patients (5 VS/UWS, 11 MCS) ([Kempny et al. 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4983150)) | Research |
| Psychiatry | Prefrontal response during a verbal fluency task as a biomarker | Review ([Ehlis et al. 2014](https://doi.org/10.1016/j.neuroimage.2013.03.067)). **Japan:** the 7-site study of 673 patients and 1007 controls classified bipolar disorder/schizophrenia correctly in 85.5% of cases and depression in 74.6% ([Takizawa et al. 2014](https://doi.org/10.1016/j.neuroimage.2013.05.126)). "Optical topography to aid differential diagnosis of depressive symptoms" became Advanced Medical Technology in 2009 and has been covered by national health insurance since April 2014, as code D236-2 (400 or 200 points) ([HR Pro](https://www.hrpro.co.jp/glossary_detail.php?id=137), [Knowlety D236-2](https://knowlety.jp/ika/d236-2/)). A 2025 clinical opinion found much lower agreement with psychiatric diagnosis in practice (44.0% for bipolar disorder, 38.2% for depression) ([Nakamura & Nagamine 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12370649)) | Reimbursed in Japan; research elsewhere |
| Cerebral oximetry in surgery and ICU | Continuous rSO₂ monitoring with a protocol to treat drops | RCT of 200 coronary bypass patients: fewer prolonged desaturations, shorter ICU stays, and less major organ morbidity or mortality (P = 0.048) ([Murkin 2007](https://doi.org/10.1213/01.ane.0000246814.29362.f4)) | Clinical standard in many cardiac centres |
| Cerebral oximetry in neonates | rSO₂-guided care of extremely preterm infants | SafeBoosC-III (1601 infants, 70 sites): no benefit; death or severe brain injury 35.2% vs 34.0% ([Hansen et al. NEJM 2023](https://doi.org/10.1056/NEJMoa2207554)) | Clinical use; benefit unproven |
| Neuroergonomics / workload | Prefrontal fNIRS tracks n-back load and skill learning in operators | Air traffic control and UAV piloting ([Ayaz et al. 2012](https://doi.org/10.1016/j.neuroimage.2011.06.023)); Tufts fNIRS2MW benchmark (section 9) | Research, field pilots |
| Sports and exercise | Prefrontal and motor oxygenation during exercise and exercise–cognition studies; muscle oximetry | Methodology review ([Herold et al. 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6306799)); PortaLite for muscle and forehead | Research |
| Space | fNIRS-based BCI tested in microgravity | Cortivision PhotonGrav on the ISS during Axiom Mission 4 (2025) ([Cortivision](https://www.cortivision.com/)) | Demonstration |
| Consumer | At-home neurofeedback and "mental fitness" | Mendi, Muse S Athena (section 2) | Commercial (wellness, not medical) |

## 4. Companies

| Company | Country | Focus | Key product | Status 2025–2026 |
|---|---|---|---|---|
| NIRx Medical Technologies | US / Germany | Research fNIRS | NIRSport2, NIRScout | Founded 2003 *unverified* (NIRx's own history implies about 2000: [NIRx](https://nirx.net/our-story)). Combined with Artinis under private-equity firm Gilde Healthcare in July 2025; NIRx keeps its own name and R&D is integrated ([NIRx](https://nirx.net/blog-content/nirx-artinis), [Techleap](https://finder.techleap.nl/news/feed/gilde-healthcare-acquires-nirx-artinis), [Clifford Chance](https://www.cliffordchance.com/news/news/2025/07/clifford-chance-advises-gilde-healthcare.html)) |
| Artinis Medical Systems | Netherlands | Portable fNIRS | Brite, Brite Lite, PortaLite | Part of the Gilde fNIRS platform (July 2025) |
| Gowerlabs | UK | Wearable HD-DOT | LUMO | Selling; subject of a UCL research-impact case study ([UCL](https://www.ucl.ac.uk/impact/case-studies/2022/apr/gowerlabs-advancing-optical-brain-imaging-neuroscience-applications-industry)) |
| Kernel | US | Whole-head TD-fNIRS + EEG | Flow 2 | Selling Flow 2 for research use ([spec sheet](https://www.kernel.com/specs/Flow%202%20Spec%20Sheet.pdf)); 2025–26 funding figures *unverified* |
| Cortivision | Poland ([contact](https://www.cortivision.com/contact)) | Wearable fNIRS | Photon Cap, Spectrum C23 | ISS experiment on Axiom-4 (2025) ([Cortivision](https://www.cortivision.com/)) |
| Shimadzu | Japan | Lab and portable fNIRS | LABNIRS, LIGHTNIRS | Selling ([Shimadzu](https://www.shimadzu.com/an/products/life-science-lab-instruments/imaging/labnirs/spec.html)) |
| Hitachi | Japan | Optical topography pioneer | ETG-4000 / ETG-4100 | Legacy product line; holds early optical topography patents (section 5) |
| ISS | US | FD-NIRS | Imagent | Selling ([ISS](https://iss.com/biomedical/imagent)) |
| Biopac / fNIR Devices | US | Prefrontal fNIRS | fNIR 2000 series | Selling ([Biopac](https://www.biopac.com/product/fnir-2000m-systems/)) |
| OBELAB | South Korea | Wearable fNIRS | NIRSIT | Exports SNIRF ([Tucker 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC9732807)); product details not checked |
| Medtronic | US / Ireland | Cerebral oximetry | INVOS 7100 | Selling |
| Masimo | US | Cerebral/somatic oximetry | O3 | Expanded FDA clearance 2020 |
| Nonin | US | Oximetry | SenSmart X-100 | Selling |
| Hamamatsu Photonics | Japan | Oximetry, photodetectors | NIRO-200NX | Selling |
| Mendi Innovations | Sweden | Consumer neurofeedback | Mendi | EU-funded 2019–20 ([CORDIS](https://cordis.europa.eu/project/id/888409)); selling |
| Interaxon (Muse) | Canada | Consumer EEG + fNIRS | Muse S Athena | Launched March 2025 |

## 5. Patents

| Patent number | Holder | Title/topic | Year | Why it matters |
|---|---|---|---|---|
| [US 4,805,623](https://patents.google.com/patent/US4805623A/en) | Vander Corp (inventor F. F. Jöbsis) | Spectrophotometric quantification of a dilute absorber in a strongly scattering medium | Filed 1987, granted 1989 | From the founder of in-vivo NIR monitoring; expired |
| [US 5,122,974](https://patents.google.com/patent/US5122974A/en) | NIM Inc (inventor B. Chance) | Phase-modulated spectrophotometry: photon migration with time, frequency and phase modulation | 1992 | Core idea behind FD/TD NIRS; expired |
| [US 5,803,909](https://patents.google.com/patent/US5803909A/en) | Hitachi (Maki, Koizumi, Kawaguchi) | Multi-wavelength light, intensity-modulated at different frequencies, at many scalp positions, used to image metabolism | Filed 1995, granted 1998 | Frequency-encoded multichannel "optical topography", the basis of Hitachi ETG systems (see [Maki 1995](https://doi.org/10.1118/1.597496)); expired |
| [US 5,795,292](https://patents.google.com/patent/US5795292A/en) | Somanetics | Improving signal-to-noise in clinical spectrometric procedures | 1998 | INVOS-era cerebral oximetry signal processing |
| [US 5,902,235](https://patents.google.com/patent/US5902235A/en) | Somanetics | Optical cerebral oximeter with a forehead sensor | 1999 | Clinical forehead-oximeter design; the line is now Medtronic INVOS |
| [US 6,526,309](https://patents.google.com/patent/US6526309B1/en) | Non Invasive Technology Inc (B. Chance) | Transcranial in-vivo examination of brain tissue with an optical-fibre array | 2003 | Early claim on fibre-array brain spectroscopy |
| [US 7,047,054](https://patents.google.com/patent/US7047054B2/en) | CAS Medical Systems (P. Benni) | Laser-diode optical transducer for non-invasive blood-oxygenation monitoring | 2006 | Laser-based clinical tissue oximetry (FORE-SIGHT line *unverified*) |
| [US 10,515,993](https://patents.google.com/patent/US10515993B2/en) | Hi LLC (inventors include R. Field, a Kernel Flow author) | Stacked photodetector assemblies | 2019 | Detector hardware for wearable time-resolved optics |
| [US 11,006,876](https://patents.google.com/patent/US11006876B2/en) | Hi LLC (inventors include Kernel founder B. Johnson) | Biofeedback for mental-state awareness via a non-invasive brain interface | 2021 | Consumer and neurofeedback use of optical BCIs |
| [US 11,213,245](https://patents.google.com/patent/US11213245B2/en) | Hi LLC | Spatial and temporal diffuse correlation spectroscopy | 2022 | Blood-flow (DCS) measurement alongside fNIRS |

Hi LLC's link to Kernel is inferred from shared people (Ryan Field, Jacob Dahle and Rong Jin, inventors on US 10,515,993, are Kernel authors of [Ban et al. 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8765296); Bryan Johnson, inventor on US 11,006,876, founded Kernel); I did not find a primary source that states it. I found no fNIRS patent litigation.

## 6. Most-cited papers

These are field-defining works. The numbers in brackets are Europe PMC citation counts, checked 2026-10-11. Europe PMC undercounts compared with Google Scholar.

| Paper | Authors | Venue/year | Why it matters |
|---|---|---|---|
| [Noninvasive, infrared monitoring of cerebral and myocardial oxygen sufficiency and circulatory parameters](https://doi.org/10.1126/science.929199) | Jöbsis | Science 1977 | Showed NIR light crosses skull and brain: the start of the field (2,092) |
| [Estimation of optical pathlength through tissue from direct time of flight measurement](https://doi.org/10.1088/0031-9155/33/12/008) | Delpy, Cope, van der Zee, Arridge, Wray, Wyatt | Phys. Med. Biol. 1988 | Measured the DPF used in the modified Beer–Lambert law (1,379) |
| [Spatial and temporal analysis of human motor activity using noninvasive NIR topography](https://doi.org/10.1118/1.597496) | Maki, Yamashita, Ito, Watanabe, Mayanagi, Koizumi | Med. Phys. 1995 | First multichannel "optical topography" maps (394) |
| [Non-invasive optical spectroscopy and imaging of human brain function](https://doi.org/10.1016/S0166-2236(97)01132-6) | Villringer, Chance | Trends Neurosci. 1997 | Classic review that set up fNIRS as functional neuroimaging (847) |
| [Non-invasive neuroimaging using near-infrared light](https://doi.org/10.1016/S0006-3223(02)01550-0) | Strangman, Boas, Sutton | Biol. Psychiatry 2002 | Standard introduction for clinicians and psychiatrists (516) |
| [HomER: a review of time-series analysis methods for near-infrared spectroscopy of the brain](https://pmc.ncbi.nlm.nih.gov/articles/PMC2761652) | Huppert, Diamond, Franceschini, Boas | Appl. Opt. 2009 | The HomER toolbox and the standard processing pipeline (1,384) |
| [A brief review on the history of human fNIRS development and fields of application](https://doi.org/10.1016/j.neuroimage.2012.03.049) | Ferrari, Quaresima | NeuroImage 2012 | History, instruments and applications (1,281) |
| [A review on continuous wave fNIRS and imaging instrumentation and methodology](https://doi.org/10.1016/j.neuroimage.2013.05.004) | Scholkmann, Kleiser, Metz, Zimmermann, Mata Pavia, Wolf, Wolf | NeuroImage 2014 | Reference for CW hardware and signal processing (1,234) |
| [Mapping distributed brain function and networks with diffuse optical tomography](https://pmc.ncbi.nlm.nih.gov/articles/PMC4114252) | Eggebrecht et al. | Nature Photonics 2014 | HD-DOT maps language and resting-state networks; works with DBS implants (362) |
| [fNIRS-based brain-computer interfaces: a review](https://pmc.ncbi.nlm.nih.gov/articles/PMC4309034) | Naseer, Hong | Front. Hum. Neurosci. 2015 | Map of BCI tasks, features and classifiers (404) |
| [False positives and false negatives in fNIRS](https://pmc.ncbi.nlm.nih.gov/articles/PMC4791590) | Tachtsidis, Scholkmann | Neurophotonics 2016 | Why systemic physiology fakes or hides activation (460) |
| [Open access dataset for EEG+NIRS single-trial classification](https://doi.org/10.1109/TNSRE.2016.2628057) | Shin, von Lühmann, Blankertz, Kim, Jeong, Hwang, Müller | IEEE TNSRE 2017 | The most-used hybrid BCI benchmark (115) |
| [The present and future use of fNIRS for cognitive neuroscience](https://pmc.ncbi.nlm.nih.gov/articles/PMC6367070) | Pinti, Tachtsidis, Hamilton, Hirsch, Aichelburg, Gilbert, Burgess | Ann. N.Y. Acad. Sci. 2020 | Current reference on uses, strengths and limits (803) |
| [Best practices for fNIRS publications](https://pmc.ncbi.nlm.nih.gov/articles/PMC7793571) | Yücel, von Lühmann, Scholkmann, Gervain, Dan, Ayaz, Boas, Cooper et al. | Neurophotonics 2021 | Community checklist: short channels, motion, statistics, reporting (368) |

## 7. New achievements (2023–2026)

- **Reproducibility measured.** In the FRESH study, 38 teams analysed the same two datasets with their own pipelines. Nearly 80% agreed on group-level results. Agreement was lower for individual subjects, and higher for more experienced teams and for better-quality data. The main sources of variability were handling of poor-quality data, response modelling and statistics ([Yücel et al. 2025, Commun. Biol.](https://pmc.ncbi.nlm.nih.gov/articles/PMC12322209)).
- **Standards.** SNIRF was formally described in 2023 ([Tucker et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC9732807)), and NIRS-BIDS was published in 2025 ([Luke et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC11772744)). Together they make cross-dataset machine learning practical.
- **Whole-head wearable HD-DOT.** An infant LUMO cap with 33 tiles (99 sources, 132 detectors) mapped the whole optically accessible cortex in 16 infants aged 5–7 months ([Collins-Jones et al. 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC12272203)). Adult whole-head caps reach 54 tiles and >7000 channels ([Gowerlabs](https://www.gowerlabs.co.uk/lumospecs)).
- **Denser optical arrays.** WashU's very-high-density DOT uses 255 sources and 252 detectors at 9.75 mm spacing, a 4× increase in measurement density, and its maps agree with fMRI in the same people ([Fogarty et al. 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12320020)). An ultra-high-density grid at 6.5 mm gave 30–50% higher spatial resolution and 19–35% lower error when decoding visual stimulus position ([Markow et al. 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11762274)).
- **Naturalistic decoding.** HD-DOT identified which of four movie clips a person watched with 94.2% accuracy, using 4 minutes of data per trial ([Tripathy et al. 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11755382)).
- **Time-domain fNIRS gets practical.** Kernel Flow 2 offers whole-head TD-fNIRS with 3,500 channels and built-in EEG ([spec sheet](https://www.kernel.com/specs/Flow%202%20Spec%20Sheet.pdf)). In a TD analysis, HRF recovery with temporal moments improved correlation with the ground truth by 98% (HbO) and 48% (HbR) over CW GLM ([Ortega-Martinez et al. 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC9587749)).
- **Open hardware.** ninjaNIRS: a whole-head, high-density system with 56 sources and up to 192 detectors, 131 dB dynamic range, designs public ([O'Brien et al. 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11482177), [GitHub](https://github.com/BUNPC/NN24_25-Hardware-Firmware)).
- **Deep learning, with a reality check.** A review of 63 papers (2015–May 2022) found that 26 of the 32 that compared deep learning with classic ML reported deep learning ahead ([Eastmond et al. 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9301871)). But BenchNIRS, which uses nested cross-validation on five open BCI datasets, found performance "typically lower than the scores often reported in literature" and no large gaps between models ([Benerradi et al. 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10790918)). A 2026 review with a code tutorial covers transformers and residual nets ([Dissanayake, Müller, von Lühmann 2026](https://doi.org/10.1109/RBME.2025.3617858), [tutorial](https://github.com/theeksnd/fnirsdl_tutorial)).
- **First fNIRS "foundation model" preprints.** A self-supervised transformer trained on surgical-skill fNIRS data reports >88% accuracy on all tasks and MCC >0.91 on intubation, and transfers to a new procedure ([arXiv 2506.22476](https://arxiv.org/abs/2506.22476)).
- **Market.** Muse S Athena brought EEG + fNIRS to consumers at $475 (March 2025). Gilde Healthcare combined NIRx and Artinis (July 2025). Cortivision flew an fNIRS BCI on Axiom-4 (2025) (sections 2–4).

## 8. Current state of the field

**Where fNIRS is used today, and where it is still research**

| Maturity | Applications |
|---|---|
| Established clinical | Cerebral oximetry in cardiac surgery and ICU (INVOS, O3, NIRO, SenSmart); depression differential-diagnosis aid reimbursed in Japan since 2014 |
| Established research tool | Cognitive, social (hyperscanning) and infant neuroscience; neuroergonomics |
| Commercial, early | Consumer neurofeedback (Mendi, Muse Athena); whole-head TD/HD-DOT research systems (Kernel Flow 2, LUMO) |
| Clinical research | Stroke-rehab neurofeedback, disorders of consciousness, psychiatric biomarkers outside Japan, neonatal oximetry (SafeBoosC-III was negative) |
| Research | fNIRS and hybrid EEG-fNIRS BCIs, naturalistic decoding with HD-DOT, deep learning and foundation models |

**Open problems**
- **Slow signal, low bit rate.** The response peaks about 5–6 s after onset ([Pinti 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC6367070)), so fNIRS BCIs need multi-second windows. That is why fNIRS is usually paired with EEG for speed.
- **Scalp and systemic physiology.** Mayer waves, breathing and task-locked scalp flow sit in the same band as the brain response. Without short channels, false positives are common ([Tachtsidis & Scholkmann 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4791590), [Yücel 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC7793571)).
- **Analysis variability.** Even experts disagree on individual-level results (FRESH), and machine-learning papers often leak data or skip nested cross-validation (BenchNIRS).
- **Small, heterogeneous datasets.** Public sets have tens of subjects (section 9), with varying montages, wavelengths and vendors. The largest workload set has 68 usable participants.
- **Depth and coverage.** Only outer cortex (1.5–2 cm); dense hair blocks light and slows setup ([Pinti 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC6367070)).
- **Clinical evidence.** The Japanese depression test's real-world agreement is debated, and cerebral oximetry did not improve outcomes in extremely preterm infants (section 3).

**Where an AI engineer can contribute.**
- Learned removal of physiological noise and motion, using short channels and auxiliary signals (PPG, IMU) as inputs.
- Self-supervised pretraining across SNIRF/BIDS datasets despite different montages; HD-DOT is a natural fit for graph or spatial models.
- EEG-fNIRS fusion that respects the hemodynamic delay.
- Subject- and session-independent decoders evaluated with nested, subject-wise splits (BenchNIRS).
- Real-time, low-latency inference for neurofeedback.
- Image reconstruction for DOT, e.g. learned inverse models alongside the Monte Carlo forward models (MCX, NIRFASTer, Toast++).
- Honest benchmarks that report chance level and confidence intervals.

## 9. Public datasets

Full specifications for each dataset, and tables of published results on them, are in [DATASETS.md](DATASETS.md).

| Dataset | Content | Size | Link |
|---|---|---|---|
| Shin 2017 hybrid EEG+NIRS (TU Berlin) | Left/right motor imagery; mental arithmetic vs rest; includes motion and physiology channels | 29 subjects | [doc.ml.tu-berlin.de/hBCI](https://doc.ml.tu-berlin.de/hBCI/), [paper](https://doi.org/10.1109/TNSRE.2016.2628057) |
| Shin 2018 EEG+NIRS cognitive | n-back, discrimination/selection response, word generation | 26 subjects, 36 NIRS channels | [Sci. Data](https://pmc.ncbi.nlm.nih.gov/articles/PMC5810421) |
| Bak 2019 finger/foot tapping | Left hand, right hand, foot tapping, 25 trials each; LIGHTNIRS 8 sources × 8 detectors | 30 subjects; 3-class SVM 70.4% ± 18.4% | [Korea Univ.](https://scholar.korea.ac.kr/handle/2021.sw.korea/61475) |
| Tufts fNIRS2MW | n-back mental workload, 4 levels, with a standardized cross-subject benchmark | 68 recommended (87 total) participants, ~21 min each | [NeurIPS 2021](https://datasets-benchmarks-proceedings.neurips.cc/paper_files/paper/2021/file/bd686fd640be98efaae0091fa301e613-Paper-round2.pdf), [code](https://github.com/tufts-ml/fNIRS-mental-workload-classifiers) |
| WashU HD-DOT naturalistic viewing (ds004569) | 10-min movie clip; ~1200 measurements; NeuroDOT, SNIRF and NIfTI; CC0 | 58 adults, 106 sessions | [OpenNeuro mirror](https://github.com/OpenNeuroDatasets/ds004569) |
| BIDS-NIRS finger tapping | Left/right thumb tapping vs control; NIRx with short channels; reference BIDS example | 5 participants | [GitHub](https://github.com/rob-luke/BIDS-NIRS-Tapping) |
| Public fNIRS dataset list | Community index of shared fNIRS datasets | — | [hubandad/fnirs-dataset](https://github.com/hubandad/fnirs-dataset) |

## 10. GitHub repositories

Stars and dates checked via the GitHub API on 2026-10-11.

"Custom" means GitHub could not detect a standard license (`NOASSERTION`), so read the repo's LICENSE file before reusing the code. "—" means no license file or no detected language.

**Toolkits and libraries**

| Repo | What it does / when to use it | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [mne-tools/mne-nirs](https://github.com/mne-tools/mne-nirs) | Extends MNE-Python's fNIRS support with GLM analysis, data-quality metrics, plotting and file-format support (incl. SNIRF). Start here in Python | Python | 116 | 2026-10 | BSD-3-Clause |
| [ibs-lab/cedalion](https://github.com/ibs-lab/cedalion) | Python fNIRS/DOT analysis toolbox from TU Berlin's IBS lab ([docs](https://doc.ibs.tu-berlin.de/cedalion/doc/dev/)); used by the 2026 deep-learning tutorial | Python | 83 | 2026-10 | MIT |
| [BUNPC/Homer3](https://github.com/BUNPC/Homer3) | The standard MATLAB GUI and pipeline for fNIRS (successor of HOMER2); reads SNIRF and `.nirs` | MATLAB | 133 | 2024-08 | — |
| [huppertt/nirs-toolbox](https://github.com/huppertt/nirs-toolbox) | NIRS Brain AnalyzIR toolbox (Huppert lab, Pittsburgh): statistical analysis for task and resting-state studies, incl. AR-IRLS GLM | HTML (MATLAB code) | 125 | 2026-10 | — |
| [BUNPC/AtlasViewer](https://github.com/BUNPC/AtlasViewer) | Probe design, sensitivity maps and image reconstruction on atlas anatomy | MATLAB | 47 | 2025-02 | Custom |
| [WUSTL-ORL/NeuroDOT](https://github.com/WUSTL-ORL/NeuroDOT) | HD-DOT processing and reconstruction toolbox from WashU | MATLAB | 22 | 2026-10 | Custom |
| [DOT-HUB/DOT-HUB_toolbox](https://github.com/DOT-HUB/DOT-HUB_toolbox) | UCL pipeline from raw fNIRS/HD-DOT data to images (LUMO users) | MATLAB | 21 | 2024-12 | GPL-3.0 |
| [Nirstorm/nirstorm](https://github.com/Nirstorm/nirstorm) | fNIRS plugin for Brainstorm: GLM statistics and optimal montages for a cortical region of interest | MATLAB | 46 | 2026-10 | GPL-3.0 |
| [brainstorm-tools/brainstorm3](https://github.com/brainstorm-tools/brainstorm3) | Multimodal MEG/EEG/fNIRS analysis app | MATLAB | 488 | 2026-10 | GPL-3.0 |
| [fieldtrip/fieldtrip](https://github.com/fieldtrip/fieldtrip) | MEG/EEG toolbox that also reads and analyses NIRS data | MATLAB | 990 | 2026-10 | GPL-3.0 |
| [bnuhouxin/NIRS-KIT](https://github.com/bnuhouxin/NIRS-KIT) | Task and resting-state fNIRS analysis with a GUI | MATLAB | 24 | 2025-10 | Custom |
| [ppsp-team/HyPyP](https://github.com/ppsp-team/HyPyP) | Hyperscanning pipeline: inter-brain connectivity for EEG/fNIRS | Python | 104 | 2026-10 | BSD-3-Clause |
| [frankfishburn/TDDR](https://github.com/frankfishburn/TDDR) | Temporal Derivative Distribution Repair motion correction (also built into MNE) | MATLAB | 17 | 2020-04 | MIT |
| [lpollonini/qt-nirs](https://github.com/lpollonini/qt-nirs) | QT-NIRS: automated signal-quality testing of fNIRS channels | MATLAB | 23 | 2026-08 | Custom |
| [HanBnrd/NIRSimple](https://github.com/HanBnrd/NIRSimple) | Small Python package: intensity to optical density to haemoglobin (MBLL), on NumPy arrays, MNE-compatible | Python | 16 | 2024-06 | MIT |
| [fangq/mcx](https://github.com/fangq/mcx) | GPU Monte Carlo photon transport: forward models and sensitivity for DOT | Pascal (C/CUDA core) | 194 | 2026-09 | Custom |
| [nirfaster/NIRFASTer](https://github.com/nirfaster/NIRFASTer) | Finite-element diffuse-optics modelling and reconstruction | HTML (MATLAB) | 13 | 2022-05 | Custom |
| [toastpp/toastpp](https://github.com/toastpp/toastpp) | Toast++: forward and inverse modelling in optical tomography | C | 46 | 2022-04 | GPL-3.0 |

**Formats and data standards**

| Repo | What it does / when to use it | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [fNIRS/snirf](https://github.com/fNIRS/snirf) | The SNIRF format specification | — | 81 | 2026-08 | Custom |
| [BUNPC/pysnirf2](https://github.com/BUNPC/pysnirf2) | Read, write and validate SNIRF files in Python | Python | 26 | 2026-04 | GPL-3.0 |
| [BUNPC/snirf2bids](https://github.com/BUNPC/snirf2bids) | Generate BIDS-NIRS sidecar files from SNIRF | Python | 4 | 2025-09 | MIT |
| [mne-tools/mne-bids](https://github.com/mne-tools/mne-bids) | Read and write BIDS (including NIRS) from MNE | Python | 182 | 2026-10 | BSD-3-Clause |
| [fNIRS/snirf-samples](https://github.com/fNIRS/snirf-samples) | Example SNIRF files for testing loaders | MATLAB | 5 | 2025-03 | Custom |
| [Gowerlabs/lumomat](https://github.com/Gowerlabs/lumomat) | Load LUMO data and export to SNIRF | MATLAB | 13 | 2026-05 | MIT |

**Models and papers with code**

| Repo | What it does / when to use it | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [wzhlearning/fNIRS-Transformer](https://github.com/wzhlearning/fNIRS-Transformer) | fNIRS-T transformer classifier ([Wang et al. 2022, IEEE JBHI](https://doi.org/10.1109/JBHI.2022.3140531)) | Python | 97 | 2026-05 | MIT |
| [wzhlearning/fNIRSNet](https://github.com/wzhlearning/fNIRSNet) | Small CNN built around the delayed hemodynamic response ([Wang et al. 2023, TNSRE](https://doi.org/10.1109/TNSRE.2023.3330911)) | Python | 36 | 2026-05 | Apache-2.0 |
| [wzhlearning/fNIRS4D](https://github.com/wzhlearning/fNIRS4D) | State-space model with fNIRS domain knowledge for BCI | Python | 5 | 2026-06 | Apache-2.0 |
| [MutianLiu-SHU/STA-Net](https://github.com/MutianLiu-SHU/STA-Net) | STA-Net: spatial–temporal alignment network for hybrid EEG-fNIRS decoding (2025) | Python | 46 | 2025-03 | — |
| [YuanyuanGao216/fNIRS_denoise_by_DL](https://github.com/YuanyuanGao216/fNIRS_denoise_by_DL) | Deep-learning motion-artifact removal | MATLAB | 13 | 2022-04 | — |
| [theeksnd/fnirsdl_tutorial](https://github.com/theeksnd/fnirsdl_tutorial) | Companion to the 2026 deep-learning review: four models on two datasets with session-wise splits, built on Cedalion | Python | 2 | 2026-07 | — |

**Benchmarks and dataset loaders**

| Repo | What it does / when to use it | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [HanBnrd/BenchNIRS](https://github.com/HanBnrd/BenchNIRS) | Benchmark framework with nested cross-validation on five open fNIRS BCI datasets ([paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC10790918)) | Python | 7 | 2025-06 | MIT |
| [tufts-ml/fNIRS-mental-workload-classifiers](https://github.com/tufts-ml/fNIRS-mental-workload-classifiers) | Official fNIRS2MW benchmark code (NeurIPS 2021) | Jupyter Notebook | 34 | 2021-11 | MIT |
| [rob-luke/BIDS-NIRS-Tapping](https://github.com/rob-luke/BIDS-NIRS-Tapping) | Reference BIDS-NIRS dataset with conversion scripts | — | 15 | 2022-11 | — |
| [OpenNeuroDatasets/ds004569](https://github.com/OpenNeuroDatasets/ds004569) | DataLad mirror of the WashU HD-DOT naturalistic-viewing dataset | — | 2 | 2025-09 | — (data CC0) |
| [hubandad/fnirs-dataset](https://github.com/hubandad/fnirs-dataset) | List of public fNIRS datasets with access links | — | 58 | 2023-05 | — |

**Hardware and firmware**

| Repo | What it does / when to use it | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [BUNPC/NN24_25-Hardware-Firmware](https://github.com/BUNPC/NN24_25-Hardware-Firmware) | Hardware, mechanical and firmware files for the ninjaNIRS 2024 whole-head system | VHDL | 5 | 2026-07 | — |
| [BUNPC/NN22-Technical-Documents](https://github.com/BUNPC/NN22-Technical-Documents) | Technical files for ninjaNIRS 2022 (the system in O'Brien et al. 2024) | C | 10 | 2025-02 | — |
| [BUNPC/ninjaGUI](https://github.com/BUNPC/ninjaGUI) | Acquisition GUI for ninjaNIRS hardware | MATLAB | 16 | 2026-01 | — |
| [BUNPC/ninjaCap2](https://github.com/BUNPC/ninjaCap2) | Generates 3D-printable caps for a given probe layout and head size | MATLAB | 3 | 2025-09 | — |

**Curated lists**

| Repo | What it does / when to use it | Language | Stars | Last update | License |
|---|---|---|---|---|---|
| [NeuroTechX/awesome-bci](https://github.com/NeuroTechX/awesome-bci) | General BCI resource list that includes fNIRS | — | 1551 | 2026-10 | — |
| [analyticalmonk/awesome-neuroscience](https://github.com/analyticalmonk/awesome-neuroscience) | Neuroscience software list that includes fNIRS tools | — | 1732 | 2026-06 | — |
| [willxxy/awesome-mmps](https://github.com/willxxy/awesome-mmps) | Multimodal ML with physiological signals, including fNIRS | — | 167 | 2026-07 | MIT |
