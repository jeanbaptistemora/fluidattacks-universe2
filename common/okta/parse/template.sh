# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function export_raw_var {
  local var="${1}"

  export "${var}=$(sops --decrypt --output-type json __argSopsData__ | jq -rc ".${var}")"
}

function export_parsed_var {
  local type="${1}"

  export "OKTA_DATA_${type}=$(python __argParser__ "${type}")"
}

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

  export_raw_var "OKTA_API_TOKEN" \
    &&
    # Export raw data
    for type in "${raw_types[@]}"; do
      export_raw_var "OKTA_DATA_RAW_${type}"
    done \
    &&
    # Export parsed data
    for type in "${parsed_types[@]}"; do
      export_parsed_var "${type}"
    done \
    &&
    # Unset parsed data
    for type in "${raw_types[@]}"; do
      unset "OKTA_DATA_RAW_${type}"
    done
}

main "${@}"
