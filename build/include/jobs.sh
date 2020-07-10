# shellcheck shell=bash

source "${srcIncludeHelpers}"
source "${srcExternalGitlabVariables}"
source "${srcExternalSops}"
source "${srcDotDotToolboxOthers}"

function job_services_repositories_cache {
  local mock_integrates_api_token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.xxx'

      aws_login \
  &&  helper_move_artifacts_to_git \
  &&  sops_env secrets-prod.yaml default \
        analytics_gitlab_user \
        analytics_gitlab_token \
  &&  echo '[INFO] Cloning our own repositories' \
  &&  python3 analytics/git/clone_us.py \
  &&  echo '[INFO] Cloning customer repositories' \
  &&  \
      CI=true \
      CI_COMMIT_REF_NAME='master' \
      INTEGRATES_API_TOKEN="${mock_integrates_api_token}" \
      PROD_AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" \
      PROD_AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" \
      python3 analytics/git/clone_them.py \
  &&  helper_move_services_fusion_to_master_git \
  &&  echo '[INFO] Generating stats' \
  &&  { python3 analytics/git/generate_stats.py || true; } \
  &&  helper_move_git_to_artifacts \

}

function job_analytics_git__process {
  local artifacts="${PWD}/artifacts"
  local mock_integrates_api_token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.xxx'
  local num_threads='4'
  export CI_NODE_INDEX
  export CI_NODE_TOTAL

      echo '[INFO] Exporting secrets' \
  &&  sops_env secrets-prod.yaml default \
        analytics_gitlab_user \
        analytics_gitlab_token \
  &&  echo '[INFO] Cloning our own repositories' \
  &&  python3 analytics/git/clone_us.py \
  &&  echo "[INFO] Generating config: ${CI_NODE_INDEX} / ${CI_NODE_TOTAL}" \
  &&  \
      CI=true \
      CI_COMMIT_REF_NAME='master' \
      INTEGRATES_API_TOKEN="${mock_integrates_api_token}" \
      PROD_AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" \
      PROD_AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" \
      python3 analytics/git/generate_config.py \
  &&  mkdir -p "${artifacts}" \
  &&  echo "[INFO] Running tap in ${num_threads} threads" \
  &&  for fork in $(seq 1 "${num_threads}")
      do
        ( tap-git \
            --conf './config.json' \
            --with-metrics \
            --threads "${num_threads}" \
            --fork-id "${fork}" > "${artifacts}/git.${CI_NODE_INDEX}.${fork}" \
        ) &
      done \
  &&  wait \

}

function job_analytics_git__upload {
  local artifacts="${PWD}/artifacts"

      aws_login \
  &&  sops_env secrets-prod.yaml default \
        analytics_auth_redshift \
  &&  echo '[INFO] Generating secret files' \
  &&  echo "${analytics_auth_redshift}" > "${TEMP_FILE1}" \
  &&  echo '[INFO] Running target' \
  &&  cat "${artifacts}/git."* \
        | target-redshift \
            --auth "${TEMP_FILE1}" \
            --drop-schema \
            --schema-name "git" \

}

function job_analytics_timedoctor_manually_create_token {
      aws_login \
  &&  sops_env secrets-prod.yaml default \
        analytics_auth_timedoctor \
        analytics_gitlab_token \
  &&  echo '[INFO] Executing creator, follow the steps' \
  &&  ./analytics/auth_helper.py --timedoctor-start \
  &&  echo '[INFO] Done! Token created at GitLab/serves env vars'
}

function job_analytics_timedoctor_refresh_token {
  export analytics_auth_timedoctor

      aws_login \
  &&  sops_env secrets-prod.yaml default \
        analytics_gitlab_token \
  &&  analytics_auth_timedoctor=$( \
        helper_get_gitlab_var \
          'analytics_auth_timedoctor' \
          "${analytics_gitlab_token}") \
  &&  echo '[INFO] Updating token...' \
  &&  ./analytics/auth_helper.py --timedoctor-refresh \
  &&  echo '[INFO] Done! Token created at GitLab/serves env vars'
}

function job_analytics_timedoctor {
  export analytics_auth_timedoctor

      aws_login \
  &&  mkdir ./logs \
  &&  sops_env secrets-prod.yaml default \
        analytics_auth_redshift \
        analytics_gitlab_token \
        analytics_s3_cache_timedoctor \
  &&  analytics_auth_timedoctor=$( \
        helper_get_gitlab_var \
          'analytics_auth_timedoctor' \
          "${analytics_gitlab_token}") \
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

function job_backup_analytics_timedoctor {
  export analytics_auth_timedoctor

      aws_login \
  &&  mkdir ./logs \
  &&  sops_env secrets-prod.yaml default \
        analytics_gitlab_token \
        analytics_s3_cache_timedoctor \
  &&  analytics_auth_timedoctor=$( \
        helper_get_gitlab_var \
          'analytics_auth_timedoctor' \
          "${analytics_gitlab_token}") \
  &&  echo '[INFO] Generating secret files' \
  &&  echo "${analytics_s3_cache_timedoctor}" > ./s3_files.json \
  &&  echo "${analytics_auth_timedoctor}" > "${TEMP_FILE2}" \
  &&  echo '[INFO] Running tap for worklogs' \
  &&  start_date=$(date -d "$(date +%m)/1 -1 month" "+%Y-%m-%d") \
  &&  end_date=$(date -d "$(date +%m)/1 +0 month - 1 day" "+%Y-%m-%d") \
  &&  tap-timedoctor \
        --auth "${TEMP_FILE2}" \
        --start-date "${start_date}" \
        --end-date "${end_date}" \
        --work-logs \
        > wl.singer \
  &&  echo '[INFO] Running tap for computer_activity' \
  &&  tap-timedoctor \
        --auth "${TEMP_FILE2}" \
        --start-date "${start_date}" \
        --end-date "${end_date}" \
        --computer-activity \
        > ca.singer \
  &&  echo "[INFO] Uploading backup to s3" \
  &&  bucket=$(< s3_files.json jq -r '.bucket_name') \
  &&  cont_folder=$(< s3_files.json jq -r '.folder_name') \
  && aws s3 cp wl.singer "s3://${bucket}/${cont_folder}/timedoctor.worklogs.${start_date}.${end_date}.singer" \
  && aws s3 cp ca.singer "s3://${bucket}/${cont_folder}/timedoctor.computer_activity.${start_date}.${end_date}.singer"
}

function job_analytics_zoho {
  local analytics_zoho_tables=(
    Candidates
    Periods
  )

      aws_login \
  &&  sops_env secrets-prod.yaml default \
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
        &&  ./analytics/singer/converter_zoho_csv.py \
              --email "${analytics_zoho_email}" \
              --token "${analytics_zoho_token}" \
              --space "${analytics_zoho_space}" \
              --table "${table}" \
              --target "${table}" \
        &&  ./analytics/singer/streamer_csv.py "${table}" \
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

function job_deploy_docker_image_nix {
  local tag="${CI_REGISTRY_IMAGE}:nix"
  local context='.'
  local dockerfile='build/Dockerfile'

  helper_docker_build_and_push \
    "${tag}" \
    "${context}" \
    "${dockerfile}"
}
