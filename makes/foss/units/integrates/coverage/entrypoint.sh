# shellcheck shell=bash

function main {
  aws_login_dev integrates \
    && pushd integrates \
    && sops_export_vars secrets-development.yaml CODECOV_TOKEN \
    && codecov -b "${CI_COMMIT_REF_NAME}" \
    && popd \
    || return 1
}

main "${@}"
