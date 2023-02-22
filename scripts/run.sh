#!/bin/bash
set -o allexport
source .env
set +o allexport

eval "$(conda shell.bash hook)"
conda activate bktraffic-analyxer
/Users/hungluong/opt/anaconda3/bin/python app.py
# python3 app.py
