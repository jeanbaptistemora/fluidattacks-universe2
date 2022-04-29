# shellcheck shell=bash

function main {
  local raw_types=(
    "apps"
    "groups"
    "rules"
    "users"
  )
  local parsed_types=(
    "apps"
    "groups"
    "rules"
    "users"
    "app_groups"
    "app_users"
    "aws_group_roles"
    "aws_user_roles"
  )

  export "OKTA_API_TOKEN=$(sops -d --output-type json --extract '["OKTA_API_TOKEN"]' __argSopsData__)" \
    &&
    # Export raw data
    for type in "${raw_types[@]}"; do
      export "OKTA_DATA_RAW_${type^^}=$(sops -d --output-type json --extract "[\"OKTA_DATA_RAW\"][\"${type}\"]" __argSopsData__)"
    done \
    &&
    # Export parsed data
    for type in "${parsed_types[@]}"; do
      export "OKTA_DATA_${type^^}=$(python __argParser__ "${type}")"
    done \
    &&
    # Unset parsed data
    for type in "${raw_types[@]}"; do
      unset "OKTA_DATA_RAW_${type^^}"
    done
}

main "${@}"
