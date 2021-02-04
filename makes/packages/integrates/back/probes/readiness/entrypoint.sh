# shellcheck shell=bash

source '__envProbes__'

function main {
  local user="${1}"
  local content="${2}"
  local endpoint_local="${3}"

      validate_aws_credentials_with_user "${user}" \
  &&  validate_response_content "${endpoint_local}" "${content}"
}

main "${@}"
