# shellcheck shell=bash

function main {
  local coverage_args=(
    --ignore-errors
  )
  pushd skims \
    && coverage combine \
    && coverage report "${coverage_args[@]}" \
    && coverage html "${coverage_args[@]}" -d build \
    && coverage xml "${coverage_args[@]}" \
    && mv .coverage .coverage."combine_${1}" \
    && popd \
    || return 1
}

main "${@}"
