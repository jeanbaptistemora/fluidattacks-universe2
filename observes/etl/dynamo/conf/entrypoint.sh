# shellcheck shell=bash

function execute {
  local selection="${1}"
  echo "[INFO] Executing job: ${selection}"
  dynamo-etl run "${selection}"
}

export_notifier_key \
  && execute "${@}"
