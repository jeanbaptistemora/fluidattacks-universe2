# shellcheck shell=bash

function main {
  local coverage_target=87.55
  local coverage_args=(
    --omit="back/migrations/*"
    --ignore-errors
  )

  : \
    && pushd integrates \
    && coverage run --data-file='.coverage.back.src' --source='back/src' "$(mktemp)" \
    && coverage combine \
    && coverage report \
      --fail-under="${coverage_target}" \
      --precision=2 \
      "${coverage_args[@]}" \
    && coverage html "${coverage_args[@]}" -d build \
    && coverage xml "${coverage_args[@]}" \
    && if test "${CI_COMMIT_REF_NAME}" = trunk; then
      aws_login "dev" "3600" \
        && sops_export_vars __argSecretsDev__ CODECOV_TOKEN \
        && codecov -B integrates -C "${CI_COMMIT_SHA}" -F integrates
    fi \
    && popd \
    || return 1
}

main "${@}"
