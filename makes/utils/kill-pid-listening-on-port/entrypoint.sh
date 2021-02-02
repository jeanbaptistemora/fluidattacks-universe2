# shellcheck shell=bash

function kill_one {
  local pids
  local port="${1}"

      pids="$(mktemp)" \
  &&  if ! __envLsof__ -t "-i:${port}" > "${pids}"
      then
            echo "[INFO] Nothing listening on port: ${port}" \
        &&  return 0
      fi \
  &&  while read -r pid
      do
        if kill -9 "${pid}"
        then
          echo "[INFO] Killed pid: ${pid}, listening on port: ${port}"
        else
          echo "[ERROR] Killing pid: ${pid}, listening on port: ${port}"
        fi
      done < "${pids}"
}

function main {
  for port in "${@}"
  do
        kill_one "${port}" \
    ||  return 1
  done
}

main "${@}"
