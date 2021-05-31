# shellcheck shell=bash

function main {
  export PYTHONPATH="${PWD}/melts:${PYTHONPATH:-}"
}

main
