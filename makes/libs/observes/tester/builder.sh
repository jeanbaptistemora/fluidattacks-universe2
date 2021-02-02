# shellcheck shell=bash

function main {
      echo "[INFO] Testing python package: ${envSrc}" \
  &&  pushd "${envSrc}" \
    &&  python -m pytest \
            -p no:cacheprovider \
            --full-trace "${envTestDir}" \
  &&  popd \
  &&  success
}

main
