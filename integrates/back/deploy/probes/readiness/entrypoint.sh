# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function main {
  local user="${1}"
  local content="${2}"
  local endpoint_local="${3}"

  : \
    && aws_login "${user}" "3600" \
    && validate_aws_credentials_with_user "${user}" \
    && validate_response_content "${endpoint_local}" "${content}"
}

main "${@}"
