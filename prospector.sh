#!/usr/bin/env bash
set -e

prospector -u django -p app/ -i node_modules
prospector -u django fluidintegrates/
python -v manage.py test app.tests --no-input