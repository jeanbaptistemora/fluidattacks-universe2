# shellcheck shell=bash

function main {
  local src='docs/src'
  local bucket
  local secrets_aws
  export env="${1}"
  export branch="${2:-default}"

  case "${env}" in
    prod)
      bucket='s3://docs.fluidattacks.com/'
      secrets_aws="__argSecretsAwsProd__"
      ;;
    dev)
      bucket="s3://docs-dev.fluidattacks.com/${branch}/"
      secrets_aws="__argSecretsAwsDev__"
      ;;
    *) error 'Either "prod" or "dev" must be passed as arg' ;;
  esac \
    && pushd "${src}" \
    && source "${secrets_aws}/template" \
    && rm -rf node_modules build .docusaurus \
    && copy "__argNodeModules__" node_modules \
    && npm run build \
    && aws s3 sync build "${bucket}" --delete \
    && popd \
    || return 1
}

main "${@}"
