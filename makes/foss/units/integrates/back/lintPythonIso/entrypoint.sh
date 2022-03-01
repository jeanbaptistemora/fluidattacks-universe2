# shellcheck shell=bash

function main {
  source __argIntegratesBackEnv__/template dev \
    && mypy --config-file __argSettingsMypy__ __argIntegratesPackage__
}

main "${@}"
