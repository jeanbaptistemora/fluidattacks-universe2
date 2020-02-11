# shellcheck shell=bash

build_builder() {

  # Build serves builder

  set -Eeuo pipefail

  # Import functions
  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/build-container.sh)

  build_container \
    "registry.gitlab.com/fluidattacks/serves/builder:$CI_COMMIT_REF_NAME" \
    containers/builder
}

build_builder
