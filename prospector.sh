#!/usr/bin/env bash
set -e

prospector -u django -p app/ -i node_modules
prospector -u django fluidintegrates/
python manage.py test app.tests --no-input
