# shellcheck shell=bash

function check_output() {
  if ! grep -q "ERROR\|TypeError\|IndexError" "$1"; then
    echo "[INFO] All clear!"
    result_code=0
  else
    echo "[ERROR] Failed check"
    grep -q "ERROR\|TypeError\|IndexError" "$1"
    result_code=1
  fi
}

function main {
  local out="out"
  export BATCH_BIN

  source __argIntegratesBackEnv__/template dev \
    && aws_login_dev \
    && sops_export_vars __argIntegratesSecrets__/secrets-development.yaml \
      TEST_FORCES_TOKEN \
    && DAEMON=true integrates-cache \
    && DAEMON=true integrates-storage \
    && DAEMON=true dynamodb-for-integrates \
    && echo "[INFO] Running DevSecOps agent check..." \
    && mkdir -p "${out}" \
    && forces --token "${TEST_FORCES_TOKEN}" > "${out}/forces-output.log" || true \
    && check_output "${out}/forces-output.log" \
    && rm -rf "${out}" \
    && return "${result_code}" \
    || return 1
}

main "${@}"
