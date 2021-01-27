# shellcheck shell=bash

function main {
      echo '[INFO] Checking flake' \
  &&  ./makes/wrappers/nix3 flake check \

}

main "${@}"
