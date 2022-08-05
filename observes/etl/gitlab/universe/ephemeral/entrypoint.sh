# shellcheck shell=bash

alias gitlab-etl="observes-etl-gitlab-ephemeral"

function start_etl {
  local db_creds

  db_creds=$(mktemp) \
    && json_db_creds "${db_creds}" \
    && export_notifier_key \
    && gitlab-etl \
      'gitlab_ci_issues' \
      'fluidattacks/universe' \
      "${UNIVERSE_API_TOKEN}" \
      "${db_creds}"
}

start_etl
