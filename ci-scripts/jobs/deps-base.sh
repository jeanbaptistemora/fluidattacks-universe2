#!/usr/bin/env bash

deps_base() {

  # Builds container if any of the specified files
  # was modified

  set -e

  # import functions
  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/build-container.sh)
  . ci-scripts/helpers/check-changed.sh

  local NAME

  NAME='deps-base'
  FILES=(
    'deploy/containers/deps-base/Dockerfile'
    'ci-scripts/jobs/deps-base.sh'
  )
  FOLDERS=(
      'ci-scripts/helpers/'
  )
  if [ x"$CI_COMMIT_REF_NAME" = x"master" ] \
     || check_folder_changed "${FOLDERS[@]}" \
     || check_file_changed "${FILES[@]}" \
     || docker_tag_not_exists deps-base $CI_COMMIT_REF_NAME \
     || container_image_differs deps-base $CI_COMMIT_REF_NAME \
     || [ $SCHEDULE ]; then
    build_container \
      "registry.gitlab.com/fluidattacks/integrates/$NAME:$CI_COMMIT_REF_NAME" \
      "deploy/containers/$NAME"
  else
      echo "No relevant files for $NAME were modified. Skipping build."
  fi

}

deps_base
