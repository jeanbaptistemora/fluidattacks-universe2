# shellcheck shell=bash

function clean_file_system {
  local group="${1}"
  local paths=(
    ~/.skims
    "groups/${group}/fusion"
  )

  rm -rf "${paths[@]}" || true
}

function main {
  export -f clean_file_system

  local env="${1:-}"

  shopt -s nullglob \
    && ensure_gitlab_env_vars \
      INTEGRATES_API_TOKEN \
      PROD_SERVICES_AWS_ACCESS_KEY_ID \
      PROD_SERVICES_AWS_SECRET_ACCESS_KEY \
    && use_git_repo_services \
    && aws_login_prod 'skims' \
    && python3 -m batch.__init__ "${@:2}" \
    && popd \
    && if test "${env}" != 'test'; then
      clean_file_system "${group}"
    fi
}

main "${@}"
