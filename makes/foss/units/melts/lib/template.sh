# shellcheck shell=bash

function clone_services_repository {
  export PROD_SERVICES_AWS_ACCESS_KEY_ID
  export PROD_SERVICES_AWS_SECRET_ACCESS_KEY
  local group="${1}"

  aws_login_prod 'services' \
    && CI='true' \
      CI_COMMIT_REF_NAME='master' \
      PROD_AWS_ACCESS_KEY_ID="${PROD_SERVICES_AWS_ACCESS_KEY_ID}" \
      PROD_AWS_SECRET_ACCESS_KEY="${PROD_SERVICES_AWS_SECRET_ACCESS_KEY}" \
      melts drills --pull-repos "${group}"
}

function list_subscriptions {
  local file

  use_git_repo_services >&2 \
    && file="$(mktemp)" \
    && ls -1 groups > "${file}" \
    && popd 1>&2 \
    && echo "${file}"
}

function forces_projects {
  local groups

  mapfile -t groups < "$(list_subscriptions)" \
    && use_git_repo_services >&2 \
    && melts misc --filter-groups-with-forces "${groups[*]}" \
    && popd >&2 \
    || return 1
}

function projects_with_forces {
  melts misc --groups-with-forces
}

function get_forces_token {
  local group="${1}"

  melts misc --get-forces-token "${group}"
}
