#!/usr/bin/env bash

build_mobile() {

  # Builds mobile container if mobile/package.json OR
  # mobile/Gemfile OR deploy/containers/mobile/Dockerfile
  # were modified.

  set -e

  # import functions
  . ci-scripts/helpers/check-changed.sh
  . ci-scripts/helpers/others.sh

  local FILES=(
    'mobile/package.json'
    'mobile/Gemfile'
    'deploy/containers/mobile/Dockerfile'
  )

  if check_file_changed "${FILES[@]}"; then
    kaniko_build mobile
    exit $?
  fi
  echo 'No relevant files for mobile build were modified. Skipping build.'
}

build_mobile
