# shellcheck shell=bash

function main {
  pushd "${envSrc}" \
    && eslint --config .eslintrc . \
    && popd \
    && touch "${out}" \
    || return 1
}

main "${@}"
