# shellcheck shell=bash

function main {
  local ports=(
    3000  # front
    6379 6380 6381  # redis
    8022  # dynamodb
    8080  # back1
    8081  # back2
  )

  '__envKillPidListeningOnPort__' "${ports[@]}"
}

main "${@}"
