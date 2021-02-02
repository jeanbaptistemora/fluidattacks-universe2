# shellcheck shell=bash

source '__envUtilsBashLibAws__'

function clone_services_repository {
  export SERVICES_PROD_AWS_ACCESS_KEY_ID
  export SERVICES_PROD_AWS_SECRET_ACCESS_KEY
  local group="${1}"

      aws_login_prod 'services' \
  &&  CI='true' \
      CI_COMMIT_REF_NAME='master' \
      PROD_AWS_ACCESS_KEY_ID="${SERVICES_PROD_AWS_ACCESS_KEY_ID}" \
      PROD_AWS_SECRET_ACCESS_KEY="${SERVICES_PROD_AWS_SECRET_ACCESS_KEY}" \
      '__envMelts__' drills --pull-repos "${group}"
}

function list_subscriptions {
  local file

      file="$(mktemp)" \
  &&  ls -1 groups > "${file}" \
  &&  echo "${file}"
}

function forces_projects {
  local groups

      mapfile -t groups < "$(list_subscriptions)" \
  &&  '__envMelts__' misc --filter-groups-with-forces "${groups[*]}"
}
