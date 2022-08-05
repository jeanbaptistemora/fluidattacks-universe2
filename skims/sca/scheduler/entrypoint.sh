# shellcheck shell=bash

function main {
  shopt -s nullglob \
    && pushd skims \
    && aws_login_prod 'skims' \
    && sops_export_vars __argSecretsProd__ "DYNAMODB_HOST" "DYNAMODB_PORT" "ENVIRONMENT" \
    && python3 -m schedulers/update_sca_table/__init__.py \
    && popd \
    || return 1
}

main "${@}"
