# shellcheck shell=bash

function _podman {
  __envPodman__ \
    --conmon '__envConmon__' \
    --runtime '__envRunc__' \
    "${@}"
}

function configure_trust {
  local policy

      if test "${USER}" = 'root'
      then
        policy='/etc/containers'
      else
        policy="${HOME}/.config/containers"
      fi \
  &&  mkdir -p "${policy}" \
  &&  echo '{}' > "${policy}/policy.json" \
  &&  _podman image trust set --type accept 'default' \
  &&  _podman image trust set --type accept '__envRegistry__'
}

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
  &&  _podman login \
        --username "${username}" \
        --password "${password}" \
      "${registry}"
}

function main {
  local oci='__envOci__'
  local tag="__envTag__"
  local oci='__envOci__'

      configure_trust \
  &&  login_to_registry \
  &&  echo '[INFO] Loading OCI' \
  &&  _podman load < "${oci}" \
  &&  echo "[INFO] Tagging: ${tag}" \
  &&  _podman tag 'oci' "${tag}" \
  &&  echo "[INFO] Pushing: ${tag}" \
  &&  _podman push "${tag}" \
  &&  echo "[INFO] Deleting local copy of: ${tag}" \
  &&  _podman image rm "${tag}"
}

main "${@}"
