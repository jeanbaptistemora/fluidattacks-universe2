# shellcheck shell=bash

function main {
  local env="${1:-}"
  local module="${2:-}"

  shopt -s nullglob \
    && if test -z "${module:-}"; then
      echo '[ERROR] Second argument must be the module to execute' \
        && return 1
    fi \
    && case "${env}" in
      dev) aws_login_dev \
        && sops_export_vars __argSecretsDev__ "DYNAMODB_HOST" "DYNAMODB_PORT" "ENVIRONMENT" ;;
      prod) aws_login_prod 'skims' \
        && sops_export_vars __argSecretsProd__ "DYNAMODB_HOST" "DYNAMODB_PORT" "ENVIRONMENT" ;;
      *) error 'First argument must be one of: dev, prod' ;;
    esac \
    && pushd skims \
    && python3 'skims/schedulers/invoker.py' "${module}" \
    && popd \
    || return 1
}

main "${@}"
