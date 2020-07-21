# shellcheck shell=bash

function helper_use_pristine_workdir {
  export WORKDIR
  export STARTDIR

  function helper_teardown_workdir {
        echo "[INFO] Deleting: ${WORKDIR}" \
    &&  rm -rf "${WORKDIR}"
  }

      echo '[INFO] Creating a pristine workdir' \
  &&  rm -rf "${WORKDIR}" \
  &&  mkdir -p "${WORKDIR}" \
  &&  echo '[INFO] Copying files to workdir' \
  &&  cp -r "${STARTDIR}/." "${WORKDIR}" \
  &&  echo '[INFO] Entering the workdir' \
  &&  pushd "${WORKDIR}" \
  &&  echo '[INFO] Running: git clean -xdf' \
  &&  git clean -xdf \
  &&  trap 'helper_teardown_workdir' 'EXIT' \
  ||  return 1
}

function helper_use_regular_workdir {
  export STARTDIR

      echo '[INFO] Entering the workdir' \
  &&  pushd "${STARTDIR}" \
  ||  return 1
}

function helper_docker_build_and_push {
  local tag="${1}"
  local context="${2}"
  local dockerfile="${3}"
  local build_arg_1_key="${4:-build_arg_1_key}"
  local build_arg_1_val="${5:-build_arg_1_val}"
  local build_arg_2_key="${6:-build_arg_2_key}"
  local build_arg_2_val="${7:-build_arg_2_val}"
  local build_arg_3_key="${8:-build_arg_3_key}"
  local build_arg_3_val="${9:-build_arg_3_val}"
  local build_arg_4_key="${10:-build_arg_4_key}"
  local build_arg_4_val="${11:-build_arg_4_val}"
  local build_arg_5_key="${12:-build_arg_5_key}"
  local build_arg_5_val="${13:-build_arg_5_val}"
  local build_arg_6_key="${14:-build_arg_6_key}"
  local build_arg_6_val="${15:-build_arg_6_val}"
  local build_arg_7_key="${16:-build_arg_7_key}"
  local build_arg_7_val="${17:-build_arg_7_val}"
  local build_arg_8_key="${18:-build_arg_8_key}"
  local build_arg_8_val="${19:-build_arg_8_val}"
  local build_arg_9_key="${20:-build_arg_9_key}"
  local build_arg_9_val="${21:-build_arg_9_val}"
  local build_args=(
    --tag "${tag}"
    --file "${dockerfile}"
    --build-arg "${build_arg_1_key}=${build_arg_1_val}"
    --build-arg "${build_arg_2_key}=${build_arg_2_val}"
    --build-arg "${build_arg_3_key}=${build_arg_3_val}"
    --build-arg "${build_arg_4_key}=${build_arg_4_val}"
    --build-arg "${build_arg_5_key}=${build_arg_5_val}"
    --build-arg "${build_arg_6_key}=${build_arg_6_val}"
    --build-arg "${build_arg_7_key}=${build_arg_7_val}"
    --build-arg "${build_arg_8_key}=${build_arg_8_val}"
    --build-arg "${build_arg_9_key}=${build_arg_9_val}"
  )

      echo "[INFO] Logging into: ${CI_REGISTRY}" \
  &&  docker login \
        --username "${CI_REGISTRY_USER}" \
        --password "${CI_REGISTRY_PASSWORD}" \
      "${CI_REGISTRY}" \
  &&  echo "[INFO] Pulling: ${tag}" \
  &&  if docker pull "${tag}"
      then
        build_args+=( --cache-from "${tag}" )
      fi \
  &&  echo "[INFO] Building: ${tag}" \
  &&  docker build "${build_args[@]}" "${context}" \
  &&  echo "[INFO] Pushing: ${tag}" \
  &&  docker push "${tag}" \
  &&  echo "[INFO] Deleting local copy of: ${tag}" \
  &&  docker image remove "${tag}"
}

function helper_build_nix_caches_parallel {
  local num_provisioners
  local num_provisioners_per_group
  local num_provisioners_remaining
  export lower_limit
  export upper_limit

      num_provisioners=$(find build/provisioners/ -type f | wc -l) \
  &&  num_provisioners_per_group=$(( num_provisioners/CI_NODE_TOTAL )) \
  &&  num_provisioners_remaining=$(( num_provisioners%CI_NODE_TOTAL )) \
  &&  if [ "${num_provisioners_remaining}" -gt '0' ]
      then
        num_provisioners_per_group=$(( num_provisioners_per_group+=1 ))
      fi \
  &&  lower_limit=$(( (CI_NODE_INDEX-1)*num_provisioners_per_group )) \
  &&  upper_limit=$(( CI_NODE_INDEX*num_provisioners_per_group-1 )) \
  &&  upper_limit=$(( upper_limit > num_provisioners-1 ? num_provisioners-1 : upper_limit ))
}

function helper_get_gitlab_var {
  local gitlab_var_name="${1}"
      echo "[INFO] Retrieving var from GitLab: ${gitlab_var_name}" 1>&2 \
  &&  curl \
        --silent \
        --header "private-token: ${GITLAB_TOKEN}" \
        "${GITLAB_API_URL}/${gitlab_var_name}" \
      | jq -r '.value'
}

function helper_bootstrap_prod_ci {
  env_prepare_python_packages \
  &&  helper_set_prod_secrets \
  &&  if test "${IS_LOCAL_BUILD}" = "${FALSE}"
      then
        helper_set_local_dynamo_and_redis
      fi \

}

function helper_bootstrap_dev_ci {
  env_prepare_python_packages \
  &&  helper_set_dev_secrets \
  &&  if test "${IS_LOCAL_BUILD}" = "${FALSE}"
      then
        helper_set_local_dynamo_and_redis
      fi \

}

function helper_invoke_py {
  local module="${1}"
  export DJANGO_SETTINGS_MODULE='fluidintegrates.settings'
  export PYTHONPATH="${PWD}:${PWD}/analytics:${PYTHONPATH}"

      echo "[INFO] Waking up: ${module}" \
  &&  python3 \
        'django-apps/integrates-back-async/cli/invoker.py' \
        "${module}" \

}

function helper_get_gitlab_registry_id {
  local registry_name="${1}"

  wget -O - "https://gitlab.com/api/v4/projects/${CI_PROJECT_ID}/registry/repositories" \
    | jq ".[] | select (.name == \"${registry_name}\") | .id"
}

function helper_get_touched_files_in_last_commit {
  git diff --name-only "${CI_COMMIT_BEFORE_SHA}" "${CI_COMMIT_SHA}" \
    | while read -r path
      do
        ! test -e "${path}" || echo "${path}"
      done
}

function helper_have_any_file_changed {
  local file
  local files=( "$@" )
  local canon_file_a
  local canon_file_b

      helper_get_touched_files_in_last_commit > "${TEMP_FD}" \
  &&  while read -r touched_file
      do
        for file in "${files[@]}"
        do
              canon_file_a=$(readlink -f "${touched_file}") \
          &&  canon_file_b=$(readlink -f "${file}") \
          &&  if [[ "${canon_file_a}" == "${canon_file_b}"* ]]
              then
                echo "${canon_file_a}"
                echo "${canon_file_b}"
                return 0
              else
                continue
              fi
        done || :
      done < "${TEMP_FD}" \
  &&  return 1
}

function helper_is_today_wednesday {
  test "$(date +%A)" == 'Wednesday'
}

function helper_is_today_first_day_of_month {
  test "$(date +%d)" == '01'
}

function helper_list_declared_jobs {
  declare -F | sed 's/declare -f //' | grep -P '^job_[a-z_]+' | sed 's/job_//' | sort
}

function helper_list_vars_with_regex {
  local regex="${1}"
  printenv | grep -oP "${regex}" | sort
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
          -Djava.library.path="${STARTDIR}/.DynamoDB/DynamoDBLocal_lib" \
          -jar "${STARTDIR}/.DynamoDB/DynamoDBLocal.jar" \
          -inMemory \
          -port "${port_dynamo}" \
          -sharedDb \
          &
        processes_to_kill+=( "$!" )
      } \
  &&  echo '[INFO] Waiting 5 seconds to leave DynamoDB start' \
  &&  sleep 5 \
  &&  echo '[INFO] Populating DynamoDB local' \
  &&  bash ./deploy/containers/common/vars/provision_local_db.sh \

}

function helper_set_dev_secrets {
  export JWT_TOKEN
  export AWS_ACCESS_KEY_ID
  export AWS_SECRET_ACCESS_KEY
  export AWS_DEFAULT_REGION

      AWS_ACCESS_KEY_ID="${DEV_AWS_ACCESS_KEY_ID}" \
  &&  AWS_SECRET_ACCESS_KEY="${DEV_AWS_SECRET_ACCESS_KEY}" \
  &&  AWS_DEFAULT_REGION='us-east-1' \
  &&  aws configure set aws_access_key_id "${AWS_ACCESS_KEY_ID}" \
  &&  aws configure set aws_secret_access_key "${AWS_SECRET_ACCESS_KEY}" \
  &&  aws configure set region 'us-east-1' \
  &&  echo '[INFO] Exporting development secrets' \
  &&  sops_vars development
}

function helper_set_prod_secrets {
  export JWT_TOKEN
  export AWS_ACCESS_KEY_ID
  export AWS_SECRET_ACCESS_KEY
  export AWS_DEFAULT_REGION

      AWS_ACCESS_KEY_ID="${PROD_AWS_ACCESS_KEY_ID}" \
  &&  AWS_SECRET_ACCESS_KEY="${PROD_AWS_SECRET_ACCESS_KEY}" \
  &&  AWS_DEFAULT_REGION='us-east-1' \
  &&  aws configure set aws_access_key_id "${AWS_ACCESS_KEY_ID}" \
  &&  aws configure set aws_secret_access_key "${AWS_SECRET_ACCESS_KEY}" \
  &&  aws configure set region 'us-east-1' \
  &&  echo '[INFO] Exporting production secrets' \
  &&  sops_vars production \
  &&  export DEBUG="True" \
  &&  export ENVIRONMENT='development' \
  &&  export REDIS_SERVER='localhost' \

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

function helper_serve_back {
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

function helper_functional_tests {
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

reg_registry_id() {
  # Get the id of a gitlab registry
  # e.g reg_registry_id deps-base

  local registry_name="$1"
  local integrates_id='4620828'
  local check_url

      check_url="https://gitlab.com/api/v4/projects/${integrates_id}/registry/repositories" \
  &&  wget -O - "${check_url}" 2> /dev/null | jq ".[] | select (.name == \"${registry_name}\") | .id"
}

reg_registry_delete() {
  # Delete registry
  # e.g: reg_registry_delete deps-production TOKEN

  local registry_name="$1"
  local token="$2"
  local registry_id
  local delete_url

      registry_id=$(reg_registry_id "${registry_name}") \
  &&  delete_url="https://gitlab.com/api/v4/projects/4620828/registry/repositories/${registry_id}" \
  &&  curl --request DELETE --header "PRIVATE-TOKEN: ${token}" "${delete_url}"
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

minutes_of_month () {
  # Returns minutes that have passed during the current month

  local minutes_of_passed_days
  local minutes_of_passed_hours
  local minutes_of_current_hour
  local minutes_of_month

      minutes_of_passed_days=$((
        ($(date +%d | sed 's/^0//') -1) * 1440
      )) \
  &&  minutes_of_passed_hours=$((
        $(date +%H | sed 's/^0//') * 60
      )) \
  &&  minutes_of_current_hour=$((
        $(date +%M | sed 's/^0//')
      )) \
  &&  minutes_of_month=$((
        minutes_of_passed_days +
        minutes_of_passed_hours +
        minutes_of_current_hour
      )) \
  &&  echo "${minutes_of_month}"
}

app_version () {
  # Return a version for integrates app

  local minutes

      minutes=$(minutes_of_month) \
  &&  echo "$(date +%y.%m.)${minutes}"
}

aws_login() {

  # Log in to aws for resources

  local user="$1"
  export TF_VAR_aws_access_key
  export TF_VAR_aws_secret_key
  export AWS_ACCESS_KEY_ID
  export AWS_SECRET_ACCESS_KEY

      if [ "${user}"  == 'production' ]; then
        if [ "${CI_COMMIT_REF_NAME}" == 'master' ]; then
              AWS_ACCESS_KEY_ID="${PROD_AWS_ACCESS_KEY_ID}" \
          &&  AWS_SECRET_ACCESS_KEY="${PROD_AWS_SECRET_ACCESS_KEY}"
        else
              echo 'Not enough permissions for logging in as production' \
          &&  return 1
        fi
      elif [ "${user}" == 'development' ]; then
            AWS_ACCESS_KEY_ID="${DEV_AWS_ACCESS_KEY_ID}" \
        &&  AWS_SECRET_ACCESS_KEY="${DEV_AWS_SECRET_ACCESS_KEY}"
      else
            echo 'No valid user was provided' \
        &&  return 1
      fi \
  &&  TF_VAR_aws_access_key="${AWS_ACCESS_KEY_ID}" \
  &&  TF_VAR_aws_secret_key="${AWS_SECRET_ACCESS_KEY}" \
  &&  aws configure set aws_access_key_id "${AWS_ACCESS_KEY_ID}" \
  &&  aws configure set aws_secret_access_key "${AWS_SECRET_ACCESS_KEY}"
}

get_sops_env() {
  local tmp_file
  local src='https://static-objects.gitlab.net/fluidattacks/public/raw/master/shared-scripts/sops.sh'

      tmp_file=$(mktemp) \
  &&  curl -sL "${src}" \
        > "${tmp_file}" \
  &&  echo "${tmp_file}"
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
    ROLLBAR_ACCESS_TOKEN \
    SQS_QUEUE_URL \
    TEST_PROJECTS \
    ZENDESK_EMAIL \
    ZENDESK_SUBDOMAIN \
    ZENDESK_TOKEN \

}
