# shellcheck shell=bash

function main {
  local login_env
  local env="${1:-}"
  login_env=$(case "${env}" in
    test) echo "dev" ;;
    *) echo "${env}" ;;
  esac)

  source __argIntegratesBackEnv__/template "${login_env}" \
    && if test "${env}" == 'prod'; then
      DAEMON=true integrates-cache \
        && ensure_gitlab_env_vars \
          SERVICES_PROD_AWS_ACCESS_KEY_ID \
          SERVICES_PROD_AWS_SECRET_ACCESS_KEY
    elif test "${env}" == 'dev'; then
      DAEMON=true integrates-cache \
        && DAEMON=true integrates-db \
        && DAEMON=true integrates-storage
    fi \
    && pushd integrates \
    && python3 -m back.src.batch.dispatch "${@:2}" \
    && popd \
    && if test "${env}" == 'test'; then
      rm -rf integrates
    fi \
    || return 1
}

main "${@}"
