# shellcheck shell=bash

function main {
  echo "${envBuilt}" > "${out}"
}

main "${@}"
