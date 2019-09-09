#!/usr/bin/env sh

build_bot() {

  # Build bot container for either production or ephemeral app

  set -e

  # Import functions
  . ci-scripts/helpers/others.sh

  kaniko_login

  # Set ENV_NAME var
  if [ "$CI_COMMIT_REF_NAME" = 'master' ]; then
    ENV_NAME='production'
  else
    ENV_NAME='development'
  fi

  NAME='bot'

  # Build container using kaniko
  kaniko_build \
    "$NAME" \
    eph=true \
    cache=false \
    --single-snapshot \
    --build-arg CI_API_V4_URL="$CI_API_V4_URL" \
    --build-arg CI_COMMIT_REF_NAME="$CI_COMMIT_REF_NAME" \
    --build-arg CI_PROJECT_ID="$CI_PROJECT_ID" \
    --build-arg ENV_NAME="$ENV_NAME"
}

build_bot
