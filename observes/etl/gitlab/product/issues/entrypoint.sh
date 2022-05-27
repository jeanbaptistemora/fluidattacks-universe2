# shellcheck shell=bash

alias gitlab-etl="observes-etl-gitlab-issues"

function start_etl {
  local db_creds

  db_creds=$(mktemp) \
    && aws_login_prod 'observes' \
    && json_db_creds "${db_creds}" \
    && export_notifier_key \
    && gitlab-etl \
      'gitlab_ci_issues' \
      'fluidattacks/product' \
      "${PRODUCT_API_TOKEN}" \
      "${db_creds}"
}

start_etl
