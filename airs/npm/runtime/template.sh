# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function install_scripts {
  rm -rf node_modules/sharp \
    && npm install --ignore-scripts=false
}
