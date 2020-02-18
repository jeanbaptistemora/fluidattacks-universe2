#!/usr/bin/env bash

deploy_playstore() {

  # Deploys Integrates apk to Google Playstore

  set -e

  # Import functions
  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/sops.sh)
  . ci-scripts/helpers/sops.sh

  local ENV_NAME

  if [ "$CI_COMMIT_REF_NAME" == 'master' ]; then
    ENV_NAME='production'
  else
    ENV_NAME='development'
  fi

  aws_login "$ENV_NAME"

  sops \
    --aws-profile default \
    --decrypt \
    --extract "[\"PLAYSTORE_CREDENTIALS\"]" \
    --output mobile/playstore-credentials.json \
    --output-type json \
    "secrets-$ENV_NAME.yaml"

  cd mobile || return 1

  bundle exec fastlane supply \
    --aab ./output/integrates.aab \
    --json_key ./playstore-credentials.json \
    --package_name "com.fluidattacks.integrates" \
    --track "$MOBILE_RELEASE_CHANNEL"

  rm playstore-credentials.json

  cd .. || return 1

}

deploy_playstore
