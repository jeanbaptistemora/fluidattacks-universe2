# shellcheck shell=bash

function main {
      mkdir "${out}" \
  &&  mkdir "${out}/tmp" \
  &&  copy "${envIntegrates}" "${out}/integrates"
}

main "${@}"
