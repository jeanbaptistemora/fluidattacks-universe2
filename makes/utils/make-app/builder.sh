# shellcheck shell=bash

source "${makeSetup}"

function main {
      echo '[INFO] Copying files' \
  &&  copy "${envEntrypoint}" "${out}" \
  &&  make_executable "${out}"
}

main "${@}"
