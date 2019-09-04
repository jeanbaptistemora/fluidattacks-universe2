#!/usr/bin/env bash

build_app() {

  # Builds app container for either production or ephemeral app

  set -e

  # import functions
  . ci-scripts/helpers/others.sh

  vault_install /busybox
  vault_login

  # Set necessary envars
  export FI_DRIVE_AUTHORIZATION
  export FI_DRIVE_AUTHORIZATION_CLIENT
  export FI_DOCUMENTROOT
  export FI_SSL_KEY
  export FI_SSL_CERT
  FI_DRIVE_AUTHORIZATION=$(vault read -field=drive_authorization secret/integrates/$ENV_NAME)
  FI_DRIVE_AUTHORIZATION_CLIENT=$(vault read -field=drive_authorization_client secret/integrates/$ENV_NAME)
  FI_DOCUMENTROOT=$(vault read -field=documentroot secret/integrates/$ENV_NAME)
  FI_SSL_KEY=$(vault read -field=ssl_key secret/integrates/$ENV_NAME)
  FI_SSL_CERT=$(vault read -field=ssl_cert secret/integrates/$ENV_NAME)

  # Get version
  FI_VERSION=$(app_version)
  echo -n "$FI_VERSION" > version.txt

  kaniko_login

  # Set destination flag based on whether the building branch is
  # either production or from a dev
  if [ "$CI_COMMIT_REF_NAME" = 'master' ]; then
    PUSH_POLICY="--destination $CI_REGISTRY_IMAGE:app"
  else
    PUSH_POLICY="--destination $CI_REGISTRY_IMAGE/ephemeral/app:$CI_COMMIT_REF_NAME"
  fi

  # Build container using kaniko
  /kaniko/executor \
    --build-arg CI_API_V4_URL="$CI_API_V4_URL" \
    --build-arg CI_COMMIT_REF_NAME="$CI_COMMIT_REF_NAME" \
    --build-arg CI_PROJECT_ID="$CI_PROJECT_ID" \
    --build-arg CI_REPOSITORY_URL="$CI_REPOSITORY_URL" \
    --build-arg DOCUMENTROOT="$FI_DOCUMENTROOT" \
    --build-arg DRIVE_AUTHORIZATION="$FI_DRIVE_AUTHORIZATION" \
    --build-arg DRIVE_AUTHORIZATION_CLIENT="$FI_DRIVE_AUTHORIZATION_CLIENT" \
    --build-arg ENV_NAME="$ENV_NAME" \
    --build-arg SSL_CERT="$FI_SSL_CERT" \
    --build-arg SSL_KEY="$FI_SSL_KEY" \
    --build-arg VERSION="$FI_VERSION" \
    --cache=false \
    --cleanup \
    --context "deploy/containers/app" \
    --dockerfile "deploy/containers/app/Dockerfile" \
    $PUSH_POLICY \
    --single-snapshot \
    --snapshotMode time
}

build_app
