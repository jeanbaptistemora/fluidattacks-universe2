# shellcheck shell=bash

function main() {
  local name
  local signal="${1}"
  local pid="${2}"

  for child in $(pgrep -P "${pid}"); do
    main "${signal}" "${child}" \
      || return 1
  done \
    && name=$(ps h --pid "${pid}" -o comm) \
    && kill -s "${signal}" "${pid}" \
    && echo "[INFO] signal ${signal} sent to ${name} with pid ${pid}" \
    || return 1
}

main "${@}"
