#! /usr/bin/env bash

function test_aws_credentials {
  if aws sts get-caller-identity | grep -q 'integrates-prod'
  then
    echo '[INFO] Passed: test_aws_credentials'
  else
        echo '[ERROR] AWS credentials could not be validated.' \
    &&  return 1
  fi
}

function test_curl_localhost {
  if curl -sS http://localhost:8080 | grep -q 'FluidIntegrates'
  then
    echo '[INFO] Passed: test_curl_localhost'
  else
        echo '[ERROR] Localhost curl failed.' \
    &&  return 1
  fi
}

function test_curl_production {
  if curl -sS "https://integrates.fluidattacks.com" | grep -q 'FluidIntegrates'
  then
    echo '[INFO] Passed: test_curl_production'
  else
        echo '[ERROR] Production curl failed.' \
    &&  return 1
  fi
}

function run_readiness_probe {
      test_aws_credentials \
  &&  test_curl_localhost
}

function run_liveness_probe {
      test_aws_credentials \
  &&  test_curl_localhost \
  &&  test_curl_production
}


set -o pipefail

"${1}"
