# shellcheck shell=bash

function main {
      copy "${envSrcIntegratesFront}" "${PWD}" \
  &&  success
}

main "$@"
