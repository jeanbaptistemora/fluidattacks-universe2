# shellcheck shell=bash

function get_mobile_version {
  local minutes

  minutes=$(
    printf "%05d" $(((\
    $(date +%d | sed 's/^0//') - 1) * 1440 + \
    $(date +%H | sed 's/^0//') * 60 + \
    $(date +%M | sed 's/^0//')))
  ) \
    && if [ "$1" = "basic" ]; then
      echo "$(date +%y.%m.)${minutes}"
    elif [ "$1" = "code" ]; then
      echo "$(date +%y%m)${minutes}"
    else
      echo "Error. Only basic or code allowed as params" \
        && exit 1
    fi
}

function get_fluidattacks_pk {
  local domain="fluidattacks.com"

  echo "Q" \
    | openssl s_client -servername "${domain}" -connect "${domain}":443 \
    | openssl x509 -pubkey -noout \
    | openssl pkey -pubin -outform der \
    | openssl dgst -sha256 -binary \
    | openssl enc -base64
}

function main {
  export CI_COMMIT_AUTHOR
  export CI_COMMIT_REF_NAME
  export CI_COMMIT_SHA
  export CI_COMMIT_SHORT_SHA
  export INTEGRATES_DEPLOYMENT_DATE
  local app_version
  local env='development'
  local secrets=(
    EXPO_PASS
    EXPO_USER
    GOOGLE_SERVICES_APP
  )
  local version_code
  local pinned_pk

  true \
    && if [ -n "${CI}" ] && [ "${CI_COMMIT_REF_NAME}" == "master" ]; then
      env='production' \
        && aws_login_prod integrates \
        && sops_export_vars __envSecretsProd__ "${secrets[@]}"
    else
      aws_login_dev integrates \
        && sops_export_vars __envSecretsDev__ "${secrets[@]}"
    fi \
    && app_version="$(get_mobile_version basic)" \
    && version_code="$(get_mobile_version code)" \
    && INTEGRATES_DEPLOYMENT_DATE="$(date -u '+%FT%H:%M:%SZ')" \
    && pinned_pk="$(get_fluidattacks_pk)" \
    && pushd integrates/mobile \
    && echo '[INFO] Copying dependencies...' \
    && copy "__envSetupIntegratesMobileDevRuntime__" node_modules \
    && echo "${GOOGLE_SERVICES_APP}" > google-services.json \
    && npx --no-install expo login \
      --username "${EXPO_USER}" \
      --password "${EXPO_PASS}" \
      --non-interactive \
    && echo '[INFO] Replacing versions...' \
    && sed -i "s/__CI_COMMIT_SHA__/${CI_COMMIT_SHA}/g" ./app.json \
    && sed -i "s/__CI_COMMIT_SHORT_SHA__/${CI_COMMIT_SHORT_SHA}/g" ./app.json \
    && sed -i "s/__INTEGRATES_DEPLOYMENT_DATE__/${INTEGRATES_DEPLOYMENT_DATE}/g" ./app.json \
    && sed -i "s/__APP_VERSION__/${app_version}/g" ./app.json \
    && sed -i "s/\"versionCode\": 0/\"versionCode\": ${version_code}/g" ./app.json \
    && sed -i "s|__PINNED_PK__|${pinned_pk}|g" ./src/utils/apollo.ts \
    && echo '[INFO] Publishing update' \
    && npx --no-install expo publish \
      --non-interactive \
      --release-channel "${CI_COMMIT_REF_NAME}" \
    && echo '[INFO] Sending build info to bugsnag' \
    && makes-announce-bugsnag c7b947a293ced0235cdd8edc8c09dad4 "mobile-${env}" \
    && rm -rf .expo google-services.json node_modules \
    && popd \
    || return 1
}

main "${@}"
