"""Start here: measures your first brain signal and shows your roadmap progress."""
import re
from pathlib import Path

import mne
from mne.datasets import eegbci

ROOT = Path(__file__).parent


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


def progress():
    print("\nRoadmap progress")
    next_up = []
    for readme in sorted(ROOT.glob("[0-9][0-9]-*/README.md")):
        text = readme.read_text()
        done = re.findall(r"^- \[x\] ", text, re.M | re.I)
        todo = re.findall(r"^- \[ \] (.+)", text, re.M)
        print(f"  {readme.parent.name:<36} {len(done):>3}/{len(done) + len(todo)}")
        if todo:
            next_up.append(f"{readme.parent.name}: {todo[0]}")
    print("\nNext up (Parts 00-02 run in parallel):")
    for item in next_up[:3]:
        print(f"  - {item}")


if __name__ == "__main__":
    print("Your first brain signal (PhysioNet subject 1, channels O1/Oz/O2)")
    first_signal()
    progress()
