#!/bin/bash
set -e

# Prepare AWS
export AWS_ACCESS_KEY_ID="$FI_AWS_INNOVATION_S3_ACCESS_KEY"
export AWS_SECRET_ACCESS_KEY="$FI_AWS_INNOVATION_S3_SECRET_KEY"
aws s3 cp "$FI_KEYSTORE_S3_URL" keystore-dev.jks
aws s3 cp "$FI_APPLE_DIST_CERT_URL" ios_dist_cert.p12
aws s3 cp "$FI_APPLE_APS_CERT_URL" aps_cert.p12
aws s3 cp "$FI_APPLE_PROV_PROFILE_URL" prov_profile.mobileprovision


# Prepare Turtle
export EXPO_ANDROID_KEYSTORE_PASSWORD=$FI_EXPO_PASSWORD
export EXPO_ANDROID_KEY_PASSWORD=$FI_EXPO_PASSWORD
export EXPO_APPLE_PASSWORD="$FI_APPLE_PASSWORD"
export EXPO_IOS_DIST_P12_PASSWORD="$FI_APPLE_DIST_CERT_PASSWORD"

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

echo "Building iOS .ipa ..."
npx expo build:ios \
  --team-id "$FI_APPLE_TEAM_ID" \
  --apple-id "$FI_APPLE_ID" \
  --release-channel "$DEVELOPER_ENV" \
  --dist-p12-path ./ios_dist_cert.p12 \
  --push-p8-path ./aps_cert.p12 \
  --provisioning-profile-path ./prov_profile.mobileprovision \
  --push-id "$FI_APPLE_PUSH_ID" \
  --output output/integrates.ipa

wget -O output/integrates.ipa "$(npx expo url:ipa)"


CURRENT=$(curl -s --header "PRIVATE-TOKEN:$FI_GITLAB_ENV_KEY" $VAR_URL | jq -r .value)
curl -s --request PUT --header "PRIVATE-TOKEN:$FI_GITLAB_ENV_KEY" $VAR_URL --form "value=$((CURRENT + 1))" > /dev/null

# Cleanup
echo "Build done! Cleaning up..."
rm keystore-dev.jks ios_dist_cert.p12 aps_cert.p12 prov_profile.mobileprovision
