#!/usr/bin/env bash
test_driver() {

  # Run selenium tests on ephemeral or prod

  set -e

  . ci-scripts/helpers/sops.sh

  local ENV_NAME

  if [ "$CI_COMMIT_REF_NAME" == 'master' ]; then
    ENV_NAME='production'
  else
    ENV_NAME='development'
  fi

  aws_login "$ENV_NAME"

  sops_vars "$ENV_NAME"

  mkdir -p screenshots

  pytest \
    --ds=fluidintegrates.settings \
    --verbose \
    --exitfirst \
    --basetemp=build/test \
    --test-group-count "$CI_NODE_TOTAL" \
    --test-group "$CI_NODE_INDEX" \
    ephemeral_tests.py
}

test_driver
