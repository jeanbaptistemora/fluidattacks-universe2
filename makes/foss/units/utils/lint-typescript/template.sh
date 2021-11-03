# shellcheck shell=bash

function lint_typescript {
  copy "__argConfig__/.eslintrc.json" "${1}/.eslintrc.json" \
    && copy "__argConfig__/.prettierrc.json" "${1}/.prettierrc.json" \
    && pushd "${1}" \
    && ./node_modules/.bin/eslint "${2}" --ext .js,.ts,.tsx --format codeframe \
    && popd \
    || return 1
}
