# shellcheck shell=bash

function main {
  aws_login_dev \
    && pushd integrates \
    && coverage combine \
    && coverage report -i \
    && coverage html -i -d build \
    && sops_export_vars secrets-development.yaml CODECOV_TOKEN \
    && codecov -b "${CI_COMMIT_REF_NAME}" \
    && popd \
    || return 1
}

main "${@}"
