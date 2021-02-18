# shellcheck shell=bash

function dynamodb_centralize {
  local db_creds

      db_creds="$(mktemp)" \
  &&  aws_login_prod 'observes' \
  &&  sops_export_vars 'observes/secrets-prod.yaml' \
        analytics_auth_redshift \
  &&  echo '[INFO] Generating secret files' \
  &&  echo "${analytics_auth_redshift}" > "${db_creds}" \
  &&  echo '[INFO] Running centralizer' \
  &&  observes-service-migrate-tables centralize-dynamo-schemas \
        --db-auth "${db_creds}" \
        --dymo-tables './observes/conf/awsdynamodb.json' \
        --schema 'dynamodb'
}

dynamodb_centralize
