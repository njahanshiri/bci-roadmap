"""Run every benchmark phase in order, then write the comparison report.

    python benchmarks/main.py                  # everything (GPU recommended)
    python benchmarks/main.py --quick          # tiny smoke test of every code path
    python benchmarks/main.py --phases 1 2     # only some phases
"""
import argparse
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import mne  # noqa: E402

from common import RESULTS_DIR, Results, env_info  # noqa: E402

PHASES = {
    1: ("EEG motor imagery", "eeg", "run_mi"),
    2: ("EMG gestures", "emg", "run_emg"),
    3: ("EEG SSVEP and P300", "eeg", "run_ssvep_p300"),
    4: ("EEG foundation models and TUAB", "eeg", "run_foundation"),
    5: ("Sleep-EDF and PTB-XL", "other", "run_other"),
    6: ("More EEG: SSVEP, seizure, emotion, clinical, imagined speech", "eeg_more", "run"),
    7: ("More EMG: Ninapro DB1-3/DB7, CapgMyo, Hyser, EPN-612, putEMG", "emg_more", "run"),
    8: ("EOG: sleep, artifact removal, activity, vigilance", "eog", "run"),
    9: ("ECG: arrhythmia, PhysioNet challenges, CODE, apnea, stress", "ecg", "run"),
    10: ("fNIRS", "fnirs", "run"),
    11: ("MEG", "meg", "run"),
    12: ("ECoG and sEEG", "ecog", "run"),
    13: ("Spikes and LFP", "spikes", "run"),
    14: ("Official benchmark pipelines: emg2qwerty, emg2pose, generic neuromotor", "external", "run"),
}


def parse():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--phases", type=int, nargs="+", default=list(PHASES))
    p.add_argument("--datasets", nargs="+", help="only these dataset names")
    p.add_argument("--models", nargs="+", help="only these deep/foundation model names")
    p.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    p.add_argument("--epochs", type=int, default=300, help="epochs for EEG deep models (others are capped lower)")
    p.add_argument("--foundation-epochs", type=int, default=50)
    p.add_argument("--batch-size", type=int, default=64)
    p.add_argument("--data-dir", default=os.path.expanduser("~/bci_data"))
    p.add_argument("--tuab-path", help="local TUAB v3.0.1 folder (needs TUH access)")
    p.add_argument("--path", action="append", default=[], metavar="NAME=FOLDER",
                   help="local folder for an access-gated dataset, e.g. --path seed=/data/SEED (repeatable)")
    p.add_argument("--tuab-windows", type=int, default=12, help="10-s windows kept per TUAB recording")
    p.add_argument("--results", help="results CSV (default: results/benchmark.csv, or results/quick.csv with --quick)")
    p.add_argument("--accept-licenses", action="store_true",
                   help="accept dataset licences that require explicit consent (e.g. Brainstorm)")
    p.add_argument("--quick", action="store_true", help="2 subjects, 2 epochs, 1 seed: checks every code path fast")
    args = p.parse_args()
    args.paths = dict(kv.split("=", 1) for kv in args.path)
    if args.tuab_path:
        args.paths.setdefault("tuab", args.tuab_path)
    if args.quick:
        args.seeds, args.epochs, args.foundation_epochs = [0], 2, 1
    args.results = args.results or str(RESULTS_DIR / ("quick.csv" if args.quick else "benchmark.csv"))
    return args


def main():
    args = parse()
    os.makedirs(args.data_dir, exist_ok=True)
    mne.set_config("MNE_DATA", args.data_dir, set_env=True)
    os.environ["MNE_DATA"] = args.data_dir
    results = Results(args.results)
    print(f"{env_info()}\nresults -> {args.results}\ndata -> {args.data_dir}")
    t0 = time.time()
    for n in args.phases:
        title, module, fn = PHASES[n]
        print(f"\n{'=' * 70}\nPhase {n}: {title}\n{'=' * 70}")
        t = time.time()
        try:
            getattr(__import__(module), fn)(results, args)
        except Exception as e:  # a broken phase must not stop the others
            from common import log_error
            log_error(f"phase{n}", f"phase crashed: {type(e).__name__}: {e}")
        print(f"Phase {n} finished in {(time.time() - t) / 60:.1f} min")
    print(f"\nAll phases finished in {(time.time() - t0) / 3600:.2f} h")
    import report
    report.main(args.results, Path(args.results).with_name(Path(args.results).stem + "_summary.md"))


if __name__ == "__main__":
    main()
