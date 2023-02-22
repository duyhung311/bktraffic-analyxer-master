#!/bin/bash

export PYSPARK_PYTHON=./environment/bin/python
export PYSPARK_DRIVER_PYTHON=python # Do not set in cluster modes.

spark-submit --deploy-mode client --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 --archives bktraffic-analyxer.tar.gz#environment SpeechReportJob_spark.py
