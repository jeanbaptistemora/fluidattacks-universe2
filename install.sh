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
echo '[INFO] Checking skims is not installed with pip'
if command -v skims | grep -v nix
then
  echo
  echo '[ERROR] Please uninstall skims with pip'
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
echo '[INFO] Checking melts is not installed with pip'
if command -v melts | grep -v nix
then
  echo
  echo '[ERROR] Please uninstall melts with pip'
  exit
fi

echo
echo '[INFO] Checking sorts is not installed with pip'
if command -v sorts | grep -v nix
then
  echo
  echo '[ERROR] Please uninstall sorts with pip'
  exit
fi

for binary in cloc sops
do
  echo
  echo "[INFO] Installing ${binary}"
  if ! nix-env -i "${binary}"
  then
    echo
    echo "[ERROR] Please unisntall ${binary} first with: nix-env -e ${binary}"
    exit
  fi
done

echo
echo '[INFO] Installing products'
nix-env -i product -f default.nix
