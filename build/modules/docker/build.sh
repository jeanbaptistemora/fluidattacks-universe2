#! /usr/bin/env bash

source ./build/include/generic/shell-options.sh

function build_single {
  local derivation_path="${1}"
  local tag
  local image
  local target

      echo "[INFO] Building: ${derivation_path}" \
  &&  target=$(mktemp) \
  &&  rm -f "${target}" \
  &&  tag="${derivation_path#build/modules/docker/images/}" \
  &&  tag="${tag%/default.nix}" \
  &&  tag="${tag////:}" \
  &&  image="${CI_REGISTRY_IMAGE}/${tag}" \
  &&  nix-build \
        --out-link "${target}" \
        --option restrict-eval false \
        --option sandbox false \
      "${derivation_path}" \
  &&  echo "[INFO] Loading: ${target}" \
  &&  docker load < "${target}" \
  &&  echo "[INFO] Tagging ${tag} as: ${image}" \
  &&  docker tag "${tag}" "${image}" \
  &&  echo "[INFO] Pushing: ${image}" \
  &&  docker push "${image}" \
  &&  echo "[INFO] Deleting local copies" \
  &&  docker image rm "${image}" \
  &&  docker image rm "${tag}" \
  &&  rm -f "${target}"
}

function build_all {
  local derivation_path

      echo "[INFO] sourcing: .envrc.public" \
  &&  source './.envrc.public' \
  &&  echo "[INFO] Logging into: ${CI_REGISTRY}" \
  &&  docker login \
        --username "${CI_REGISTRY_USER}" \
        --password "${CI_REGISTRY_PASSWORD}" \
      "${CI_REGISTRY}" \
  &&  find build/modules/docker/images -type f \
      | while read -r derivation_path
        do
          build_single "${derivation_path}" \
            || return 1
        done
}

build_all
