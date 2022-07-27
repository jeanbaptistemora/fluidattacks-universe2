# shellcheck shell=bash

function main {
  local env="${1:-}"
  local user="${2}"
  local content="${3}"
  local endpoint_local="${4}"

  case "${env}" in
    dev) aws_login_dev ;;
    eph) : ;;
    prod) : ;;
    prod-local) aws_login_prod 'integrates' ;;
    *) error 'First argument must be one of: dev, eph, prod, prod-local' ;;
  esac \
    && validate_aws_credentials_with_user "${user}" \
    && validate_response_content "${endpoint_local}" "${content}"
}

main "${@}"
