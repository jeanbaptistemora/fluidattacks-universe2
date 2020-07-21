#! /usr/bin/env bash

echo '[INFO] Checking nix is installed'
if ! nix-env --version
then
  echo
  echo '[ERROR] Please install nix: https://nixos.org/download.html'
  echo '  On most systems it is:'
  echo '    $ curl -L https://nixos.org/nix/install | sh'
  exit
fi

echo
echo '[INFO] Checking fluidasserts is not installed with pip'
if command -v asserts | grep -v nix
then
  echo
  echo '[ERROR] Please uninstall fluidasserts with pip'
  exit
fi

echo
echo '[INFO] Installing products'
nix-env -i product -f default.nix
