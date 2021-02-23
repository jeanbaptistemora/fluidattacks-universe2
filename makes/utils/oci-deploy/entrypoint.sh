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
  local oci='__envOci__'
  local tag="__envTag__"
  local oci='__envOci__'

      login_to_registry \
  &&  echo '[INFO] Loading OCI' \
  &&  __envDocker__ load < "${oci}" \
  &&  echo "[INFO] Tagging: ${tag}" \
  &&  __envDocker__ tag 'oci' "${tag}" \
  &&  echo "[INFO] Pushing: ${tag}" \
  &&  __envDocker__ push "${tag}" \
  &&  echo "[INFO] Deleting local copy of: ${tag}" \
  &&  __envDocker__ image remove "${tag}"
}

main "${@}"
