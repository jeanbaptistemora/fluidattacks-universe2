#!/usr/bin/env bash

deps_production() {

  # Builds container if any of the specified files
  # was modified

  set -e

  # import functions
  . ci-scripts/helpers/check-changed.sh
  . ci-scripts/helpers/others.sh

  local NAME
  local FILES

  NAME='deps-production'
  FILES=(
    'deploy/containers/deps-production/requirements.txt'
    'front/package.json'
    'deploy/containers/deps-production/Dockerfile'
  )

  if check_file_changed "${FILES[@]}" \
    || ! reg_repo_tag_exists "$NAME" "$CI_COMMIT_REF_NAME"; then
    kaniko_build_experimental \
      "$NAME" \
      cache=true
  else
    echo "No relevant files for $NAME were modified. Skipping build."
  fi
}

deps_production
