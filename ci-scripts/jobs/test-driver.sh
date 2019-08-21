#!/usr/bin/env bash

test_driver() {

  # Run selenium tests on ephemeral or prod

  set -e

  mkdir -p screenshots

  pytest \
    --ds=fluidintegrates.settings \
    --verbose \
    --exitfirst \
    --basetemp=build/test \
    --test-group-count "${CI_NODE_TOTAL}" \
    --test-group "${CI_NODE_INDEX}" \
    app/ephimeral_tests.py
}

test_driver
