# shellcheck shell=bash

alias gitlab-etl="observes-etl-gitlab"

function start_etl {
  local db_creds

  db_creds=$(mktemp) \
    && aws_login_prod 'observes' \
    && db_creds_legacy "${db_creds}" \
    && gitlab-etl \
      'gitlab-ci' \
      'autonomicjump/challenges' \
      's3://observes.state/gitlab_etl/challenges_state.json' \
      "${AUTONOMIC_API_TOKEN}" \
      "${db_creds}"
}

start_etl
