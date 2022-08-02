# shellcheck shell=bash

function main {
  local module="${1:-}"

  echo "[INFO] Executing ${module} consumer" \
    && pushd integrates/streams/src \
    && python3 "invoker.py" "${module}" \
    && popd \
    || return 1
}

main "${@}"
