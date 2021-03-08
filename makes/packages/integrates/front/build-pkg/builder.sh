# shellcheck shell=bash

function main {
  export CI_COMMIT_REF_NAME='__CI_COMMIT_REF_NAME__'
  export CI_COMMIT_SHA='__CI_COMMIT_SHA__'
  export CI_COMMIT_SHORT_SHA='__CI_COMMIT_SHORT_SHA__'
  export INTEGRATES_DEPLOYMENT_DATE='__INTEGRATES_DEPLOYMENT_DATE__'

      mkdir -p "${out}/output" \
  &&  copy "${envIntegratesFront}" front \
  &&  pushd front \
    &&  copy "${envSetupIntegratesFrontDevRuntime}/node_modules" node_modules \
    &&  chmod 755 node_modules/.bin/tcm node_modules/.bin/webpack \
    &&  patch \
          -p1 \
          --binary \
          node_modules/jquery-comments_brainkit/js/jquery-comments.js \
          < "${envJqueryCommentsPatch}" \
    &&  npm run build -- \
          --env CI_COMMIT_REF_NAME="${CI_COMMIT_REF_NAME}" \
          --env CI_COMMIT_SHA="${CI_COMMIT_SHA}" \
          --env CI_COMMIT_SHORT_SHA="${CI_COMMIT_SHORT_SHA}" \
          --env INTEGRATES_DEPLOYMENT_DATE="${INTEGRATES_DEPLOYMENT_DATE}" \
  &&  popd \
  ||  return 1
}

main "${@}"
