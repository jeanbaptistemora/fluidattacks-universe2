#!/usr/bin/env bash

analytics_sync_timedoctor() {

  # Sync analytics with formstack

  set -Eeuo pipefail

  # Import functions
  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/sops-source/sops.sh)
  . toolbox/others.sh

  aws_login

  sops_env secrets-production.yaml default \
    aws_s3_access_key \
    aws_s3_secret_key \
    aws_s3_default_region \
    analytics_s3_cache_timedoctor \
    analytics_auth_timedoctor \
    analytics_auth_redshift

  mkdir /logs
  pip3 install \
    boto3 \
    analytics/singer/tap_timedoctor \
    analytics/singer/target_redshift

  echo '{' > /s3_auth.json
  echo "\"AWS_ACCESS_KEY_ID\":\"$aws_s3_access_key\"," >> /s3_auth.json
  echo "\"AWS_SECRET_ACCESS_KEY\":\"$aws_s3_secret_key\"," >> /s3_auth.json
  echo "\"AWS_DEFAULT_REGION\":\"$aws_s3_default_region\"" >> /s3_auth.json
  echo '}' >> /s3_auth.json

  echo "$analytics_s3_cache_timedoctor" > /s3_files.json
  echo "$analytics_auth_timedoctor" > /tap_secret.json
  echo "$analytics_auth_redshift" > /target_secret.json

  python3 analytics/download_from_aws_sss.py -auth /s3_auth.json -conf /s3_files.json
  cat timedoctor.worklogs.2013-01-01.2018-12-31.singer > timedoctor.singer
  cat timedoctor.computer_activity.2018-01-01.2018-12-31.singer >> timedoctor.singer
  tap-timedoctor --auth /tap_secret.json >> timedoctor.singer
  cat timedoctor.singer | \
  target-redshift --auth /target_secret.json --drop-schema --schema-name 'timedoctor'
  rm -fr /s3_auth.json /s3_files.json /tap_secret.json /target_secret.json
}
