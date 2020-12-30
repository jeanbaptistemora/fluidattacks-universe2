# shellcheck shell=bash

source "${makeDerivation}"

function main {
  local location="${out}${envLocation}"

      echo '[INFO] Copying files' \
  &&  mkdir -p "$(dirname "${location}")" \
  &&  {
            cat "${envEntrypointSetup}" \
        &&  echo \
        &&  cat "${envEntrypoint}" \

      } > "${location}" \
  &&  make_executable "${location}"
}

main "${@}"
