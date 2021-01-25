# shellcheck shell=bash

function main {
      copy "${envSrcIntegratesFront}" "${out}" \
  &&  success
}

main "$@"
