# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function sorts {
  python3.8 '__argSrcSortsSorts__/cli/__init__.py' "$@"
}
