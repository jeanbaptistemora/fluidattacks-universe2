#!/usr/bin/env bash

get_active_subscriptions(){

  #Get active subscriptions from DynamoDB
  #Returns a variable with all subscription names

  set -Eeuo pipefail

  local SCAN_JSON
  local SUBSCRIPTIONS

  SCAN_JSON=$(aws dynamodb scan \
    --table-name 'FI_projects' \
    --filter-expression 'project_status = :active' \
    --expression-attribute-values '{":active": {"S":"ACTIVE"}}' \
    --projection-expression 'project_name')

  SUBSCRIPTIONS=$(echo $SCAN_JSON | jq -r '.Items | .[].project_name.S')

  echo $SUBSCRIPTIONS
}

set_subscriptions_terraform_variable(){

  # Set a terraform map variable with all the subscriptions found
  # As specified in:
  # https://www.terraform.io/docs/commands/environment-variables.html

  set -Eeuo pipefail

  local SUBSCRIPTIONS
  local COUNT
  export TF_VAR_break_build_projects

  SUBSCRIPTIONS=$(get_asserts_subscriptions)

  # Prepare list
  TF_VAR_break_build_projects='['
  for SUB in $SUBSCRIPTIONS; do
    TF_VAR_break_build_projects="$TF_VAR_break_build_projects\"$SUB\","
  done
  TF_VAR_break_build_projects="$TF_VAR_break_build_projects]"

  echo $TF_VAR_break_build_projects
}
