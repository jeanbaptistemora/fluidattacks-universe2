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
npx expo login -u "$FI_EXPO_USERNAME" -p "$FI_EXPO_PASSWORD"
echo "fs.inotify.max_user_watches=524288" >> /etc/sysctl.conf && sysctl -p
DEVELOPER_ENV=${CI_COMMIT_REF_NAME:-"local"}

JAVA_OPTS="-Xmx1500m -XX:+HeapDumpOnOutOfMemoryError -XX:+UnlockExperimentalVMOptions -XX:+UseCGroupMemoryLimitForHeap -XX:+UseG1GC"
export JAVA_OPTS
GRADLE_OPTS="-Dorg.gradle.parallel=true -Dorg.gradle.daemon=false -Dorg.gradle.jvmargs='$JAVA_OPTS'"
export GRADLE_OPTS
GRADLE_DAEMON_DISABLED="1"
export GRADLE_DAEMON_DISABLED
DISABLE_DEX_MAX_HEAP="true"
export DISABLE_DEX_MAX_HEAP
echo "$FI_GOOGLE_SERVICES_APP" > google-services.json


# Build
echo "Updating app manifest ..."
npx expo publish \
  --release-channel "$DEVELOPER_ENV" \
  --non-interactive
echo "Building android .apk ..."
rm -r output/ && mkdir output/
npx turtle build:android \
  --username "$FI_EXPO_USERNAME" \
  --password "$FI_EXPO_PASSWORD" \
  --release-channel "$DEVELOPER_ENV" \
  --keystore-path ./keystore-dev.jks \
  --keystore-alias fluidintegrates-keystore \
  --output output/integrates.apk


# Cleanup
echo "All done! Cleaning up..."
npx expo logout && rm google-services.json keystore-dev.jks
