#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell -p openvpn
#
# shellcheck shell=bash

set -o errexit
set -o nounset

# shellcheck disable=SC1091
source toolbox/vpns/include/generic-p.sh

start_vpn
