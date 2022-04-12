# shellcheck shell=bash

function main {
  local ports=(
    3000           # front
    6379 6380 6381 # redis
    8001           # back
    8022           # dynamodb
    8080           # back
    8081           # back
    9000           # storage
  )

  kill_port "${ports[@]}"
}

main "${@}"
