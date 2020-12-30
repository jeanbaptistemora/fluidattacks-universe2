# shellcheck shell=bash

function main {
      echo "[INFO] Logging into: ${CI_REGISTRY}" \
  &&  __envDocker__ login \
        --username "${CI_REGISTRY_USER}" \
        --password "${CI_REGISTRY_PASSWORD}" \
      "${CI_REGISTRY}" \
  &&  echo '[INFO] Building: __envTag__' \
  &&  __envDocker__ build --tag '__envTag__' '__envDockerContext__' \
  &&  echo '[INFO] Pushing: __envTag__' \
  &&  __envDocker__ push '__envTag__' \
  &&  echo '[INFO] Deleting local copy of: __envTag__' \
  &&  __envDocker__ image remove '__envTag__' \

}

main "${@}"
