# shellcheck shell=bash

alias migrate-tables="observes-service-migrate-tables-bin"

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
    && echo '[INFO] Running centralizer' \
    && dynamo-etl centralize main \
      --schema 'dynamodb' \
      --tables 'integrates_vms' \
      --parts-schema-prefix 'dynamodb_integrates_vms_part_' \
      --parts-loading-schema 'dynamodb_integrates_vms_merged_parts_loading'
}

dynamodb_centralize
