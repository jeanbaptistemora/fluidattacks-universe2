# shellcheck shell=bash

function main {
  local coverage_args=(
    --omit="back/migrations/*"
    --skip-empty
    -i
  )

  : \
    && aws_login "dev" "3600" \
    && pushd integrates \
    && coverage combine \
    && coverage report "${coverage_args[@]}" \
    && coverage html "${coverage_args[@]}" -d build \
    && coverage xml "${coverage_args[@]}" \
    && sops_export_vars __argSecretsDev__ CODECOV_TOKEN \
    && if test "${CI_COMMIT_REF_NAME}" = trunk; then
      codecov -B trunk -C "${CI_COMMIT_SHA}" -F integrates
    fi \
    && popd \
    || return 1
}

main "${@}"
