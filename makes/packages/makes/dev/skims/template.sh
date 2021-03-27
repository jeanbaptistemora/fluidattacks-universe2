# shellcheck shell=bash

function main {
  export PYTHONPATH="${PWD}/skims/skims:${PYTHONPATH:-}"
  export SKIMS_SHOULD_UPDATE_TESTS='1'
}

main
