#!/usr/bin/env bash

test_driver() {

  # Run selenium tests on ephemeral or prod

  # import functions
  . ci-scripts/helpers/others.sh

  # Logs in to vault in order to run vaultenv
  vault_login

  cp -a "$PWD" /usr/src/app_src
  cd /usr/src/app_src || return 1
  mkdir -p screenshots

  vaultenv -- pytest \
    --ds=fluidintegrates.settings \
    --verbose \
    --exitfirst \
    --basetemp=build/test \
    --test-group-count "${CI_NODE_TOTAL}" \
    --test-group "${CI_NODE_INDEX}" \
    app/ephimeral_tests.py

  cp -a screenshots "${CI_PROJECT_DIR}"
}

set -e

test_driver
