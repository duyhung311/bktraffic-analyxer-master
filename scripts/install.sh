#!/bin/bash
set -o allexport
source .env
set +o allexport

eval "$(conda shell.bash hook)"
conda create --name bktraffic-analyxer python=3.7.12 --yes --file pkgs.txt
conda activate bktraffic-analyxer
pip install -r requirements.txt
