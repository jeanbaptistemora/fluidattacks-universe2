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
    && coverage xml "${coverage_args[@]}" \
    && sops_export_vars __argSecretsDev__ CODECOV_TOKEN \
    && __argCodecov__ -C "${CI_COMMIT_SHA}" -B "trunk" -F integrates \
    && popd \
    || return 1
}

main "${@}"
