#!/bin/bash
set -e

# Prepare AWS
export AWS_ACCESS_KEY_ID="$FI_AWS_INNOVATION_S3_ACCESS_KEY"
export AWS_SECRET_ACCESS_KEY="$FI_AWS_INNOVATION_S3_SECRET_KEY"


# Prepare Turtle
npx expo login -u "$FI_EXPO_USERNAME" -p "$FI_EXPO_PASSWORD"
echo "$FI_GOOGLE_SERVICES_APP" > google-services.json
DEVELOPER_ENV=${CI_COMMIT_REF_NAME:-"local"}
export LOGGER_LEVEL="info"


# Build
rm -r output/ && mkdir output/

echo "Building android .apk ..."
export EXPO_ANDROID_KEYSTORE_PASSWORD=$FI_EXPO_PASSWORD
export EXPO_ANDROID_KEY_PASSWORD=$FI_EXPO_PASSWORD
export JAVA_OPTS="-Xmx1500m -XX:+HeapDumpOnOutOfMemoryError -XX:+UnlockExperimentalVMOptions -XX:+UseCGroupMemoryLimitForHeap -XX:+UseG1GC"
export GRADLE_OPTS="-Dorg.gradle.parallel=true -Dorg.gradle.daemon=false -Dorg.gradle.jvmargs='$JAVA_OPTS'"
export GRADLE_DAEMON_DISABLED="1"
export DISABLE_DEX_MAX_HEAP="true"
aws s3 cp "$FI_KEYSTORE_S3_URL" keystore-dev.jks

npx turtle build:android \
  --username "$FI_EXPO_USERNAME" \
  --password "$FI_EXPO_PASSWORD" \
  --release-channel "$DEVELOPER_ENV" \
  --keystore-path ./keystore-dev.jks \
  --keystore-alias fluidintegrates-keystore \
  --output output/integrates.apk \
  --type apk

echo "Building iOS .ipa ..."
export EXPO_APPLE_PASSWORD="$FI_APPLE_PASSWORD"
export EXPO_IOS_DIST_P12_PASSWORD="$FI_APPLE_DIST_CERT_PASSWORD"
aws s3 cp "$FI_APPLE_DIST_CERT_URL" ios_dist_cert.p12
aws s3 cp "$FI_APPLE_APNS_CERT_URL" apns_cert.p8
aws s3 cp "$FI_APPLE_PROV_PROFILE_URL" prov_profile.mobileprovision

npx expo build:ios \
  --team-id "$FI_APPLE_TEAM_ID" \
  --apple-id "$FI_APPLE_ID" \
  --release-channel "$DEVELOPER_ENV" \
  --dist-p12-path ./ios_dist_cert.p12 \
  --push-p8-path ./apns_cert.p8 \
  --provisioning-profile-path ./prov_profile.mobileprovision \
  --push-id "$FI_APPLE_PUSH_ID" \
  --output output/integrates.ipa

wget -O output/integrates.ipa "$(npx expo url:ipa)"

# Cleanup
echo "Build done, cleaning up..."
npx expo logout
rm keystore-dev.jks ios_dist_cert.p12 apns_cert.p8 prov_profile.mobileprovision google-services.json
