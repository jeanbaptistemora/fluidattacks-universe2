# shellcheck shell=bash

function main {
  export CI_COMMIT_REF_NAME='__CI_COMMIT_REF_NAME__'
  export CI_COMMIT_SHA='__CI_COMMIT_SHA__'
  export CI_COMMIT_SHORT_SHA='__CI_COMMIT_SHORT_SHA__'
  export INTEGRATES_DEPLOYMENT_DATE='__INTEGRATES_DEPLOYMENT_DATE__'

  mkdir -p "${out}/output" \
    && copy "${envIntegratesFront}" front \
    && pushd front \
    && copy "${envSetupIntegratesFrontDevRuntime}" node_modules \
    && for bin in webpack webpack-cli; do
      copy "$(realpath "node_modules/.bin/${bin}")" "node_modules/.bin/${bin}2" \
        && mv "node_modules/.bin/${bin}"{2,}
    done \
    && tcm src/ --silent \
    && webpack-cli \
      --config webpack.prod.config.ts \
      --env CI_COMMIT_REF_NAME="${CI_COMMIT_REF_NAME}" \
      --env CI_COMMIT_SHA="${CI_COMMIT_SHA}" \
      --env CI_COMMIT_SHORT_SHA="${CI_COMMIT_SHORT_SHA}" \
      --env INTEGRATES_DEPLOYMENT_DATE="${INTEGRATES_DEPLOYMENT_DATE}" \
    && popd \
    && mkdir -p app/static/external/C3 \
    && copy "${envExternalC3}" app/static/external/C3 \
    && copy "${envIntegratesBackAppTemplates}" app/static \
    && mv app "${out}/output/app" \
    || return 1
}

main "${@}"
