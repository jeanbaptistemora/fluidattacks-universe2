#!/bin/bash
set -e

# Prepare AWS
AWS_ACCESS_KEY_ID="$FI_AWS_INNOVATION_S3_ACCESS_KEY"
export AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY="$FI_AWS_INNOVATION_S3_SECRET_KEY"
export AWS_SECRET_ACCESS_KEY
aws s3 cp "$FI_KEYSTORE_S3_URL" keystore-dev.jks


# Prepare Expo
echo fs.inotify.max_user_watches=524288 >> /etc/sysctl.conf && sysctl -p
npx expo login -u "$FI_EXPO_USERNAME" -p "$FI_EXPO_PASSWORD"


# Build
echo "Building android .apk ..."
mkdir output/
echo "./keystore-dev.jks \
  $FI_EXPO_PASSWORD \
  $FI_EXPO_PASSWORD" \
  | npx expo build:android --no-publish | tee output_log.txt


# Download generated .apk
APK_URL=$"$(grep -Eo 'https:\/\/expo\.io\/artifacts\/[a-zA-Z0-9-]+' output_log.txt)"
wget -O output/integrates.apk $APK_URL


# Cleanup
echo "All done! Cleaning up..."
npx expo logout && rm keystore-dev.jks output_log.txt
