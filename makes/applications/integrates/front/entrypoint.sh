# shellcheck shell=bash

source "__envSearchPaths__"

function main {
  export INTEGRATES_DEPLOYMENT_DATE

      INTEGRATES_DEPLOYMENT_DATE="$(date -u '+%FT%H:%M:%SZ')" \
  &&  pushd integrates/front \
    &&  copy "__envSetupIntegratesDevelopmentFront__/node_modules" node_modules \
    &&  copy "__envSetupIntegratesRuntimeFront__/node_modules" node_modules \
    &&  chmod 755 node_modules/.bin/ts-node \
      &&  npm start \
    &&  rm -rf node_modules \
  &&  popd \
  || return 1
}

main "${@}"
