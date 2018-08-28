#!/usr/bin/env bash

# Script to generate dynamic AWS credentials and update the project variables
# on a daily basis.
# It has the following requirements:
#   - Have an AWS policy which will set the keys permissions
#   - Define a role linked to the AWS policy in Vault's AWS secret engine
#   - The Vault token used must have permissions to read the AWS role
#     and to read and update credentials in the respective projects

function vault_generate_aws_keys() {
  local role="$1"
  local project="${role/-*/}"
  local aws_service=${role/*-/}
  local access_key_name="aws_${aws_service}_access_key"
  local access_key
  local secret_key_name="aws_${aws_service}_secret_key"
  local secret_key
  echo-green "Generating ${aws_service^} keys for ${project^}..."
  vault read -format=json "aws/creds/$role" > aws-keys.json
  access_key="$(cat aws-keys.json | jq -r '.data.access_key')"
  secret_key="$(cat aws-keys.json | jq -r '.data.secret_key')"
  rm aws-keys.json
  if [ "$project" = "integrates" ]; then
    echo-green "Updating ${aws_service^} variables in ${project^}..."
    vault_update_keys "$project/development" "$access_key_name" "$access_key" \
      "$secret_key_name" "$secret_key"
    vault_update_keys "$project/production" "$access_key_name" "$access_key" \
      "$secret_key_name" "$secret_key"
    if [ "$aws_service" = "dynamodb" ]; then
      echo-green "Updating ${aws_service^} variables in Continuous..."
      vault_update_keys "continuous/tools" "$access_key_name" "$access_key" \
        "$secret_key_name" "$secret_key"
    fi
  else
    echo-green "Updating ${aws_service^} variables in ${project^}..."
    vault_update_keys "$project" "$access_key_name" "$access_key" \
      "$secret_key_name" "$secret_key"
  fi
}

function vault_update_keys() {
  local secret_path="secret/${1}"
  shift 1
  vault read -format=json "${secret_path}" | jq '.data' > vars.json
  for args in "$@"; do
    var="$1"
    value="$2"
    shift 2
    cat vars.json | vault_update_value "${var}" "${value}" > vars_tmp.json
    mv vars_tmp.json vars.json
  done
  vault write "${secret_path}" @vars.json
  rm vars.json
}

function vault_update_value() {
  jq "to_entries |
        map(if .key == \"$1\"
          then . + {\"value\":\"$2\"}
          else .
          end
        ) |
      from_entries"
}

function echo-green() {
  local GC='\033[0;32m'
  local NC='\033[0m'
  echo -e "${GC}${1}${NC}"
}
