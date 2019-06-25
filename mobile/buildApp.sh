#!/bin/bash
set -e

# Prepare AWS
export AWS_ACCESS_KEY_ID="$FI_AWS_INNOVATION_S3_ACCESS_KEY"
export AWS_SECRET_ACCESS_KEY="$FI_AWS_INNOVATION_S3_SECRET_KEY"
aws s3 cp "$FI_KEYSTORE_S3_URL" keystore-dev.jks


# Prepare Turtle
export EXPO_ANDROID_KEYSTORE_PASSWORD=$FI_EXPO_PASSWORD
export EXPO_ANDROID_KEY_PASSWORD=$FI_EXPO_PASSWORD
export LOGGER_LEVEL="info"
export JAVA_OPTS="-Xmx1500m -XX:+HeapDumpOnOutOfMemoryError -XX:+UnlockExperimentalVMOptions -XX:+UseCGroupMemoryLimitForHeap -XX:+UseG1GC"
export GRADLE_OPTS="-Dorg.gradle.parallel=true -Dorg.gradle.daemon=false -Dorg.gradle.jvmargs='$JAVA_OPTS'"
export GRADLE_DAEMON_DISABLED="1"
export DISABLE_DEX_MAX_HEAP="true"
DEVELOPER_ENV=${CI_COMMIT_REF_NAME:-"local"}


# Build
echo "Building android .apk ..."
rm -r output/ && mkdir output/
npx turtle build:android \
  --username "$FI_EXPO_USERNAME" \
  --password "$FI_EXPO_PASSWORD" \
  --release-channel "$DEVELOPER_ENV" \
  --keystore-path ./keystore-dev.jks \
  --keystore-alias fluidintegrates-keystore \
  --output output/integrates.apk \
  --type apk

CURRENT=$(curl -s --header "PRIVATE-TOKEN:$FI_GITLAB_ENV_KEY" $VAR_URL | jq -r .value)
curl -s --request PUT --header "PRIVATE-TOKEN:$FI_GITLAB_ENV_KEY" $VAR_URL --form "value=$((CURRENT + 1))" > /dev/null

# Cleanup
echo "Build done! Cleaning up..."
rm keystore-dev.jks
