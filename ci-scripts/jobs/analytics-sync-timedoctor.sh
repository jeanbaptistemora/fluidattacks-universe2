#!/usr/bin/env bash

analytics_sync_timedoctor() {

  # Sync analytics with Timedoctor

  set -Eeuo pipefail

  # Import functions
  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/sops-source/sops.sh)
  . toolbox/others.sh

  aws_login

  sops_env secrets-production.yaml default \
    analytics_auth_formstack \
    analytics_auth_redshift

  mkdir /logs
  ./analytics/set-aws-cli.sh
  pip3 install \
    analytics/singer/tap_formstack \
    analytics/singer/target_redshift

  echo "$analytics_auth_formstack" > /tap_secret.json
  echo "$analytics_auth_redshift" > /target_secret.json

  tap-formstack \
    --auth /tap_secret.json --conf analytics/conf/formstack.json > .singer

  cat .singer | \
    target-redshift \
    --auth /target_secret.json --drop-schema --schema-name 'formstack'

  aws s3 cp /logs s3://fluidanalytics/formstack --recursive
  rm -fr /tap_secret.json /target_secret.json ~/.aws
}

analytics_sync_timedoctor
