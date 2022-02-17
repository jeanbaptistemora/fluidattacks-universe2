# shellcheck shell=bash

function main {
  export CI_COMMIT_REF_NAME
  export EXPO_APPLE_PASSWORD
  export EXPO_IOS_DIST_P12_PASSWORD
  local secrets=(
    APPLE_DIST_CERT_PASSWORD
    APPLE_ID
    APPLE_PASSWORD
    APPLE_PUSH_ID
    APPLE_TEAM_ID
    EXPO_USER
    EXPO_PASS
  )

  echo '[INFO] Logging in to AWS...' \
    && aws_login_prod integrates \
    && sops_export_vars __argSecretsProd__ "${secrets[@]}" \
    && EXPO_APPLE_PASSWORD="${APPLE_PASSWORD}" \
    && EXPO_IOS_DIST_P12_PASSWORD="${APPLE_DIST_CERT_PASSWORD}" \
    && pushd integrates/mobile \
    && echo '[INFO] Copying dependencies...' \
    && copy __argIntegratesMobileDevRuntime__ node_modules \
    && echo "[INFO] Using NodeJS $(node -v)" \
    && npx --no-install expo login \
      --username "${EXPO_USER}" \
      --password "${EXPO_PASS}" \
      --non-interactive \
    && aws s3 cp \
      --recursive \
      "s3://fluidintegrates.build/mobile/certs" \
      ./certs \
    && echo '[INFO] Building iOS app...' \
    && if test -z "${CI_COMMIT_REF_NAME:-}"; then
      CI_COMMIT_REF_NAME="$(get_abbrev_rev . HEAD)"
    fi \
    && npx --no-install expo-cli build:ios \
      --apple-id "${APPLE_ID}" \
      --dist-p12-path ./certs/apple_ios_distribution.p12 \
      --no-publish \
      --provisioning-profile-path ./certs/apple_prov_profile.mobileprovision \
      --push-id "${APPLE_PUSH_ID}" \
      --push-p8-path ./certs/apple_apns.p8 \
      --release-channel "${CI_COMMIT_REF_NAME}" \
      --team-id "${APPLE_TEAM_ID}" \
      --type archive \
      --non-interactive \
    && mkdir -p output \
    && curl -sSo output/integrates.ipa "$(npx expo-cli url:ipa)" \
    && rm -rf certs node_modules \
    && popd \
    || return 1
}

main "${@}"
