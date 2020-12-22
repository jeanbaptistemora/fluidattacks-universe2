#! __envShell__
# shellcheck shell=bash

source '__makeEntrypoint__'

function main {
  local tag='registry.gitlab.com/fluidattacks/product/makes:ci'
  local build_args=(
    --tag "${tag}"
  )

      echo "[INFO] Logging into: ${CI_REGISTRY}" \
  &&  __envDocker__ login \
        --username "${CI_REGISTRY_USER}" \
        --password "${CI_REGISTRY_PASSWORD}" \
      "${CI_REGISTRY}" \
  &&  echo "[INFO] Building: ${tag}" \
  &&  __envDocker__ build "${build_args[@]}" "__envDockerContext__" \
  &&  echo "[INFO] Pushing: ${tag}" \
  &&  __envDocker__ push "${tag}" \
  &&  echo "[INFO] Deleting local copy of: ${tag}" \
  &&  __envDocker__ image remove "${tag}" \

}

main "${@}"
