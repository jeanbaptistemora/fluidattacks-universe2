#! /usr/bin/env bash

# shellcheck disable=SC1091
source toolbox/vpns/include/generic.sh

function start_vpn() {
  # Required secrets
  local vpn_host
  local vpn_user
  local vpn_pass
  local vpn_auth_group

  vpn_host="$(get_secret vpn_host)"
  vpn_user="$(get_secret vpn_user)"
  vpn_pass="$(get_secret vpn_pass)"
  vpn_auth_group="$(get_secret vpn_auth_group)"
  echo

  # Fire up the vpn
  echo 'Setting VPN...'
  # shellcheck disable=SC2024
  sudo "$(command -v openconnect)" \
      --protocol='anyconnect' \
      --user="${vpn_user}" \
      --authgroup="${vpn_auth_group}" \
      --passwd-on-stdin \
    "${vpn_host}" \
    < <(
        echo "${vpn_pass}"
        echo "yes"
      )
}
