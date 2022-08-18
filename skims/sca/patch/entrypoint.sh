# shellcheck shell=bash

function main {
  local env="${1:-}"
  local action="${2:-}"
  local path="${3:-}"

  shopt -s nullglob \
    && case "${env}" in
      dev) aws_login_dev \
        && sops_export_vars __argSecretsDev__ "DYNAMODB_HOST" "DYNAMODB_PORT" "ENVIRONMENT" ;;
      prod) aws_login_prod 'skims' \
        && sops_export_vars __argSecretsProd__ "DYNAMODB_HOST" "DYNAMODB_PORT" "ENVIRONMENT" ;;
      *) error 'First argument must be one of: dev, prod' ;;
    esac \
    && pushd skims \
    && python3 'skims/sca_patch/__init__.py' "${action}" "${path}" \
    && popd \
    || return 1
}

main "${@}"
