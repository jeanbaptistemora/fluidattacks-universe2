#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell -p openconnect
#
# shellcheck shell=bash

set -o errexit
set -o nounset

# shellcheck disable=SC1091
source toolbox/vpns/include/generic-b.sh

start_vpn
