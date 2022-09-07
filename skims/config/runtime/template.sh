# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

if test -n "${HOME_IMPURE:-}"; then
  export HOME="${HOME_IMPURE}"
fi
export PYTHONHASHSEED=0

function skims {
  python '__argSrcSkimsSkims__/cli/__init__.py' "$@"
}
