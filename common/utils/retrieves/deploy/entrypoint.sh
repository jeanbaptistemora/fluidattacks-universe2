# shellcheck shell=bash

function main {
  : && pushd common/utils/retrieves \
    && copy __argSetupRetrievesDevRuntime__ ./node_modules \
    && aws_login "prod_common" "3600" \
    && sops_export_vars __argSecretsProd__ "AZURE_ACCESS_TOKEN" \
    && ./node_modules/.bin/rimraf dist \
    && ./node_modules/.bin/webpack-cli --mode production --config ./webpack/extension.config.js \
    && ./node_modules/.bin/webpack-cli --mode production --config ./webpack/webview.config.js \
    && ./node_modules/.bin/vsce publish \
      -p "${AZURE_ACCESS_TOKEN}" \
      --allow-missing-repository \
      --skip-duplicate \
      minor \
    && popd \
    || return 1
}

main "$@"
