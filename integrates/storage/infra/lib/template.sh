# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function _env_exists {
  local env="${1}"

  if terraform workspace list | grep -q "${env}"; then
    return 0
  else
    return 1
  fi
}

function select_workspace {
  local infra_path="${1}"
  local env="${2}"

  : \
    && pushd "${infra_path}" \
    && terraform init \
    && if _env_exists "${env}"; then
      info "Selecting already-existing namespace: ${env}" \
        && terraform workspace select "${env}"
    else
      info "Creating new namespace: ${env}" \
        && terraform workspace new "${env}"
    fi \
    && popd \
    || return 1
}
