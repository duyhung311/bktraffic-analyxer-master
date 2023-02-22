.ONESHELL:

.PHONY: clean clean-all setup install run start stop all

clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete

clean-all:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete
	find resources/ -not -name 'streets.txt' -delete

setup:
	conda env create --file conda.yml

install:
	bash scripts/install.sh

run:
	chmod 755 cron_job.py
	bash scripts/run.sh

start:
	chmod 755 cron_job.py
	bash scripts/start-server.sh

stop:
	bash scripts/stop-server.sh

all: clean setup start
