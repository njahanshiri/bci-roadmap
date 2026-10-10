# Part 05: Classical ML for BCI

**When:** months 3–6, alongside Part 04.

## Features
- [ ] Band power, log-variance, spectral features
- [ ] Autoregressive (AR) model coefficients
- [ ] Temporal features for ERPs (downsampled amplitudes)

## Spatial filters
- [ ] CSP as a generalized eigenvalue problem; regularized CSP
- [ ] xDAWN
- [ ] Spatial filters vs. spatial patterns: which one you can interpret (Haufe et al.)

## Classifiers
- [ ] LDA and shrinkage LDA (Ledoit-Wolf)
- [ ] Logistic regression, SVM
- [ ] Why simple linear models often win on small EEG datasets

## Riemannian geometry
- [ ] Covariance matrices as points on the SPD manifold
- [ ] Riemannian distance and the Riemannian mean
- [ ] Minimum Distance to Mean (MDM) classifier
- [ ] Tangent space mapping + a linear classifier
- [ ] Re-centering and Riemannian Procrustes analysis for transfer between subjects
- [ ] Special covariances for ERPs (xDAWN covariances)

## Evaluation done right
- [ ] Within-session, cross-session, and cross-subject evaluation
- [ ] Leave-one-subject-out cross-validation
- [ ] Data leakage: fitting filters, ICA, or normalization on test data
- [ ] Nested cross-validation for hyperparameters
- [ ] Permutation tests for significance
- [ ] Benchmarking with MOABB

## Build
- [ ] Notebook: CSP+LDA vs. tangent space vs. MDM on 3 MOABB datasets, within- and cross-subject
- [ ] Notebook: the leakage experiment — the same model with a random split vs. a subject split

## Resources
- Blankertz et al. (2008), "Optimizing spatial filters for robust EEG single-trial analysis", *IEEE Signal Processing Magazine*
- Lotte et al. (2018), "A review of classification algorithms for EEG-based brain–computer interfaces: a 10 year update", *J Neural Eng*
- Congedo, Barachant & Bhatia (2017), "Riemannian geometry for EEG-based brain-computer interfaces; a primer and a review", *Brain-Computer Interfaces*
- Haufe et al. (2014), "On the interpretation of weight vectors of linear models in multivariate neuroimaging", *NeuroImage*
- Jayaram & Barachant (2018), "MOABB: trustworthy algorithm benchmarking for BCIs", *J Neural Eng*
- pyRiemann and MOABB documentation
