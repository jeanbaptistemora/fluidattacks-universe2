#!/bin/bash
set -e

echo "Deploying to Apple TestFlight ..."
export FASTLANE_APPLE_APPLICATION_SPECIFIC_PASSWORD="$FI_APPLE_TESTFLIGHT_PASSWORD"
export EXPO_APPLE_ID="$FI_APPLE_ID"
export EXPO_APPLE_ID_PASSWORD="$FI_APPLE_PASSWORD"

npx expo upload:ios \
  --app-name Integrates \
  --sku com.fluidattacks.integrates \
  --path output/integrates.ipa
