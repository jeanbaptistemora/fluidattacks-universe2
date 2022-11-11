# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function lint_npm_deps {
  local return_value=0

  : \
    && if jq -r ".dependencies * (.devDependencies // {}) | .[]" "${1}" | grep -qE '\.x|\.X|\^|\*|~|>|<|="'; then
      : && critical "Dependencies must be pinned to an exact version" \
        && return_value=1
    fi \
    && return "${return_value}"
}
