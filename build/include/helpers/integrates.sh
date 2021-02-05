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

# Back

function helper_integrates_back_build {
  local branch="${1}"
  local context='.'
  local dockerfile='integrates/deploy/containers/app/Dockerfile'
  local use_cache='false'
  local base_image='registry.gitlab.com/fluidattacks/product/nix:integrates_serve_components'
  local base_provisioner='build/provisioners/integrates_serve_components.nix'

  helper_common_docker_build_and_push \
    "${CI_REGISTRY_IMAGE}/app:${branch}" \
    "${context}" \
    "${dockerfile}" \
    "${use_cache}" \
    'PROVISIONER' "${base_provisioner}" \
    'BASE' "${base_image}"
}

function helper_integrates_back_deploy {
  local region="${1}"
  local cluster="${2}"
  local namespace="${3}"
  local deployment="${4}"
  local timeout="${5}"
  local files_path="${6}"

      helper_common_update_kubeconfig "${cluster}" "${region}" \
  &&  for file in $(find "${files_path}/"*)
      do
            vars="$(grep -oP '__.*__' "${file}" || true)" \
        &&  for var in ${vars}
            do
                  var="${var:2:-2}" \
              &&  helper_common_replace_var \
                    "__${var}__" \
                    "${!var}" \
                    "${file}" \
              ||  return 1
            done \
        &&  echo "[INFO] Applying: ${file}" \
        &&  kubectl apply -f "${file}" \
        ||  return 1
      done \
  &&  kubectl rollout status \
        "deploy/integrates-${deployment}" \
        -n "${namespace}" \
        --timeout="${timeout}"
}

function helper_integrates_back_deploy_newrelic {
      helper_common_sops_env 'secrets-production.yaml' 'default' \
        NEW_RELIC_API_KEY \
        NEW_RELIC_APP_ID \
  &&  curl "https://api.newrelic.com/v2/applications/${NEW_RELIC_APP_ID}/deployments.json" \
    --request 'POST' \
    --header "X-Api-Key: ${NEW_RELIC_API_KEY}" \
    --header 'Content-Type: application/json' \
    --include \
    --data "{
        \"deployment\": {
          \"revision\": \"${CI_COMMIT_SHA}\",
          \"changelog\": \"${CHANGELOG}\",
          \"description\": \"production\",
          \"user\": \"${CI_COMMIT_AUTHOR}\"
        }
      }"
}

function helper_integrates_back_deploy_checkly {
  local checkly_params

      helper_common_sops_env 'secrets-production.yaml' 'default' \
        CHECKLY_CHECK_ID \
        CHECKLY_TRIGGER_ID \
  &&  checkly_params="${CHECKLY_TRIGGER_ID}?deployment=true&repository=product/integrates&sha=${CI_COMMIT_SHA}" \
  &&  curl \
        --request 'GET' \
        "https://api.checklyhq.com/check-groups/${CHECKLY_CHECK_ID}/trigger/${checkly_params}"
}

function helper_integrates_back_build_lambda {
  local lambda_name="${1}"
  local lambda_zip_file
  local current_path="${PWD}/lambda"
  local path_to_lambda="${current_path}/${lambda_name}"
  local path_to_lambda_venv="${current_path}/.venv.${lambda_name}"

  # shellcheck disable=SC1091
      lambda_zip_file="$(mktemp -d)/${lambda_name}.zip" \
  &&  echo '[INFO] Creating virtual environment' \
  &&  python3 -m venv --clear "${path_to_lambda_venv}" \
  &&  pushd "${path_to_lambda_venv}" \
    &&  echo '[INFO] Entering virtual environment' \
    &&  source './bin/activate' \
      &&  echo '[INFO] Installing dependencies' \
      &&  pip3 install -U setuptools==41.4.0 wheel==0.33.6 \
      &&  if test -f "${path_to_lambda}/requirements.txt"
          then
            pip3 install -r "${path_to_lambda}/requirements.txt"
          fi \
    &&  deactivate \
    &&  echo '[INFO] Exiting virtual environment' \
    &&  pushd "${path_to_lambda_venv}/lib/python3.7/site-packages" \
      &&  zip -r9 "${lambda_zip_file}" . \
    &&  popd \
    &&  pushd "${path_to_lambda}" \
      &&  zip -r -g "${lambda_zip_file}" ./* \
      &&  mv "${lambda_zip_file}" "${current_path}/packages" \
    && popd \
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

function helper_integrates_serve_front {
      helper_integrates_deployment_date \
  &&  pushd front \
        &&  npm install \
        &&  { npm start & } \
  &&  popd \
  ||  return 1
}

function helper_integrates_serve_redis {
      { integrates-cache & } \
  &&  makes-wait 60 localhost:26379
}

function helper_integrates_serve_dynamo {
      { integrates-db & } \
  &&  makes-wait 60 localhost:28022
}

function helper_integrates_serve_minio {
      { integrates-storage & } \
  &&  makes-wait 120 localhost:29000
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
    COMMUNITY_PROJECTS \
    CLOUDFRONT_ACCESS_KEY \
    CLOUDFRONT_PRIVATE_KEY \
    CLOUDFRONT_RESOURCES_DOMAIN \
    CLOUDFRONT_REPORTS_DOMAIN \
    CLOUDMERSIVE_API_KEY \
    DEBUG \
    DEFAULT_ORG \
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
    MIXPANEL_API_TOKEN \
    NEW_RELIC_API_KEY \
    NEW_RELIC_APP_ID \
    NEW_RELIC_LICENSE_KEY \
    NEW_RELIC_ENVIRONMENT \
    REDIS_SERVER \
    SQREEN_TOKEN \
    SQS_QUEUE_URL \
    STARLETTE_SESSION_KEY \
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

function helper_install_c3 {
  local path="${1}"

      echo '[INFO] Unzipping C3 local' \
  &&  mkdir -p "${path}/C3" \
  &&  pushd "${path}/C3" \
    &&  unzip -ou "${srcExternalC3}" \
  && popd \
  ||  return 1
}
