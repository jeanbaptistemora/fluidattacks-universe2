# shellcheck shell=bash
function configure_nss {
  mkdir -p "${out}/etc" \
    && echo 'hosts: dns files' > "${out}/etc/nsswitch.conf"
}

function configure_ssh {
  # Configure SSH, the host key verification is weakened on purpose because
  # many jobs that run on this image connect to thousands of unknown providers

  mkdir -p "${out}/home/makes/.ssh" \
    && echo 'Host *' > "${out}/home/makes/.ssh/config" \
    && echo '  StrictHostKeyChecking no' >> "${out}/home/makes/.ssh/config" \
    && chmod 400 "${out}/home/makes/.ssh/config"
}

function configure_tmp {
  mkdir -p "${out}/tmp" \
    && mkdir -p "${out}/var/tmp"
}

function configure_users {
  mkdir -p "${out}/etc" \
    && mkdir -p "${out}/home/makes" \
    && mkdir -p "${out}/etc/pam.d" \
    && touch "${out}/etc/login.defs" \
    && echo "${envEtcGroup}" > "${out}/etc/group" \
    && echo "${envEtcGshadow}" > "${out}/etc/gshadow" \
    && echo "${envEtcPamdOther}" > "${out}/etc/pam.d/other" \
    && echo "${envEtcPasswd}" > "${out}/etc/passwd" \
    && echo "${envEtcShadow}" > "${out}/etc/shadow"
}

function configure_usr_bin_env {
  mkdir -p "${out}/usr/bin" \
    && ln -s "$(command -v env)" "${out}/usr/bin/env"
}

function main {
  configure_nss \
    && configure_ssh \
    && configure_tmp \
    && configure_users \
    && configure_usr_bin_env
}

main "${@}"
