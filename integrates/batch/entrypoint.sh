# shellcheck shell=bash

function main {
  local login_env
  local env="${1:-}"
  login_env=$(case "${env}" in
    test) echo "dev" ;;
    *) echo "${env}" ;;
  esac)

  source __argIntegratesBackEnv__/template "${login_env}" \
    && export NODE_OPTIONS='--max_old_space_size=4096' \
    && if test "${env}" == 'prod'; then
      ensure_gitlab_env_vars \
        CACHIX_AUTH_TOKEN \
        INTEGRATES_API_TOKEN \
        UNIVERSE_API_TOKEN
    elif test "${env}" == 'dev'; then
      DAEMON=true dynamodb-for-integrates \
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
