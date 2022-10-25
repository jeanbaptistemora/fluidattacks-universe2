# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function check_output() {
  if ! grep -q "ERROR\|TypeError\|IndexError\|Traceback" "$1"; then
    echo "[INFO] All clear!"
    result_code=0
  else
    echo "[ERROR] Failed check"
    grep -q "ERROR\|TypeError\|IndexError\|Traceback" "$1"
    result_code=1
  fi
}

function main {
  local out="out"
  export BATCH_BIN

  : \
    && source __argIntegratesBackEnv__/template dev \
    && aws_login "dev" "3600" \
    && sops_export_vars __argIntegratesSecrets__/secrets/development.yaml \
      TEST_FORCES_TOKEN \
    && DAEMON=true integrates-storage \
    && DAEMON=true integrates-db \
    && echo "[INFO] Running DevSecOps agent check..." \
    && mkdir -p "${out}" \
    && forces --token "${TEST_FORCES_TOKEN}" --lax > "${out}/forces-output.log" || true \
    && check_output "${out}/forces-output.log" \
    && rm -rf "${out}" \
    && return "${result_code}" \
    || return 1
}

main "${@}"
