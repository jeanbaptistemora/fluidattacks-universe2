# shellcheck shell=bash

function list_groups {
  local store="${1}"

  echo "[INFO] getting groups..." \
    asm-dal list-all-groups > "${store}"
}
