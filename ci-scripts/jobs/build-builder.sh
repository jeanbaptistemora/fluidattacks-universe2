build_builder() {

  # Build serves builder

  set -Eeuo pipefail

  # Import functions
  . ci-scripts/helpers/others.sh

  build_container \
    "registry.gitlab.com/fluidattacks/serves/builder:$CI_COMMIT_REF_NAME" \
    containers/builder
}

build_builder
