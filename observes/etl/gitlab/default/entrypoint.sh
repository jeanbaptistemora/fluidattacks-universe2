# shellcheck shell=bash

alias gitlab-etl="observes-etl-gitlab"

function start_etl {
  local db_creds

  db_creds=$(mktemp) \
    && aws_login_prod 'observes' \
    && json_db_creds "${db_creds}" \
    && export_notifier_key \
    && ensure_gitlab_env_vars \
      AUTONOMIC_API_TOKEN \
    && gitlab-etl \
      'gitlab-ci' \
      'autonomicmind/default' \
      's3://observes.state/gitlab_etl/default_state.json' \
      "${AUTONOMIC_API_TOKEN}" \
      "${db_creds}"
}

start_etl
