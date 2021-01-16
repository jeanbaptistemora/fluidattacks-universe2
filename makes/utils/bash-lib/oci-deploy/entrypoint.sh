# shellcheck shell=bash

function main {
      echo "[INFO] Logging into: ${CI_REGISTRY}" \
  &&  __envDocker__ login \
        --username "${CI_REGISTRY_USER}" \
        --password "${CI_REGISTRY_PASSWORD}" \
      "${CI_REGISTRY}" \
  &&  echo '[INFO] Loading OCI' \
  &&  __envDocker__ load < '__envOci__' \
  &&  echo '[INFO] Tagging: __envTag__' \
  &&  __envDocker__ tag 'oci' '__envTag__' \
  &&  echo '[INFO] Pushing: __envTag__' \
  &&  __envDocker__ push '__envTag__' \
  &&  echo '[INFO] Deleting local copy of: __envTag__' \
  &&  __envDocker__ image remove '__envTag__' \

}

main "${@}"
