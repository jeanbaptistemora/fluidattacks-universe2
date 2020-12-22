#! /usr/bin/env bash

apps=(
  common-deploy-oci
  skims
  skims-lint
)
packages=(
  skims-parsers-antlr
  skims-parsers-babel
)

function build_with_internet {
  local attr="${1}"

  ./makes/nix build \
    --option 'sandbox' 'false' \
    --option 'restrict-eval' 'false' \
    --out-link "makes/outputs/${attr}" \
    --no-update-lock-file \
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
  local cmd="${1:-}"
  local attr="${2:-}"

      main_ctx "${@}" \
  &&  for attribute in "${apps[@]}"
      do
        if test "${attribute}" = "${attr}"
        then
          if run_with_internet "${attribute}" "${@:3}"
          then
            return 0
          else
            return 1
          fi
        fi
      done \
  &&  for attribute in "${packages[@]}"
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
      echo "Use: ${0} [build/run] [attribute]" \
  &&  echo \
  &&  echo 'Valid build attributes are:' \
  &&  echo \
  &&  for attribute in "${packages[@]}"; do echo "  ${attribute}"; done \
  &&  echo \
  &&  echo 'Valid run attributes are:' \
  &&  echo \
  &&  for attribute in "${apps[@]}"; do echo "  ${attribute}"; done \
  &&  echo \

}

main "${@}"
