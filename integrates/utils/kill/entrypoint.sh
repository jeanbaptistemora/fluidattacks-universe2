# shellcheck shell=bash

function main {
  local ports=(
    3000 # front
    8001 # back
    8022 # dynamodb
    9200 # opensearch
  )

  kill_port "${ports[@]}"
}

main "${@}"
