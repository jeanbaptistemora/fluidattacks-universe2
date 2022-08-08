# shellcheck shell=bash

alias migrate-tables="observes-service-migrate-tables-bin"

function dynamodb_centralize {
  export AWS_DEFAULT_REGION="us-east-1"
  : \
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
      --schema 'dynamodb' \
    && dynamo-etl centralize parts \
      --schema-prefix 'dynamodb_integrates_vms_part_' \
      --schema 'dynamodb_integrates_vms_loading'
}

dynamodb_centralize
