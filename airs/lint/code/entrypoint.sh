# shellcheck shell=bash

function main {
  copy __argAirsFront__ out \
    && sops_export_vars __argAirsSecrets__/dev.yaml \
    && pushd out \
    && copy __argAirsNpm__ 'node_modules' \
    && install_scripts \
    && ./node_modules/.bin/tsc --noEmit -p tsconfig.json \
    && lint_typescript "$(pwd)" "$(pwd)" \
    && popd \
    && rm -rf out/ \
    || return 1
}

main "${@}"
