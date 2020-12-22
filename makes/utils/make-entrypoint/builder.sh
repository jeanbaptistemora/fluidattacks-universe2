# shellcheck shell=bash

source "${makeDerivation}"

function main {
      echo '[INFO] Copying files' \
  &&  copy "${envEntrypoint}" "${out}" \
  &&  make_executable "${out}"
}

main "${@}"
