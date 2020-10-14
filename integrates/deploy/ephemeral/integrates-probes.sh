#! /usr/bin/env bash

function test_aws_credentials {
  if aws sts get-caller-identity | grep -q 'integrates-dev'
  then
    echo '[INFO] Passed: test_aws_credentials'
  else
        echo '[ERROR] AWS credentials could not be validated.' \
    &&  return 1
  fi
}

function test_curl_localhost {
  if curl -sSiL http://localhost:8080 | grep -q 'Please contact your administrator'
  then
    echo '[INFO] Passed: test_curl_localhost'
  else
        echo '[ERROR] Localhost curl failed.' \
    &&  return 1
  fi
}

function test_curl_ephemeral {
  if curl -sSiL "https://${CI_COMMIT_REF_NAME}.integrates.fluidattacks.com" | grep -q 'FluidIntegrates'
  then
    echo '[INFO] Passed: test_curl_ephemeral'
  else
        echo '[ERROR] Ephemeral curl failed.' \
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
  &&  test_curl_ephemeral
}


set -o pipefail

"${1}"
