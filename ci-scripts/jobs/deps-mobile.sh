#!/usr/bin/env bash

deps_mobile() {

  # Builds container if any of the specified files
  # was modified

  set -e

  # import functions
  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/build-container.sh)
  . ci-scripts/helpers/check-changed.sh

  local NAME
  local FILES

  NAME='deps-mobile'
  FILES=(
    'mobile/package.json'
    'mobile/Gemfile'
    'deploy/containers/deps-mobile/Dockerfile'
    'ci-scripts/jobs/deps-mobile.sh'
  )

  if check_file_changed "${FILES[@]}" \
     || [ $SCHEDULE ]; then
    echo "fs.inotify.max_user_watches=524288" >> /etc/sysctl.conf \
      && sysctl -p
    build_container \
      "registry.gitlab.com/fluidattacks/integrates/$NAME:$CI_COMMIT_REF_NAME" \
      "$CI_PROJECT_DIR" \
      -f "deploy/containers/$NAME/Dockerfile"
  else
    echo "No relevant files for $NAME were modified. Skipping build."
  fi
}

deps_mobile
