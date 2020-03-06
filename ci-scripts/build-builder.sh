#!/usr/bin/env bash

build_builder() {

  # Build web builder

  set -e

  # shellcheck source=https://static-objects.gitlab.net/fluidattacks/public/raw/master/shared-scripts/build-container.sh
  # shellcheck disable=SC1091
  . <(curl -sL https://static-objects.gitlab.net/fluidattacks/public/raw/master/shared-scripts/build-container.sh)

  build_container \
    "registry.gitlab.com/fluidattacks/web/builder:${CI_COMMIT_REF_NAME}" \
    "${CI_PROJECT_DIR}" \
    --file "${CI_PROJECT_DIR}/deploy/builder/Dockerfile"
}
