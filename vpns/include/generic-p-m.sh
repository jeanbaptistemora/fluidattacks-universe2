#! /usr/bin/env bash

# shellcheck disable=SC1091
source toolbox/vpns/include/generic.sh

function start_vpn() {
  # Required secrets
  local vpn_host_medellin
  local vpn_port
  local vpn_user
  local vpn_pass
  local vpn_trusted_cert

  echo 'Remember to edit your hosts file if needed!!'
  echo '    $ sudo vim /etc/hosts in linux'

  echo
  vpn_host_medellin="$(get_secret vpn_host_medellin)"
  vpn_port="$(get_secret vpn_port)"
  vpn_user="$(get_secret vpn_user)"
  vpn_pass="$(get_secret vpn_pass)"
  vpn_trusted_cert="$(get_secret vpn_trusted_cert)"

  # Fire up the vpn
  echo
  echo 'Setting VPN...'
  # shellcheck disable=SC2024
  sudo "$(command -v openfortivpn)" \
    "${vpn_host_medellin}:${vpn_port}" \
    -u "${vpn_user}" \
    -p "${vpn_pass}" \
    --trusted-cert "${vpn_trusted_cert}"
}
