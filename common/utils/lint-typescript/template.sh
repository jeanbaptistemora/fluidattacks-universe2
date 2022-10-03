# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function lint_typescript {
  local return_value=0
  local lint=(
    ./node_modules/.bin/eslint
    "${2}"
    --ext '.js,.ts,.tsx'
    --format codeframe
  )

  copy "__argConfig__/.eslintrc.json" "${1}/.eslintrc.json" \
    && copy "__argConfig__/.prettierrc.json" "${1}/.prettierrc.json" \
    && pushd "${1}" \
    && if ! "${lint[@]}"; then
      : && info 'Some files do not follow the suggested style.' \
        && info 'we will fix some of the issues automatically,' \
        && info 'but the job will fail.' \
        && { "${lint[@]}" --fix || true; } \
        && return_value=1
    fi \
    && popd \
    && return "${return_value}"
}
