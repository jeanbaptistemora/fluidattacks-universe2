# shellcheck shell=bash

source "${makeDerivation}"

function main {
      nix-linter \
        --recursive \
        --verbose \
        "${envSrcMakes}" \
  &&  success
}

main "${@}"
