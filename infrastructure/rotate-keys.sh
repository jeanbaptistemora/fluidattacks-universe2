#!/usr/bin/env bash

# Script to generate dynamic AWS credentials and update the project variables
# on a daily basis.
# It has the following requirements:
#   - Have an AWS policy which will set the keys permissions
#   - Define a role linked to the AWS policy in Vault's AWS secret engine
#   - The Vault token used must have permissions to read the AWS role
#     and to read and update credentials in the respective projects

function generate_keys() {
  local role="$1"
  local project="${role/-*/}"
  local aws_service=${role/*-/}
  local access_key
  local secret_key
  echo-green "Generating ${aws_service^} keys for ${project^}..."
  vault read -format=json "aws/creds/$role" > aws-keys.json
  access_key="$(cat aws-keys.json | jq -r '.data.access_key')"
  secret_key="$(cat aws-keys.json | jq -r '.data.secret_key')"
  rm aws-keys.json
  if [ "$project" = "integrates" ]; then
    update-keys "$project/development" "$aws_service" "$access_key" \
      "$secret_key"
    update-keys "$project/production" "$aws_service" "$access_key" \
      "$secret_key"
    if [ "$aws_service" = "dynamodb" ]; then
      update-keys "continuous/tools" "$aws_service" "$access_key" "$secret_key"
    fi
  else
    update-keys "$project" "$aws_service" "$access_key" "$secret_key"
  fi
}

function update-keys() {
  local project="$1"
  local access_key_name="aws_${2}_access_key"
  local secret_key_name="aws_${2}_secret_key"
  local access_key="$3"
  local secret_key="$4"
  vault read -format=json "secret/${project}" | jq '.data' > vars.json
  cat vars.json | \
    update-value "$access_key_name" "$access_key" | \
    update-value "$secret_key_name" "$secret_key" > vars_tmp.json
  mv vars_tmp.json vars.json
  vault write "secret/${project}" @vars.json && \
    echo-green "${2^} variables in \"${project}\" were updated successfully"
  rm vars.json
}

function update-value() {
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
