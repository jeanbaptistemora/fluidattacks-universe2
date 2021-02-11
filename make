#! /usr/bin/env bash

set -e
source makes/utils/shopts/template.sh

function build_package {
  local attribute="${1}"
  local attribute_output

  ./makes/wrappers/nix3.sh build \
    --out-link "out/${attribute////-}" \
    --show-trace \
    ".#${attribute}"
}

function cache_push {
  local nix_store_path="${1}"

  if test -n "${CACHIX_FLUIDATTACKS_TOKEN:-}"
  then
        echo '---' \
    &&  nix-env -iA cachix -f https://cachix.org/api/v1/install \
    &&  echo "[INFO] Pushing to cache: ${nix_store_path}" \
    &&  cachix authtoken "${CACHIX_FLUIDATTACKS_TOKEN}" \
    &&  echo "${nix_store_path}" | cachix push -c 0 fluidattacks \
    ||  return 0
  fi
}

function load_commands {
  export APPLICATIONS
  export PACKAGES

      mapfile -t APPLICATIONS < 'makes/attrs/applications.lst' \
  &&  mapfile -t PACKAGES < 'makes/attrs/packages.lst'
}

function main {
  local attr="${1:-}"

      main_ctx "${@}" \
  &&  source "${PWD}/.envrc.public" \
  &&  load_commands \
  &&  for attribute in "${APPLICATIONS[@]}"
      do
        if test "${attribute}" = "${attr}"
        then
          if run_application "${attribute}" "${@:2}"
          then
                echo '---' \
            &&  echo "[INFO] ${attribute} executed successfully" \
            &&  echo '[INFO]   Congratulations!' \
            &&  return 0
          else
                echo '---' \
            &&  echo "[ERROR] ${attribute}'s execution failed :(" \
            &&  return 1
          fi
        fi
      done \
  &&  for attribute in "${PACKAGES[@]}"
      do
        if test "${attribute}" = "${attr}"
        then
          if build_package "${attribute}"
          then
                echo '---' \
            &&  nix_store_path=$(readlink -f "out/${attribute////-}") \
            &&  echo "[INFO] ${attribute} built successfully" \
            &&  echo '[INFO]   Congratulations!' \
            &&  echo '[INFO]' \
            &&  echo "[INFO] Store path: ${nix_store_path}" \
            &&  echo "[INFO] Symlink at: out/${attribute////-}" \
            &&  cache_push "${nix_store_path}" \
            &&  return 0 \
            ||  return 0
          else
                echo '---' \
            &&  echo "[ERROR] ${attribute}'s build failed :(" \
            &&  return 1
          fi
        fi
      done \
  &&  main_help
}

function main_ctx {
      echo "[INFO] Running: ${0}" \
  &&  for arg in "${@}"
      do
        echo "[INFO]          ${arg}"
      done
}

function main_help {
      echo "Use: ${0} [attribute]" \
  &&  echo \
  &&  echo 'Applications:' \
  &&  echo \
  &&  for attr in "${APPLICATIONS[@]}"; do echo "  ${attr}"; done \
  &&  echo \
  &&  echo 'Packages:' \
  &&  echo \
  &&  for attr in "${PACKAGES[@]}"; do echo "  ${attr}"; done \
  &&  echo \
  &&  return 1 \
  ||  return 1
}

function run_application {
  local attribute="${1}"

      build_package "${attribute}" \
  &&  "${PWD}/out/${attribute////-}/bin/${attribute////-}" "${@:2}"
}

main "${@}"
