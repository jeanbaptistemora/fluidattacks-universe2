# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function lint_typescript {
  copy "__argConfig__/.eslintrc.json" "${1}/.eslintrc.json" \
    && copy "__argConfig__/.prettierrc.json" "${1}/.prettierrc.json" \
    && pushd "${1}" \
    && ./node_modules/.bin/eslint "${2}" --ext .js,.ts,.tsx --format codeframe \
    && popd \
    || return 1
}
