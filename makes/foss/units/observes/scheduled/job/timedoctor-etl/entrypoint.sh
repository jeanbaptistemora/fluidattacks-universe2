# shellcheck shell=bash

alias tap-timedoctor="observes-singer-tap-timedoctor-bin"
alias target-redshift="observes-target-redshift"
alias job-last-success="observes-service-job-last-success-bin"

function job_timedoctor {
  local db_creds
  local timedoctor_creds
  export OBSERVES_DEBUG="true"

  db_creds=$(mktemp) \
    && timedoctor_creds=$(mktemp) \
    && mkdir ./logs \
    && aws_login_prod 'observes' \
    && sops_export_vars 'observes/secrets-prod.yaml' \
      analytics_auth_redshift \
      analytics_s3_cache_timedoctor \
    && analytics_auth_timedoctor=$(
      get_project_variable \
        "${PRODUCT_API_TOKEN}" \
        "${CI_PROJECT_ID}" \
        "analytics_auth_timedoctor"
    ) \
    && echo '[INFO] Generating secret files' \
    && echo "${analytics_s3_cache_timedoctor}" > ./s3_files.json \
    && echo "${analytics_auth_timedoctor}" > "${timedoctor_creds}" \
    && echo "${analytics_auth_redshift}" > "${db_creds}" \
    && echo '[INFO] Downloading backups from S3' \
    && bucket="$(jq < s3_files.json -r '.bucket_name')" \
    && cont_folder=$(jq < s3_files.json -r '.folder_name') \
    && new_folder=$(jq < s3_files.json -r '.save_as') \
    && aws_s3_sync "s3://${bucket}/${cont_folder}/" "${new_folder}/" \
    && cat "${new_folder}"/* \
      > .singer \
    && echo '[INFO] Running tap' \
    && tap-timedoctor \
      --auth "${timedoctor_creds}" \
      --start-date "$(date +"%Y-%m-01")" \
      --end-date "$(date +"%Y-%m-%d")" \
      --work-logs \
      --computer-activity \
      >> .singer \
    && echo '[INFO] Running target' \
    && target-redshift \
      --auth "${db_creds}" \
      --drop-schema \
      --schema-name 'timedoctor' \
      < .singer \
    && job-last-success single-job \
      --auth "${db_creds}" \
      --job 'timedoctor_etl'
}

job_timedoctor
