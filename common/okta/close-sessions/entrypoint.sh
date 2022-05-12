# shellcheck shell=bash

function main {
  aws_login_prod "common" \
    && sops_export_vars __argData__ \
      OKTA_API_TOKEN \
    && python __argScript__
}

main "${@}"
