#!/usr/bin/env bash

build_deps_dev() {

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
    'deploy/containers/production/requirements.txt'
    'deploy/containers/development/requirements.txt'
    'deploy/containers/production/Dockerfile'
    'deploy/containers/development/Dockerfile'
    'front/package.json'
  )

  if check_file_changed "${FILES[@]}"; then
    kaniko_build "$NAME"
  else
    echo "No relevant files for $NAME were modified. Skipping build."
  fi
}

build_deps_dev
