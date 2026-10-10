"""Start here: measures your first brain signal."""
import mne
from mne.datasets import eegbci


def first_signal():
    """Eyes open vs. eyes closed alpha (8-13 Hz) over the occipital cortex, PhysioNet subject 1."""
    mne.set_log_level("WARNING")
    alpha = {}
    for run, label in [(1, "eyes open"), (2, "eyes closed")]:
        raw = mne.io.read_raw_edf(eegbci.load_data(1, [run], update_path=True)[0], preload=True)
        eegbci.standardize(raw)
        power, freqs = raw.compute_psd(fmin=1, fmax=40, picks=["O1", "Oz", "O2"]).get_data(return_freqs=True)
        power = power.mean(axis=0)
        band = (freqs >= 8) & (freqs <= 13)
        alpha[label] = power[band].mean()
        print(f"  {label:<12} alpha peak at {freqs[band][power[band].argmax()]:.1f} Hz")
    ratio = alpha["eyes closed"] / alpha["eyes open"]
    print(f"  Alpha power is {ratio:.1f}x higher with eyes closed: the Berger effect, first seen in 1929.")


if __name__ == "__main__":
    print("Your first brain signal (PhysioNet subject 1, channels O1/Oz/O2)")
    first_signal()
