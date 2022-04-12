# shellcheck shell=bash

alias gitlab-etl="observes-etl-gitlab"

function start_etl {
  local db_creds

  db_creds=$(mktemp) \
    && aws_login_prod 'observes' \
    && json_db_creds "${db_creds}" \
    && gitlab-etl \
      'gitlab-ci' \
      'fluidattacks/services' \
      's3://observes.state/gitlab_etl/services_state.json' \
      "${SERVICES_API_TOKEN}" \
      "${db_creds}"
}

start_etl
