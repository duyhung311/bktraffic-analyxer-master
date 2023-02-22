# Bktraffic Analyxer

## System requirements
```
RAM: 2GB
Disk: 3GB
OS: Linux (Ubuntu)
Python: 3.7 (setup with Conda or Docker)
```
<br />

# Setup server environment
## Conda (RECOMMEND)
### 1. Install Anaconda (or Miniconda) in home directory (ie. `/home/<user>/anaconda3/`)

https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html

### 2. Setup conda virtual environment (make sure you can use `conda` in terminal, only Linux)
```
make setup
```

This command creates a new conda environment name `bktraffic-analyxer` using `conda.yml`, if error occurs (ie. due to OS build), try below command to install from scratch:
```
make install
```

### 3. Conda utility
#### To use environment
```
conda activate bktraffic-analyxer
```

#### To deactivate current running Conda environment
```
conda deactivate
```

#### To update `conda.yml` in case of environment modification (add/update packages, change python version, etc.)
```
conda env export --no-builds --name bktraffic-analyxer > conda.yml
```
Remember to set **prefix** in conda.yml to: `~/anaconda3/envs/bktraffic-analyxer`
<br />

## Docker (ignore if using Conda)

### 1. Build image
```
docker build . -t bktraffic-analyxer:0.1
```

### 2. Run container
#### 2.1. If using CUDA backend (Install [nvidia-docker](https://github.com/NVIDIA/nvidia-docker))
```
docker run --runtime=nvidia --rm -itd --ipc=host --name bktraffic-analyxer bktraffic-analyxer:0.1
```

#### 2.2. If using CPU backend
```
docker run --rm -itd --ipc=host --name bktraffic-analyxer bktraffic-analyxer:0.1
```

### 3. Start a terminal session inside the container
```
docker exec -it bktraffic-analyxer bash
```
<br />

# Run server
## 1. Create .env
- Copy `.env.example` to `.env`

## 2. Run
- Developement:
```
# Set `FLASK_ENV=development` in file `.env`
make run        # To start Flask in local
make stop       # To clear cron_job
```
- Deploy production:
```
# Set `FLASK_ENV=production` in file `.env`
make start      # To start Flask with gunicorn
make stop       # To stop server (gunicorn workers)
```

<br />

# Run Spark job (required using Conda) [WIP ⚠]
https://databricks.com/blog/2020/12/22/how-to-manage-python-dependencies-in-pyspark.html
## 1. Activate Conda environment (if haven't) and pack it
```
conda activate bktraffic-analyxer
conda pack
```
A packed file will be created: `bktraffic-analyxer.tar.gz`

## 2. Deploy (https://spark.apache.org/docs/latest/submitting-applications.html)
Modify --master yarn if you want to run in different way

### 2.1. Client mode
```
PYSPARK_DRIVER_PYTHON=python PYSPARK_PYTHON=/Users/hungluong/opt/anaconda3/pkgs/pyspark-3.1.2-pyhd3eb1b0_0/site-packages/pyspark/bin/spark-submit --deploy-mode client --master yarn --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 --archives bktraffic-analyxer.tar.gz#environment SpeechReportJob_spark.py
```

### 2.2. Cluster mode
```
PYSPARK_PYTHON=./environment/bin/python spark-submit --deploy-mode cluster --master yarn --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 --archives bktraffic-analyxer.tar.gz#environment SpeechReportJob_spark.py
```
