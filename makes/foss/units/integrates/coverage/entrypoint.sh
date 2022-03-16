# shellcheck shell=bash

function main {
  local coverage_args=(
    --omit="back/migrations/*"
    --skip-empty
    -i
  )
  aws_login_dev \
    && pushd integrates \
    && coverage combine \
    && coverage report "${coverage_args[@]}" \
    && coverage html "${coverage_args[@]}" -d build \
    && sops_export_vars secrets-development.yaml CODECOV_TOKEN \
    && codecov -b "${CI_COMMIT_REF_NAME}" \
    && popd \
    || return 1
}

main "${@}"
