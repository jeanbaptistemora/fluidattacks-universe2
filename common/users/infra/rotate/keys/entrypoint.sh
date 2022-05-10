# shellcheck shell=bash

function main {
  local day="${1:-}"

  aws_login_prod "common" \
    && if [ "${day}" = "even" ]; then
      taint-terraform-for-commonUsersKeys1
    elif [ "${day}" = "odd" ]; then
      taint-terraform-for-commonUsersKeys2
    else
      error "Either 'even' or 'odd' must be passed."
    fi \
    && aws_login_prod "integrates" \
    && integrates-back-deploy-prod "${day}"
}

main "${@}"
