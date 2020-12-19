#! /usr/bin/env bash

function build_with_internet {
  local attr="${1}"

  nix-build \
    --attr "${attr}" \
    --option 'sandbox' 'false' \
    --option 'restrict-eval' 'false' \
    --no-out-link \
    --show-trace \
    makes
}

function list_attributes {
  nix-env -qa -f makes
}

function main {
  local arg_1="${1:-}"
  local attributes
  local tempfile

      main_ctx "${@}" \
  &&  tempfile="$(mktemp)" \
  &&  list_attributes > "${tempfile}" \
  &&  while read -r attribute
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
            &&  echo "[INFO] ${attribute} build failed :(" \
            &&  return 1
          fi
        fi
      done < "${tempfile}" \
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
  &&  list_attributes
}

main "${@}"
