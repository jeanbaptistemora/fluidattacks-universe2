# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

alias tap-json="observes-singer-tap-json-bin"
alias target-redshift="observes-target-redshift"

function start_etl {
  local db_creds

  db_creds=$(mktemp) \
    && aws_login "prod_observes" "3600" \
    && sops_export_vars 'observes/secrets/prod.yaml' \
      checkly_api_user \
      checkly_api_key \
      bugsnag_notifier_key \
    && echo '[INFO] Generating secret files' \
    && json_db_creds "${db_creds}" \
    && echo '[INFO] Running tap' \
    && tap-checkly stream \
      --api-user "${checkly_api_user}" \
      --api-key "${checkly_api_key}" \
      --all-streams \
    | tap-json \
      > .singer \
    && echo '[INFO] Running target' \
    && target-redshift \
      --auth "${db_creds}" \
      --drop-schema \
      --schema-name 'checkly' \
      < .singer \
    && job-last-success single-job \
      --auth "${db_creds}" \
      --job 'checkly'
}

start_etl
