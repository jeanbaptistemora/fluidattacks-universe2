# shellcheck shell=bash

function main {
  aws_login_dev \
    && pushd integrates \
    && sops_export_vars secrets-development.yaml CODECOV_TOKEN \
    && codecov -b "${CI_COMMIT_REF_NAME}" \
    && popd \
    || return 1
}

main "${@}"
