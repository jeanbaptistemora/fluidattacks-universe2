# shellcheck shell=bash

alias gitlab-etl="observes-etl-gitlab"

function start_etl {
  local db_creds

  db_creds=$(mktemp) \
    && source "__argSecretsAwsProd__/template" \
    && json_db_creds "${db_creds}" \
    && export_notifier_key \
    && ensure_gitlab_env_vars \
      SERVICES_API_TOKEN \
    && gitlab-etl \
      'gitlab-ci' \
      'fluidattacks/services' \
      's3://observes.state/gitlab_etl/services_state.json' \
      "${SERVICES_API_TOKEN}" \
      "${db_creds}"
}

start_etl
