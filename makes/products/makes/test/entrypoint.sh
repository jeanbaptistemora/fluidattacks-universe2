# shellcheck disable=SC2041,SC2043 shell=bash

function main {
      ./makes/wrappers/nix3 flake check \
  &&  for attr in __envBuilt__
      do
        echo "[INFO] Succesfully built: ${attr}"
      done
}

main "${@}"
