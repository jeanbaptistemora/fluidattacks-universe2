# shellcheck shell=bash

function dynamodb_centralize {
  export AWS_DEFAULT_REGION="us-east-1"

  : \
    && aws_login "prod_observes" "3600" \
    && export_notifier_key \
    && echo '[INFO] Generating secret files' \
    && sops_export_vars 'observes/secrets/prod.yaml' \
      'REDSHIFT_DATABASE' \
      'REDSHIFT_HOST' \
      'REDSHIFT_PASSWORD' \
      'REDSHIFT_PORT' \
      'REDSHIFT_USER' \
    && echo '[INFO] Running centralizer final phase' \
    && dynamo-etl centralize dynamo-tables \
      --schema 'dynamodb' \
      --tables 'integrates_vms'
}

dynamodb_centralize
