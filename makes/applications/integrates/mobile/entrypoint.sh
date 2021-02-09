# shellcheck shell=bash

source '__envSearchPaths__'
source '__envUtilsAws__'
source '__envUtilsCommon__'
source '__envUtilsSops__'

function main {
  local secrets=(
    EXPO_PASS
    EXPO_USER
    GOOGLE_SERVICES_APP
  )

      aws_login_dev 'integrates' \
  &&  sops_export_vars __envSecretsDev__ "${secrets[@]}" \
  &&  pushd integrates/mobile \
    &&  copy __envSetupIntegratesMobileDevRuntime__/node_modules node_modules \
    &&  chmod 755 node_modules/.bin/expo node_modules/.bin/expo-cli \
      &&  echo "${GOOGLE_SERVICES_APP}" > google-services.json \
      &&  npx --no-install expo login \
          --username "${EXPO_USER}" \
          --password "${EXPO_PASS}" \
          --non-interactive \
      &&  npm start -- --clear --non-interactive \
    &&  rm -rf .expo google-services.json node_modules \
  &&  popd \
  ||  return 1
}

main "${@}"
