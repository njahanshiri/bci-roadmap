# ECG datasets: specifications and benchmark results

This file is a companion to [README.md](README.md). Every number comes with the link where it was read, mostly primary sources: PhysioNet pages, WFDB headers, dataset papers and official challenge results. Papers with Code shut down in 2025, so nothing here comes from it.

How to read the markings:
- **"not reported"** means the source does not give the value.
- **⚠** marks a conflict or uncertainty found in the sources.
- **[secondary]** means the number was read in a paper citing the original, not in the original itself.

Sources were checked on 2026-10-10/11.

## Overview

| Dataset | Patients | Records | Leads | Hz | Length | Labels | License |
|---|---|---|---|---|---|---|---|
| [MIT-BIH Arrhythmia](https://physionet.org/content/mitdb/1.0.0/) | 47 | 48 | 2 | 360 | ~30 min | Beat labels from ≥2 cardiologists (~110k beats) | ODC-By 1.0 |
| [INCART](https://physionet.org/content/incartdb/1.0.0/) | 32 | 75 | 12 | 257 | 30 min | Beat labels, algorithm then manual correction (>175k) | ODC-By 1.0 |
| [PTB](https://physionet.org/content/ptbdb/1.0.0/) | 290 | 549 | 15 (12 + Frank) | 1000 | Variable | One diagnosis per subject | ODC-By 1.0 |
| [PTB-XL](https://physionet.org/content/ptb-xl/1.0.3/) | 18,869 | 21,799 (v1.0.3) | 12 | 500 (+100) | 10 s | 71 SCP-ECG statements, cardiologist plus device | CC BY 4.0 |
| [CPSC 2018](http://2018.icbeb.org/Challenge.html) | 9,458 incl. Extra | 6,877 train + 2,954 hidden | 12 | 500 | 6–60 s | 9 rhythm/morphology classes | Not stated |
| [Chapman-Shaoxing](https://pmc.ncbi.nlm.nih.gov/articles/PMC7016169/) | 10,646 | 10,646 | 12 | 500 | 10 s | 11 rhythms + 67 conditions, physicians | CC BY 4.0 |
| [Ningbo](https://physionet.org/content/ecg-arrhythmia/1.0.0/) | not reported | 34,905 | 12 | 500 | 10 s | SNOMED-CT, physicians | CC BY 4.0 |
| [Georgia (G12EC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8015789/) | 15,742 | 20,678 | 12 | 500 | 5–10 s | SNOMED-CT | CC BY 4.0 (training part) |
| [CinC 2017 (AF)](https://physionet.org/content/challenge-2017/1.0.0/) | not reported | 8,528 + 3,658 hidden | 1 | 300 | 9–61 s | Normal/AF/Other/Noisy | ODC-By 1.0 |
| [CinC 2020](https://physionet.org/content/challenge-2020/1.0.2/) | multi-source | 66,361 (43,101 public) | 12 | 257–1000 | Variable | 27 scored SNOMED-CT | CC BY 4.0 |
| [CinC 2021](https://physionet.org/content/challenge-2021/1.0.3/) | multi-source | 131,149 (88,253 public) | 12/6/4/3/2 | 250–1000 | Variable | 30 scored SNOMED-CT | CC BY 4.0 |
| [CODE](https://pmc.ncbi.nlm.nih.gov/articles/PMC7145824/) | 1,676,384 | 2,322,513 | 12 | 400 (resampled) | 7–10 s | 6 classes, automatic + text reports + review | Restricted |
| [CODE-15%](https://zenodo.org/records/4916206) | 233,770 | 345,779 | 12 | 400 | 7/10 s (4096 padded) | Same 6 classes, normal flag, mortality | CC BY 4.0 |
| [CODE-test](https://zenodo.org/records/3765780) | 827 | 827 | 12 | 400 | 7/10 s | 2 cardiologists + senior | CC BY 4.0 |
| [MIMIC-IV-ECG](https://physionet.org/content/mimic-iv-ecg/1.0/) | ~160,000 | ~800,000 | 12 | 500 | 10 s | Machine reports; ~600k cardiologist reports | ODbL 1.0 |
| [HEEDB](https://bdsp.io/content/heedb/) | 1,818,247 (MGH) + Emory | 10,608,417 (MGH) + Emory ⚠ | 12 | 250/500 | 10 s | GE 12SL, physician overreads, ICD codes | BDSP credentialed ⚠ |
| [Apnea-ECG](https://physionet.org/content/apnea-ecg/1.0.0/) | not reported | 70 | 1 | 100 | 7–10 h | Apnea/normal per minute, experts | ODC-By 1.0 |
| [WESAD (ECG)](https://www.eti.uni-siegen.de/ubicomp/papers/ubi_icmi2018.pdf) | 15 | 15 | 1 (chest) | 700 | ~2 h | Protocol condition (baseline/stress/amusement) | Non-commercial |
| [CinC 2025 Chagas](https://moody-challenge.physionet.org/2025/) | multi-source | 345,779 + 1,631 + 21,799 public | 12 | 300–1000 | ~7–10 s | Chagas, self-reported or serology | CC BY 4.0 (public parts) |

# Part 1: Dataset specifications

## MIT-BIH Arrhythmia Database (mitdb v1.0.0)

Sources: [P1](https://physionet.org/content/mitdb/1.0.0/), [P2](https://physionet.org/physiobank/database/html/mitdbdir/intro.htm), [H](https://physionet.org/files/mitdb/1.0.0/100.hea)

| Field | Value |
|---|---|
| Year & paper | Recorded 1975–79; distributed from 1980; PhysioNet v1.0.0 dated 2005-02-24. Cite Moody & Mark, IEEE EMB Mag 2001 [P1] |
| Subjects | 48 records from 47 subjects; ~60% inpatients, 40% outpatients, Beth Israel Hospital [P1]. 25 men aged 32–89 and 22 women aged 23–89 [P2]. Records 201 and 202 are the same subject ([Zhang 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8181174/)) |
| Device | Del Mar Avionics 445 two-channel Holter; played back on Del Mar 660 [P2] |
| Leads | 2. Usually MLII plus modified V1. Records 102/104 have modified V5 on top; 114 is reversed [P2] |
| Sampling rate | 360 Hz [P1] |
| Resolution | 11-bit over 10 mV [P1]; band-pass 0.1–100 Hz [P2]; gain 200 adu/mV, format 212 [H] |
| Record length | Half-hour excerpts; record 100 is 650,000 samples (~30.1 min) [H] |
| Records | 48 [P1] |
| Labels | ~110,000 beat annotations. Two or more cardiologists annotated independently and resolved disagreements [P1] |
| Class balance (AAMI, de Chazal split) | DS1: N 45,683, S 944, V 3,778, F 413, Q 8. DS2: N 44,082, S 1,831, V 3,208, F 388, Q 7 ([Zhang 2021, Table 2](https://pmc.ncbi.nlm.nih.gov/articles/PMC8181174/)). The DS1 and DS2 V totals were summed by the helper because the table was garbled. ⚠ Papers count differently: Garcia 2017 has DS1 S 782 and DS2 S 1,808 ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC5585360/)); Mondéjar-Guerra 2019 has DS2 N 44,033, S 2,050, V 3,220, F 388 ([PDF](https://ruc.udc.es/bitstreams/27ee7d17-9c5e-41d6-903f-85801556010c/download)) |
| Size | 104.3 MB uncompressed; 73.5 MB zip [P1] |
| Format | WFDB `.dat` (212), `.hea`, `.atr`, `.xws` [P1] |
| Access & license | Open; ODC Attribution v1.0 [P1] |
| Standard splits | De Chazal 2004 inter-patient split ([Zou 2022, Table 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC9455809/)).<br>**DS1 (train):** 101, 106, 108, 109, 112, 114, 115, 116, 118, 119, 122, 124, 201, 203, 205, 207, 208, 209, 215, 220, 223, 230.<br>**DS2 (test):** 100, 103, 105, 111, 113, 117, 121, 123, 200, 202, 210, 212, 213, 214, 219, 221, 222, 228, 231, 232, 233, 234.<br>Paced records 102, 104, 107 and 217 are excluded, leaving 44 records ([de Chazal abstract](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=15248536&rettype=abstract&retmode=text)) |
| Known issues | **Records 201 (DS1) and 202 (DS2) are the same subject**, so the split is not strictly patient-disjoint. The 102.atr annotation was shifted in 2018 (original kept as 102-0.atr) [P1]. Leads are not uniform. Only 47 patients |

## St Petersburg INCART 12-lead Arrhythmia Database (incartdb v1.0.0)

Sources: [I1](https://physionet.org/content/incartdb/1.0.0/), [IH](https://physionet.org/files/incartdb/1.0.0/I01.hea)

| Field | Value |
|---|---|
| Year & paper | PhysioNet 2008-05-01. No original dataset paper; PhysioNet asks you to cite its platform paper [I1] |
| Subjects | 32 patients tested for coronary artery disease; 17 men, 15 women, aged 18–80 (mean 58). No pacemakers; most had ventricular ectopy [I1] |
| Device | Holter recordings from the St Petersburg Institute of Cardiological Technics; model not reported [I1] |
| Leads | 12 [I1] |
| Sampling rate | 257 Hz [I1] |
| Resolution | Gain 250–1100 adu/mV, varying by record; stored 16-bit (I01 gain 306) [I1][IH]. ADC bits not reported |
| Record length | 30 min [I1] |
| Records | 75, extracted from 32 Holter records [I1] |
| Labels | >175,000 beat annotations; algorithm first, then manual correction [I1] |
| Class balance | Not reported |
| Size | 794.5 MB uncompressed [I1] |
| Format | WFDB `.dat`, `.hea`, `.atr` [I1] |
| Access & license | Open; ODC Attribution v1.0 [I1] |
| Standard splits | None. Split by patient number, because several records share one Holter recording [I1] |
| Known issues | Annotation positions were not manually corrected, so some may be misaligned. Headers were fixed in 2015 [I1] |

## PTB Diagnostic ECG Database (ptbdb v1.0.0)

Sources: [T1](https://physionet.org/content/ptbdb/1.0.0/), [TH](https://physionet.org/files/ptbdb/1.0.0/patient001/s0010_re.hea)

| Field | Value |
|---|---|
| Year & paper | Bousseljot et al., Biomed Tech 1995; PhysioNet 2004 [T1] |
| Subjects | 290 subjects aged 17–87 (mean 57.2); 209 men, 81 women; patients and healthy volunteers, Berlin [T1] |
| Device | Non-commercial PTB prototype, 16 channels, 0–1 kHz bandwidth [T1] |
| Leads | 15: 12 standard plus Frank vx, vy, vz [T1] |
| Sampling rate | 1000 Hz (up to 10 kHz on request) [T1] |
| Resolution | 16-bit, 0.5 µV/LSB, ±16.384 mV [T1][TH] |
| Record length | Variable; e.g. s0010_re is 38.4 s [TH] |
| Records | 549 (1–5 per subject) [T1] |
| Labels | Diagnosis per subject from the clinical summary in `.hea`; missing for 22 subjects [T1] |
| Class balance (268 subjects) | MI 148, cardiomyopathy/HF 18, BBB 15, dysrhythmia 14, hypertrophy 7, valvular 6, myocarditis 4, misc 4, healthy 52 [T1] |
| Size | 1.7 GB [T1] |
| Format | WFDB (format 16), `.hea` with clinical summary, `.xyz` [T1] |
| Access & license | Open; ODC Attribution v1.0 [T1] |
| Standard splits | None reported |
| Known issues | Heavy MI imbalance. Multiple records per subject, so split by patient. Subject numbers 124, 132, 134 and 161 are absent [T1] |

## PTB-XL (v1.0.3)

Sources: [PhysioNet](https://physionet.org/content/ptb-xl/1.0.3/), [Wagner 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7248071/), [Strodthoff 2021](https://arxiv.org/pdf/2004.13701)

| Field | Value |
|---|---|
| Year & paper | Wagner et al., Sci Data 2020; v1.0.3 released 2022-11-09 |
| Subjects | 18,869 patients in v1.0.3 (18,885 in the paper). Age 0–95, median 62; 52% male. Recorded 1989–1996 |
| Device | Schiller AG |
| Leads | 12 |
| Sampling rate | 500 Hz plus a 100 Hz version. The paper says the original rate was 400 Hz |
| Resolution | 16-bit, 1 µV/LSB |
| Record length | 10 s |
| Records | **21,799 in v1.0.3; 21,837 in the paper and v1.0.1** |
| Labels | 71 SCP-ECG statements: 44 diagnostic, 19 form, 12 rhythm. Diagnostic statements group into 5 superclasses and subclasses. Annotated by up to two cardiologists. 67.13% are manual interpretations and 31.2% are device-generated ([Wagner](https://pmc.ncbi.nlm.nih.gov/articles/PMC7248071/)). ⚠ Subclass count is 24 in Wagner 2020 and in Strodthoff's Sec. II and Table I, but 23 in Strodthoff's Sec. IV; MERL uses 23 |
| Class balance (superclass) | NORM 9,514; MI 5,469; STTC 5,235; CD 4,898; HYP 2,649. About 12k ECGs have no form label (Strodthoff) |
| Size | 3.0 GB uncompressed; 1.7 GB zip |
| Format | WFDB |
| Access & license | Open; CC BY 4.0 |
| Standard splits | `strat_fold` 1–10: folds 1–8 train, 9 validation, 10 test. Folds 9 and 10 had at least one human evaluation |
| Known issues | 26.3% of records are not validated by a human. v1.0.2 removed 36 duplicate waveforms and v1.0.3 removed two more. ⚠ Challenges 2020/2021 used v1.0.1 (21,837 records), which still contains the duplicates ([PhysioNet 2021](https://physionet.org/content/challenge-2021/1.0.3/)) |

## CPSC 2018 (China Physiological Signal Challenge)

Sources: [challenge page](http://2018.icbeb.org/Challenge.html), [Perez Alday 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC8015789/)

| Field | Value |
|---|---|
| Year & paper | Liu F. et al., JMIHI 2018;8(7):1368–1373. The paper itself was not read; fields come from the challenge page |
| Subjects | 11 hospitals. Training set has 3,178 female and 3,699 male recordings. 9,458 patients including CPSC-Extra (Perez Alday) |
| Device | Not reported |
| Leads | 12 |
| Sampling rate | 500 Hz |
| Resolution | Not reported for the original files. The Challenge WFDB version is 16-bit at 1000/mV ([A0001.hea](https://physionet.org/files/challenge-2021/1.0.3/training/cpsc_2018/g1/A0001.hea)) |
| Record length | 6–60 s (6–144 s including CPSC-Extra, per [2021 page](https://moody-challenge.physionet.org/2021/)) |
| Records | 6,877 training; 2,954 hidden test; 3,453 CPSC-Extra released in 2020 ([2020 page](https://moody-challenge.physionet.org/2020/)) |
| Labels | 9 classes: Normal, AF, I-AVB, LBBB, RBBB, PAC, PVC, STD, STE. Mostly one label each, up to three |
| Class balance (training, first label) | Normal 918, AF 1,098, I-AVB 704, LBBB 207, RBBB 1,695, PAC 556, PVC 672, STD 825, STE 202 |
| Size | Not reported |
| Format | MATLAB `.mat` plus REFERENCE.csv |
| Access & license | Training set free to download; license not stated |
| Standard splits | Hidden test set. Challenges 2020 and 2021 reused it as 1,463 validation and 1,463 test records (⚠ 2,926 in total, not 2,954) |
| Known issues | Not reported |

## Chapman-Shaoxing

Sources: [Zheng 2020, Sci Data](https://pmc.ncbi.nlm.nih.gov/articles/PMC7016169/), [CinC 2021](https://moody-challenge.physionet.org/2021/)

| Field | Value |
|---|---|
| Year & paper | Zheng et al., Sci Data 2020 (figshare doi 10.6084/m9.figshare.c.4560497.v2) |
| Subjects | 10,646 patients aged 4–98; 5,956 male, 4,690 female; Shaoxing People's Hospital |
| Device | GE MUSE ECG system (cart model not given) |
| Leads / rate / length | 12 / 500 Hz / 10 s |
| Resolution | "4.88" volts per A/D bit with a "32-bit" converter, amplitude in µV. ⚠ The unit is ambiguous. The Challenge WFDB version is 16-bit at 1000/mV ([JS00001.hea](https://physionet.org/files/challenge-2021/1.0.3/training/chapman_shaoxing/g1/JS00001.hea)) |
| Records | 10,646 |
| Labels | 11 rhythms and 67 other conditions. One physician labels, a second validates, a senior physician arbitrates |
| Class balance | Largest class is sinus bradycardia (3,889); the rarest rhythm has 7 records |
| Size | Not reported |
| Format | CSV (5000×12), raw and denoised |
| Access & license | Open; CC BY 4.0 |
| Standard splits | None |
| Known issues | Records with electrode errors were excluded; no count given. ⚠ Challenge 2021 contains 10,247 Chapman records, not 10,646, with no reason found |

## Ningbo (part of PhysioNet "ecg-arrhythmia" v1.0.0)

Sources: [PhysioNet](https://physionet.org/content/ecg-arrhythmia/1.0.0/), [Reyna 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9469795/)

| Field | Value |
|---|---|
| Year & paper | No standalone paper. Cite Zheng Sci Data 2020 and Zheng Sci Rep 2020;10:2898. Published on PhysioNet 2022-08-24 |
| Subjects | Mean age 57.7; 43% female, 56% male (Reyna 2022 Table 4). Patient count not reported |
| Device | GE MUSE |
| Leads / rate / length | 12 / 500 Hz / 10 s |
| Resolution | Same "4.88 per A/D bit, 32-bit" description as Chapman |
| Records | 34,905 Ningbo records ([2021 page](https://moody-challenge.physionet.org/2021/)). The combined PhysioNet set has 45,152 |
| Labels | Physicians, using the same scheme as Chapman, mapped to SNOMED-CT |
| Class balance | Not reported |
| Size | 5.1 GB uncompressed for the combined set |
| Format | WFDB (`.mat` + `.hea`) |
| Access & license | Open; CC BY 4.0 |
| Standard splits | None |
| Known issues | None listed by PhysioNet. ⚠ No primary source checks for Chapman/Ningbo duplicates. A duplicate study ([Leinonen 2024](https://arxiv.org/pdf/2403.15012)) concerns the SPH dataset and says it "could not" check the CinC data |

## Georgia 12-lead ECG Challenge Database (G12EC)

Sources: [Perez Alday 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC8015789/), [Reyna 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9469795/)

| Field | Value |
|---|---|
| Year & paper | Perez Alday et al., Physiol Meas 2020 |
| Subjects | 15,742 patients; mean age 60.5; 54% male; Emory University Hospital, Atlanta |
| Device | Not reported |
| Leads / rate / length | 12 / 500 Hz / 5–10 s |
| Resolution | 16-bit at 1000/mV ([E00001.hea](https://physionet.org/files/challenge-2021/1.0.3/training/georgia/g1/E00001.hea)) |
| Records | 20,678: 10,344 training, 5,167 validation, 5,167 test. ⚠ The 2021 page gives 20,672 total and 5,161 test |
| Labels | SNOMED-CT |
| Class balance | Not reported |
| Size | Not reported separately |
| Format | WFDB |
| Access & license | Training part only; CC BY 4.0 |
| Standard splits | The validation and test parts are hidden |
| Known issues | See CinC 2020 label-quality note |

## PhysioNet/CinC Challenge 2017: AF from short single-lead ECG

Sources: [C1](https://physionet.org/content/challenge-2017/1.0.0/), [Clifford 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5978770), [CH](https://physionet.org/files/challenge-2017/1.0.0/training/A00/A00001.hea)

| Field | Value |
|---|---|
| Year & paper | Clifford et al., CinC 2017 |
| Subjects | Patient-initiated recordings; patient count not reported |
| Device | AliveCor [C1] |
| Leads | 1 |
| Sampling rate | 300 Hz |
| Resolution | 16-bit, 0.5–40 Hz, ±5 mV [Clifford]; gain 1000/mV [CH] |
| Record length | 9 s to just over 60 s; mean 32.5 s, median 30 s |
| Records | 8,528 training; 3,658 hidden test; 12,186 total |
| Labels | Normal, AF, Other rhythm, Too noisy. Originally one expert per record. The 1,129 most disputed were relabeled by 8 experts; κ = 0.245 [Clifford] |
| Class balance (training) | Normal 5,154; AF 771; Other 2,557; Noisy 46 (original REFERENCE-v0 labels, as on the project page). Final REFERENCE-v3: Normal 5,076; AF 758; Other 2,415; Noisy 279 |
| Size | Training zip 94.6 MB; whole-project zip 1.4 GB |
| Format | MATLAB v4 WFDB `.mat` + `.hea`; REFERENCE-v0 to v3 `.csv` |
| Access & license | Open; ODC Attribution v1.0 |
| Standard splits | 8,528 train / 3,658 hidden test |
| Known issues | Labels revised across v0–v3; low inter-expert agreement. **The official score uses 3 classes (Noisy excluded), although the project page shows a 4-class formula** (see Part 2) |

## PhysioNet/CinC Challenge 2020

Sources: [Perez Alday 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC8015789/), [PhysioNet 1.0.2](https://physionet.org/content/challenge-2020/1.0.2/), [2020 page](https://moody-challenge.physionet.org/2020/)

| Field | Value |
|---|---|
| Records | 66,361 from 6 hospital systems. Public training 43,101: CPSC 6,877; CPSC-Extra 3,453; INCART 74; PTB 516; PTB-XL 21,837; Georgia 10,344 |
| Hidden sets | 6,630 validation; 16,630 test (CPSC 1,463, G12EC 5,167, Undisclosed 10,000) |
| Labels | 27 scored of 111 diagnoses, SNOMED-CT |
| Sampling rate | 257 Hz (INCART), 500 Hz, 1000 Hz (PTB); Undisclosed is 300 Hz |
| Size / format / license | 7.5 GB; WFDB `.mat` + `.hea`; CC BY 4.0 |
| Known issues | "Bound to be some errors or debatable labels". Label provenance differs between sources |

## PhysioNet/CinC Challenge 2021 ("Will Two Do?")

Sources: [Reyna 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9469795/), [2021 page](https://moody-challenge.physionet.org/2021/), [PhysioNet 1.0.3](https://physionet.org/content/challenge-2021/1.0.3/)

| Field | Value |
|---|---|
| Records | 131,149 total; 88,253 public training; 6,630 validation; 36,266 test |
| New sources | Chapman-Shaoxing 10,247; Ningbo 34,905; UMich 19,642 (test only, 250 or 500 Hz) |
| Lead sets | 12; 6 (I, II, III, aVR, aVL, aVF); 4 (I, II, III, V2); 3 (I, II, V2); 2 (I, II) |
| Labels | 30 scored of 133 diagnoses, SNOMED-CT |
| Size / license | 12.6 GB; CC BY 4.0 |
| Splits | Recordings from the same person stay in one split |
| Known issues | "Some of the data and labels are likely to have errors". Contains PTB-XL v1.0.1 duplicates |

## CODE (full)

Source: [Ribeiro 2020, Nat Commun](https://pmc.ncbi.nlm.nih.gov/articles/PMC7145824/)

| Field | Value |
|---|---|
| Subjects | 1,676,384 patients in 811 counties of Minas Gerais, Brazil (Telehealth Network). 60.3% female. Age bands: 16–25 6.7%, 26–40 17.5%, 41–60 38.8%, 61–80 31.4%, ≥81 5.6% |
| Device | TEB ECGPC or Micromed ErgoPC 13 |
| Leads / rate / length | 12 / 300–600 Hz resampled to 400 Hz / 7–10 s, zero-padded to 4096 samples |
| Resolution | Not reported |
| Records | 2,322,513 |
| Labels | 1dAVb, RBBB, LBBB, SB, AF, ST. Combined from Glasgow automatic analysis, Minnesota codes, and cardiologist text reports (parsed with a Lazy Associative Classifier), plus manual review of 34,512 ambiguous exams |
| Class balance | 1dAVb 1.5%, RBBB 2.7%, LBBB 1.7%, SB 1.6%, AF 1.8%, ST 2.1% |
| Splits | 98% train, 2% validation |
| Size / format | Not reported |
| Access | "Restrictions apply to the availability of the training set" |

## CODE-15%

Source: [Zenodo 4916206](https://zenodo.org/records/4916206)

| Field | Value |
|---|---|
| Year | v1.0.0, 2021-06-09; data collected 2010–2016 |
| Subjects | 233,770 patients; a stratified 15% patient sample of CODE |
| Leads / rate / length | 12 (DI, DII, DIII, AVR, AVL, AVF, V1–V6) / 400 Hz / 7 s (2800 samples) or 10 s (4000 samples), zero-padded to 4096 |
| Resolution | Not stated on Zenodo. The 2025 Challenge WFDB version is 16-bit at 1000 adu/mV ([2025 page](https://moody-challenge.physionet.org/2025/)) |
| Records | 345,779 |
| Labels | Binary 1dAVb, RBBB, LBBB, SB, AF, ST; `normal_ecg` (from the automatic system); death and time-to-event (first exam only); age and sex |
| Size | 46.3 GB (summed from the [Zenodo API](https://zenodo.org/api/records/4916206)) |
| Format | `exams.csv` plus 18 HDF5 parts; `tracings` has shape (N, 4096, 12) |
| Access & license | Open; CC BY 4.0 |
| Known issues | ⚠ The h5py example in the description uses different key names from the text. The 2025 Challenge describes the durations as 7.3 s and 10.2 s |

## CODE-test

Sources: [Zenodo 3765780](https://zenodo.org/records/3765780), [Ribeiro 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7145824/)

| Field | Value |
|---|---|
| Records / subjects | 827 exams from 827 patients; 61.2% female |
| Signal | 12 leads, 400 Hz, HDF5 (827, 4096, 12) |
| Labels | Two cardiologists annotated independently; a senior specialist resolved disagreements. κ ranges from 0.741 (1dAVb) to 0.964 (LBBB). Also includes annotations from residents and students, and the DNN's predictions |
| Class balance | Prevalence 1.6–4.4%. Counts: SB 16, AF 13, ST 37 (⚠ Ribeiro 2020 Table 1 gives 36), RBBB 34, LBBB 30, 1dAVb 28 ([ECGFounder Table 2](https://pmc.ncbi.nlm.nih.gov/articles/PMC12327759/)) |
| Size / license | 218.2 MB; CC BY 4.0 |
| Known issues | ⚠ The units note ("scale 1e-4V… multiplied by 1000 to obtain V") is internally inconsistent; check amplitudes yourself |

## MIMIC-IV-ECG v1.0

Source: [PhysioNet](https://physionet.org/content/mimic-iv-ecg/1.0/)

| Field | Value |
|---|---|
| Year & paper | Gow et al., published 2023-09-15 |
| Subjects | ~160,000 patients, 2008–2019, BIDMC (ED, inpatient including ICU, outpatient). Demographics not reported on the page |
| Device | Burdick/Spacelabs, Philips, GE |
| Leads / rate / length | 12 / 500 Hz / 10 s |
| Resolution | 16-bit at 200 adu/mV (5 µV/LSB), from one [example header](https://physionet.org/files/mimic-iv-ecg/1.0/files/p1000/p10001725/s41420867/41420867.hea); not checked for every record |
| Records | ~800,000; exact count not reported on the page |
| Labels | Machine reports (`machine_measurements.csv`); ~600,000 cardiologist reports linked through MIMIC-IV-Note |
| Size | 90.4 GB uncompressed; 33.8 GB zip |
| Format | WFDB |
| Access & license | Open; ODbL v1.0 |
| Standard splits | ~5% withheld as a hidden test set |
| Known issues | Machine clocks are unsynchronized, so timestamps "could be significantly out of sync" with the rest of MIMIC-IV |

## Harvard-Emory ECG Database (HEEDB)

Sources: [BDSP v5.0 (2026-02-25)](https://bdsp.io/content/heedb/), [preprint via Europe PMC](https://europepmc.org/article/PPR/PPR918411)

| Field | Value |
|---|---|
| Subjects / records | MGH: 10,608,417 ECGs from 1,818,247 patients. Emory: ⚠ 998,844 ECGs from 349,548 patients in the BDSP Methods text; 1,061,598 in the v3.0 notes; 1,452,964 from 552,481 patients in the preprint |
| Signal | 12 leads, 10 s, 250 or 500 Hz, 16-bit |
| Labels | GE 12SL v24 re-processing; original 12SL output plus physician overreads (v5.0); ICD-9/10 codes |
| Demographics | Not reported as summary statistics |
| Format | WFDB/Matlab v4 |
| Size | Not reported |
| Access & license | Credentialed access with DUA and CITI training. "BDSP Credentialed Health Data License 1.5.0"; ⚠ the [AWS registry](https://registry.opendata.aws/bdsp-heedb) says "Restricted Health Data License 1.0.0" |
| Known issues | Use v3.0 or later, which removed MGH duplicates and fixed wrong sampling frequencies. Emory metadata is incomplete |

## Apnea-ECG Database (CinC 2000)

Sources: [A1](https://physionet.org/content/apnea-ecg/1.0.0/), [A2](https://physionet.org/files/apnea-ecg/1.0.0/additional-information.txt), [A3](https://physionet.org/content/challenge-2000/1.0.0/), [AH](https://physionet.org/files/apnea-ecg/1.0.0/a01.hea)

| Field | Value |
|---|---|
| Year & paper | Penzel et al., Computers in Cardiology 27:255–258 (2000). The PDF was unavailable |
| Subjects | Men and women aged 27–63, BMI 20.3–42.1, AHI 0–93.5 [A3]. **Subject count is not stated.** The helper counted 32 distinct demographic profiles in [A2]; this is an inference, not an official number |
| Device | Not reported; data from Philipps-University Marburg |
| Leads | 1 ECG. Eight learning records also have respiration and SpO2 |
| Sampling rate | 100 Hz |
| Resolution | 12-bit ADC stored as 16-bit; 200 adu/mV [AH] |
| Record length | ~7 to ~10 h; 401–578 scored minutes |
| Records | 70: 35 learning (a01–a20, b01–b05, c01–c10) and 35 test (x01–x35) |
| Labels | One apnea/normal label per minute, by experts from respiration signals; hypopnea counts as apnea. The `.qrs` files are unaudited machine output |
| Class balance | Learning set 6,514 apnea vs 10,611 normal minutes; test set 6,552 vs 10,751 (summed from [A2]). The challenge scored 17,268 test minutes |
| Size | 580.6 MB |
| Format | WFDB `.dat`, `.hea`, `.apn`, `.qrs` |
| Access & license | Open; ODC Attribution v1.0 |
| Standard splits | 35 released / 35 withheld |
| Known issues | c05 and c06 are from the same recording. **Apparent subject overlap between learning and test sets** (e.g. a07, a16, x01 and x30 share one demographic profile). This is the helper's inference, not an official statement |

## WESAD (ECG part)

Sources: [Schmidt 2018](https://www.eti.uni-siegen.de/ubicomp/papers/ubi_icmi2018.pdf), [download page](https://ubi29.informatik.uni-siegen.de/usi/data_wesad.html), [UCI](https://archive.ics.uci.edu/dataset/465/wesad+wearable+stress+and+affect+detection)

| Field | Value |
|---|---|
| Year & paper | Schmidt et al., ICMI 2018 |
| Subjects | 15 kept of 17 (2 lost to sensor faults); age 27.5 ± 2.4; 12 male, 3 female; lab study |
| Device | RespiBAN Professional chest hub, three-point ECG (one channel) |
| Sampling rate | 700 Hz |
| Resolution | Not reported |
| Record length | ~2 h per subject; ~36 min of baseline, stress and amusement data used |
| Labels | Protocol condition: baseline, amusement, TSST stress, meditation. Self-reports included |
| Class balance (paper's windows) | ~133k windows: 53% baseline, 30% stress, 17% amusement |
| Size | 2.5 GB zipped |
| Format | Per-subject `.pkl` (not verified from a primary source) |
| Access & license | Scientific, non-commercial use with credit |
| Standard splits | Leave-one-subject-out (LOSO) |

## PhysioNet/Moody Challenge 2025: Chagas

Sources: [2025 page](https://moody-challenge.physionet.org/2025/), [Reyna et al. arXiv 2510.02202](https://arxiv.org/html/2510.02202)

| Field | Value |
|---|---|
| Public training | CODE-15%: 345,779 records, self-reported ("weak") labels, prevalence ~2% (Table 1: 1.92%).<br>SaMi-Trop: 1,631 records, all positive by serology, 400 Hz ([Zenodo 4905618](https://zenodo.org/records/4905618), CC BY 4.0, 264.6 MB).<br>PTB-XL: all assumed negative on geographic grounds, not tested |
| Hidden validation/test | REDS-II: 1,979 records from 631 patients, 300 Hz, serology; validation 1,419 (54.85% positive), test 560 (50.00%).<br>SaMi-Trop 3: 3,855 records (3,854 in the table); 28.50% positive.<br>ELSA-Brasil: 13,739 records, 2.04% positive, 300 Hz.<br>Negatives were oversampled and augmented to ~2% prevalence |
| Format | WFDB, 16-bit at 1000/mV. Zero-padding removed; ages >89 set to 90 |
| Metric | True positive rate among the top 5% of patients ranked by predicted probability |
| Participation | 111 teams; 1,317 submissions; 41 ranked (⚠ the results TSV ranks 39) |
| Known issues | ⚠ The arXiv paper says SaMi-Trop came "from 1959 patients", while Zenodo says 1,631; 1,959 is the cohort size. ⚠ PTB-XL is 21,799 in the text but 21,779 in Table 1. ⚠ CODE-15% is 335,621 in Table 1 but 345,779 in the text |

# Part 2: Published results

Only rows with the same protocol and metric share a table. Rows are sorted by year.

## MIT-BIH: inter-patient (de Chazal DS1 → DS2, AAMI classes)

| Paper | Year | Method | Protocol | Acc | SVEB Se / +P | VEB Se / +P |
|---|---|---|---|---|---|---|
| [de Chazal et al., IEEE TBME](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=15248536&rettype=abstract&retmode=text) | 2004 | Linear discriminants on morphology and RR features | DS1→DS2 | ⚠ Not in the abstract. 83% per [Garcia](https://pmc.ncbi.nlm.nih.gov/articles/PMC5585360/) and 86.2% per Mondéjar-Guerra [secondary, the two disagree] | 75.9 / 38.5 | 77.7 / 81.9 |
| [Llamedo & Martínez, EMBC](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=21096269&rettype=abstract&retmode=text) | 2010/2011 | Wavelet/RR features, LDA | DS1→DS2 | 93 | 77 / 39 | 81 / 87 |
| [Garcia et al., Sci Rep](https://pmc.ncbi.nlm.nih.gov/articles/PMC5585360/) | 2017 | Vectorcardiogram + complex networks + SVM | DS1→DS2, 3 classes (N/S/V) | 92.4 | 62.0 / 53.0 | 87.3 / 59.4 |
| [Mondéjar-Guerra et al., BSPC](https://ruc.udc.es/bitstreams/27ee7d17-9c5e-41d6-903f-85801556010c/download) | 2019 | SVM ensemble | DS1→DS2, 4 classes (Q excluded) | 94.5 | 78.1 / 49.7 | 94.7 / 93.9 |
| [Zhang et al., J Healthc Eng](https://pmc.ncbi.nlm.nih.gov/articles/PMC8181174/) | 2021 | Adversarial CNN + RR features | DS1→DS2 | 94.7 | 78.8 / 90.8 | 92.5 / 94.3 |

Mondéjar-Guerra's Table 6 cites de Chazal at SVEB 0.760/0.385 and VEB 0.803/0.866 [secondary]. ⚠ The VEB Se of 0.803 differs from the abstract's 77.7.

Not directly comparable, because only F1 is reported: Niu et al., IEEE JBHI 2020, F1 S 76.5% and F1 V 89.7% [secondary] ([Zhang 2021, Table 4](https://pmc.ncbi.nlm.nih.gov/articles/PMC8181174/)).

## MIT-BIH: intra-patient and patient-specific (⚠ leakage, do not compare with the table above)

| Paper | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| Kiranyaz et al., IEEE TBME | 2016 | Patient-specific 1D CNN | 245 common beats plus the first 5 min of each test record | SVEB Acc/Se/+P; VEB Acc/Se/+P | 97.6 / 60.3 / 63.5; 99.0 / 93.9 / 90.6 [secondary, [Malik 2021 Table IV](https://arxiv.org/pdf/2110.02215v1)] |
| [Acharya et al., Comput Biol Med](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=28869899&rettype=abstract&retmode=text) | 2017 | 9-layer CNN | Random beats, 5 AAMI classes, augmented to balance (⚠ unclear whether before or after the split) | Accuracy | 94.03% (original), 93.47% (noise-free); 89.07% when trained on imbalanced data |
| [Kachuee et al., arXiv 1805.00794](https://arxiv.org/pdf/1805.00794) | 2018 | Residual CNN | Random beat-level split, 5 classes, 4,079 test beats | Average accuracy | 93.4% |
| [Garcia 2017 survey, Table 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC5585360/) | 2004–2017 | Various | Intra-patient | Accuracy | 99–100% reported |

**Why these numbers are inflated.** Garcia et al. 2017 call intra-patient-only reporting "a serious problem": using heartbeats from the same patient for training and testing "makes the evaluation process biased", because models learn each person's beat particularities, giving accuracies "very close to 100%" ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC5585360/)). Compare 99–100% intra-patient with 83–94% inter-patient.

## PhysioNet/CinC 2017: official hidden-test F1

The official score is (F1 Normal + F1 AF + F1 Other) / 3, **with Noisy excluded** ([Clifford 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5978770)). The [per-class results CSV](https://physionet.org/files/challenge-2017/1.0.0/results_all_F1_scores_for_each_classification_type.csv) confirms this. Four teams tied for first at 0.83 ([PhysioNet](https://physionet.org/content/challenge-2017/1.0.0/); [results.csv](https://physionet.org/files/challenge-2017/1.0.0/results.csv)).

| Paper / team | Year | Method | Protocol | Metric | Result (F1n / F1a / F1o) |
|---|---|---|---|---|---|
| Teijeiro et al. | 2017 | Not stated in source used | Hidden test, 3,658 | 3-class F1 | 0.831 (0.903 / 0.855 / 0.737) |
| Datta et al. (TCS) | 2017 | Not stated in source used | Hidden test | 3-class F1 | 0.829 (0.916 / 0.823 / 0.750) |
| Zabihi, Bahrami Rad et al. | 2017 | Not stated in source used | Hidden test | 3-class F1 | 0.826 (0.909 / 0.835 / 0.734) |
| Hong et al. | 2017 | Not stated in source used | Hidden test | 3-class F1 | 0.825 (0.912 / 0.813 / 0.751) |
| Baydoun; Zihlmann; Bin; Xiong & Zhao | 2017 | Various | Hidden test | 3-class F1 | 0.82 (rank 5, tie) |
| [Hannun et al., Nat Med](https://pmc.ncbi.nlm.nih.gov/articles/PMC6784839/) | 2019 | Deep CNN | Hidden test, after the challenge (not an official entry) | Class-average F1 | 0.83 |

Clifford 2017 also reports voting ensembles: all 75 algorithms reached 0.855, and 45 LASSO-selected algorithms reached 0.858 (0.868 for "LASSO+"). ⚠ The abstract gives the LASSO result as 0.87.

Not directly comparable: Hannun et al.'s own test set (cardiologist committee) gives sequence-level F1 0.807 vs cardiologists 0.753, and set-level F1 0.837 vs 0.780 ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC6784839/)).

## PTB-XL: Strodthoff et al. benchmark (macro AUC, 100 Hz, folds 1–8 train / 9 val / 10 test)

Source: [arXiv 2004.13701, Table II](https://arxiv.org/pdf/2004.13701); same values (except the ensemble row) in the [GitHub README](https://github.com/helme/ecg_ptbxl_benchmarking).

| Paper | Year | Model | all | diag | subdiag | superdiag | form | rhythm |
|---|---|---|---|---|---|---|---|---|
| Strodthoff et al., IEEE JBHI | 2021 | xresnet1d101 | .925 | .937 | .929 | .928 | .896 | .957 |
| " | 2021 | inception1d | .925 | .931 | .930 | .921 | .899 | .953 |
| " | 2021 | resnet1d_wang | .919 | .936 | .928 | .930 | .880 | .946 |
| " | 2021 | fcn_wang | .918 | .926 | .927 | .925 | .869 | .931 |
| " | 2021 | lstm_bidir | .914 | .932 | .923 | .921 | .876 | .949 |
| " | 2021 | lstm | .907 | .927 | .928 | .927 | .851 | .953 |
| " | 2021 | Wavelet+NN | .849 | .855 | .859 | .874 | .757 | .890 |
| " | 2021 | ensemble | .929 | .939 | .933 | .934 | .907 | .965 |

## PTB-XL: later results on the "all" task (macro AUC, same folds)

| Paper | Year | Method | Protocol | Result |
|---|---|---|---|---|
| [Mehari & Strodthoff](https://arxiv.org/pdf/2103.12676) | 2022 | CPC pretrained on "All" (⚠ includes CinC 2020, which contains PTB-XL including the test fold) | Linear eval / fine-tune, mean of 10 runs | 0.9272 / 0.9418 |
| " | 2022 | CPC pretrained on PTB-XL only | Linear / fine-tune | 0.9246 / 0.9395 |
| " | 2022 | SimCLR; BYOL | Linear / fine-tune | 0.8828 / 0.9265; 0.8781 / 0.9290 |
| " | 2022 | Supervised 4FC+2LSTM+2FC | Supervised | 0.9318 |
| [Mehari & Strodthoff](https://arxiv.org/pdf/2308.15291) | 2023 | S4, supervised | Supervised | 0.9417 |
| " | 2023 | S4 + CPC pretraining (All2021; ⚠ includes CinC 2021, which contains PTB-XL) | Fine-tune | 0.9445 |
| " | 2023 | S4 + patient metadata | Fine-tune (All2021 pretraining, ⚠ as above) | 0.9463 |

## PTB-XL: linear probe with limited labels (MERL table; not comparable to the tables above)

Source: [MERL, ICML 2024](https://arxiv.org/html/2403.06659). "Official split" at 500 Hz, macro AUC in %, at 1% / 10% / 100% of labels.

| Paper | Year | Method | Superclass | Subclass (23) | Form | Rhythm |
|---|---|---|---|---|---|---|
| SimCLR (as reported in MERL) | 2024 | Linear probe | 63.41 / 69.77 / 73.53 | – | – | – |
| ST-MEM (as reported in MERL) | 2024 | Linear probe | 61.12 / 66.87 / 71.36 | – | – | – |
| MERL | 2024 | ECG-text pretraining, linear probe | 82.39 / 86.27 / 88.67 | 64.90 / 80.56 / 84.72 | 58.26 / 72.43 / 79.65 | 53.33 / 82.88 / 88.34 |

Not directly comparable on PTB-XL:
- ST-MEM's own paper uses a single-label superclass subset with its own split; fine-tuned AUROC 0.933 ([arXiv](https://arxiv.org/html/2402.09450)).
- ECGFounder evaluates PTB-XL zero-shot as an external set; average AUROC 0.924 ([arXiv](https://arxiv.org/html/2410.04133)).
- ECG-FM includes PTB-XL in pretraining and reports no fold results ([arXiv](https://arxiv.org/html/2408.05178)).
- HuBERT-ECG could not be verified because the paper was inaccessible.

## CPSC 2018: official hidden test (2,954 records, mean F1 over 9 classes)

Source: [challenge page](http://2018.icbeb.org/Challenge.html).

| Paper / team | Year | Method | Protocol | Metric | Result |
|---|---|---|---|---|---|
| Tsai-Min Chen et al. (rank 1) | 2018 | Not stated in the source used | Hidden test | Mean F1 | 0.837 (F_AF 0.933, F_block 0.899, F_PC 0.847, F_ST 0.779) |
| Wenjie Cai et al. (rank 2) | 2018 | Not stated in the source used | Hidden test | Mean F1 | 0.830 |
| Runnan He et al. (rank 3) | 2018 | Not stated in the source used | Hidden test | Mean F1 | 0.806 |

Not directly comparable:
- The winners' follow-up paper reports a "median overall F1-score of 0.84" ([Chen et al., iScience 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7031313/)).
- Strodthoff 2021 split the public CPSC data into 10 stratified folds (train 1–8, validation 9, test 10) with xresnet1d101: AUC 0.974, F_β=2 0.819, G_β=2 0.602 ([README](https://github.com/helme/ecg_ptbxl_benchmarking)).

## PhysioNet/CinC 2020: official challenge metric, hidden test

Source: [official scores CSV](https://moody-challenge.physionet.org/2020/results/physionet_2020_official_scores.csv). 217 teams entered and 41 were ranked.

| Team | Year | Protocol | Full test | Hidden CPSC | Hidden G12EC | Undisclosed |
|---|---|---|---|---|---|---|
| prna (rank 1) | 2020 | Hidden test | 0.533 | 0.761 | 0.558 | 0.492 |
| Between_a_ROC_and_a_heart_place (2) | 2020 | Hidden test | 0.520 | – | – | – |
| HeartBeats (3) | 2020 | Hidden test | 0.514 | – | – | – |

## PhysioNet/CinC 2021: official challenge metric, hidden test

Source: [12-lead leaderboard](https://moody-challenge.physionet.org/2021/results/2021_Challenge_Test_Results_Leaderboard_For_Official_Entries-12-lead.csv) (2-decimal precision).

| Team | Year | Lead set | Score |
|---|---|---|---|
| ISIBrno-AIMT (winner) | 2021 | 12, 6, 4, 3 and 2 leads | 0.58 each |
| NIMA; DSAIL_SNU; cardiochallenger | 2021 | 12 | 0.55 (tied 2nd) |
| DSAIL_SNU | 2021 | 6 | 0.58 (tied 1st) |

ISIBrno-AIMT's 12-lead scores per database are CPSC 0.725, G12EC 0.617, Undisclosed 0.532 and UMich 0.589 ([all-scores CSV](https://moody-challenge.physionet.org/2021/results/Final_2021_Challenge_All_Scores_Official_Entries-12-lead.csv)).

⚠ Not official: Reyna 2022 Table 7 reports post-challenge follow-up entries on the 12-lead test: CeZIS 0.62, a voting model 0.62, ISIBrnoAIMT 0.59 ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC9469795/)).

## CODE-test: F1 per class (Ribeiro 2020)

Source: [Table 2](https://pmc.ncbi.nlm.nih.gov/articles/PMC7145824/). The DNN threshold is the point of maximum F1 on the test-set precision-recall curve (Fig. 2), so DNN F1 is optimistic, and DNN specificity is ≥0.995 for every class. The paper gives no macro F1.

| Class | DNN | Cardiology residents | Emergency residents | Medical students |
|---|---|---|---|---|
| 1dAVb | 0.897 | 0.776 | 0.719 | 0.732 |
| RBBB | 0.944 | 0.917 | 0.852 | 0.928 |
| LBBB | 1.000 | 0.947 | 0.912 | 0.915 |
| SB | 0.882 | 0.882 | 0.848 | 0.750 |
| AF | 0.870 | 0.769 | 0.696 | 0.706 |
| ST | 0.960 | 0.882 | 0.946 | 0.873 |

## CODE-test: average AUROC (external test in ECGFounder; not comparable with F1 above)

Source: [ECGFounder, NEJM AI 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12327759/). ⚠ Some confidence intervals in the source table are malformed.

| Model | Year | Protocol | Average AUROC |
|---|---|---|---|
| S12L-ECG (Ribeiro's model; CODE-test is internal for it) | 2020 | As reported in ECGFounder | 0.980 |
| CTN | – | As reported in ECGFounder | 0.963 |
| ECG-SE-ResNet | – | As reported in ECGFounder | 0.963 |
| ECGFounder | 2025 | External test | 0.981 (0.979–0.984) |

## Apnea-ECG: per-minute accuracy on the 35 withheld records

Official CinC 2000 Event 2 results, scored on 17,268 minutes ([PhysioNet](https://physionet.org/content/challenge-2000/1.0.0/)). The page calls these accuracies "comparable to the roughly 90% concurrence of human experts". In Event 1 (recording-level), four entrants scored 30/30.

| Paper / entrant | Year | Method | Protocol | Accuracy (Se / Sp) |
|---|---|---|---|---|
| McNames, Fraser, Rechtsteiner | 2000 | Challenge entry | Official test | 92.62% |
| Raymond, Cayton, Bates, Chappell | 2000 | Challenge entry | Official test | 92.30% |
| de Chazal, Heneghan et al. | 2000 | Challenge entry | Official test | 89.36% |
| Schrader et al. | 2000 | Challenge entry | Official test | 87.56% |
| Jarvis & Mitra | 2000 | Challenge entry | Official test | 87.30% |
| Shinar et al. | 2000 | Challenge entry | Official test | 85.63% |
| Maier et al. | 2000 | Challenge entry | Official test | 85.54% |
| [Wang et al., PeerJ](https://pmc.ncbi.nlm.nih.gov/articles/PMC6756143/) | 2019 | Modified LeNet-5 using adjacent segments | Train on 35, test on 35 withheld | 87.6% (83.1 / 90.3); AUC 0.950 |
| [Chang et al., Sensors](https://pmc.ncbi.nlm.nih.gov/articles/PMC7435835) | 2020 | 1-D CNN | Same; ⚠ best of 10 runs, selected on the withheld set | 87.9% (81.1 / 92.0) |

Not directly comparable:
- Nguyen et al. 2022 ([arXiv 2208.03408](https://arxiv.org/pdf/2208.03408)) report 91.13% on 16,945 test segments, not 17,268 minutes. ⚠ Their Se and Sp are swapped between the abstract and Table III.
- Wang 2019 cites HMM 86.2% (Song 2016) and 83.8% (Sharma 2016; ⚠ 83.4% in Wang's own comparison table) [secondary].
- ⚠ The apparent subject overlap between learning and test sets (Part 1) may favour all of these results.

## WESAD: stress detection from chest ECG

**Binary (stress vs non-stress), LOSO:**

| Paper | Year | Method | Protocol | Accuracy | F1 |
|---|---|---|---|---|---|
| [Schmidt et al.](https://www.eti.uni-siegen.de/ubicomp/papers/ubi_icmi2018.pdf) | 2018 | LDA on ECG features | LOSO, 60 s windows | 85.44 | 81.31 (macro) |
| Schmidt et al. | 2018 | Random forest | LOSO | 82.78 | 79.64 |
| [Behinaein et al., ISWC](https://ar5iv.labs.arxiv.org/html/2108.09737) | 2021 | Transformer, untuned | LOSO, 30 s windows | 80.4 | 69.7 |
| [Prajod & André, ICMLA](https://arxiv.org/pdf/2210.06225) | 2022 | Deep ECGNet on 10 s raw ECG at 256 Hz | LOSO | 90.8 | 85.7 (macro) |
| Prajod & André | 2022 | MLP on HRV | LOSO | 89.5 | 85.9 |
| Prajod & André | 2022 | SVM on HRV | LOSO | 87.1 | 83.2 |
| [Ahmad & Khan (preprint)](https://arxiv.org/html/2603.26721) | 2026 | ViT on spectrograms, 1 s segments | LOSO | 88.3 | 88.4 (averaging not stated) |

**3-class (baseline / stress / amusement), LOSO:**

| Paper | Year | Method | Protocol | Accuracy | F1 |
|---|---|---|---|---|---|
| Schmidt et al. | 2018 | LDA | LOSO | 66.29 | 56.03 (macro) |
| Schmidt et al. | 2018 | AdaBoost | LOSO | 61.71 | 52.48 |
| Ahmad & Khan (preprint) | 2026 | ViT on spectrograms | LOSO | 76.7 | 76.8 |

Not directly comparable:
- **Behinaein 2021 fine-tuned: 91.1 accuracy / 83.3 F1. ⚠ Not pure LOSO**, because it was fine-tuned on 10% of the test subject's data.
- Prajod & André 2022, trained on WESAD and tested on SWELL-KW: 53.8 accuracy / 53.5 F1. Cross-dataset results drop sharply.
- Unverified LOSO figures cited in those papers: Bota 2020 85.7; Karan & Kaygun 2021 88.7; Liakopoulos 2021 82.4 / 79.4 [secondary].

## PhysioNet/Moody 2025 (Chagas): official test scores

The metric is the true positive rate in the top 5%; ranking uses the mean of the three test sources. Sources: [results TSV](https://moody-challenge.physionet.org/2025/results/challenge_2025_results.tsv), [arXiv Table 3](https://arxiv.org/html/2510.02202).

| Team | Year | REDS-II val | REDS-II test | SaMi-Trop 3 test | ELSA-Brasil test | Mean test |
|---|---|---|---|---|---|---|
| Biomed-Cardio (1) | 2025 | 0.445 | 0.468 | 0.376 | 0.125 | 0.323 |
| DlaskaLabMUI (2) | 2025 | 0.440 | 0.357 | 0.375 | 0.118 | 0.283 |
| AIChagas (3) | 2025 | 0.360 | 0.382 | 0.329 | 0.129 | 0.280 |
| ISIBrno-AIMT (4) | 2025 | – | – | – | – | 0.271 |
| Ahus AIM (5) | 2025 | – | – | – | – | 0.269 |
| cardio_Basel25 (6) | 2025 | – | – | – | – | 0.256 |
| CinCo Amigos (7) | 2025 | – | – | – | – | 0.250 |
| chagas_detector (8) | 2025 | – | – | – | – | 0.245 |
| AIMED (9) | 2025 | – | – | – | – | 0.240 |
| Chagas_UBT; MIWEAR (10, tie) | 2025 | – | – | – | – | 0.238 |

The median score fell 64% from REDS-II validation (0.279) to ELSA-Brasil (0.100). ⚠ The arXiv text misprints the median REDS-II test score as "0.0275".

## MIMIC-IV-ECG and HEEDB

There is no single standard benchmark for either dataset.
- **MIMIC-IV-ECG:** the closest is [MIMIC-IV-ECG-Ext-ICD](https://physionet.org/content/mimic-iv-ecg-ext-icd-labels/). It has 1,076 ICD-10-CM codes and 20 patient-disjoint folds (0–17 train, 18 validation, 19 test). On it, [Strodthoff et al. 2024](https://arxiv.org/abs/2312.11050) found 253 codes (81 cardiac, 172 non-cardiac) predictable with AUROC > 0.8 from a single ED ECG.
- **HEEDB:** [ECGFounder](https://pmc.ncbi.nlm.nih.gov/articles/PMC12327759/) used an internal split: 7,519,035 development ECGs and 834,926 test ECGs.
  - AUROC > 0.95 for 80 of 150 labels.
  - On a 523-ECG committee set: average AUROC 0.968, and average F1 0.677 against 0.640 for cardiologists.
  - This is not a public benchmark.

# How to read these numbers

- **Inter- vs intra-patient.** If beats from the same person appear in both training and test, the model can memorize that person's beat shape. MIT-BIH intra-patient results (93–100%) are far higher than inter-patient ones (83–95%) for this reason. Even de Chazal's split shares one subject (records 201 and 202). For any dataset with several records per person (PTB, INCART, Apnea-ECG, CODE), split by patient.
- **Different label subsets.** PTB-XL "superdiag", "form" and "all" are different tasks. MERL and ST-MEM use their own splits or label subsets. The CinC 2017 score excludes the Noisy class. CODE-test reports per-class F1, not a macro score. Check the exact task before comparing two numbers.
- **Hidden test vs cross-validation.** Challenge scores (CinC 2017/2020/2021/2025, CPSC) come from sequestered data the teams never saw. Paper results on public data (e.g. CPSC public-data folds, WESAD) are usually higher. The 2025 Chagas scores show how much results drop on a new population: the median fell 64% from validation to ELSA-Brasil.
- **Dataset versions and leakage through pretraining.** PTB-XL v1.0.1 has 21,837 records and v1.0.3 has 21,799, after duplicate removal. Pretraining on CinC 2020/2021 data that contains PTB-XL can leak the PTB-XL test fold.
- **Same metric name, different averaging.** "F1" may be macro, class-average or per-class, and "accuracy" may be per beat, per minute or per recording. The tables keep the definition each paper states.
