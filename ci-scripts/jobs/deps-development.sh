#!/usr/bin/env bash

deps_development() {

  # Builds container if any of the specified files
  # was modified

  set -e

  # import functions
  . ci-scripts/helpers/check-changed.sh
  . ci-scripts/helpers/others.sh

  local NAME
  local FILES

  NAME='deps-development'
  FILES=(
    'deploy/containers/deps-production/requirements.txt'
    'deploy/containers/deps-development/requirements.txt'
    'deploy/containers/deps-production/Dockerfile'
    'deploy/containers/deps-development/Dockerfile'
    'front/package.json'
  )

  if check_file_changed "${FILES[@]}"; then
    kaniko_build "$NAME"
  else
    echo "No relevant files for $NAME were modified. Skipping build."
  fi
}

deps_development
