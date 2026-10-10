# 03: Machine learning and evaluation

**Shared by all data types.** **When:** months 3–9, alongside the EEG paradigms.
Methods specific to one data type (e.g. CSP for EEG, Kalman decoders for spikes) live in that data type's folder.

## Features and classifiers
- [ ] Band power, log-variance, spectral features
- [ ] Autoregressive (AR) model coefficients
- [ ] LDA and shrinkage LDA (Ledoit-Wolf)
- [ ] Logistic regression, SVM
- [ ] Why simple linear models often win on small neural datasets
- [ ] Spatial filters vs. spatial patterns: which one you can interpret (Haufe et al.)

## Covariance and Riemannian geometry
- [ ] Covariance matrices as points on the SPD manifold
- [ ] Riemannian distance and the Riemannian mean
- [ ] Minimum Distance to Mean (MDM) classifier
- [ ] Tangent space mapping + a linear classifier
- [ ] Re-centering and Riemannian Procrustes analysis for transfer between subjects

## Evaluation done right
- [ ] Within-session, cross-session, and cross-subject evaluation
- [ ] Leave-one-subject-out cross-validation
- [ ] Data leakage: fitting filters, ICA, or normalization on test data
- [ ] Nested cross-validation for hyperparameters
- [ ] Permutation tests for significance
- [ ] BCI metrics: accuracy, balanced accuracy, Cohen's kappa, ROC AUC
- [ ] Information transfer rate (ITR, Wolpaw formula) and its pitfalls
- [ ] False positives per minute for self-paced BCIs; offline vs. online performance
- [ ] Benchmarking with MOABB

## Deep learning for neural data
- [ ] Normalization: per-channel, exponential moving standardization
- [ ] Data augmentation for neural signals: time shift, noise, channel dropout, frequency shift, FT surrogate, mixup
- [ ] Cropped training (sliding windows)
- [ ] Variance across seeds and subjects: report mean ± std, not your best run
- [ ] Domain shift across subjects and sessions
- [ ] Euclidean and Riemannian alignment as preprocessing
- [ ] Fine-tuning with a small calibration set
- [ ] Domain adaptation (e.g. adversarial/DANN) and domain generalization
- [ ] Self-supervised pretraining: contrastive and masked reconstruction
- [ ] Linear probing vs. full fine-tuning evaluation
- [ ] Interpretability: saliency and gradient attributions; checking the model uses brain signals, not artifacts

## Build
- [ ] Notebook: the leakage experiment — the same model with a random split vs. a subject split
- [ ] Notebook: implement LDA, the Riemannian mean, and tangent space in NumPy; check them against scikit-learn and pyRiemann

## Resources
- Lotte et al. (2018), "A review of classification algorithms for EEG-based brain–computer interfaces: a 10 year update", *J Neural Eng*
- Congedo, Barachant & Bhatia (2017), "Riemannian geometry for EEG-based brain-computer interfaces; a primer and a review", *Brain-Computer Interfaces*
- Haufe et al. (2014), "On the interpretation of weight vectors of linear models in multivariate neuroimaging", *NeuroImage*
- Jayaram & Barachant (2018), "MOABB: trustworthy algorithm benchmarking for BCIs", *J Neural Eng*
- He & Wu (2020), "Transfer learning for brain–computer interfaces: a Euclidean space data alignment approach", *IEEE TBME*
- Rommel et al. (2022), "Data augmentation for learning predictive models on EEG: a systematic comparison", *J Neural Eng*
