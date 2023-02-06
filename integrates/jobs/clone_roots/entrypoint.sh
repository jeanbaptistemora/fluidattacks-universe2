# shellcheck shell=bash

function main {
  : \
    && source __argPythonEnv__/template \
    && aws_login "prod_integrates" "3600" \
    && ensure_gitlab_env_vars \
      INTEGRATES_API_TOKEN \
    && python3 __argScript__ "${@}" \
    && rm -rf /tmp/* \
    && if test -n "${CI}"; then
      nix-store --gc
    fi
}

main "${@}"
