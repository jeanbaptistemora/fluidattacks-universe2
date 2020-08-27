#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell -p openfortivpn
#
# shellcheck shell=bash

set -o errexit
set -o nounset

# shellcheck disable=SC1091
source toolbox/vpns/include/forti-generic.sh

start_vpn
