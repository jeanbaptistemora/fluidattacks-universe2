# shellcheck shell=bash

function main {
      source __envIntegratesEnv__ dev \
  &&  pushd integrates \
    &&  python3 deploy/permissions-matrix/matrix.py \
  &&  popd \
  ||  return 1
}

main "${@}"
