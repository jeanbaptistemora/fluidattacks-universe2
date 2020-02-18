#!/usr/bin/env bash

publish_ota() {

  # Publishes an OTA update for mobile app

  set -e

  # Import functions
  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/sops.sh)
  . ci-scripts/helpers/others.sh
  . ci-scripts/helpers/sops.sh

  local ENV_NAME

  if [ "$CI_COMMIT_REF_NAME" == 'master' ]; then
    ENV_NAME='production'
  else
    ENV_NAME='development'
  fi

  aws_login "$ENV_NAME"
  sops_env "secrets-$ENV_NAME.yaml" default \
  EXPO_USER \
  EXPO_PASS \
  ROLLBAR_ACCESS_TOKEN

  sops \
    --aws-profile default \
    --decrypt \
    --extract "[\"GOOGLE_SERVICES_APP\"]" \
    --output mobile/google-services.json \
    --output-type json \
    "secrets-$ENV_NAME.yaml"

  cd mobile || return 1

  # Prepare Expo
  npx expo login -u "$EXPO_USER" -p "$EXPO_PASS"
  DEVELOPER_ENV=${CI_COMMIT_REF_NAME:-"local"}

  # Publish
  echo "Publishing update ..."
  FI_VERSION=$(mobile_get_version basic)
  FI_VERSION_CODE=$(mobile_get_version code)
  sed -i "s/integrates_version/$FI_VERSION/g" ./app.json
  sed -i "s/\"versionCode\": 0/\"versionCode\": $FI_VERSION_CODE/g" ./app.json

  npx expo publish \
    --release-channel "$DEVELOPER_ENV" \
    --non-interactive

  if [ "$ENV_NAME" = 'production' ]; then
    curl https://api.rollbar.com/api/1/deploy/ \
      -F access_token="$ROLLBAR_ACCESS_TOKEN" \
      -F environment='mobile-production' \
      -F revision="$CI_COMMIT_SHA" \
      -F local_username="$CI_COMMIT_REF_NAME"
  fi

  # Cleanup
  echo "Published to Expo, cleaning up..."
  npx expo logout
  rm google-services.json

  cd .. || return 1

}

deploy_mobile() {

  # This runs a deploy if mobile/ folder was modified

  set -e

  # import functions
  . ci-scripts/helpers/check-changed.sh

  local FOLDERS
  local FILES

  FOLDERS=(
    'mobile/'
  )
  FILES=(
    'ci-scripts/jobs/deploy-mobile.sh'
  )

  # Increase max_user_watches as deployment requires it
  echo 'fs.inotify.max_user_watches=524288' >> /etc/sysctl.conf && sysctl -p

  if check_folder_changed "${FOLDERS[@]}" \
    || check_file_changed "${FILES[@]}"; then
      mv /usr/src/app/node_modules mobile/
      publish_ota
  else
    echo 'No relevant files for mobile build were modified. Skipping build.'
  fi
}

deploy_mobile
