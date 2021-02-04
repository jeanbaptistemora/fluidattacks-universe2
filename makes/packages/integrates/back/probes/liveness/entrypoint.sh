# shellcheck shell=bash

source '__envProbes__'

function main {
  local user="${1}"
  local content="${2}"
  local endpoint_local="${3}"
  local endpoint_remote="${4}"

      validate_aws_credentials_with_user "${user}" \
  &&  validate_response_content "${endpoint_local}" "${content}" \
  &&  validate_response_content "${endpoint_remote}" "${content}"
}

main "${@}"
