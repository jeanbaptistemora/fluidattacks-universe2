# shellcheck shell=bash

function main {
      echo "[INFO] Testing python package: ${envSrc}" \
  &&  pushd "${envSrc}" \
    &&  USER=nobody python -m pytest \
            -p no:cacheprovider \
            --full-trace "${envTestDir}" \
  &&  popd \
  &&  touch "${out}"
}

main
