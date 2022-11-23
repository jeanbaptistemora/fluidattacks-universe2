# shellcheck shell=bash

function main {
  local success=0

  : \
    && if integrates-front-lint-stylelint; then
      success=$((success + 1))
    fi \
    && if integrates-front-lint-eslint; then
      success=$((success + 1))
    fi \
    && if lint_npm_deps integrates/front/package.json; then
      success=$((success + 1))
    fi \
    && if test "${success}" -eq 3; then
      info "Congratulations! Your code comply with the suggested style"
    else
      critical "Your code doesn't comply with the suggested style"
    fi
}

main "${@}"
