# shellcheck shell=bash

source "__envSearchPaths__"

function main {
  export CI_COMMIT_REF_NAME
  export CI_COMMIT_SHA
  export CI_COMMIT_SHORT_SHA

      pushd integrates/front \
    &&  copy "__envSetupIntegratesDevelopmentFront__/node_modules" node_modules \
    &&  copy "__envSetupIntegratesRuntimeFront__/node_modules" node_modules \
    &&  chmod 755 -R node_modules \
      &&  < ../../build/patches/jquery-comments.diff \
            patch \
              -p1 \
              --binary \
            node_modules/jquery-comments_brainkit/js/jquery-comments.js \
      &&  npm run build -- \
            --env CI_COMMIT_REF_NAME="${CI_COMMIT_REF_NAME}" \
            --env CI_COMMIT_SHA="${CI_COMMIT_SHA}" \
            --env CI_COMMIT_SHORT_SHA="${CI_COMMIT_SHORT_SHA}" \
            --env INTEGRATES_DEPLOYMENT_DATE="$(date -u '+%FT%H:%M:%SZ')" \
   &&  rm -rf node_modules \
  &&  popd \
  || return 1
}

main "${@}"
