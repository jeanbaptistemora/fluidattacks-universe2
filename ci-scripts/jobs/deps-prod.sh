#!/usr/bin/env bash

deps_prod() {

  # Builds container if any of the specified files
  # was modified

  set -e

  # import functions
  . ci-scripts/helpers/check-changed.sh
  . ci-scripts/helpers/others.sh

  local NAME
  local FILES

  NAME='deps-prod'
  FILES=(
    'deploy/containers/deps-prod/requirements.txt'
    'front/package.json'
    'deploy/containers/deps-prod/Dockerfile'
  )

  if check_file_changed "${FILES[@]}"; then
    kaniko_build "$NAME"
  else
    echo "No relevant files for $NAME were modified. Skipping build."
  fi
}

deps_prod
