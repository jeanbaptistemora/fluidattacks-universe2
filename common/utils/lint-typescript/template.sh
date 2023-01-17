# shellcheck shell=bash

function lint_typescript {
  local return_value=0
  local lint=(
    ./node_modules/.bin/eslint
    "${2}"
    --ext '.js,.ts,.tsx'
    --format codeframe
  )

  copy "__argConfig__/.eslintrc.js" "${1}/.eslintrc.js" \
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
