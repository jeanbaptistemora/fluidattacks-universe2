#!/usr/bin/env bash

analytics_sync_infrastructure() {

  # Sync analytics with formstack

  set -Eeuo pipefail

  # Import functions
  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/sops-source/sops.sh)
  . toolbox/others.sh

  aws_login

  sops_env secrets-production.yaml default \
    analytics_auth_ms_sql_server_erp \
    analytics_auth_redshift

  pip3 install \
    pyodbc \
    analytics/singer/tap_json \
    analytics/singer/target_redshift

  echo "$analytics_auth_ms_sql_server_erp" > /convert_secret.json
  mkdir csv
  analytics/singer/converter_mssqlserver_csv.py \
    --auth /convert_secret.json --output-dir csv

  for csv_path in csv/*.csv; do
    echo "$csv_path";
    analytics/singer/streamer_csv.py "$csv_path" >> .jsonstream;
  done

  cat .jsonstream | tap-json > .singer
  echo "$analytics_auth_redshift" > /target_secret.json
  cat .singer | \
    target-redshift --auth /target_secret.json --drop-schema --schema-name 'erp'
  rm -rf /convert_secret.json /target_secret.json
}

analytics_sync_infrastructure
