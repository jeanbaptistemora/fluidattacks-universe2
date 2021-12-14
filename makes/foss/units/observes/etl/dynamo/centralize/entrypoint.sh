# shellcheck shell=bash

alias migrate-tables="observes-service-migrate-tables-bin"

function dynamodb_centralize {
  local db_creds

  db_creds="$(mktemp)" \
    && aws_login_prod_new 'observes' \
    && sops_export_vars 'observes/secrets-prod.yaml' \
      analytics_auth_redshift \
    && echo '[INFO] Generating secret files' \
    && echo "${analytics_auth_redshift}" > "${db_creds}" \
    && echo '[INFO] Running centralizer' \
    && migrate-tables centralize-dynamo-schemas \
      --db-auth "${db_creds}" \
      --dymo-tables './observes/conf/awsdynamodb.json' \
      --schema 'dynamodb'
}

dynamodb_centralize
