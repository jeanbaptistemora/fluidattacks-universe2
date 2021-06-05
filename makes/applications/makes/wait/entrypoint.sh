# shellcheck shell=bash

function wait_for_tcp {
  local elapsed='1'
  local timeout="${1}"
  local host="${2%:*}"
  local port="${2#*:}"

  while true; do
    if timeout 1s nc -z "${host}" "${port}"; then
      return 0
    elif test "${elapsed}" -gt "${timeout}"; then
      echo "[ERROR] Timeout while waiting for ${host}:${port} to open" \
        && return 1
    else
      echo "[INFO] Waiting 1 second for ${host}:${port} to open, ${elapsed} seconds in total" \
        && sleep 1 \
        && elapsed="$(("${elapsed}" + 1))" \
        && continue
    fi
  done
}

function main {
  local pids=()
  local timeout="${1}"

  for address in "${@:2}"; do
    { wait_for_tcp "${timeout}" "${address}" & } \
      && pids+=("${!}")
  done \
    && for pid in "${pids[@]}"; do
      wait "${pid}" \
        || return 1
    done
}

main "${@}"
