#!/usr/bin/env bash

get_asserts_subscriptions(){

  #Get active subscriptions from DynamoDB
  #Returns a variable with all subscription names

  set -e

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

  # Sets a terraform map variable with all the subscriptions found
  # As specified in:
  # https://www.terraform.io/docs/commands/environment-variables.html

  set -e

  local SUBSCRIPTIONS
  local COUNT
  export TF_VAR_asserts_projects

  SUBSCRIPTIONS=$(get_asserts_subscriptions)
  COUNT=0
  TF_VAR_asserts_projects='{ '

  #Prepare map syntax
  for SUB in $SUBSCRIPTIONS; do
    TF_VAR_asserts_projects="$TF_VAR_asserts_projects \"$COUNT\" = \"$SUB\", "
    COUNT=$(($COUNT + 1))
  done

  # Removes last comma (,) and adds closing bracket (}) to map
  TF_VAR_asserts_projects=$(echo $TF_VAR_asserts_projects | sed 's/\(.*\),/\1/')
  TF_VAR_asserts_projects="$TF_VAR_asserts_projects}"

  echo $TF_VAR_asserts_projects
}
