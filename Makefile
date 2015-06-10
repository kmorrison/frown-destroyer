.PHONY: clean build deploy

all: build

clean:
	find . -name '*.pyc' -exec rm -f {} +
	rm -rf lib/*

build:
	pip install -r requirements.txt -t lib/

dev: build
	dev_appserver.py .

deploy: clean build
	appcfg.py -A frown-destroyer --oauth2 update .
