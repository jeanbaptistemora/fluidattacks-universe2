#!/usr/bin/env bash

deps_production() {

  # Builds container if any of the specified files
  # was modified

  set -e

  # import functions
  . ci-scripts/helpers/check-changed.sh
  . ci-scripts/helpers/others.sh

  local NAME

  NAME='deps-production'

  kaniko_build \
    "$NAME" \
    eph=true \
    cache=true
}

deps_production
