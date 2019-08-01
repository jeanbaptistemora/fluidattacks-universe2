#!/usr/bin/env bash

deploy_playstore() {

  # Deploys Integrates apk to Google Playstore

  # import functions
  . ci-scripts/helpers/others.sh

  # Logs in to vault in order to read variables
  vault_login

  cd mobile/
  vault read -field=playstore_credentials secret/integrates/production \
    > playstore-credentials.json
  bundle install
  bundle exec fastlane supply \
    --aab ./output/integrates.aab \
    --json_key ./playstore-credentials.json \
    --package_name "com.fluidattacks.integrates" \
    --track "$MOBILE_RELEASE_CHANNEL"

  rm mobile/playstore-credentials.json
}

deploy_playstore
