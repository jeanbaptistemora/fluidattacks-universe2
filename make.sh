#! /usr/bin/env bash

attributes=(
  # Can be generated with:
  #   ./makes/nix.sh search --json | jq -er 'to_entries[] | .value.pname'
  # Stated explicitely here for performance

  skims-bin
  skims-parsers-antlr
)

function build_with_internet {
  local attr="${1}"

  ./makes/nix.sh build \
    --option 'sandbox' 'false' \
    --option 'restrict-eval' 'false' \
    --out-link "makes/outputs/${attr}" \
    --no-update-lock-file \
    --show-trace \
    ".#${attr}"
}

function main {
  local arg_1="${1:-}"
  local tempfile

      main_ctx "${@}" \
  &&  tempfile="$(mktemp)" \
  &&  for attribute in "${attributes[@]}"
      do
        if test "${attribute}" = "${arg_1}"
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
      echo "Use: ${0} [attribute]" \
  &&  echo \
  &&  echo 'Valid attributes are:' \
  &&  echo \
  &&  for attribute in "${attributes[@]}"
      do
        echo "${attribute}"
      done
}

main "${@}"
