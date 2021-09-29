# shellcheck shell=bash

function validate_aws_credentials_with_user {
  local user="${1}"

  if aws sts get-caller-identity | grep --quiet "${user}"; then
    info validate_aws_credentials_with_user
  else
    error validate_aws_credentials_with_user
  fi
}

function validate_response_content {
  local url="${1}"
  local content="${2}"

  if curl -sSiLk "${url}" | grep -q "${content}"; then
    info validate_response_content
  else
    error validate_response_content
  fi
}
