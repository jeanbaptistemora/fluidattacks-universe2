# shellcheck shell=bash

function main {
  local out='docs/src/build'
  local bucket
  local aws_role
  local env="${1}"
  local branch="${2:-default}"

  case "${env}" in
    prod)
      bucket='s3://docs.fluidattacks.com/' \
        && aws_role="prod_docs"
      ;;
    dev)
      bucket="s3://docs-dev.fluidattacks.com/${branch}/" \
        && aws_role="dev"
      ;;
    *) error 'Either "prod" or "dev" must be passed as arg' ;;
  esac \
    && docs build "${env}" "${branch}" \
    && aws_login "${aws_role}" "3600" \
    && aws s3 sync "${out}" "${bucket}" \
    && aws s3 sync "${out}" "${bucket}" --delete
}

main "${@}"
