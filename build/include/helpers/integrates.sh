# shellcheck shell=bash

function helper_integrates_aws_login {

  # Log in to aws for resources

  local user="$1"
  export TF_VAR_aws_access_key
  export TF_VAR_aws_secret_key
  export AWS_ACCESS_KEY_ID
  export AWS_SECRET_ACCESS_KEY

      if [ "${user}"  == 'production' ]; then
        if [ "${CI_COMMIT_REF_NAME}" == 'master' ]; then
              AWS_ACCESS_KEY_ID="${INTEGRATES_PROD_AWS_ACCESS_KEY_ID}" \
          &&  AWS_SECRET_ACCESS_KEY="${INTEGRATES_PROD_AWS_SECRET_ACCESS_KEY}"
        else
              echo 'Not enough permissions for logging in as production' \
          &&  return 1
        fi
      elif [ "${user}" == 'development' ]; then
            AWS_ACCESS_KEY_ID="${INTEGRATES_DEV_AWS_ACCESS_KEY_ID}" \
        &&  AWS_SECRET_ACCESS_KEY="${INTEGRATES_DEV_AWS_SECRET_ACCESS_KEY}"
      else
            echo 'No valid user was provided' \
        &&  return 1
      fi \
  &&  TF_VAR_aws_access_key="${AWS_ACCESS_KEY_ID}" \
  &&  TF_VAR_aws_secret_key="${AWS_SECRET_ACCESS_KEY}" \
  &&  aws configure set aws_access_key_id "${AWS_ACCESS_KEY_ID}" \
  &&  aws configure set aws_secret_access_key "${AWS_SECRET_ACCESS_KEY}"
}

function helper_integrates_set_dev_secrets {
  export JWT_TOKEN
  export AWS_ACCESS_KEY_ID
  export AWS_SECRET_ACCESS_KEY
  export AWS_DEFAULT_REGION

      helper_integrates_aws_login development \
  &&  echo '[INFO] Exporting development secrets' \
  &&  helper_integrates_sops_vars development
}

function helper_integrates_set_prod_secrets {
  export JWT_TOKEN
  export AWS_ACCESS_KEY_ID
  export AWS_SECRET_ACCESS_KEY
  export AWS_DEFAULT_REGION

      helper_integrates_aws_login production \
  &&  echo '[INFO] Exporting production secrets' \
  &&  helper_integrates_sops_vars production \
  &&  export DEBUG="True" \
  &&  export ENVIRONMENT='development' \
  &&  export REDIS_SERVER='localhost'
}

function app_version {
  # Return a version for integrates app

  local minutes

      minutes=$(minutes_of_month) \
  &&  echo "$(date +%y.%m.)${minutes}"
}

function helper_bootstrap_prod_ci {
  env_prepare_python_packages \
  &&  helper_integrates_set_prod_secrets \
  &&  if test "${IS_LOCAL_BUILD}" = "${FALSE}"
      then
        helper_set_local_dynamo_and_redis
      fi
}

function helper_bootstrap_dev_ci {
  env_prepare_python_packages \
  &&  helper_integrates_set_dev_secrets \
  &&  if test "${IS_LOCAL_BUILD}" = "${FALSE}"
      then
        helper_set_local_dynamo_and_redis
      fi
}

function helper_invoke_py {
  local module="${1}"
  export DJANGO_SETTINGS_MODULE='fluidintegrates.settings'
  export PYTHONPATH="${PWD}:${PWD}/analytics:${PYTHONPATH}"

      echo "[INFO] Waking up: ${module}" \
  &&  python3 \
        'django-apps/integrates-back-async/cli/invoker.py' \
        "${module}"
}

function helper_set_local_dynamo_and_redis {
  local processes_to_kill=()
  local port_dynamo='8022'
  local port_redis='6379'

  function kill_processes {
    for process in "${processes_to_kill[@]}"
    do
      echo "[INFO] Killing PID: ${process}"
      kill -9 "${process}" || true
    done
  }

  trap kill_processes EXIT

      echo '[INFO] Launching Redis' \
  &&  {
        redis-server --port "${port_redis}" \
          &
        processes_to_kill+=( "$!" )
      } \
  &&  echo '[INFO] Launching DynamoDB local' \
  &&  env_prepare_dynamodb_local \
  &&  {
        java \
          -Djava.library.path="${STARTDIR}/integrates/.DynamoDB/DynamoDBLocal_lib" \
          -jar "${STARTDIR}/integrates/.DynamoDB/DynamoDBLocal.jar" \
          -inMemory \
          -port "${port_dynamo}" \
          -sharedDb \
          &
        processes_to_kill+=( "$!" )
      } \
  &&  echo '[INFO] Waiting 5 seconds to leave DynamoDB start' \
  &&  sleep 5 \
  &&  echo '[INFO] Populating DynamoDB local' \
  &&  bash ./deploy/containers/common/vars/provision_local_db.sh
}

function helper_build_django_apps {
  local app

  for app in \
    'django-apps/integrates-'* \

  do
        echo "[INFO] Building: ${app}" \
    &&  pushd "${app}" \
      &&  python3 setup.py sdist -d ../packages/ \
    &&  popd
  done \
  ||  return 1
}

function helper_integrates_serve_back {
  local app='fluidintegrates.asgi:APP'
  local host='0.0.0.0'
  local http_port='8000'
  local https_port='8080'
  local workers='5'
  local worker_class='fluidintegrates.asgi.IntegratesWorker'
  local common_args=(
    --timeout "3600"
    --workers "${workers}"
    --worker-class "${worker_class}"
  )

      env_prepare_python_packages \
  &&  env_prepare_ruby_modules \
  &&  env_prepare_node_modules \
  &&  "helper_integrates_set_${1}_secrets" \
  &&  echo "[INFO] Serving HTTP on port ${http_port}" \
  &&  {
        gunicorn \
          "${common_args[@]}" \
          --bind="${host}:${http_port}" \
          "${app}" \
          &
        HTTP_PID=$!
      } \
  &&  echo "[INFO] Serving HTTPS on port ${https_port}" \
  &&  gunicorn \
        "${common_args[@]}" \
        --bind="${host}:${https_port}" \
        --certfile="${srcDerivationsCerts}/fluidla.crt" \
        --keyfile="${srcDerivationsCerts}/fluidla.key" \
        "${app}" \
  &&  kill -TERM "${HTTP_PID}"
}

function helper_integrates_serve_back2 {
  local app='backend_new.app:APP'
  local host='0.0.0.0'
  local http_port='8000'
  local https_port='8080'
  local workers='5'
  local worker_class='uvicorn.workers.UvicornWorker'
  local common_args=(
    --timeout "3600"
    --workers "${workers}"
    --worker-class "${worker_class}"
  )

      env_prepare_python_packages \
  &&  env_prepare_ruby_modules \
  &&  env_prepare_node_modules \
  &&  "helper_integrates_set_${1}_secrets" \
  &&  echo "[INFO] Serving HTTP on port ${http_port}" \
  &&  {
        gunicorn \
          "${common_args[@]}" \
          --bind="${host}:${http_port}" \
          "${app}" \
          &
        HTTP_PID=$!
      } \
  &&  echo "[INFO] Serving HTTPS on port ${https_port}" \
  &&  gunicorn \
        "${common_args[@]}" \
        --bind="${host}:${https_port}" \
        --certfile="${srcDerivationsCerts}/fluidla.crt" \
        --keyfile="${srcDerivationsCerts}/fluidla.key" \
        "${app}" \
  &&  kill -TERM "${HTTP_PID}"
}

function helper_integrates_functional_tests {
  local modifier=""
  if [ $# -eq 1 ]; then
      local modifier="not $1"
  fi

      env_prepare_python_packages \
  &&  echo '[INFO] Logging in to AWS' \
  &&  helper_integrates_aws_login "${ENVIRONMENT_NAME}" \
  &&  echo "[INFO] Firefox: ${pkgFirefox}" \
  &&  echo "[INFO] GeckoDriver:  ${pkgGeckoDriver}" \
  &&  echo '[INFO] Exporting vars' \
  &&  helper_integrates_sops_vars "${ENVIRONMENT_NAME}" \
  &&  echo "[INFO] Running test suite: ${CI_NODE_INDEX}/${CI_NODE_TOTAL}" \
  &&  mkdir -p test/functional/screenshots \
  &&  pytest \
        -m "${modifier}" \
        --ds='fluidintegrates.settings' \
        --verbose \
        --exitfirst \
        --basetemp='build/test' \
        --reruns 10 \
        --test-group-count "${CI_NODE_TOTAL}" \
        --test-group "${CI_NODE_INDEX}" \
        deploy/functional-tests.py
}

mobile_get_version() {
  # Get the current version for a mobile deployment

  local minutes
  local fi_version

      minutes=$(
        printf "%05d" $((
        ($(date +%d | sed 's/^0//') -1) * 1440 +
        $(date +%H | sed 's/^0//') * 60 +
        $(date +%M | sed 's/^0//')
        ))
      ) \
  &&  if [ "$1" = "basic" ]; then
            fi_version="$(date +%y.%m.)${minutes}" \
        &&  echo "${fi_version}"
      elif [ "$1" = "code" ]; then
            fi_version="$(date +%y%m)${minutes}" \
        &&  echo "${fi_version}"
      else
            echo "Error. Only basic or code allowed as params" \
        &&  exit 1
      fi
}

function helper_integrates_sops_vars {
  # Set necessary vars for integrates

  local env_name="$1"

  helper_common_sops_env "secrets-${env_name}.yaml" default \
    AWS_DEFAULT_REGION \
    AWS_REDSHIFT_DBNAME \
    AWS_REDSHIFT_HOST \
    AWS_REDSHIFT_PASSWORD \
    AWS_REDSHIFT_USER \
    AZUREAD_OAUTH2_KEY \
    AZUREAD_OAUTH2_SECRET \
    BITBUCKET_OAUTH2_KEY \
    BITBUCKET_OAUTH2_SECRET \
    BUGSNAG_ACCESS_TOKEN \
    BUGSNAG_API_KEY_SCHEDULER \
    COMMUNITY_PROJECTS \
    CLOUDFRONT_ACCESS_KEY \
    CLOUDFRONT_PRIVATE_KEY \
    CLOUDFRONT_RESOURCES_DOMAIN \
    CLOUDFRONT_REPORTS_DOMAIN \
    CLOUDMERSIVE_API_KEY \
    DB_HOST \
    DB_PASSWD \
    DB_USER \
    DEBUG \
    DJANGO_SECRET_KEY \
    DYNAMODB_HOST \
    DYNAMODB_PORT \
    ENVIRONMENT \
    FORCES_TRIGGER_REF \
    FORCES_TRIGGER_TOKEN \
    FORCES_TRIGGER_URL \
    GOOGLE_OAUTH2_KEY \
    GOOGLE_OAUTH2_SECRET \
    JWT_ENCRYPTION_KEY \
    JWT_SECRET \
    JWT_SECRET_API \
    MAIL_CONTINUOUS \
    MAIL_PRODUCTION \
    MAIL_PROJECTS \
    MAIL_REVIEWERS \
    MAIL_RESOURCERS \
    MANDRILL_APIKEY \
    MINIO_LOCAL_ENABLED \
    MIXPANEL_API_TOKEN \
    NEW_RELIC_API_KEY \
    NEW_RELIC_APP_ID \
    NEW_RELIC_LICENSE_KEY \
    NEW_RELIC_ENVIRONMENT \
    REDIS_SERVER \
    REDIS_SERVER_2 \
    SQS_QUEUE_URL \
    TEST_PROJECTS \
    ZENDESK_EMAIL \
    ZENDESK_SUBDOMAIN \
    ZENDESK_TOKEN
}

function helper_upload_to_devicefarm {
    local resource_arn_out="${1}"
    local run_name="${2}"
    local file_path="${3}"
    local file_type="${4}"
    local file_name
    local upload_status

        echo "[INFO] Uploading ${file_type} to AWS Device Farm" \
    &&  file_name=$(basename "${file_path}") \
    &&  resource_data=$(
          aws devicefarm create-upload \
            --content-type "application/octet-stream" \
            --name "${run_name}_${file_name}" \
            --project-arn "${project_arn}" \
            --type "${file_type}" \
        ) \
    &&  resource_arn=$(echo "${resource_data}" | jq -r '.upload | .arn') \
    &&  resource_url=$(echo "${resource_data}" | jq -r '.upload | .url') \
    &&  curl \
          --header 'Content-Type: application/octet-stream' \
          --upload-file \
          "${file_path}" \
          "${resource_url}" \
    &&  while true;
        do
          upload_status=$(
            aws devicefarm get-upload \
              --arn "${resource_arn}" \
            | jq -r '.upload | .status'
          ) \
          &&  if [ "${upload_status}" == "SUCCEEDED" ];
              then
                break
              elif [ "${upload_status}" == "FAILED" ];
              then
                    echo "[ERROR] Couldn't upload ${file_type}" \
                &&  return 1
              else
                    echo "[INFO] Upload in ${upload_status} status, waiting for completion" \
                &&  sleep 5 \
                ||  return 1
              fi
        done \
    &&  export "${resource_arn_out}"="${resource_arn}"
  }

function helper_run_test_devicefarm {
    local app_arn="${1}"
    local device_pool_arn="${2}"
    local project_arn="${3}"
    local run_name="${4}"
    local test_pkg_arn="${5}"
    local test_spec_arn="${6}"
    local job_arn
    local logs_url
    local run_arn
    local run_result

        echo "[INFO] Scheduling run" \
    &&  run_arn=$(
          aws devicefarm schedule-run \
            --app-arn "${app_arn}" \
            --device-pool-arn "${device_pool_arn}" \
            --name "${run_name}" \
            --project-arn "${project_arn}" \
            --test "{
              \"parameters\": {
                \"app_performance_monitoring\": \"false\",
                \"video_recording\": \"false\"
              },
              \"testPackageArn\": \"${test_pkg_arn}\",
              \"testSpecArn\": \"${test_spec_arn}\",
              \"type\": \"APPIUM_PYTHON\"
            }" \
          | jq -r '.run | .arn'
        ) \
    &&  while true;
        do
              run_status=$(
                aws devicefarm get-run \
                  --arn "${run_arn}" \
                | jq -r '.run | .status'
              ) \
          &&  if [ "${run_status}" == "COMPLETED" ]; then
                break
              elif [ "${run_status}" == "RUNNING" ]; then
                    job_arn=$(
                      aws devicefarm list-jobs \
                        --arn "${run_arn}" \
                      | jq -r '.jobs[0] | .arn'
                    ) \
                &&  logs_url=$(
                      aws devicefarm list-artifacts \
                        --arn "${job_arn}" \
                        --type FILE \
                      | jq -r '.artifacts | .[] | select(.type == "TESTSPEC_OUTPUT") | .url'
                    ) \
                &&  if curl -so "${TEMP_FILE1}" "${logs_url}"
                    then
                          comm -13 --nocheck-order "${TEMP_FILE2}" "${TEMP_FILE1}" \
                      &&  mv "${TEMP_FILE1}" "${TEMP_FILE2}"
                    fi \
                &&  sleep 5 \
                ||  return 1
              else
                    echo "[INFO] Run in ${run_status} status, waiting for completion" \
                &&  sleep 10 \
                ||  return 1
              fi
        done \
    &&  run_result=$(
          aws devicefarm get-run \
            --arn "${run_arn}" \
          | jq -r '.run | .result'
        ) \
    &&  if [ "${run_result}" == "PASSED" ];
        then
          return 0
        else
              echo "[ERROR] Run finished with status ${run_result}" \
          &&  return 1
        fi
  }

function helper_integrates_to_b64 {
  local value="${1}"

  echo -n "${value}" | base64 --wrap=0
}

function helper_integrates_terraform_plan {
  local target="${1}"
  local config

      config="$(readlink -f ../.tflint.hcl)" \
  &&  helper_common_terraform_plan_new "${target}" "${config}"
}
