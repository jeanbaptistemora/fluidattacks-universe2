#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell --show-trace
#  shellcheck shell=bash

set -e

# Set ODBC drivers
echo "We are setting ODBC configurations!"
echo
echo "We'll try without sudo, and then with sudo"
echo
if odbcinst -i -d -r <<< "${odbcIniContents}" \
  || sudo "$(command -v odbcinst)" -i -d -r <<< "${odbcIniContents}"
then
  echo '  Ok!'
else
  echo '  Failed, please check the source code'
fi
echo
echo 'If everything went well, you will see the contents of /etc/odbcinst.ini'
echo
cat /etc/odbcinst.ini
