# shellcheck shell=bash

function main {
  export PYTHONPATH="${PWD}/skims/skims:${PYTHONPATH:-}"
}

main
