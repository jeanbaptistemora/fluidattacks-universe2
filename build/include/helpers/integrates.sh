# shellcheck shell=bash

function app_version {
  # Return a version for integrates app

  local minutes

      minutes=$(minutes_of_month) \
  &&  echo "$(date +%y.%m.)${minutes}"
}

function helper_bootstrap_prod_ci {
  env_prepare_python_packages \
  &&  helper_set_prod_secrets \
  &&  if test "${IS_LOCAL_BUILD}" = "${FALSE}"
      then
        helper_set_local_dynamo_and_redis
      fi
}

function helper_bootstrap_dev_ci {
  env_prepare_python_packages \
  &&  helper_set_dev_secrets \
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
  &&  "helper_set_${1}_secrets" \
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
      env_prepare_python_packages \
  &&  echo '[INFO] Logging in to AWS' \
  &&  aws_login "${ENVIRONMENT_NAME}" \
  &&  echo "[INFO] Firefox: ${pkgFirefox}" \
  &&  echo "[INFO] GeckoDriver:  ${pkgGeckoDriver}" \
  &&  echo '[INFO] Exporting vars' \
  &&  sops_vars "${ENVIRONMENT_NAME}" \
  &&  echo "[INFO] Running test suite: ${CI_NODE_INDEX}/${CI_NODE_TOTAL}" \
  &&  mkdir -p test/functional/screenshots \
  &&  pytest \
        --ds='fluidintegrates.settings' \
        --verbose \
        --exitfirst \
        --basetemp='build/test' \
        --reruns 10 \
        --test-group-count "${CI_NODE_TOTAL}" \
        --test-group "${CI_NODE_INDEX}" \
        ephemeral_tests.py
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

sops_vars() {
  # Set necessary vars for integrates

  local env_name="$1"

  sops_env "secrets-${env_name}.yaml" default \
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
    JWT_SECRET \
    JWT_SECRET_API \
    MAIL_CONTINUOUS \
    MAIL_PRODUCTION \
    MAIL_PROJECTS \
    MAIL_REVIEWERS \
    MAIL_RESOURCERS \
    MANDRILL_APIKEY \
    MIXPANEL_API_TOKEN \
    NEW_RELIC_API_KEY \
    NEW_RELIC_APP_ID \
    NEW_RELIC_LICENSE_KEY \
    NEW_RELIC_ENVIRONMENT \
    REDIS_SERVER \
    SQS_QUEUE_URL \
    TEST_PROJECTS \
    ZENDESK_EMAIL \
    ZENDESK_SUBDOMAIN \
    ZENDESK_TOKEN
}

function helper_upload_to_devicefarm {
    local resource_arn_out="${1}"
    local file_path="${2}"
    local file_type="${3}"
    local file_name
    local upload_status

        echo "[INFO] Uploading ${file_type} to AWS Device Farm" \
    &&  file_name=$(basename "${file_path}") \
    &&  resource_data=$(
          aws devicefarm create-upload \
            --content-type "application/octet-stream" \
            --name "${file_name}" \
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
          )
          if [ "${upload_status}" == "SUCCEEDED" ];
          then
            break;
          elif [ "${upload_status}" == "FAILED" ];
          then
            echo "[ERROR] Couldn't upload ${file_type}";
            return 1;
          else
            echo "[INFO][${upload_status}] sleeping 5 seconds...";
            sleep 5;
          fi;
        done \
    &&  eval "${resource_arn_out}"="${resource_arn}"
  }
