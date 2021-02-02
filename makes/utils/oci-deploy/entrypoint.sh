# shellcheck shell=bash

function login_to_registry {
  local registry
  local username
  local password

  if test '__envRegistry__' = 'registry.gitlab.com'
  then
        registry="${CI_REGISTRY}" \
    &&  username="${CI_REGISTRY_USER}" \
    &&  password="${CI_REGISTRY_PASSWORD}"
  elif  test '__envRegistry__' = 'docker.io'
  then
        registry="${DOCKER_HUB_URL}" \
    &&  username="${DOCKER_HUB_USER}" \
    &&  password="${DOCKER_HUB_PASS}"
  else
        echo "Ivalid registry" \
    &&  return 1
  fi \
  &&  echo "[INFO] Logging into: ${registry}" \
  &&  __envDocker__ login \
        --username "${username}" \
        --password "${password}" \
      "${registry}"
}

function main {
      login_to_registry \
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
