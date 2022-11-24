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
