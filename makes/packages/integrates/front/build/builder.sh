# shellcheck shell=bash

function main {
  export CI_COMMIT_SHA='__CI_COMMIT_SHA__'
  export CI_COMMIT_SHORT_SHA='__CI_COMMIT_SHORT_SHA__'
  export INTEGRATES_DEPLOYMENT_DATE='__INTEGRATES_DEPLOYMENT_DATE__'

      mkdir -p "${out}/output" \
  &&  copy "${envIntegratesFront}" front \
  &&  pushd front \
    &&  copy "${envSetupIntegratesFrontDevRuntime}/node_modules" node_modules \
    &&  patch \
          -p1 \
          --binary \
          node_modules/jquery-comments_brainkit/js/jquery-comments.js \
          < "${envJqueryCommentsPatch}" \
    &&  tcm src/ --silent \
    &&  webpack \
          --config webpack.prod.config.ts \
          --env CI_COMMIT_SHA="${CI_COMMIT_SHA}" \
          --env CI_COMMIT_SHORT_SHA="${CI_COMMIT_SHORT_SHA}" \
          --env INTEGRATES_DEPLOYMENT_DATE="${INTEGRATES_DEPLOYMENT_DATE}" \
  &&  popd \
  &&  mkdir -p app/static/external/C3 \
  &&  copy "${envExternalC3}" app/static/external/C3 \
  &&  copy "${envIntegratesBackAppTemplates}" app/static \
  &&  mv app "${out}/output/app" \
  ||  return 1
}

main "${@}"
