#!/usr/bin/env bash

# build image from dockerfile
echo "INFO: attempting to build image"
if docker build -f orchestrator.dockerfile -t orchestrate:now . ; then
  echo "INFO: built succesfully"
  echo "INFO: running"

  # move everything from formstack API to stitchdata API
  docker run --rm orchestrate:now /bin/bash -c \
    "tap_formstack -c /auth/auth_formstack.json | target-stitch -c /auth/auth_stitchdata.json"
else
  echo "ERROR: couldn't build image"
fi
