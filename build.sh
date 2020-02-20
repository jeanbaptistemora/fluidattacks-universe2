#! /usr/bin/env bash

source ./build/include/generic/shell-options.sh

# Check that Nix is installed
if ! nix --version
then
  echo 'Please install nix: https://nixos.org/nix/download.html'
  echo '  on most systems this is:'
  echo '    $ curl https://nixos.org/nix/install | sh'
  return 1
fi

# Call the nix-shell executor
./build/shell.sh "${@}"
