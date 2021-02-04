# shellcheck shell=bash

function validate_aws_credentials_with_user {
  local user="${1}"

  if __envAws__ sts get-caller-identity | __envGrep__ --quiet "${user}"
  then
    echo '[INFO] validate_aws_credentials_with_user'
  else
        echo '[ERROR] validate_aws_credentials_with_user' \
    &&  return 1
  fi
}

function validate_response_content {
  local url="${1}"
  local content="${2}"

  if __envCurl__ -sSiLk "${url}" | __envGrep__ -q "${content}"
  then
    echo '[INFO] validate_response_content'
  else
        echo '[ERROR] validate_response_content' \
    &&  return 1
  fi
}
