# shellcheck shell=bash

function compile {
  local env="${1}"
  export CI_COMMIT_SHA='__CI_COMMIT_SHA__'
  export CI_COMMIT_SHORT_SHA='__CI_COMMIT_SHORT_SHA__'
  export INTEGRATES_DEPLOYMENT_DATE='__INTEGRATES_DEPLOYMENT_DATE__'

      mkdir -p "${out}/output" \
  &&  copy "__envIntegratesFront__" front \
  &&  pushd front \
    &&  copy "__envSetupIntegratesFrontDevRuntime__/node_modules" node_modules \
    &&  patch \
          -p1 \
          --binary \
          node_modules/jquery-comments_brainkit/js/jquery-comments.js \
          < "__envJqueryCommentsPatch__" \
    &&  tcm src/ --silent \
    &&  webpack \
          --config "webpack.${env}.config.ts" \
          --env CI_COMMIT_SHA="${CI_COMMIT_SHA}" \
          --env CI_COMMIT_SHORT_SHA="${CI_COMMIT_SHORT_SHA}" \
          --env INTEGRATES_DEPLOYMENT_DATE="${INTEGRATES_DEPLOYMENT_DATE}" \
  &&  popd \
  &&  mkdir -p app/static/external/C3 \
  &&  copy "__envExternalC3__" app/static/external/C3 \
  &&  copy "__envIntegratesBackAppTemplates__" app/static \
  &&  mv app "${out}/output/app" \
  ||  return 1
}
