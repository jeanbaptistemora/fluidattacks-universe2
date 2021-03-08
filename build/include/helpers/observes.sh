# shellcheck shell=bash

function helper_observes_aws_login {
  local user="${1}"
  export AWS_ACCESS_KEY_ID
  export AWS_DEFAULT_REGION='us-east-1'
  export AWS_SECRET_ACCESS_KEY


      if [ "${user}" = 'dev' ]
      then
            AWS_ACCESS_KEY_ID="${OBSERVES_DEV_AWS_ACCESS_KEY_ID}" \
        &&  AWS_SECRET_ACCESS_KEY="${OBSERVES_DEV_AWS_SECRET_ACCESS_KEY}"
      elif [ "${user}" = 'prod' ]
      then
            AWS_ACCESS_KEY_ID="${OBSERVES_PROD_AWS_ACCESS_KEY_ID}" \
        &&  AWS_SECRET_ACCESS_KEY="${OBSERVES_PROD_AWS_SECRET_ACCESS_KEY}"
      else
            echo '[ERROR] either prod or dev must be passed as arg' \
        &&  return 1
      fi \
  &&  echo "[INFO] Logging into Observes AWS with ${user} credentials" \
  &&  aws configure set aws_access_key_id "${AWS_ACCESS_KEY_ID}" \
  &&  aws configure set aws_secret_access_key "${AWS_SECRET_ACCESS_KEY}"
}

function helper_observes_gitlab {
  export GITLAB_API_TOKEN
  helper_common_get_projects

      helper_observes_aws_login prod \
  &&  helper_common_sops_env observes/secrets-prod.yaml default \
        analytics_auth_redshift \
  &&  echo '[INFO] Generating secret files' \
  &&  echo "${analytics_auth_redshift}" > "${TEMP_FILE2}" \
  &&  dif-gitlab-etl start-etl "${PROJECTS[@]}" "${TEMP_FILE2}"
}

function helper_observes_timedoctor {
  export analytics_auth_timedoctor

      helper_observes_aws_login prod \
  &&  mkdir ./logs \
  &&  helper_common_sops_env observes/secrets-prod.yaml default \
        analytics_auth_redshift \
        analytics_s3_cache_timedoctor \
  &&  analytics_auth_timedoctor=$( \
        helper_common_get_gitlab_var \
          'analytics_auth_timedoctor' \
          "${GITLAB_API_TOKEN}") \
  &&  echo '[INFO] Generating secret files' \
  &&  echo "${analytics_s3_cache_timedoctor}" > ./s3_files.json \
  &&  echo "${analytics_auth_timedoctor}" > "${TEMP_FILE1}" \
  &&  echo "${analytics_auth_redshift}" > "${TEMP_FILE2}" \
  &&  echo '[INFO] Downloading backups from S3' \
  &&  bucket="$(< s3_files.json jq -r '.bucket_name')" \
  &&  cont_folder=$(< s3_files.json jq -r '.folder_name') \
  &&  new_folder=$(< s3_files.json jq -r '.save_as') \
  &&  aws s3 cp --recursive "s3://${bucket}/${cont_folder}/" "${new_folder}/" \
  &&  cat "${new_folder}"/* \
        > .singer \
  &&  echo '[INFO] Running tap' \
  &&  tap-timedoctor \
        --auth "${TEMP_FILE1}" \
        --start-date "$(date +"%Y-%m-01")" \
        --end-date "$(date +"%Y-%m-%d")" \
        --work-logs \
        --computer-activity \
        >> .singer \
  &&  echo '[INFO] Running target' \
  &&  target-redshift \
        --auth "${TEMP_FILE2}" \
        --drop-schema \
        --schema-name 'timedoctor' \
        < .singer
}

function helper_observes_zoho {
  local analytics_zoho_tables=(
    Candidates
    Periods
  )

      helper_observes_aws_login prod \
  &&  helper_common_sops_env observes/secrets-prod.yaml default \
        analytics_zoho_email \
        analytics_zoho_token \
        analytics_zoho_space \
        analytics_auth_redshift \
  &&  echo '[INFO] Generating secret files' \
  &&  echo "${analytics_auth_redshift}" > "${TEMP_FILE2}" \
  &&  echo '[INFO] Running converter and streamer' \
  &&  for table in "${analytics_zoho_tables[@]}"
      do
            echo "  [INFO] Table: ${table}" \
        &&  ./observes/singer/converter_zoho_csv.py \
              --email "${analytics_zoho_email}" \
              --token "${analytics_zoho_token}" \
              --space "${analytics_zoho_space}" \
              --table "${table}" \
              --target "${table}" \
        &&  ./observes/singer/streamer_csv.py "${table}" \
              >> .jsonstream \
        || return 1
      done \
  &&  echo '[INFO] Running tap' \
  &&  tap-json  \
        --date-formats '%Y-%m-%d %H:%M:%S' \
        > .singer \
        < .jsonstream \
  &&  echo '[INFO] Running target' \
  &&  target-redshift \
        --auth "${TEMP_FILE2}" \
        --drop-schema \
        --schema-name 'zoho' \
        < .singer
}

function helper_observes_zoho_crm_prepare {
      helper_observes_aws_login prod \
  &&  helper_common_sops_env observes/secrets-prod.yaml default \
        analytics_auth_redshift \
        zoho_crm_bulk_creator_creds \
  &&  echo '[INFO] Generating secret files' \
  &&  echo "${zoho_crm_bulk_creator_creds}" > "${TEMP_FILE1}" \
  &&  echo "${analytics_auth_redshift}" > "${TEMP_FILE2}" \
  &&  streamer-zoho-crm init-db "${TEMP_FILE2}" \
  &&  streamer-zoho-crm create-jobs "${TEMP_FILE1}" "${TEMP_FILE2}"
}

function helper_observes_zoho_crm {
      helper_observes_aws_login prod \
  &&  helper_common_sops_env observes/secrets-prod.yaml default \
        analytics_auth_redshift \
        zoho_crm_etl_creds \
  &&  echo '[INFO] Generating secret files' \
  &&  echo "${zoho_crm_etl_creds}" > "${TEMP_FILE1}" \
  &&  echo "${analytics_auth_redshift}" > "${TEMP_FILE2}" \
  &&  streamer-zoho-crm stream "${TEMP_FILE1}" "${TEMP_FILE2}" \
        | tap-csv | tap-json > .singer \
  &&  target-redshift \
        --auth "${TEMP_FILE2}" \
        --schema-name 'zoho_crm' \
        --drop-schema \
        < .singer
}

function helper_observes_timedoctor_refresh_token {
  export analytics_auth_timedoctor

      helper_observes_aws_login prod \
  &&  analytics_auth_timedoctor=$( \
        helper_common_get_gitlab_var \
          'analytics_auth_timedoctor' \
          "${GITLAB_API_TOKEN}") \
  &&  echo '[INFO] Updating token...' \
  &&  ./observes/services/timedoctor_tokens/timedoctor_tokens/__init__.py --timedoctor-refresh \
  &&  echo '[INFO] Done! Token created for current project'
}

function helper_observes_timedoctor_manually_create_token {
      helper_observes_aws_login prod \
  &&  helper_common_sops_env observes/secrets-prod.yaml default \
        analytics_auth_timedoctor \
  &&  echo '[INFO] Executing creator, follow the steps' \
  &&  ./observes/services/timedoctor_tokens/timedoctor_tokens/__init__.py --timedoctor-start \
  &&  echo '[INFO] Done! Token created at GitLab/production env vars'
}
