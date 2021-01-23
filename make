#! /usr/bin/env bash

set -e
source makes/utils/shopts/template.sh

function build_with_internet {
  local attr="${1}"

  ./makes/wrappers/nix3 build \
    --option 'sandbox' 'false' \
    --option 'restrict-eval' 'false' \
    --out-link "makes/outputs/${attr}" \
    --show-trace \
    ".#${attr}"
}

function cachix_push {
  local nix_store_path="${1}"

  if test -n "${CACHIX_FLUIDATTACKS_TOKEN:-}"
  then
        echo "[INFO] Pushing to cache: ${nix_store_path}" \
    &&  cachix authtoken "${CACHIX_FLUIDATTACKS_TOKEN}" \
    &&  echo "${nix_store_path}" | cachix push -c 9 fluidattacks
  fi
}

function ensure_cachix {
      if test -z "$(command -v cachix)"
      then
        nix-env -iA cachix -f https://cachix.org/api/v1/install
      fi \
  &&  if ! cachix use fluidattacks
      then
        echo '[WARNING] Could not configure binary cache'
      fi \
  &&  echo '---'
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
  &&  ensure_cachix \
  &&  source "${PWD}/.envrc.public" \
  &&  load_commands \
  &&  for attribute in "${APPLICATIONS[@]}"
      do
        if test "${attribute}" = "${attr}"
        then
          if run_with_internet "${attribute}" "${@:2}"
          then
                echo '---' \
            &&  echo "[INFO] ${attribute} executed successfully" \
            &&  echo '[INFO]   Congratulations!' \
            &&  return 0
          else
                echo \
            &&  echo "[ERROR] ${attribute}'s execution failed :(" \
            &&  return 1
          fi
        fi
      done \
  &&  for attribute in "${PACKAGES[@]}"
      do
        if test "${attribute}" = "${attr}"
        then
          if build_with_internet "${attribute}"
          then
                echo '---' \
            &&  nix_store_path=$(readlink -f "makes/outputs/${attribute}") \
            &&  cachix_push "${nix_store_path}" \
            &&  echo "[INFO] ${attribute} built successfully" \
            &&  echo '[INFO]   Congratulations!' \
            &&  echo '[INFO]' \
            &&  echo "[INFO] Store path: ${nix_store_path}" \
            &&  echo "[INFO] Symlink at: ./makes/outputs/${attribute}" \
            &&  return 0
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
      done \
  &&  echo '---' \
  &&  echo
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

function run_with_internet {
  local attr="${1}"

  ./makes/wrappers/nix3 run \
    --option 'sandbox' 'false' \
    --option 'restrict-eval' 'false' \
    --show-trace \
    ".#${attr}" \
    -- \
    "${@:2}"
}

main "${@}"
