# shellcheck shell=bash

export PATH="__envNetworkManager__/bin:${PATH:-}"

function main {
  local vpn_data
  local vpn_ipsec_psk
  local vpn_user
  local connection_id='fluidvpn'

      if ! nmcli connection show "${connection_id}" >&2:
      then
            echo "[INFO] Setting up the vpn" \
        &&  read -r -p "Enter your psk: " vpn_ipsec_psk \
        &&  read -r -p "Enter your username: " vpn_user \
        &&  vpn_data="gateway = 190.217.110.94, ipsec-enabled = yes, ipsec-psk = ${vpn_ipsec_psk}, mru = 1400, mtu = 1400, password-flags = 0, refuse-chap = yes, refuse-eap = yes, refuse-mschap = yes, refuse-pap = yes, user = ${vpn_user}" \
        &&  nmcli connection add  \
              connection.id "${connection_id}" \
              con-name fluidvpn \
              type VPN \
              vpn-type l2tp \
              ifname -- \
              connection.autoconnect no \
              ipv4.method auto \
              vpn.data "${vpn_data}"
      fi \
  &&  if ! nmcli connection up "${connection_id}"
      then
        # If the VPN is already connected, then disconnect
        nmcli connection down "${connection_id}"
      fi
}

main
