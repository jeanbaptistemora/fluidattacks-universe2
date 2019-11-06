#!/usr/bin/env bash

test_driver() {

  # Run selenium tests on ephemeral or prod

  set -e

  if [[ x"${CI_COMMIT_REF_NAME}" = x"master" ]]; then
    TEST_FILE=app/ephemeral_tests_prod.py
  else
    TEST_FILE=app/ephemeral_tests_dev.py
  fi

  mkdir -p screenshots

  pytest \
    --ds=fluidintegrates.settings \
    --verbose \
    --exitfirst \
    --basetemp=build/test \
    --test-group-count "${CI_NODE_TOTAL}" \
    --test-group "${CI_NODE_INDEX}" \
    ${TEST_FILE}
}

test_driver
