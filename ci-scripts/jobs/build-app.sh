#!/usr/bin/env sh

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
  export FI_SSL_KEY
  export FI_SSL_CERT
  FI_DRIVE_AUTHORIZATION=$(vault read -field=drive_authorization secret/integrates/$ENV_NAME)
  FI_DRIVE_AUTHORIZATION_CLIENT=$(vault read -field=drive_authorization_client secret/integrates/$ENV_NAME)
  FI_SSL_KEY=$(vault read -field=ssl_key secret/integrates/$ENV_NAME)
  FI_SSL_CERT=$(vault read -field=ssl_cert secret/integrates/$ENV_NAME)

  # Get version
  FI_VERSION=$(app_version)
  echo -n "$FI_VERSION" > version.txt

  kaniko_login

  NAME='app'

  # Build container using kaniko
  kaniko_build \
    "$NAME" \
    eph=true \
    cache=false \
    --single-snapshot \
    --build-arg CI_API_V4_URL="$CI_API_V4_URL" \
    --build-arg CI_COMMIT_REF_NAME="$CI_COMMIT_REF_NAME" \
    --build-arg CI_PROJECT_ID="$CI_PROJECT_ID" \
    --build-arg CI_REPOSITORY_URL="$CI_REPOSITORY_URL" \
    --build-arg FI_DRIVE_AUTHORIZATION="$FI_DRIVE_AUTHORIZATION" \
    --build-arg FI_DRIVE_AUTHORIZATION_CLIENT="$FI_DRIVE_AUTHORIZATION_CLIENT" \
    --build-arg ENV_NAME="$ENV_NAME" \
    --build-arg SSL_CERT="$FI_SSL_CERT" \
    --build-arg SSL_KEY="$FI_SSL_KEY" \
    --build-arg VERSION="$FI_VERSION"
}

build_app
