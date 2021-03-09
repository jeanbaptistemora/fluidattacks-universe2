# shellcheck shell=bash

function main {
      mkdir -p "${out}/etc/nix" \
  &&  mkdir -p "${out}/tmp" \
  &&  echo "build-users-group =" > "${out}/etc/nix/nix.conf" \

}

main "${@}"
