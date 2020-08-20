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

  local CACHE_DIR
  local TEMP_FD
  local TEMP_CA
  local TEMP_CERT
  local TEMP_KEY
  local TEMP_TLS_CRYPT

  CACHE_DIR=$(mktemp)
  exec {TEMP_FD}>TEMP_FD
  TEMP_CA=$(mktemp -t XXXXXXXX.pem)
  TEMP_CERT=$(mktemp -t XXXXXXXX.pem)
  TEMP_KEY=$(mktemp -t XXXXXXXX.pem)
  TEMP_TLS_CRYPT=$(mktemp -t XXXXXXXX.pem)

  echo 'Remember to edit your hosts file if needed!!'
  echo '    $ sudo vim /etc/hosts in linux'

  echo
  vpn_host="$(get_secret vpn_host)"
  vpn_port="$(get_secret vpn_port)"
  vpn_ca="$(get_secret vpn_ca)"
  vpn_cert="$(get_secret vpn_cert)"
  vpn_key="$(get_secret vpn_key)"
  vpn_tls_crypt="$(get_secret vpn_tls_crypt)"

  echo "${vpn_ca}">$TEMP_CA
  echo "${vpn_cert}">$TEMP_CERT
  echo "${vpn_key}">$TEMP_KEY
  echo "${vpn_tls_crypt}">$TEMP_TLS_CRYPT

  echo
  echo 'Setting VPN...'

  sudo openvpn \
  --client \
  --dev tun \
  --proto tcp-client \
  --remote "${vpn_host}" "${vpn_port}" \
  --resolv-retry infinite \
  --nobind \
  --persist-key \
  --persist-tun \
  --remote-cert-tls server \
  --auth SHA512 \
  --cipher AES-256-CBC \
  --verb 3 \
  --ca "${TEMP_CA}" \
  --cert "${TEMP_CERT}" \
  --key "${TEMP_KEY}" \
  --tls-crypt "${TEMP_TLS_CRYPT}"
}
