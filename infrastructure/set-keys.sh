#!/usr/bin/env bash
set -e

function update-value() {
  jq "to_entries |
        map(if .key == \"$1\"
          then . + {\"value\":\"$2\"}
          else .
          end
        ) |
      from_entries"
}

function update-variables() {
  src_file="$1"
  secret_path="$2"
  shift 2
  vars=("$@")
  cp "$src_file" vars.json
  for var in "${vars[@]}"; do
    cat vars.json |
      update-value "$var" "${!var}" > tmp_vars.json 
    mv tmp_vars.json vars.json
  done
  if diff "$src_file" vars.json > /dev/null; then
    echo "Variables in '$secret_path' are updated!"
  else
    echo "Updating variables in '$secret_path'..."
    vault write 'secret/'"$secret_path" @vars.json
  fi
}

# Integrates Variables
aws_s3_access_key="$(terraform output fis3integrationID)"
aws_s3_secret_key="$(terraform output fis3integrationSECRET)"
aws_cloudwatch_access_key="$(terraform output cloudwatchID)"
aws_cloudwatch_secret_key="$(terraform output cloudwatchSECRET)"
aws_dynamodb_access_key="$(terraform output fluidintegratesdynamoID)"
aws_dynamodb_secret_key="$(terraform output fluidintegratesdynamoSECRET)"

VARS_INTEGRATES=("aws_s3_access_key"
  "aws_s3_secret_key"
  "aws_cloudwatch_access_key"
  "aws_cloudwatch_secret_key"
  "aws_dynamodb_access_key"
  "aws_dynamodb_secret_key")

vault read -format=json secret/integrates/development | \
  jq '.data' > integrates-development.json
vault read -format=json secret/integrates/production | \
  jq '.data' > integrates-production.json

update-variables integrates-development.json integrates/development \
  "${VARS_INTEGRATES[@]}"
update-variables integrates-production.json integrates/production \
  "${VARS_INTEGRATES[@]}" 

# Web variables
aws_access_key_id="$(terraform output fws3userID)"
aws_secret_access_key="$(terraform output fws3userSECRET)"

VARS_WEB=("aws_access_key_id" "aws_secret_access_key")

vault read -format=json secret/web | \
  jq '.data' > web.json

update-variables web.json web "${VARS_WEB[@]}"

# Cleanup
rm *.json
