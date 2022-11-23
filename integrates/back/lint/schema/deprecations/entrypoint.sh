# shellcheck shell=bash

function main {

  source __argIntegratesBackEnv__/template dev \
    && pushd integrates \
    && info "Linting schema deprecations..." \
    && python back/lint/schema/deprecations/lint_schema.py \
    && popd \
    || return 1
}

main "${@}"
