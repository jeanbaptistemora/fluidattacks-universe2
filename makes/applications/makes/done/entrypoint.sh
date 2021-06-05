# shellcheck shell=bash

function main {
  local host='localhost'
  local port="${1}"

  makes-kill-port "${port}" \
    && echo "[INFO] Done at ${host}:${port}" \
    && nc -kl "${host}" "${port}"
}

main "${@}"
