# shellcheck shell=bash

source "${makeSetup}"

function main {
      echo '[INFO] Copying files' \
  &&  copy "${envSrcEntry}" './entrypoint.sh' \
  &&  copy "${envSrcSkimsSkims}" './skims' \
  &&  copy "${envSrcSkimsStatic}" './static' \
  &&  copy "${envSrcSkimsVendor}" './vendor' \
  &&  make_executable './entrypoint.sh' \
  &&  mv "${PWD}" "${out}"
}

main "${@}"
