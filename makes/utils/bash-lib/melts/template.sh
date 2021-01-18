# shellcheck shell=bash

function clone_services_repository {
  export SERVICES_PROD_AWS_ACCESS_KEY_ID
  export SERVICES_PROD_AWS_SECRET_ACCESS_KEY
  local group="${1}"

  CI='true' \
  CI_COMMIT_REF_NAME='master' \
  PROD_AWS_ACCESS_KEY_ID="${SERVICES_PROD_AWS_ACCESS_KEY_ID}" \
  PROD_AWS_SECRET_ACCESS_KEY="${SERVICES_PROD_AWS_SECRET_ACCESS_KEY}" \
  '__envMelts__' drills --pull-repos "${group}"
}
