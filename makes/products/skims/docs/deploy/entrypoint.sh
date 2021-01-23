# shellcheck shell=bash

source '__envUtilsBashLibAws__'

function main {
  local source='__envSkimsDocsBuild__'
  local target='s3://fluidattacks.com/resources/doc/skims'

      aws_login_prod 'skims' \
  &&  aws_s3_sync "${source}" "${target}" --delete
}

main "${@}"
