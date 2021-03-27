# shellcheck shell=bash

function main {
  export PYTHONPATH="${PWD}/observes/singer/tap_mixpanel:${PYTHONPATH:-}"
}

main
