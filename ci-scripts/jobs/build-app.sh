#!/usr/bin/env bash

build_app() {

  # Builds app container for either production or ephemeral app

  set -e

  # import functions
  . <(curl -sL https://static-objects.gitlab.net/fluidattacks/public/raw/master/shared-scripts/build-container.sh)
  . <(curl -sL https://static-objects.gitlab.net/fluidattacks/public/raw/master/shared-scripts/sops.sh)
  . ci-scripts/helpers/others.sh
  . ci-scripts/helpers/sops.sh

  # Set necessary env vars

  local ENV_NAME
  local NAME

  if [ "$CI_COMMIT_REF_NAME" == 'master' ]; then
    ENV_NAME="production"
  else
    ENV_NAME="development"
  fi

  aws_login "$ENV_NAME"

  sops_env "secrets-$ENV_NAME.yaml" default \
    SSL_KEY \
    SSL_CERT \
    DRIVE_AUTHORIZATION \
    DRIVE_AUTHORIZATION_CLIENT

  NAME='app'

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
    --build-arg SSL_CERT="$SSL_CERT" \
    --build-arg SSL_KEY="$SSL_KEY" \
    --build-arg VERSION="$FI_VERSION"
}

build_app
