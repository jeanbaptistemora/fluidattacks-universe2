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
  FILES=(
    'front/package.json'
    'deploy/containers/deps-production/Dockerfile'
    'deploy/containers/deps-production/requirements.txt'
    'ci-scripts/jobs/deps-production.sh'
  )
  
  if check_file_changed "${FILES[@]}" \
     || [ $SCHEDULE ]; then
	  kaniko_build \
	    "$NAME" \
	    eph=true \
	    cache=true
  else
      echo "No relevant files for $NAME were modified. Skipping build."
  fi
}

deps_production
