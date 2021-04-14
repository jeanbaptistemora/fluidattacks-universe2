# shellcheck shell=bash

function main {
  export PYTHONPATH="${PWD}/forces:${PYTHONPATH:-}"
}

main
