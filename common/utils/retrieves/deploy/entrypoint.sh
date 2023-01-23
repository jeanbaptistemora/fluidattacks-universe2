# shellcheck shell=bash

function main {
  : && pushd common/utils/retrieves \
    && copy __argSetupRetrievesDevRuntime__ ./node_modules \
    && sops_export_vars __argSecretsProd__ "AZURE_ACCESS_TOKEN" \
    && ./node_modules/.bin/webpack-cli \
    && ./node_modules/.bin/webpack-cli \
      --mode production \
      --devtool hidden-source-map \
    && ./node_modules/.bin/vsce publish \
      -p "${AZURE_ACCESS_TOKEN}" \
      --allow-missing-repository \
      --skip-duplicate \
      minor \
    && popd \
    || return 1
}

main "$@"
