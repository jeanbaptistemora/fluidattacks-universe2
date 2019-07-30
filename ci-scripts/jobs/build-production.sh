#!/usr/bin/env bash

build_production() {

  # Builds mobile container if mobile/package.json OR
  # mobile/Gemfile OR deploy/containers/mobile/Dockerfile
  # were modified.

  set -e

  # import functions
  . ci-scripts/helpers/check-changed.sh
  . ci-scripts/helpers/others.sh

  local FILES=(
    'deploy/containers/production/requirements.txt'
    'front/package.json'
    'deploy/containers/production/Dockerfile'
  )

  if check_file_changed "${FILES[@]}"; then
    kaniko_build production
  else
    echo 'No relevant files for mobile build were modified. Skipping build.'
  fi
}

build_production
