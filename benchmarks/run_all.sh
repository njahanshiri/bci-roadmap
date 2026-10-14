#!/usr/bin/env bash
# Run every benchmark phase, then write the comparison report.
#
#   ./benchmarks/run_all.sh --quick     # smoke test first: small downloads, a few minutes per phase
#   ./benchmarks/run_all.sh             # full run (GPU; downloads tens of GB; can take days)
#
# Any extra arguments go to main.py, for example:
#   ./benchmarks/run_all.sh --phases 1 2
#   ./benchmarks/run_all.sh --tuab-path /data/tuh_eeg_abnormal/v3.0.1/edf
#   ./benchmarks/run_all.sh --data-dir /big/disk/bci_data
#
# Safe to stop and restart: finished (dataset, protocol, model, seed) units are skipped.
# Environment variables: PYTHON (default python3), TORCH_INDEX_URL (optional CUDA wheel index).
set -euo pipefail
cd "$(dirname "$0")"

PY="${PYTHON:-python3}"
if [ ! -x .venv/bin/python ]; then
  echo "Creating .venv with $($PY --version)"
  "$PY" -m venv .venv
  .venv/bin/pip install -q --upgrade pip
  if [ -n "${TORCH_INDEX_URL:-}" ]; then
    .venv/bin/pip install -q torch --index-url "$TORCH_INDEX_URL"
  fi
  .venv/bin/pip install -q -r requirements.txt
fi

.venv/bin/python - <<'EOF'
import torch
if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
else:
    print("WARNING: no CUDA GPU found; deep models will run on CPU and be very slow.")
EOF

mkdir -p results
LOG="results/run_$(date +%Y%m%d_%H%M%S).log"
echo "Logging to benchmarks/$LOG"
.venv/bin/python -u main.py "$@" 2>&1 | tee "$LOG"
