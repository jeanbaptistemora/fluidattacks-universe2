# shellcheck shell=bash

function main {
  copy "${envAirsFront}" front \
    && pushd front \
    && copy "${envAirsNpm}" 'node_modules' \
    && HOME=. ./node_modules/.bin/stylelint '**/*.scss' \
    && popd \
    && touch "${out}" \
    || return 1
}

main "${@}"
