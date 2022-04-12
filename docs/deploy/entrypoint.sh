# shellcheck shell=bash

function main {
  local out='docs/src/build'
  local bucket
  local secrets_aws
  local env="${1}"
  local branch="${2:-default}"

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
    && docs build "${env}" "${branch}" \
    && source "${secrets_aws}/template" \
    && aws s3 sync "${out}" "${bucket}" --delete
}

main "${@}"
