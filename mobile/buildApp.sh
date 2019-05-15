#!/bin/bash
set -e

# Prepare AWS
AWS_ACCESS_KEY_ID="$FI_AWS_INNOVATION_S3_ACCESS_KEY"
export AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY="$FI_AWS_INNOVATION_S3_SECRET_KEY"
export AWS_SECRET_ACCESS_KEY
aws s3 cp "$FI_KEYSTORE_S3_URL" keystore-dev.jks


# Prepare Expo
EXPO_ANDROID_KEYSTORE_PASSWORD=$FI_EXPO_PASSWORD
export EXPO_ANDROID_KEYSTORE_PASSWORD
EXPO_ANDROID_KEY_PASSWORD=$FI_EXPO_PASSWORD
export EXPO_ANDROID_KEY_PASSWORD
LOGGER_LEVEL="info"
export LOGGER_LEVEL


# Build
echo "Building android .apk ..."
mkdir output/
npx turtle build:android \
  --username "$FI_EXPO_USERNAME" \
  --password "$FI_EXPO_PASSWORD" \
  --keystore-path ./keystore-dev.jks \
  --keystore-alias fluidintegrates-keystore \
  --output output/integrates.apk


# Cleanup
echo "All done! Cleaning up..."
rm keystore-dev.jks
