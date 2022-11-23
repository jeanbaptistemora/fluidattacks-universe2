# shellcheck shell=bash

function main {
  aws_login "prod_integrates" "3600" \
    && source __argIntegratesBackEnv__/template "prod" \
    && pushd '__argIntegratesSrc__' \
    && celery \
      -A server \
      worker \
      -l INFO \
    && popd || return
}

main "${@}"
