# shellcheck shell=bash

alias migrate-tables="observes-service-migrate-tables-bin"

function dynamodb_centralize {
  aws_login_prod 'observes' \
    && export_notifier_key \
    && echo '[INFO] Generating secret files' \
    && sops_export_vars 'observes/secrets/prod.yaml' \
      'REDSHIFT_DATABASE' \
      'REDSHIFT_HOST' \
      'REDSHIFT_PASSWORD' \
      'REDSHIFT_PORT' \
      'REDSHIFT_USER' \
    && echo '[INFO] Running centralizer' \
    && dynamo-etl centralize dynamo-tables \
      --tables './observes/conf/awsdynamodb.json' \
      --schema 'dynamodb'
}

dynamodb_centralize
