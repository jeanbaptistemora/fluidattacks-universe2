# shellcheck shell=bash

function main {
  local out='docs/src/build'
  local bucket
  local env="${1}"
  local branch="${2:-default}"

  case "${env}" in
    prod)
      bucket='s3://docs.fluidattacks.com/'
      ;;
    dev)
      bucket="s3://docs-dev.fluidattacks.com/${branch}/"
      ;;
    *) error 'Either "prod" or "dev" must be passed as arg' ;;
  esac \
    && docs build "${env}" "${branch}" \
    && aws s3 sync "${out}" "${bucket}" --delete
}

main "${@}"
