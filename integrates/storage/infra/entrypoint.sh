# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function main {
  local action="${1:-}"
  local infra_path="integrates/storage/infra/src"
  local env
  local bin

  export TF_VAR_endpoint

  : \
    && if [ "${action}" = "deploy" ]; then
      bin="deploy-terraform-for-integratesStorage"
    elif [ "${action}" = "test" ]; then
      bin="test-terraform-for-integratesStorage"
    else
      error "You must either pass a 'deploy' or 'test' argument."
    fi \
    && env="$(get_abbrev_rev . HEAD)" \
    && info "Running on environment: ${env}" \
    && TF_VAR_endpoint="${env}" \
    && select_workspace "${infra_path}" "${env}" \
    && "${bin}"
}

main "${@}"
