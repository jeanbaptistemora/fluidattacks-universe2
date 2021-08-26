# shellcheck shell=bash

function main {
  pushd "${envGraphsSrc}" \
    && eslint --config .eslintrc . \
    && popd \
    && touch "${out}" \
    || return 1
}

main "${@}"
