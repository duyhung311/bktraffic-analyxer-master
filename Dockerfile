FROM python:3.7

# set working directory
WORKDIR /bktraffic-analyxer

# copy requirements.txt to working directory
COPY requirements.txt .

# install library on OS
RUN apt-get update && apt-get install -y \
  ffmpeg \
  libtinfo5 \
  vim

# install our dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy source
COPY . .
