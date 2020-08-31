#! /usr/bin/env bash

# shellcheck disable=SC1091
source toolbox/vpns/include/generic.sh

function start_vpn() {
  # Required secrets
  local vpn_host
  local vpn_port
  local vpn_user
  local vpn_pass
  local vpn_trusted_cert

  echo 'Remember to edit your hosts file !!'
  echo '  The mapping is at Integrates resources:'
  echo '    $ sudo vim /etc/hosts in linux'

  echo
  vpn_host="$(get_secret vpn_host)"
  vpn_port="$(get_secret vpn_port)"
  vpn_user="$(get_secret vpn_user)"
  vpn_pass="$(get_secret vpn_pass)"
  vpn_trusted_cert="$(get_secret vpn_trusted_cert)"

  # Fire up the vpn
  echo
  echo 'Setting VPN...'
  # shellcheck disable=SC2024
  sudo "$(command -v openfortivpn)" \
    "${vpn_host}:${vpn_port}" \
    -u "${vpn_user}" \
    -p "${vpn_pass}" \
    --trusted-cert "${vpn_trusted_cert}"
}
