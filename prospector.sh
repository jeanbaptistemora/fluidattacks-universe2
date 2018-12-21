#!/usr/bin/env bash
set -e

prospector -u django -p app/ -i node_modules
prospector -u django fluidintegrates/

cp -a $PWD /usr/src/app_src
cd /usr/src/app_src
pytest --ds=fluidintegrates.settings --verbose --exitfirst --cov=fluidintegrates --cov-report term --cov-report html:build/coverage/html --cov-report xml:build/coverage/results.xml --cov-report annotate:build/coverage/annotate --basetemp=build/test --junitxml=build/test/results.xml app/tests.py
