# shellcheck shell=bash

function main {
  local coverage_args=(
    --omit="back/migrations/*"
    --skip-empty
    -i
  )
  pushd integrates \
    && ls -al \
    && coverage combine \
    && coverage report "${coverage_args[@]}" \
    && coverage html "${coverage_args[@]}" -d build \
    && mv .coverage .coverage."functional_${1}" \
    && popd \
    || return 1
}

main "${@}"
