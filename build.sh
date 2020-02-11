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

# Ensure that a required policy is set
if ! test -e '/etc/containers/policy.json'
then
  echo '[INFO] Creating /etc/containers/policy.json'
  if test -x "$(command -v sudo)"
  then
    echo '[INFO] Please allow sudo privileges here'
    sudo mkdir -p /etc/containers
    sudo cp -f {./build,}/etc/containers/policy.json
  else
    mkdir -p /etc/containers
    cp -f {./build,}/etc/containers/policy.json
  fi
fi

# Call the nix-shell executor
./build/shell.sh "${@}"
