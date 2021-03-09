# shellcheck shell=bash

function main {
      mkdir -p "${out}/.config/nix" \
  &&  mkdir -p "${out}/etc/nix" \
  &&  mkdir -p "${out}/tmp" \
  &&  mkdir -p "${out}/var/tmp" \
  &&  echo 'build-users-group =' > "${out}/.config/nix/nix.conf" \
  &&  echo 'build-users-group =' > "${out}/etc/nix/nix.conf" \
  &&  echo 'hosts: dns files' > "${out}/etc/nsswitch.conf" \

}

main "${@}"
