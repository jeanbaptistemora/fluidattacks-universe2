# shellcheck shell=bash

function main {
  local credentials
  local oci='__envOci__'
  local tag="__envTag__"

      echo '[INFO] Setting up credentials' \
  &&  if test '__envRegistry__' = 'registry.gitlab.com'
      then
        credentials="${CI_REGISTRY_USER}:${CI_REGISTRY_PASSWORD}"
      elif  test '__envRegistry__' = 'docker.io'
      then
        credentials="${DOCKER_HUB_USER}:${DOCKER_HUB_PASS}"
      else
            echo "Ivalid registry" \
        &&  return 1
      fi \
  &&  echo "[INFO] Syncing OCI: ${tag}" \
  &&  skopeo \
        --insecure-policy \
        copy \
        --dest-creds "${credentials}" \
        "docker-archive://${oci}" \
        "docker://${tag}"
}

main "${@}"
