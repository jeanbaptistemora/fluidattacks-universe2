# shellcheck shell=bash

function main {
  local raw_types=(
    "APPS"
    "GROUPS"
    "RULES"
    "USERS"
  )
  local parsed_types=(
    "APPS"
    "GROUPS"
    "RULES"
    "USERS"
    "APP_GROUPS"
    "APP_USERS"
    "AWS_GROUP_ROLES"
    "AWS_USER_ROLES"
  )

  export "OKTA_API_TOKEN=$(sops -d --output-type json --extract '["OKTA_API_TOKEN"]' __argSopsData__)" \
    &&
    # Export raw data
    for type in "${raw_types[@]}"; do
      export "OKTA_DATA_RAW_${type}=$(sops -d --output-type json --extract "[\"OKTA_DATA_RAW_${type}\"]" __argSopsData__)"
    done \
    &&
    # Export parsed data
    for type in "${parsed_types[@]}"; do
      export "OKTA_DATA_${type}=$(python __argParser__ "${type}")"
    done \
    &&
    # Unset parsed data
    for type in "${raw_types[@]}"; do
      unset "OKTA_DATA_RAW_${type}"
    done
}

main "${@}"
