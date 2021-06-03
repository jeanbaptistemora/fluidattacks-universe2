# shellcheck shell=bash

function main {
  local login_env
  local env="${1:-}"
  login_env=$(case "${env}" in
    test) echo "dev";;
    *) echo "${env}";;
  esac)

      source __envIntegratesEnv__ "${login_env}" \
  &&  if test "${env}" == 'prod'
      then
        DAEMON=true integrates-cache
      elif test "${env}" == 'dev'
      then
            DAEMON=true integrates-cache \
        &&  DAEMON=true integrates-db \
        &&  DAEMON=true integrates-storage
      fi \
  &&  pushd integrates \
    &&  python3 -m back.src.batch.dispatch "${@:2}" \
  &&  popd \
  ||  return 1
}

main "${@}"
