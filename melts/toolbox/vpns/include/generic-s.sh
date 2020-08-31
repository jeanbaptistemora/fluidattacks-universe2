#! /usr/bin/env bash

# shellcheck disable=SC1091
source toolbox/vpns/include/generic.sh

function start_vpn() {
  # Required secrets
  local vpn_host
  local vpn_user
  local vpn_pass
  local vpn_pass_pfx
  
  echo
  vpn_host="$(get_secret vpn_host)"
  vpn_user="$(get_secret vpn_user)"
  vpn_pass="$(get_secret vpn_pass)"
  vpn_pass_pfx="$(get_secret vpn_pass_pfx)"
  echo

  # Fire up the vpn
  echo 'Setting VPN...'
  # shellcheck disable=SC2024
  sudo "$(command -v openconnect)" \
      --protocol='gp' \
      --user="${vpn_user}" \
      --certificate './vpns/data/simplexity.pfx' \
      --passwd-on-stdin \
    "${vpn_host}" \
    < <(
        echo "${vpn_pass}"
        echo "${vpn_pass_pfx}"
        echo 'yes'
        echo
      )
}
