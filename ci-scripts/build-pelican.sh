#!/usr/bin/env bash

build_pelican() {
  # Build pelican container

  set -e

  # shellcheck source=https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/build-container.sh
  # shellcheck disable=SC1091
  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/build-container.sh)

  # Build container
  build_container \
    "${CI_REGISTRY_IMAGE}/review:$CI_COMMIT_REF_SLUG" \
    "$CI_PROJECT_DIR/review/" \
    --build-arg CI_COMMIT_REF_NAME="${CI_COMMIT_REF_NAME}" \
    --build-arg CI_PROJECT_NAME="${CI_PROJECT_NAME}" \
    --build-arg CI_PROJECT_NAMESPACE="${CI_PROJECT_NAMESPACE}" \
    --build-arg CI_REPOSITORY_URL="${CI_REPOSITORY_URL}" \
    --build-arg ENV_DNS="${ENV_DNS}" \
    --build-arg REGISTRY_IMAGE="${CI_REGISTRY_IMAGE}/review" \
    --file "${CI_PROJECT_DIR}/review/Dockerfile"
}
