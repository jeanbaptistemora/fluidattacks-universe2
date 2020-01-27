#!/usr/bin/env bash

build_builder() {

  # Build web builder

  set -e

  # shellcheck source=https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/build-container.sh
  # shellcheck disable=SC1091
  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/build-container.sh)

  build_container \
    "registry.gitlab.com/fluidattacks/web/builder:$CI_COMMIT_REF_NAME" \
    builder/base
}
