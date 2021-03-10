# shellcheck shell=bash

function start_etl {
  local db_creds
  local projects

      projects=(
        'autonomicmind/default'
        'autonomicmind/challenges'
        'fluidattacks/services'
        'fluidattacks/product'
      ) \
  &&  db_creds=$(mktemp) \
  &&  aws_login_prod 'observes' \
  &&  sops_export_vars 'observes/secrets-prod.yaml' \
        analytics_auth_redshift \
  &&  echo '[INFO] Generating secret files' \
  &&  echo "${analytics_auth_redshift}" > "${db_creds}" \
  &&  observes-bin-dif-gitlab-etl start-etl "${projects[@]}" "${db_creds}"
}

start_etl
