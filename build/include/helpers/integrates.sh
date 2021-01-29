# shellcheck shell=bash


# Front

function helper_integrates_front_build {
      pushd front \
    &&  npm install \
    &&  < ../../build/patches/jquery-comments.diff \
          patch -p1 --binary node_modules/jquery-comments_brainkit/js/jquery-comments.js \
    &&  helper_integrates_deployment_date \
    &&  npm run build -- \
          --env CI_COMMIT_SHA="${CI_COMMIT_SHA}" \
          --env CI_COMMIT_SHORT_SHA="${CI_COMMIT_SHORT_SHA}" \
          --env INTEGRATES_DEPLOYMENT_DATE="${INTEGRATES_DEPLOYMENT_DATE}" \
  &&  popd \
  || return 1
}

function helper_integrates_front_deploy {
  local branch="${1}"
  local env="${2}"
  local source='app'
  local templates='back/app/templates/static'

      helper_integrates_aws_login "${env}" \
  &&  helper_install_c3 "${source}/static/external" \
  &&  cp -r "${templates}/"* "${source}/static/" \
  &&  aws s3 sync --delete \
        "${source}" \
        "s3://integrates.front.${env}.fluidattacks.com/${branch}/"
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
  local timeout="${6}"
  local files="${7}"

      helper_common_update_kubeconfig "${cluster}" "${region}" \
  &&  for file in $(helper_common_string_to_lines "${files}" '|')
      do
            grep -oP '__.*__' "${file}" | while IFS= read -r var
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

function helper_integrates_cloudflare_login {
  local user="${1}"
  export TF_VAR_cloudflare_api_token

      helper_common_sops_env "secrets-${user}.yaml" default \
        CLOUDFLARE_API_TOKEN \
  &&  TF_VAR_cloudflare_api_token="${CLOUDFLARE_API_TOKEN}"
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
  local port='6379'
  local pord_end='6381'
  local cluster_addrs=()
  local cluster_path='.Redis'

      echo '[INFO] Launching Redis' \
  &&  rm -rf "${cluster_path}" \
  &&  for port in $(seq "${port}" "${pord_end}")
      do
            echo "[INFO] Configuring replica ${port}" \
        &&  helper_common_kill_pid_listening_on_port "${port}" \
        &&  mkdir -p "${cluster_path}/${port}" \
        &&  pushd "${cluster_path}/${port}" \
          &&  {
                    echo 'appendonly yes' \
                &&  echo 'cluster-config-file nodes.conf' \
                &&  echo 'cluster-enabled yes' \
                &&  echo 'cluster-node-timeout 5000' \
                &&  echo 'cluster-slave-validity-factor 1' \
                &&  echo "port ${port}" \

              } > redis.conf \
          &&  { redis-server redis.conf & } \
        &&  popd \
        &&  cluster_addrs+=( "127.0.0.1:${port}" ) \
        ||  return 1
      done \
  &&  sleep 1 \
  &&  redis-cli \
        --cluster create "${cluster_addrs[@]}" \
        --cluster-replicas 0 \
        --cluster-yes \

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
    --backlog '512'  #  The maximum number of pending connections. [2048]
    --forwarded-allow-ips="${forwarded_ips}"  # Front-end's IPs from which allowed to handle set secure headers. [127.0.0.1]
    --graceful-timeout '30'  # Timeout for graceful workers restart. [30]
    --log-level 'info'  # The granularity of Error log outputs. [info]
    --max-requests '64'  # The maximum number of requests a worker will process before restarting. [0]
    --max-requests-jitter '32'  # The maximum jitter to add to the max_requests setting. [0]
    --timeout '60'  # Workers silent for more than this many seconds are killed and restarted. [30]
    --workers "${workers}"  # The number of worker processes for handling requests. [1]
    --worker-class "${worker_class}"  # The type of workers to use. [sync]
    --worker-connections '512'  # The maximum number of simultaneous clients. [1000]
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
        "${data_path}/fluidintegrates.analytics/${CI_COMMIT_REF_NAME}" \
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
