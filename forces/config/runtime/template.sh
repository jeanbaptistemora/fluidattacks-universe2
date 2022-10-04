# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function forces {
  python3.10 '__argSrcForces__/forces/cli/__init__.py' "$@"
}
