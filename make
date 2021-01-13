#! /usr/bin/env bash

source makes/utils/bash-lib/shopts.sh

function build_with_internet {
  local attr="${1}"

  ./makes/nix build \
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
  &&  cachix use fluidattacks
}

function main {
  local attr="${1:-}"

      main_ctx "${@}" \
  &&  source "${PWD}/.envrc.public" \
  &&  ensure_cachix \
  &&  while read -r attribute
      do
        if test "${attribute}" = "${attr}"
        then
          if run_with_internet "${attribute}" "${@:2}"
          then
            return 0
          else
            return 1
          fi
        fi
      done < "makes/attrs/applications.lst" \
  &&  while read -r attribute
      do
        if test "${attribute}" = "${attr}"
        then
          if build_with_internet "${attribute}"
          then
                echo \
            &&  nix_store_path=$(readlink -f "makes/outputs/${attribute}") \
            &&  cachix_push "${nix_store_path}" \
            &&  echo "[INFO] ${attribute} built successfully" \
            &&  echo '[INFO]   Congratulations!' \
            &&  echo '[INFO]' \
            &&  echo "[INFO] Store path: ${nix_store_path}" \
            &&  echo "[INFO] Symlink at: ./makes/outputs/${attribute}" \
            &&  return 0
          else
                echo \
            &&  echo "[INFO] ${attribute}'s build failed :(" \
            &&  return 1
          fi
        fi
      done < "makes/attrs/packages.lst" \
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
  &&  while read -r attr; do echo "  ${attr}"; done < "makes/attrs/applications.lst" \
  &&  echo \
  &&  echo 'Packages are:' \
  &&  echo \
  &&  while read -r attr; do echo "  ${attr}"; done < "makes/attrs/packages.lst" \
  &&  echo \
  &&  return 1 \
  ||  return 1
}

function run_with_internet {
  local attr="${1}"

  ./makes/nix run \
    --option 'sandbox' 'false' \
    --option 'restrict-eval' 'false' \
    --show-trace \
    ".#${attr}" \
    -- \
    "${@:2}"
}

main "${@}"
