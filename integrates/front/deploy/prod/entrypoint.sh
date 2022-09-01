# shellcheck shell=bash

function main {
  deploy prod_integrates production trunk
}

main "${@}"
