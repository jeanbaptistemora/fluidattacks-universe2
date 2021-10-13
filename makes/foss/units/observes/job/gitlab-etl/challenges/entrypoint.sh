# shellcheck shell=bash

alias gitlab-etl="observes-job-gitlab-etl"

function start_etl {
  local db_creds

  db_creds=$(mktemp) \
    && aws_login_prod 'observes' \
    && sops_export_vars 'observes/secrets-prod.yaml' \
      analytics_auth_redshift \
    && echo "${analytics_auth_redshift}" > "${db_creds}" \
    && gitlab-etl \
      'gitlab-ci' \
      'autonomicjump/challenges' \
      's3://observes.state/gitlab_etl/challenges_state.json' \
      "${AUTONOMIC_API_TOKEN}" \
      "${db_creds}"
}

start_etl
