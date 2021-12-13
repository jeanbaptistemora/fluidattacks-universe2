# shellcheck shell=bash

function main {
  deploy prod_new production master
}

main "${@}"
