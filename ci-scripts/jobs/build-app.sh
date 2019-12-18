#!/usr/bin/env bash

build_app() {

  # Builds app container for either production or ephemeral app

  set -e

  # import functions
  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/build-container.sh)
  . ci-scripts/helpers/others.sh

  vault_install /usr/bin/
  vault_login

  # Set necessary envars
  local NAME
  export FI_DRIVE_AUTHORIZATION
  export FI_DRIVE_AUTHORIZATION_CLIENT
  export FI_SSL_KEY
  export FI_SSL_CERT
  NAME='app'
  FI_SSL_KEY=$(vault read -field=ssl_key secret/integrates/$ENV_NAME)
  FI_SSL_CERT=$(vault read -field=ssl_cert secret/integrates/$ENV_NAME)

  # Get version
  FI_VERSION=$(app_version)
  echo -n "$FI_VERSION" > version.txt

  # Build container
  build_container \
    "registry.gitlab.com/fluidattacks/integrates/$NAME:$CI_COMMIT_REF_NAME" \
    "$CI_PROJECT_DIR" \
    -f "deploy/containers/$NAME/Dockerfile" \
    --build-arg CI_API_V4_URL="$CI_API_V4_URL" \
    --build-arg CI_COMMIT_REF_NAME="$CI_COMMIT_REF_NAME" \
    --build-arg CI_PROJECT_ID="$CI_PROJECT_ID" \
    --build-arg CI_REPOSITORY_URL="$CI_REPOSITORY_URL" \
    --build-arg ENV_NAME="$ENV_NAME" \
    --build-arg SSL_CERT="$FI_SSL_CERT" \
    --build-arg SSL_KEY="$FI_SSL_KEY" \
    --build-arg VERSION="$FI_VERSION"
}

build_app
