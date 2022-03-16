# shellcheck shell=bash

function main {
  pushd integrates \
    && ls -al \
    && coverage combine \
    && coverage report -i \
    && coverage html -i -d build \
    && mv .coverage .coverage."functional_${1}" \
    && popd \
    || return 1
}

main "${@}"
