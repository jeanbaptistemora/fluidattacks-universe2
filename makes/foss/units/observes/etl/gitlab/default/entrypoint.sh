# shellcheck shell=bash

alias gitlab-etl="observes-etl-gitlab"

function start_etl {
  local db_creds

  db_creds=$(mktemp) \
    && aws_login_prod_new 'observes' \
    && sops_export_vars 'observes/secrets-prod.yaml' \
      analytics_auth_redshift \
    && echo "${analytics_auth_redshift}" > "${db_creds}" \
    && gitlab-etl \
      'gitlab-ci' \
      'autonomicmind/default' \
      's3://observes.state/gitlab_etl/default_state.json' \
      "${AUTONOMIC_API_TOKEN}" \
      "${db_creds}"
}

start_etl
