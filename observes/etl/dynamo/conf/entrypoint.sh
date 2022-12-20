# shellcheck shell=bash

function execute {
  local selection="${1}"
  echo "[INFO] Executing job: ${selection}"
  observes-etl-dynamo-conf run "${selection}"
}

export_notifier_key \
  && execute "${@}"
