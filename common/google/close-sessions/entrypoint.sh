# shellcheck shell=bash

function main {
  aws_login_prod "common" \
    && sops_export_vars __argData__ \
      GOOGLE_AUTH \
    && python __argScript__
}

main "${@}"
