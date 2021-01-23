# shellcheck shell=bash

function main {
      echo '[INFO] Building parser' \
  &&  copy "${envSrc}" . \
  &&  HOME=. npm install \
  &&  mv "${PWD}" "${out}" \
  ||  return 1
}

main "${@}"
