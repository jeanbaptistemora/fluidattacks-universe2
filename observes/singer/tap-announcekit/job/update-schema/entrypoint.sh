# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

alias tap-announcekit="observes-singer-tap-announcekit-bin"

tap-announcekit update-schema \
  --out "./observes/singer/tap-announcekit/src/tap_announcekit/api/gql_schema.py"
