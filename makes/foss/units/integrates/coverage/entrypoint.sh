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
    && coverage html "${coverage_args[@]}" \
    && sops_export_vars secrets-development.yaml CODECOV_TOKEN \
    && curl -Os https://uploader.codecov.io/latest/linux/codecov \
    && chmod +x codecov \
    && ./codecov -B "master" \
    && popd \
    || return 1
}

main "${@}"
