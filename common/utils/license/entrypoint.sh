# shellcheck shell=bash

function main {
  if ! reuse lint; then
    error "Some files are not properly licensed. Please adapt the licensing file under ./reuse/dep5"
  fi
}

main "${@}"
