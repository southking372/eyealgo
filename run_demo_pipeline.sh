#!/bin/bash
set -e

source ~/miniconda3/etc/profile.d/conda.sh
conda activate eye-hpc
export PYTHONNOUSERSITE=1

cd ~/eyealgo

python -u scripts/01_run_pymovements.py
python -u scripts/02_make_generic_csv.py
python -u scripts/03_export_for_remodnav.py
remodnav data/processed/remodnav_input.tsv data/events/remodnav_events.tsv 0.03 1000
python -u scripts/04_prepare_pupeyes_csv.py
python -u scripts/05_plot_pupil_basic.py

echo "all done"
