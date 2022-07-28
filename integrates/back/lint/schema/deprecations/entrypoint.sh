# shellcheck shell=bash

function main {

  source __argIntegratesBackEnv__/template dev \
    && pushd integrates \
    && python back/lint/schema/deprecations/lint_schema.py \
    && popd \
    || return 1
}

main "${@}"
