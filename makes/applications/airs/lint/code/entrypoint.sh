# shellcheck shell=bash

function main {
  copy __envAirsFront__ out \
    && aws_login_dev_new \
    && sops_export_vars __envAirsSecrets__/dev.yaml \
      FONTAWESOME_NPM_AUTH_TOKEN \
    && pushd out \
    && copy __envAirsNpm__ 'node_modules' \
    && install_scripts \
    && install_fontawesome_pro "" \
    && ./node_modules/.bin/tsc --noEmit -p tsconfig.json \
    && lint_typescript "$(pwd)" "$(pwd)" \
    && popd \
    && rm -rf out/ \
    || return 1
}

main "${@}"
