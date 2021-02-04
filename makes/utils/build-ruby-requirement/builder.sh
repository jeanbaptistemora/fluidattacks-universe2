# shellcheck shell=bash

function main {
  gem install \
    --no-document \
    --install-dir "${out}" \
    "${envRequirement}"
}

main "${@}"
