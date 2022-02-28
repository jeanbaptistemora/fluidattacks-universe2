# shellcheck shell=bash

function main {
  source __argIntegratesBackEnv__/template dev \
    && mypy __argIntegratesPackage__
}

main "${@}"
