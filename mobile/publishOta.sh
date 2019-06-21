# Prepare Expo
export EXPO_ANDROID_KEYSTORE_PASSWORD=$FI_EXPO_PASSWORD
export EXPO_ANDROID_KEY_PASSWORD=$FI_EXPO_PASSWORD
npx expo login -u "$FI_EXPO_USERNAME" -p "$FI_EXPO_PASSWORD"
echo "fs.inotify.max_user_watches=524288" >> /etc/sysctl.conf && sysctl -p
echo "$FI_GOOGLE_SERVICES_APP" > google-services.json
DEVELOPER_ENV=${CI_COMMIT_REF_NAME:-"local"}

# Publish
echo "Publishing update ..."
VAR_URL="https://gitlab.com/api/v4/projects/fluidattacks%2Fintegrates/variables/MOBILE_VERSION"
CURRENT=$(curl -s --header "PRIVATE-TOKEN:$FI_GITLAB_ENV_KEY" $VAR_URL | jq -r .value)
MINUTES=$(printf "%05d" $((
        ($(date +%d | sed 's/^0//') -1) * 1440 +
        $(date +%H | sed 's/^0//') * 60 +
        $(date +%M | sed 's/^0//')
      )))
FI_VERSION="$(date +%y.%m.)${MINUTES}"
FI_VERSION_CODE="$(date +%y%m)${CURRENT}"
if [ "$(date +%m)" -eq 07 ]; then FI_VERSION_CODE="$(date +%y%m)${MINUTES}"; fi;
sed -i 's/integrates_version/'"${FI_VERSION}"'/g' ./app.json
sed -i "s/"\"versionCode\":" 0/"\"versionCode\":" ${FI_VERSION_CODE}/g" ./app.json

npx expo publish \
  --release-channel "$DEVELOPER_ENV" \
  --non-interactive

if [ ${FI_ROLLBAR_ENVIRONMENT:-""} = "production" ]; then
  curl https://api.rollbar.com/api/1/deploy/ \
    -F access_token="$ROLLBAR_ACCESS_TOKEN" \
    -F environment="mobile-production" \
    -F revision="$CI_COMMIT_SHA" \
    -F local_username="$CI_COMMIT_REF_NAME"
fi;

# Cleanup
echo "Published to Expo! Cleaning up..."
npx expo logout && rm google-services.json
