#! /usr/bin/env bash

function build_with_internet {
  local attr="${1}"

  ./makes/nix build \
    --option 'sandbox' 'false' \
    --option 'restrict-eval' 'false' \
    --out-link "makes/outputs/${attr}" \
    --show-trace \
    ".#${attr}"
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

function main {
  local attr="${1:-}"

      main_ctx "${@}" \
  &&  source .envrc.public \
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
            &&  echo "[INFO] ${attribute} built successfully" \
            &&  echo '[INFO]   Congratulations!' \
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

}

main "${@}"
