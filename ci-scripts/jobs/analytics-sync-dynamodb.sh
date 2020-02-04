#!/usr/bin/env bash

analytics_sync_dynamodb() {

  # Sync analytics with dynamodb

  set -Eeuo pipefail

  # Import functions
  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/sops.sh)
  . toolbox/others.sh

  aws_login

  sops_env secrets-prod.yaml default \
    aws_dynamodb_access_key \
    aws_dynamodb_secret_key \
    aws_dynamodb_default_region \
    analytics_auth_redshift

  mkdir /logs
  pip3 install \
    analytics/singer/tap_awsdynamodb \
    analytics/singer/target_redshift

  echo '{' > /tap_secret.json
  echo "\"AWS_ACCESS_KEY_ID\":\"$aws_dynamodb_access_key\"," >> /tap_secret.json
  echo "\"AWS_SECRET_ACCESS_KEY\":\"$aws_dynamodb_secret_key\"," >> /tap_secret.json
  echo "\"AWS_DEFAULT_REGION\":\"$aws_dynamodb_default_region\"" >> /tap_secret.json
  echo '}' >> /tap_secret.json

  echo "$analytics_auth_redshift" > /target_secret.json

  tap-awsdynamodb \
    --auth /tap_secret.json --conf analytics/conf/awsdynamodb.json > .singer

  cat .singer | \
    target-redshift \
    --auth /target_secret.json --drop-schema --schema-name 'dynamodb'

  rm -rf /tap_secret.json /target_secret.json
}

analytics_sync_dynamodb
