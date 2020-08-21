# shellcheck shell=bash

function helper_analytics_formstack {
      helper_serves_aws_login prod \
  &&  sops_env secrets-prod.yaml default \
        analytics_auth_redshift \
        analytics_auth_formstack \
  &&  echo '[INFO] Generating secret files' \
  &&  echo "${analytics_auth_formstack}" > "${TEMP_FILE1}" \
  &&  echo "${analytics_auth_redshift}" > "${TEMP_FILE2}" \
  &&  echo '[INFO] Running tap' \
  &&  mkdir ./logs \
  &&  tap-formstack \
        --auth "${TEMP_FILE1}" \
        --conf ./analytics/conf/formstack.json \
        > .singer \
  &&  echo '[INFO] Running target' \
  &&  target-redshift \
        --auth "${TEMP_FILE2}" \
        --drop-schema \
        --schema-name 'formstack' \
        < .singer
}

function helper_analytics_dynamodb {
      helper_serves_aws_login prod \
  &&  sops_env secrets-prod.yaml default \
        analytics_aws_access_key \
        analytics_aws_secret_key \
        analytics_aws_default_region \
        analytics_auth_redshift \
  &&  echo '[INFO] Generating secret files' \
  &&  {
        echo '{'
        echo "\"AWS_ACCESS_KEY_ID\":\"${analytics_aws_access_key}\","
        echo "\"AWS_SECRET_ACCESS_KEY\":\"${analytics_aws_secret_key}\","
        echo "\"AWS_DEFAULT_REGION\":\"${analytics_aws_default_region}\""
        echo '}'
      } > "${TEMP_FILE1}" \
  &&  echo "${analytics_auth_redshift}" > "${TEMP_FILE2}" \
  &&  echo '[INFO] Running tap' \
  &&  mkdir ./logs \
  &&  tap-awsdynamodb \
        --auth "${TEMP_FILE1}" \
        --conf ./analytics/conf/awsdynamodb.json \
        > .singer \
  &&  echo '[INFO] Running target' \
  &&  target-redshift \
        --auth "${TEMP_FILE2}" \
        --drop-schema \
        --schema-name 'dynamodb' \
        < .singer
}

function helper_analytics_services_toe {
      helper_serves_aws_login prod \
  &&  sops_env secrets-prod.yaml default \
        analytics_auth_redshift \
  &&  echo '[INFO] Generating secret files' \
  &&  echo "${analytics_auth_redshift}" > "${TEMP_FILE2}" \
  &&  pushd analytics/services || return 1 \
    &&  echo '[INFO] Cloning services repository' \
    &&  git clone --depth 1 --single-branch \
          "https://${GITLAB_API_USER}:${GITLAB_API_TOKEN}@gitlab.com/fluidattacks/services.git" \
    &&  echo '[INFO] Running streamer' \
    &&  ./streamer_toe.py \
          > .jsonstream \
    &&  echo '[INFO] Running tap' \
    &&  tap-json  \
          > .singer \
          < .jsonstream \
    &&  echo '[INFO] Running target' \
    &&  target-redshift \
          --auth "${TEMP_FILE2}" \
          --drop-schema \
          --schema-name 'continuous_toe' \
          < .singer \
  && popd || return 1
}

function helper_analytics_infrastructure {
      helper_serves_aws_login prod \
  &&  sops_env secrets-prod.yaml default \
        analytics_auth_infra \
        analytics_auth_redshift \
  &&  echo '[INFO] Generating secret files' \
  &&  echo "${analytics_auth_infra}" > "${TEMP_FILE1}" \
  &&  echo "${analytics_auth_redshift}" > "${TEMP_FILE2}" \
  &&  echo '[INFO] Running streamer' \
  &&  streamer-infrastructure \
        --auth "${TEMP_FILE1}" \
        > .jsonstream \
  &&  echo '[INFO] Running tap' \
  &&  tap-json \
        > .singer \
        < .jsonstream \
  &&  echo '[INFO] Running target' \
  &&  target-redshift \
        --auth "${TEMP_FILE2}" \
        --drop-schema \
        --schema-name 'infrastructure' \
        < .singer
}

function helper_analytics_intercom {
      helper_serves_aws_login prod \
  &&  sops_env secrets-prod.yaml default \
        analytics_auth_intercom \
        analytics_auth_redshift \
  &&  echo '[INFO] Generating secret files' \
  &&  echo "${analytics_auth_intercom}" > "${TEMP_FILE1}" \
  &&  echo "${analytics_auth_redshift}" > "${TEMP_FILE2}" \
  &&  echo '[INFO] Running streamer' \
  &&  streamer-intercom \
        --auth "${TEMP_FILE1}" \
        > .jsonstream \
  &&  echo '[INFO] Running tap' \
  &&  tap-json \
        --enable-timestamps \
        > .singer \
        < .jsonstream \
  &&  echo '[INFO] Running target' \
  &&  target-redshift \
        --auth "${TEMP_FILE2}" \
        --drop-schema \
        --schema-name 'intercom' \
        < .singer
}

function helper_analytics_mandrill {
      helper_serves_aws_login prod \
  &&  sops_env secrets-prod.yaml default \
        analytics_auth_mandrill \
        analytics_auth_redshift \
  &&  echo '[INFO] Generating secret files' \
  &&  echo "${analytics_auth_mandrill}" > "${TEMP_FILE1}" \
  &&  echo "${analytics_auth_redshift}" > "${TEMP_FILE2}" \
  &&  echo '[INFO] Running streamer' \
  &&  streamer-mandrill \
        --auth "${TEMP_FILE1}" \
        > .jsonstream \
  &&  echo '[INFO] Running tap' \
  &&  tap-json  \
        --date-formats '%Y-%m-%d %H:%M:%S,%Y-%m-%d %H:%M:%S.%f' \
        > .singer \
        < .jsonstream \
  &&  echo '[INFO] Running target' \
  &&  target-redshift \
        --auth "${TEMP_FILE2}" \
        --drop-schema \
        --schema-name 'mandrill' \
        < .singer
}

function helper_analytics_gitlab {
  export GITLAB_API_TOKEN
  local project
  local projects=(
    'autonomicmind/default'
    'autonomicmind/challenges'
    'fluidattacks/services'
    'fluidattacks/asserts'
    'fluidattacks/integrates'
    'fluidattacks/private'
    'fluidattacks/public'
    'fluidattacks/serves'
    'fluidattacks/web'
    'fluidattacks/writeups'
  )

      helper_serves_aws_login prod \
  &&  sops_env secrets-prod.yaml default \
        analytics_auth_redshift \
  &&  echo '[INFO] Generating secret files' \
  &&  echo "${analytics_auth_redshift}" > "${TEMP_FILE2}" \
  &&  echo '[INFO] Running streamer' \
  &&  for project in "${projects[@]}"
      do
        ./analytics/singer/streamer_gitlab.py "${project}" >> .jsonstream \
            || return 1
      done \
  &&  echo '[INFO] Running tap' \
  &&  tap-json  \
        > .singer \
        < .jsonstream \
  &&  echo '[INFO] Running target' \
  &&  target-redshift \
        --auth "${TEMP_FILE2}" \
        --drop-schema \
        --schema-name 'gitlab-ci' \
        < .singer
}

function helper_analytics_timedoctor {
  export analytics_auth_timedoctor

      helper_serves_aws_login prod \
  &&  mkdir ./logs \
  &&  sops_env secrets-prod.yaml default \
        analytics_auth_redshift \
        analytics_s3_cache_timedoctor \
  &&  analytics_auth_timedoctor=$( \
        helper_get_gitlab_var \
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

function helper_analytics_zoho {
  local analytics_zoho_tables=(
    Candidates
    Periods
  )

      helper_serves_aws_login prod \
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

function helper_analytics_git_process {
  local artifacts="${PWD}/artifacts"
  local mock_integrates_api_token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.xxx'
  local num_threads='4'
  export CI_NODE_INDEX
  export CI_NODE_TOTAL

      helper_serves_aws_login prod \
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
  &&  wait
}

function helper_analytics_git_upload {
  local artifacts="${PWD}/artifacts"

      helper_serves_aws_login prod \
  &&  sops_env secrets-prod.yaml default \
        analytics_auth_redshift \
  &&  echo '[INFO] Generating secret files' \
  &&  echo "${analytics_auth_redshift}" > "${TEMP_FILE1}" \
  &&  echo '[INFO] Running target' \
  &&  cat "${artifacts}/git."* \
        | target-redshift \
            --auth "${TEMP_FILE1}" \
            --drop-schema \
            --schema-name "git"
}

function helper_analytics_timedoctor_refresh_token {
  export analytics_auth_timedoctor

      helper_serves_aws_login prod \
  &&  analytics_auth_timedoctor=$( \
        helper_get_gitlab_var \
          'analytics_auth_timedoctor' \
          "${GITLAB_API_TOKEN}") \
  &&  echo '[INFO] Updating token...' \
  &&  ./analytics/auth_helper.py --timedoctor-refresh \
  &&  echo '[INFO] Done! Token created for current project'
}

function helper_analytics_timedoctor_backup {
  export analytics_auth_timedoctor

      helper_serves_aws_login prod \
  &&  mkdir ./logs \
  &&  sops_env secrets-prod.yaml default \
        analytics_s3_cache_timedoctor \
  &&  analytics_auth_timedoctor=$( \
        helper_get_gitlab_var \
          'analytics_auth_timedoctor' \
          "${GITLAB_API_TOKEN}") \
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
  &&  aws s3 cp wl.singer "s3://${bucket}/${cont_folder}/timedoctor.worklogs.${start_date}.${end_date}.singer" \
  &&  aws s3 cp ca.singer "s3://${bucket}/${cont_folder}/timedoctor.computer_activity.${start_date}.${end_date}.singer"
}

function helper_analytics_timedoctor_manually_create_token {
      helper_serves_aws_login prod \
  &&  sops_env secrets-prod.yaml default \
        analytics_auth_timedoctor \
  &&  echo '[INFO] Executing creator, follow the steps' \
  &&  ./analytics/auth_helper.py --timedoctor-start \
  &&  echo '[INFO] Done! Token created at GitLab/serves env vars'
}

function helper_analytics_services_repositories_cache {
  local mock_integrates_api_token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.xxx'

      helper_serves_aws_login prod \
  &&  helper_serves_move_artifacts_to_git \
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
  &&  helper_serves_move_services_fusion_to_master_git \
  &&  echo '[INFO] Generating stats' \
  &&  { python3 analytics/git/generate_stats.py || true; } \
  &&  helper_serves_move_git_to_artifacts
}
