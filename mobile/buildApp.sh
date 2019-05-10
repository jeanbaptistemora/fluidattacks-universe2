#!/bin/bash
set -e

# Prepare AWS
AWS_ACCESS_KEY_ID="$(vault read -field=aws_innovation_s3_access_key secret/integrates/development)"
export AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY="$(vault read -field=aws_innovation_s3_secret_key secret/integrates/development)"
export AWS_SECRET_ACCESS_KEY
KEYSTORE_S3_URL="$(vault read -field=keystore_dev_s3_url secret/integrates/development)"
aws s3 cp "$KEYSTORE_S3_URL" keystore-dev.jks


# Prepare Expo
EXPO_USERNAME="$(vault read -field=expo_user secret/integrates/development)"
EXPO_PASSWORD="$(vault read -field=expo_pass secret/integrates/development)"
echo fs.inotify.max_user_watches=524288 >> /etc/sysctl.conf && sysctl -p
npx expo login -u "$EXPO_USERNAME" -p "$EXPO_PASSWORD"


# Build
echo "Building android .apk ..."
mkdir output/
echo "./keystore-dev.jks \
  $EXPO_PASSWORD \
  $EXPO_PASSWORD" \
  | npx expo build:android --no-publish | tee output_log.txt


# Download generated .apk
APK_URL=$"$(grep -Eo 'https:\/\/expo\.io\/artifacts\/[a-zA-Z0-9-]+' output_log.txt)"
wget -O output/integrates.apk $APK_URL


# Cleanup
echo "All done! Cleaning up..."
npx expo logout && rm keystore-dev.jks output_log.txt
