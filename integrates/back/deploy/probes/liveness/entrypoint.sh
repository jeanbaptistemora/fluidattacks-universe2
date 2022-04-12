# shellcheck shell=bash

function main {
  local aws_login="${1}"
  local user="${2}"
  local content="${3}"
  local endpoint_local="${4}"
  local endpoint_remote="${5}"

  "${aws_login}" integrates \
    && validate_aws_credentials_with_user "${user}" \
    && validate_response_content "${endpoint_local}" "${content}" \
    && validate_response_content "${endpoint_remote}" "${content}"
}

main "${@}"
