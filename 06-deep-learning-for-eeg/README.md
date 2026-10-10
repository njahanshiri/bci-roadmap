# Part 06: Deep learning for EEG

**When:** months 6–12.
This is your strongest area as an AI engineer. What's new here is everything specific to EEG.

## Architectures
- [ ] ShallowConvNet and DeepConvNet
- [ ] EEGNet: depthwise and separable convolutions as learned spatial and temporal filters
- [ ] Temporal convolutional networks (EEG-TCNet, ATCNet)
- [ ] Transformers for EEG (e.g. EEG Conformer)
- [ ] Input choices: raw signal vs. filtered vs. spectrogram vs. covariance

## Training on small, noisy data
- [ ] Normalization: per-channel, exponential moving standardization
- [ ] EEG data augmentation: time shift, noise, channel dropout, frequency shift, FT surrogate, mixup
- [ ] Cropped training (sliding windows)
- [ ] Regularization and early stopping with few subjects
- [ ] Variance across seeds and subjects: report mean ± std, not your best run

## Transfer and generalization
- [ ] Cross-subject and cross-session domain shift
- [ ] Euclidean alignment and Riemannian alignment as preprocessing
- [ ] Fine-tuning with a small calibration set
- [ ] Domain adaptation (e.g. adversarial/DANN) and domain generalization
- [ ] Handling different channel layouts across datasets

## Self-supervised learning and foundation models
- [ ] Contrastive and masked-reconstruction pretraining for EEG
- [ ] Large EEG corpora (e.g. TUH EEG Corpus) and their biases
- [ ] EEG foundation models: BENDR, BIOT, LaBraM, EEGPT, CBraMod
- [ ] Linear probing vs. full fine-tuning evaluation
- [ ] Do foundation models beat strong classical baselines? How to test it fairly

## Interpretability
- [ ] Saliency and gradient-based attributions on EEG
- [ ] Checking that the model uses brain signals, not artifacts
- [ ] Mapping learned filters back to frequencies and scalp topographies

## Build
- [ ] Notebook: EEGNet vs. CSP+LDA vs. tangent space on the same MOABB splits
- [ ] Notebook: augmentation study — which augmentations help motor imagery
- [ ] Project: evaluate one EEG foundation model against classical baselines, cross-subject

## Resources
- Schirrmeister et al. (2017), "Deep learning with convolutional neural networks for EEG decoding and visualization", *Human Brain Mapping*
- Lawhern et al. (2018), "EEGNet: a compact convolutional neural network for EEG-based brain–computer interfaces", *J Neural Eng*
- Roy et al. (2019), "Deep learning-based electroencephalography analysis: a systematic review", *J Neural Eng*
- He & Wu (2020), "Transfer learning for brain–computer interfaces: a Euclidean space data alignment approach", *IEEE TBME*
- Rommel et al. (2022), "Data augmentation for learning predictive models on EEG: a systematic comparison", *J Neural Eng*
- Jiang et al. (2024), "Large brain model for learning generic representations with tremendous EEG data in BCI" (LaBraM), *ICLR*
- Braindecode documentation
