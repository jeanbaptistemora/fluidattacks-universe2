#! __envShell__
# shellcheck shell=bash

source '__makeEntrypoint__'

function main {
  local source='__envSkimsDocsBuild__'
  local target='s3://fluidattacks.com/resources/doc/skims'

  '__envAwscli__' s3 sync --delete "${source}" "${target}"
}

main "${@}"
