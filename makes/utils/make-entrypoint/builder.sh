# shellcheck shell=bash

source "${makeDerivation}"

function main {
  local location="${out}${envLocation}"

      echo '[INFO] Copying files' \
  &&  mkdir -p "$(dirname "${location}")" \
  &&  copy "${envEntrypoint}" "${location}" \
  &&  make_executable "${location}"
}

main "${@}"
