#!/usr/bin/env bash

build_pelican() {
  # Build pelican container

  set -e

  # shellcheck source=https://static-objects.gitlab.net/fluidattacks/public/raw/master/shared-scripts/build-container.sh
  # shellcheck disable=SC1091
  . <(curl -sL https://static-objects.gitlab.net/fluidattacks/public/raw/master/shared-scripts/build-container.sh)

  # Build container
  build_container \
    "${CI_REGISTRY_IMAGE}/ephemeral:${CI_COMMIT_REF_SLUG}" \
    "${CI_PROJECT_DIR}" \
    --build-arg CI_COMMIT_REF_NAME="${CI_COMMIT_REF_NAME}" \
    --file "${CI_PROJECT_DIR}/deploy/ephemeral/Dockerfile"
}
