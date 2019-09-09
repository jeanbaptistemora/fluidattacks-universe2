#!/usr/bin/env bash

deps_mobile() {

  # Builds container if any of the specified files
  # was modified

  set -e

  # import functions
  . ci-scripts/helpers/check-changed.sh
  . ci-scripts/helpers/others.sh

  local NAME
  local FILES

  NAME='deps-mobile'
  FILES=(
    'mobile/package.json'
    'mobile/Gemfile'
    'deploy/containers/mobile/Dockerfile'
    'ci-scripts/jobs/deps-mobile.sh'
  )

  if check_file_changed "${FILES[@]}" \
    || [ $SCHEDULE ]; then
      kaniko_build \
        "$NAME" \
        eph=false \
        cache=true
  else
    echo "No relevant files for $NAME were modified. Skipping build."
  fi
}

deps_mobile
