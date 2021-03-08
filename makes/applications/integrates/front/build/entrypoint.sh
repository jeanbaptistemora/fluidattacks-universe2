# shellcheck shell=bash

function main {
  export CI_COMMIT_REF_NAME
  export CI_COMMIT_SHA
  export CI_COMMIT_SHORT_SHA
  export INTEGRATES_DEPLOYMENT_DATE

      INTEGRATES_DEPLOYMENT_DATE="$(date -u '+%FT%H:%M:%SZ')" \
  &&  pushd integrates/front \
    &&  copy "__envSetupIntegratesFrontDevRuntime__/node_modules" node_modules \
      &&  < ../../build/patches/jquery-comments.diff \
            patch \
              -p1 \
              --binary \
            node_modules/jquery-comments_brainkit/js/jquery-comments.js \
      &&  npm run build -- \
            --env CI_COMMIT_REF_NAME="${CI_COMMIT_REF_NAME}" \
            --env CI_COMMIT_SHA="${CI_COMMIT_SHA}" \
            --env CI_COMMIT_SHORT_SHA="${CI_COMMIT_SHORT_SHA}" \
            --env INTEGRATES_DEPLOYMENT_DATE="${INTEGRATES_DEPLOYMENT_DATE}" \
   &&  rm -rf node_modules \
  &&  popd \
  || return 1
}

main "${@}"
