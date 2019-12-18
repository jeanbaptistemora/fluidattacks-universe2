#!/usr/bin/env bash

deps_mobile() {

  # Builds container if any of the specified files
  # was modified

  set -e

  # import functions
  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/build-container.sh)

  local NAME

  NAME='deps-mobile'

  echo "fs.inotify.max_user_watches=524288" >> /etc/sysctl.conf \
    && sysctl -p
  build_container \
    "registry.gitlab.com/fluidattacks/integrates/$NAME:$CI_COMMIT_REF_NAME" \
    "$CI_PROJECT_DIR" \
    -f "deploy/containers/$NAME/Dockerfile"
}

deps_mobile
