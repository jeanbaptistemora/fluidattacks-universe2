#!/usr/bin/env bash

deps_dev() {

  # Builds container if any of the specified files
  # was modified

  set -e

  # import functions
  . ci-scripts/helpers/check-changed.sh
  . ci-scripts/helpers/others.sh

  local NAME
  local FILES

  NAME='deps-dev'
  FILES=(
    'deploy/containers/deps-prod/requirements.txt'
    'deploy/containers/deps-dev/requirements.txt'
    'deploy/containers/deps-prod/Dockerfile'
    'deploy/containers/deps-dev/Dockerfile'
    'front/package.json'
  )

  if check_file_changed "${FILES[@]}"; then
    kaniko_build "$NAME"
  else
    echo "No relevant files for $NAME were modified. Skipping build."
  fi
}

deps_dev
