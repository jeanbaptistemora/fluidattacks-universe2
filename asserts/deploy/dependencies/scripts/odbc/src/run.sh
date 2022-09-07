#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell --show-trace

# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

#  shellcheck shell=bash

set -e

# Set ODBC drivers
echo "We are setting ODBC configurations!"
echo
echo "We'll try without sudo, and then with sudo"
echo
if odbcinst -i -d -r <<< "${odbcIniContents}" \
  || sudo "$(command -v odbcinst)" -i -d -r <<< "${odbcIniContents}"; then
  echo '  Ok!'
else
  echo '  Failed, please check the source code'
fi
echo
echo 'If everything went well, you will see the contents of /etc/odbcinst.ini'
echo
cat /etc/odbcinst.ini
