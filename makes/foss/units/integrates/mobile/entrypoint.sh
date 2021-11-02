# shellcheck shell=bash

function main {
  local secrets=(
    EXPO_PASS
    EXPO_USER
    GOOGLE_SERVICES_APP
  )

  if test -z "${CI:-}"; then
    export CI='false'
  fi

  aws_login_dev_new \
    && sops_export_vars __argSecretsDev__ "${secrets[@]}" \
    && pushd integrates/mobile \
    && copy __argSetupIntegratesMobileDevRuntime__ node_modules \
    && echo "${GOOGLE_SERVICES_APP}" > google-services.json \
    && npx --no-install expo login \
      --username "${EXPO_USER}" \
      --password "${EXPO_PASS}" \
      --non-interactive \
    && npm start -- --clear --non-interactive \
    && rm -rf .expo google-services.json node_modules \
    && popd \
    || return 1
}

main "${@}"
