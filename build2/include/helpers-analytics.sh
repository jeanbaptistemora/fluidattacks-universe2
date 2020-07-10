# shellcheck shell=bash

function helper_analytics_formstack {
      helper_aws_login \
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
      helper_aws_login \
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
      helper_aws_login \
  &&  sops_env secrets-prod.yaml default \
        analytics_gitlab_user \
        analytics_gitlab_token \
        analytics_auth_redshift \
  &&  echo '[INFO] Generating secret files' \
  &&  echo "${analytics_auth_redshift}" > "${TEMP_FILE2}" \
  &&  pushd analytics/services || return 1 \
    &&  echo '[INFO] Cloning services repository' \
    &&  git clone --depth 1 --single-branch \
          "https://${analytics_gitlab_user}:${analytics_gitlab_token}@gitlab.com/fluidattacks/services.git" \
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
