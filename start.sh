#!/bin/sh
# First run: creates the Python environment, installs packages, runs start.py.
# Later runs reuse the environment, so they're fast.
set -e
cd "$(dirname "$0")"
[ -d .venv ] || python3 -m venv .venv
.venv/bin/pip install -q -r requirements.txt
.venv/bin/python start.py
printf "\nNext: open the notebooks with  .venv/bin/jupyter lab\n"
