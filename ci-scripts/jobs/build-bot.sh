#!/usr/bin/env bash

build_bot() {

  # Build bot container for either production or ephemeral app

  set -e

  # import functions
  . ci-scripts/helpers/others.sh

  kaniko_login

  # Set destination flag based on whether the building branch is
  # either production or from a dev
  if [ "$CI_COMMIT_REF_NAME" = 'master' ]; then
    PUSH_POLICY="--destination $CI_REGISTRY_IMAGE:bot"
    ENV_NAME='production'
  else
    PUSH_POLICY="--destination $CI_REGISTRY_IMAGE/ephemeral/bot:$CI_COMMIT_REF_NAME"
    ENV_NAME='development'
  fi

  # Build container using kaniko
  /kaniko/executor \
    --build-arg CI_API_V4_URL="${CI_API_V4_URL}" \
    --build-arg CI_COMMIT_REF_NAME="${CI_COMMIT_REF_NAME}" \
    --build-arg CI_PROJECT_ID="${CI_PROJECT_ID}" \
    --build-arg ENV_NAME="${ENV_NAME}" \
    --cleanup \
    --context "deploy/containers/bot/" \
    --dockerfile "deploy/containers/bot/Dockerfile" \
    $PUSH_POLICY \
    --single-snapshot \
    --snapshotMode time

}

build_bot
