#!/usr/bin/env bash

test_app() {

  # Runs linters and unit tests on app

  set -e

  # Linters
  prospector -F -s veryhigh -u django -p app/ -i node_modules || true
  prospector -F -s high -u django -p app/ -i node_modules
  prospector -F -s veryhigh -u django fluidintegrates/

  # Unit tests
  cp -a "$PWD" /usr/src/app_src
  cd /usr/src/app_src || return 1
  service redis-server start
  pytest \
    --ds=fluidintegrates.settings \
    --verbose \
    --exitfirst \
    --cov=fluidintegrates \
    --cov=app \
    --cov-report term \
    --cov-report html:build/coverage/html \
    --cov-report xml:build/coverage/results.xml \
    --cov-report annotate:build/coverage/annotate \
    --basetemp=build/test \
    --junitxml=build/test/results.xml \
    app/test/
  cp -a build/coverage/results.xml "$CI_PROJECT_DIR/coverage.xml"

  cd "$CI_PROJECT_DIR" || return 1
}

test_app
