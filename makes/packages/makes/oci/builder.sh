# shellcheck shell=bash

function configure_nix {
      mkdir -p "${out}/home/makes/.config/nix" \
  &&  mkdir -p "${out}/etc/nix" \
  &&  mkdir -p "${out}/nix/store/.links" \
  &&  mkdir -p "${out}/nix/var" \
  &&  echo 'build-users-group =' | tee \
        "${out}/home/makes/.config/nix/nix.conf" \
        "${out}/etc/nix/nix.conf"
}

function configure_nss {
      mkdir -p "${out}/etc" \
  &&  echo 'hosts: dns files' > "${out}/etc/nsswitch.conf"
}

function configure_tmp {
      mkdir -p "${out}/tmp" \
  &&  mkdir -p "${out}/var/tmp"
}

function configure_product {
      mkdir -p "${out}/product" \
  &&  mkdir -p "${out}/product/makes/utils/shopts" \
  &&  mirror "/m" \
  &&  mirror "/makes/utils/shopts/template.sh"
}

function configure_users {
      mkdir -p "${out}/etc" \
  &&  mkdir -p "${out}/home/makes" \
  &&  mkdir -p "${out}/etc/pam.d" \
  &&  touch "${out}/etc/login.defs" \
  &&  echo "${envEtcGroup}" > "${out}/etc/group" \
  &&  echo "${envEtcGshadow}" > "${out}/etc/gshadow" \
  &&  echo "${envEtcPamdOther}" > "${out}/etc/pam.d/other" \
  &&  echo "${envEtcPasswd}" > "${out}/etc/passwd" \
  &&  echo "${envEtcShadow}" > "${out}/etc/shadow"
}

function main {
      configure_nix \
  &&  configure_nss \
  &&  configure_product \
  &&  configure_tmp \
  &&  configure_users
}

function mirror {
  copy "${envSrc}${1}" "${out}/product/${1}"
}

main "${@}"
