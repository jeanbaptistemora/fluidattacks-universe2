# shellcheck shell=bash

function main {
  local host='localhost'
  local port="${1}"

      __envKillPidListeningOnPort__ "${port}" \
  &&  echo "[INFO] Done at ${host}:${port}" \
  &&  __envNc__ -kl "${host}" "${port}"
}

main "${@}"
