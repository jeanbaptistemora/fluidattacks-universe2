#! __envShell__
# shellcheck shell=bash

source "__makeEntrypoint__"

function main {
  __envDocker__ build --help
}

main "${@}"
