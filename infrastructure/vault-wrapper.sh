#!/usr/bin/env bash

# Script to generate dynamic AWS credentials and update the project variables
# on a daily basis.
# It has the following requirements:
#   - Have an AWS policy which will set the keys permissions
#   - Define a role linked to the AWS policy in Vault's AWS secret engine
#   - The Vault token used must have permissions to read the AWS role
#     and to read and update credentials in the respective projects

function vault_create_radius_user() {
  local email="$1"
  shift 1
  local policies
  policies=$(printf ', %s' "$@" | sed 's/,\ //')
  if [[ "$email" =~ (@fluidattacks.com|@autonomicmind.co) ]]; then
    vault write "auth/radius/users/$email" policies="$policies"
  else
    echo 'Email address does not belong neither to Fluid Attacks nor to Autonomicmind'
  fi
}

function vault_delete_radius_user() {
  local email="$1"
  vault delete "auth/radius/users/$email"
}

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
  access_key="$(jq -r '.data.access_key' aws-keys.json)"
  secret_key="$(jq -r '.data.secret_key' aws-keys.json)"
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
    shift 2 || break
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

if [[ "$*" =~ (-h|help|--help|usage) ]]; then
  cat <<HELP

  Script containing multiple functions to make the usage of Vault simpler.
  Import the functions by sourcing the script:

  source ./vault-wrapper.sh

  Functions:

  1. vault_generate_aws_keys: Dynamically generate AWS credentials with a TTL of 25h.

     usage:
       vault_generate_aws_keys role
    
     params:
       - role: Pre-defined role in Vault for which the credentials are going to be created. 
               IAM policies are already attached in the role definition.

     Find existing roles: vault list aws/roles

  2. vault_update_keys: Overwrite the value of existing variables.

     usage:
       vault_update_keys path var_name1 var_value1 var_name2 var_value2 ...

     params:
       - path: Path in Vault where the variables are going to be overwritten. The prefix "secret/" should not be included.
       - var_name: Name of the variable in Vault which is going to be modified.
       - var_value: New value which is going to be saved in Vault.

     Find variable names: vault read secret/path

  3. vault_create_radius_user: Create a new user who authenticates using OneLogin via RADIUS.

     usage:
       vault_create_radius_user user_email
       vault_create_radius_user user_email policy1 policy2 ...

     params:
       - user_email: Email address of the user which is going to be created. It must be the same one used in OneLogin.
       - policies (optional): Set of policies to attach to the newly created user. If none specified, the user will be created but will not have access to any resource.

  4. vault_delete_radius_user: Delete a user who authenticates using OneLogin via RADIUS.

     usage:
       vault_delete_radius_user user_email

     params:
       - user_email: Email address of the user which is going to be deleted
HELP
fi
