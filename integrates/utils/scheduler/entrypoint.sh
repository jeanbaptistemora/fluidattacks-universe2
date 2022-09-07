# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function main {
  local env="${1:-}"
  local module="${2:-}"

  echo "[INFO] Waking up: ${module}" \
    && source __argIntegratesBackEnv__/template "${env}" \
    && if test -z "${module:-}"; then
      echo '[ERROR] Second argument must be the module to execute' \
        && return 1
    fi \
    && pushd integrates \
    && python3 'back/src/cli/invoker.py' "${module}" \
    && popd \
    || return 1
}

main "${@}"
