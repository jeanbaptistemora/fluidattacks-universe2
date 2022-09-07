# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function main {
  copy __argAirsFront__ out \
    && aws_login "dev" "3600" \
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
