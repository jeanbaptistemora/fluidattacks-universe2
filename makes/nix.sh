#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell -I nixpkgs=https://github.com/NixOS/nixpkgs/archive/030e2ce817c8e83824fb897843ff70a15c131b96.tar.gz
#!   nix-shell -p nixFlakes

nix \
  --experimental-features 'nix-command flakes' \
  --print-build-logs \
  --verbose \
  "${@}"
