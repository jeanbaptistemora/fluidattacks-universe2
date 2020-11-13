# shellcheck shell=bash

function helper_integrates_aws_login {

  # Log in to aws for resources

  local user="$1"
  export TF_VAR_aws_access_key
  export TF_VAR_aws_secret_key
  export AWS_ACCESS_KEY_ID
  export AWS_SECRET_ACCESS_KEY

      if [ "${user}"  == 'production' ]; then
            AWS_ACCESS_KEY_ID="${INTEGRATES_PROD_AWS_ACCESS_KEY_ID}" \
        &&  AWS_SECRET_ACCESS_KEY="${INTEGRATES_PROD_AWS_SECRET_ACCESS_KEY}"
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
  &&  aws configure set aws_secret_access_key "${AWS_SECRET_ACCESS_KEY}" \
  &&  aws configure set region 'us-east-1'
}

function helper_integrates_set_dev_secrets {
  export AWS_ACCESS_KEY_ID
  export AWS_SECRET_ACCESS_KEY
  export AWS_DEFAULT_REGION

      helper_integrates_aws_login development \
  &&  echo '[INFO] Exporting development secrets' \
  &&  helper_integrates_sops_vars development
}

function helper_integrates_set_prod_secrets {
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

function helper_integrates_deployment_date {
  export INTEGRATES_DEPLOYMENT_DATE

  INTEGRATES_DEPLOYMENT_DATE="$(date -u '+%FT%H:%M:%SZ')"
}

function helper_bootstrap_prod_ci {
  env_prepare_python_packages \
  &&  helper_integrates_set_prod_secrets \
  &&  if test "${IS_LOCAL_BUILD}" = "${FALSE}"
      then
            helper_integrates_serve_dynamo \
        &&  helper_integrates_serve_minio \
        &&  helper_integrates_serve_redis
      fi
}

function helper_bootstrap_dev_ci {
  env_prepare_python_packages \
  &&  helper_integrates_set_dev_secrets \
  &&  if test "${IS_LOCAL_BUILD}" = "${FALSE}"
      then
            helper_integrates_serve_dynamo \
        &&  helper_integrates_serve_minio \
        &&  helper_integrates_serve_redis
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

function helper_integrates_serve_nginx {
  local conf='deploy/local/nginx/nginx.conf'

      cp -r "${nginxPath}" .nginx \
  &&  chmod -R 777 .nginx \
  &&  cp "${conf}" .nginx/conf/ \
  &&  sed -i "s|__srcDerivationsCerts__|${srcDerivationsCerts}|g" .nginx/conf/nginx.conf \
  &&  { nginx -p .nginx & }
}

function helper_integrates_serve_front {
      helper_integrates_deployment_date \
  &&  pushd front \
        &&  npm install \
        &&  { npm start & } \
  &&  popd \
  ||  return 1
}

function helper_integrates_serve_redis {
  local port='6379'

      echo '[INFO] Launching Redis' \
  &&  { redis-server --port "${port}" & }
}

function helper_integrates_serve_dynamo {
  local port='8022'

      echo '[INFO] Launching DynamoDB local' \
  &&  env_prepare_dynamodb_local \
  &&  { java \
        -Djava.library.path='.DynamoDB/DynamoDBLocal_lib' \
        -jar '.DynamoDB/DynamoDBLocal.jar' \
        -inMemory \
        -port "${port}" \
        -sharedDb \
        & } \
  &&  sleep 10 \
  &&  echo '[INFO] Populating DynamoDB local' \
  &&  { bash ./deploy/database/provision_local_db.sh & }
}

function helper_integrates_serve_back {
  local protocol="${1}"
  local environment="${2}"
  local app="${3}"
  local worker_class="${4}"
  local workers="${5}"
  local host="${6}"
  local port="${7}"
  local forwarded_ips="${8}"
  local common_args=(
    --timeout "3600"
    --workers "${workers}"
    --worker-class "${worker_class}"
    --forwarded-allow-ips="${forwarded_ips}"
  )

      env_prepare_python_packages \
  &&  env_prepare_ruby_modules \
  &&  env_prepare_node_modules \
  &&  helper_integrates_sops_vars "${environment}" \
  &&  echo "[INFO] Serving ${protocol} on ${host}:${port}" \
  &&  if [ "${protocol}" == 'http' ]
      then
        :
      elif [ "${protocol}" == 'https' ]
      then
        common_args+=(
          --certfile="${srcDerivationsCerts}/fluidla.crt"
          --keyfile="${srcDerivationsCerts}/fluidla.key"
        )
      else
            echo "[ERROR] Only 'http' and 'https' allowed for protocol." \
        &&  return 1
      fi \
  &&  { gunicorn \
        "${common_args[@]}" \
        --bind="${host}:${port}" \
        "${app}" \
        & }
}

function helper_integrates_serve_minio {
  local port='9000'
  local data_path='.MinIO/data'

      env_prepare_minio_local \
  &&  echo '[INFO] Launching MinIO local' \
  &&  { "${minio}" server "${data_path}" --address ":${port}" & } \
  &&  sleep 5 \
  &&  echo '[INFO] Configuring local user' \
  &&  "${mc}" alias set local_minio \
        "http://localhost:${port}" \
        "${MINIO_ACCESS_KEY}" \
        "${MINIO_SECRET_KEY}" \
  &&  "${mc}" admin user add local_minio \
        "${USER_MINIO_ACCESS_KEY}" \
        "${USER_MINIO_SECRET_KEY}" \
  &&  "${mc}" admin policy set local_minio readwrite \
        user="${USER_MINIO_ACCESS_KEY}" \
  &&  echo '[INFO] Setting buckets' \
  &&  "${mc}" mb --ignore-existing local_minio/fluidintegrates.evidences \
  &&  "${mc}" mb --ignore-existing local_minio/fluidintegrates.analytics \
  &&  "${mc}" mb --ignore-existing local_minio/fluidintegrates.resources \
  &&  "${mc}" mb --ignore-existing local_minio/fluidintegrates.reports \
  &&  "${mc}" mb --ignore-existing local_minio/fluidintegrates.forces \
  &&  echo '[INFO] Populating MinIO local' \
  &&  readarray -d , -t projects <<< "${TEST_PROJECTS}" \
  &&  {
        for project in "${projects[@]}"
        do
              aws s3 sync --quiet "s3://fluidintegrates.evidences/${project}" \
                "${data_path}/fluidintegrates.evidences/${project}" \
          &&  aws s3 sync --quiet "s3://fluidintegrates.resources/${project}" \
                "${data_path}/fluidintegrates.resources/${project}" \
          &&  aws s3 sync --quiet "s3://fluidintegrates.forces/${project}" \
                "${data_path}/fluidintegrates.forces/${project}" \
          ||  return 1
        done
      } \
  &&  aws s3 sync --quiet "s3://fluidintegrates.analytics/${CI_COMMIT_REF_NAME}" \
        "${data_path}/fluidintegrates.analytics/${CI_COMMIT_REF_NAME}" &> /dev/null \
  &&  mkdir -p "${data_path}/fluidintegrates.reports/tmp" \
  &&  echo "[INFO] MinIO is ready and listening on port ${port}!"
}

function helper_integrates_serve_mobile {
      helper_integrates_aws_login 'development' \
  &&  helper_common_sops_env 'secrets-development.yaml' 'default' \
        EXPO_USER \
        EXPO_PASS \
  &&  sops \
        --aws-profile default \
        --decrypt \
        --extract '["GOOGLE_SERVICES_APP"]' \
        --output 'mobile/google-services.json' \
        --output-type 'json' \
        'secrets-development.yaml' \
  &&  pushd mobile \
    &&  npm install \
    &&  rm -rf ~/.expo ./.expo \
    &&  npx --no-install expo login \
            --username "${EXPO_USER}" \
            --password "${EXPO_PASS}" \
            --non-interactive \
    &&  { npm start -- \
          --clear \
          --non-interactive & } \
  &&  popd \
  ||  return 1
}

function helper_integrates_probe_aws_credentials {
  local user="${1}"

  if aws sts get-caller-identity | grep -q "${user}"
  then
    echo '[INFO] Passed: test_aws_credentials'
  else
        echo '[ERROR] AWS credentials could not be validated.' \
    &&  return 1
  fi
}

function helper_integrates_probe_curl {
  local endpoint="${1}"

  if curl -sSiLk "${endpoint}" | grep -q 'FluidIntegrates'
  then
    echo "[INFO] Passed: helper_integrates_probe_curl on ${endpoint}"
  else
        echo "[ERROR] helper_integrates_probe_curl failed on ${endpoint}" \
    &&  return 1
  fi
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

function helper_integrates_mobile_version_playstore {
  local minutes
  local version

      minutes=$(
        printf "%05d" $((
        ($(date +%d | sed 's/^0//') -1) * 1440 +
        $(date +%H | sed 's/^0//') * 60 +
        $(date +%M | sed 's/^0//')
        ))
      ) \
  &&  version="$(date +%y%m)${minutes}" \
  &&  echo "${version}"
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
    DEFAULT_ORG \
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
    PRODUCT_PIPELINE_TOKEN \
    REDIS_SERVER \
    SQS_QUEUE_URL \
    STARLETTE_TEST_KEY \
    TEST_PROJECTS \
    ZENDESK_EMAIL \
    ZENDESK_SUBDOMAIN \
    ZENDESK_TOKEN
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
