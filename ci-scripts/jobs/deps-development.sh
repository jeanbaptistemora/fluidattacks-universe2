#!/usr/bin/env bash

deps_development() {

  # Builds container if any of the specified files
  # was modified

  set -e

  # import functions
  . ci-scripts/helpers/check-changed.sh
  . ci-scripts/helpers/others.sh

  local NAME

  NAME='deps-development'

  kaniko_build \
    "$NAME" \
    eph=true \
    cache=true \
    --build-arg CI_COMMIT_REF_NAME="$CI_COMMIT_REF_NAME"
}

deps_development
