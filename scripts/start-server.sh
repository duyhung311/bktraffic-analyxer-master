#!/bin/bash
set -o allexport
source .env
set +o allexport

eval "$(conda shell.bash hook)"
conda activate bktraffic-analyxer

if [ $FLASK_ENV == "production" ]
then
  while [ true ]
  do
    echo "STARTING WEB SERVER"
    timeout 8h gunicorn --config gunicorn.conf.py
    sleep 8h
  done
fi
