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
    'deploy/containers/deps-production/requirements_local.txt'
    'ci-scripts/jobs/deps-production.sh'
  )
  FOLDERS=(
      'ci-scripts/helpers/'
  )
  if check_folder_changed "${FOLDERS[@]}" \
     || check_file_changed "${FILES[@]}" \
     || docker_tag_not_exists deps-production $CI_COMMIT_REF_NAME \
     || container_image_differs deps-production $CI_COMMIT_REF_NAME \
     || [ $SCHEDULE ]; then
	  kaniko_build \
	    "$NAME" \
	    eph=true \
	    cache=true \
	    --build-arg CI_COMMIT_REF_NAME="$CI_COMMIT_REF_NAME"
  else
      echo "No relevant files for $NAME were modified. Skipping build."
  fi

}

deps_production
