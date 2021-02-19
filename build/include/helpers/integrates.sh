# shellcheck shell=bash


# Mobile

function helper_integrates_mobile_deploy_ota {
  local env="${1}"
  local release_channel="${2}"

  local app_version
  local version_code

      echo '[INFO] Logging in to AWS' \
  &&  app_version="$(helper_integrates_mobile_version basic)" \
  &&  version_code="$(helper_integrates_mobile_version code)" \
  &&  helper_integrates_deployment_date \
  &&  helper_common_sops_env "secrets-${env}.yaml" 'default' \
        EXPO_USER \
        EXPO_PASS \
  &&  sops \
        --aws-profile default \
        --decrypt \
        --extract '["GOOGLE_SERVICES_APP"]' \
        --output 'mobile/google-services.json' \
        --output-type 'json' \
        "secrets-${env}.yaml" \
  &&  echo '[INFO] Installing deps' \
  &&  pushd mobile \
    &&  echo '[INFO] Using NodeJS '"$(node -v)"'' \
    &&  npm install \
    &&  npx --no-install expo login \
          --username "${EXPO_USER}" \
          --password "${EXPO_PASS}" \
          --non-interactive \
    &&  echo '[INFO] Replacing versions' \
    &&  sed -i "s/__CI_COMMIT_SHA__/${CI_COMMIT_SHA}/g" ./app.json \
    &&  sed -i "s/__CI_COMMIT_SHORT_SHA__/${CI_COMMIT_SHORT_SHA}/g" ./app.json \
    &&  sed -i "s/__INTEGRATES_DEPLOYMENT_DATE__/${INTEGRATES_DEPLOYMENT_DATE}/g" ./app.json \
    &&  sed -i "s/__APP_VERSION__/${app_version}/g" ./app.json \
    &&  sed -i "s/\"versionCode\": 0/\"versionCode\": ${version_code}/g" ./app.json \
    &&  echo '[INFO] Publishing update' \
    &&  npx --no-install expo publish \
          --non-interactive \
          --release-channel "${release_channel}" \
    &&  echo '[INFO] Sending build info to bugsnag' \
    &&  npx bugsnag-build-reporter \
          --api-key c7b947a293ced0235cdd8edc8c09dad4 \
          --app-version "${CI_COMMIT_SHORT_SHA}" \
          --release-stage "mobile-${env}" \
          --builder-name "${CI_COMMIT_AUTHOR}" \
          --source-control-provider gitlab \
          --source-control-repository https://gitlab.com/fluidattacks/product.git \
          --source-control-revision "${CI_COMMIT_SHA}/integrates/mobile" \
  &&  popd \
  ||  return 1
}

# Others

function helper_integrates_aws_login {
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
  &&  helper_integrates_serve_redis
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
  export PYTHONPATH="${PWD}:${PWD}/analytics:${PYTHONPATH}"

      echo "[INFO] Waking up: ${module}" \
  &&  python3 \
        'back/packages/integrates-back/cli/invoker.py' \
        "${module}"
}

function helper_integrates_serve_redis {
  DAEMON=true integrates-cache
}

function helper_integrates_serve_dynamo {
  DAEMON=true integrates-db
}

function helper_integrates_serve_minio {
  DAEMON=true integrates-storage
}

function helper_integrates_mobile_version {
  local minutes

      minutes=$(
        printf "%05d" $((
        ($(date +%d | sed 's/^0//') -1) * 1440 +
        $(date +%H | sed 's/^0//') * 60 +
        $(date +%M | sed 's/^0//')
        ))
      ) \
  &&  if [ "$1" = "basic" ]; then
            echo "$(date +%y.%m.)${minutes}"
      elif [ "$1" = "code" ]; then
            echo "$(date +%y%m)${minutes}"
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
    AZUREAD_OAUTH2_KEY \
    AZUREAD_OAUTH2_SECRET \
    BITBUCKET_OAUTH2_KEY \
    BITBUCKET_OAUTH2_SECRET \
    BUGSNAG_ACCESS_TOKEN \
    BUGSNAG_API_KEY_SCHEDULER \
    CLOUDFRONT_ACCESS_KEY \
    CLOUDFRONT_PRIVATE_KEY \
    CLOUDFRONT_REPORTS_DOMAIN \
    CLOUDFRONT_RESOURCES_DOMAIN \
    CLOUDMERSIVE_API_KEY \
    COMMUNITY_PROJECTS \
    DEBUG \
    DEFAULT_ORG \
    DYNAMODB_HOST \
    DYNAMODB_PORT \
    ENVIRONMENT \
    GOOGLE_OAUTH2_KEY \
    GOOGLE_OAUTH2_SECRET \
    JWT_ENCRYPTION_KEY \
    JWT_SECRET \
    JWT_SECRET_API \
    MAIL_CONTINUOUS \
    MAIL_PRODUCTION \
    MAIL_PROJECTS \
    MAIL_RESOURCERS \
    MAIL_REVIEWERS \
    MANDRILL_APIKEY \
    MIXPANEL_API_TOKEN \
    NEW_RELIC_API_KEY \
    NEW_RELIC_APP_ID \
    NEW_RELIC_ENVIRONMENT \
    NEW_RELIC_LICENSE_KEY \
    REDIS_SERVER \
    SQS_QUEUE_URL \
    STARLETTE_SESSION_KEY \
    TEST_PROJECTS \
    ZENDESK_EMAIL \
    ZENDESK_SUBDOMAIN \
    ZENDESK_TOKEN
}
