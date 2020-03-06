#!/usr/bin/env bash

deps_development() {

  # Builds container if any of the specified files
  # was modified

  set -e

  # import functions
  . <(curl -sL https://static-objects.gitlab.net/fluidattacks/public/raw/master/shared-scripts/build-container.sh)

  local NAME

  NAME='deps-development'

  build_container \
    "registry.gitlab.com/fluidattacks/integrates/$NAME:$CI_COMMIT_REF_NAME" \
    "$CI_PROJECT_DIR" \
    -f "deploy/containers/$NAME/Dockerfile" \
    --build-arg CI_COMMIT_REF_NAME="$CI_COMMIT_REF_NAME"
}

deps_development
