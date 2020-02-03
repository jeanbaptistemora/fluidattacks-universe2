#!/usr/bin/env bash

deploy_playstore() {

  # Deploys Integrates apk to Google Playstore

  cd mobile/
  bundle install
  bundle exec fastlane supply \
    --aab ./output/integrates.aab \
    --json_key ./playstore-credentials.json \
    --package_name "com.fluidattacks.integrates" \
    --track "$MOBILE_RELEASE_CHANNEL"

  rm mobile/playstore-credentials.json
}

deploy_playstore
