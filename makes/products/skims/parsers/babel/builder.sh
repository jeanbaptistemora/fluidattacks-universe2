# shellcheck shell=bash

function main {
      echo '[INFO] Building parser' \
  &&  mkdir "${out}" \
  &&  copy "${envNodeRequirements}/node_modules" "${out}/node_modules" \
  &&  copy "${envParseJs}" "${out}/parse.js" \
  ||  return 1
}

main "${@}"
