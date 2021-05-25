# shellcheck shell=bash

function main {
      source __envIntegratesBackEnv__ dev \
  &&  export PYTHONPATH="${PWD}/integrates:${PYTHONPATH:-}" \
  &&  export PYTHONPATH="${PWD}/integrates/back/packages/modules:${PYTHONPATH:-}"
}

main
