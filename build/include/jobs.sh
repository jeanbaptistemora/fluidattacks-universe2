# shellcheck shell=bash

source "${srcIncludeHelpers}"
source "${srcExternalGitlabVariables}"
source "${srcExternalSops}"
source "${srcCiScriptsHelpersSops}"

function job_build_django_apps {
  local app

  for app in 'django-apps/integrates-'*; do
        echo "[INFO] Building: ${app}" \
    &&  pushd "${app}" \
      &&  python3 setup.py sdist -d ../packages/ \
    &&  popd
  done \
  ||  return 1
}

function job_build_front {
      echo '[INFO] Logging in to AWS' \
  &&  aws_login "${ENVIRONMENT_NAME}" \
  &&  sops_vars "${ENVIRONMENT_NAME}" \
  &&  pushd front \
    &&  npm install \
    &&  npm run build \
  &&  popd \
  &&  sed --in-place \
        "s/integrates_version/v. ${FI_VERSION}/g" \
        'app/assets/dashboard/app-bundle.min.js'
}

function job_build_lambdas {

  function _job_build_lambdas {
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

      _job_build_lambdas 'send_mail_new_vulnerabilities' \
  &&  _job_build_lambdas 'project_to_pdf'
}

function job_coverage_report {
      echo '[INFO] Logging in to AWS' \
  &&  aws_login "${ENVIRONMENT_NAME}" \
  &&  sops_env "secrets-${ENVIRONMENT_NAME}.yaml" 'default' \
        CODECOV_TOKEN \
  &&  codecov
}

function job_clean_registries {
  local registry_name='deps-app'
  local registry_id

  if helper_is_today_first_day_of_month
  then
        echo '[INFO] Cleaning registries' \
    &&  CI_COMMIT_REF_NAME='master' aws_login 'production' \
    &&  sops_env 'secrets-production.yaml' 'default' \
          GITLAB_API_TOKEN \
    &&  echo "[INFO] Computing registry ID for: ${registry_name}" \
    &&  registry_id=$(helper_get_gitlab_registry_id "${registry_name}") \
    &&  echo "[INFO] Deleting registry ID: ${registry_id}" \
    &&  curl "https://gitlab.com/api/v4/projects/${CI_PROJECT_ID}/registry/repositories/${registry_id}" \
          --request 'DELETE' \
          --header "private-token: ${GITLAB_API_TOKEN}"
  else
        echo '[INFO] Skipping, this is only meant to be run on first of each month' \
    &&  return 0
  fi
}

function job_deploy_container_nix_caches {
  local context='.'
  local dockerfile='build/Dockerfile'
  local provisioner
  local provisioner_path

      helper_use_pristine_workdir \
  &&  for provisioner_path in ./build/provisioners/*
      do
            provisioner=$(basename "${provisioner_path}") \
        &&  provisioner="${provisioner%.*}" \
        &&  helper_docker_build_and_push \
              "${CI_REGISTRY_IMAGE}/nix:${provisioner}" \
              "${context}" \
              "${dockerfile}" \
              'PROVISIONER' "${provisioner}" \
        ||  return 1
      done
}

function job_deploy_container_deps_app {
  local context='.'
  local dockerfile='deploy/containers/deps-app/Dockerfile'
  local tag="${CI_REGISTRY_IMAGE}/deps-app:${CI_COMMIT_REF_NAME}"

      helper_use_pristine_workdir \
  &&  helper_docker_build_and_push \
        "${tag}" \
        "${context}" \
        "${dockerfile}"
}

function job_deploy_container_deps_mobile {
  local context='.'
  local dockerfile='deploy/containers/deps-mobile/Dockerfile'
  local tag="${CI_REGISTRY_IMAGE}/deps-mobile:${CI_COMMIT_REF_NAME}"

      helper_use_pristine_workdir \
  &&  helper_docker_build_and_push \
        "${tag}" \
        "${context}" \
        "${dockerfile}"
}

function job_deploy_container_app {
  local context='.'
  local dockerfile='deploy/containers/app/Dockerfile'
  local tag="${CI_REGISTRY_IMAGE}/app:${CI_COMMIT_REF_NAME}"

      echo '[INFO] Remember that this job needs: build_lambdas' \
  &&  echo '[INFO] Remember that this job needs: build_django_apps' \
  &&  echo '[INFO] Computing Fluid Integrates version' \
  &&  echo -n "${FI_VERSION}" > 'version.txt' \
  &&  echo '[INFO] Logging in to AWS' \
  &&  aws_login "${ENVIRONMENT_NAME}" \
  &&  sops_env "secrets-${ENVIRONMENT_NAME}.yaml" 'default' \
        SSL_KEY \
        SSL_CERT \
        DRIVE_AUTHORIZATION \
        DRIVE_AUTHORIZATION_CLIENT \
  &&  helper_docker_build_and_push \
        "${tag}" \
        "${context}" \
        "${dockerfile}" \
        'CI_API_V4_URL' "${CI_API_V4_URL}" \
        'CI_COMMIT_REF_NAME' "${CI_COMMIT_REF_NAME}" \
        'CI_PROJECT_ID' "${CI_PROJECT_ID}" \
        'CI_REPOSITORY_URL' "${CI_REPOSITORY_URL}" \
        'SSL_CERT' "${SSL_CERT}" \
        'SSL_KEY' "${SSL_KEY}" \
        'VERSION' "${FI_VERSION}"
}

function job_deploy_container_app_async {
  local context='.'
  local dockerfile='deploy/containers/app-async/Dockerfile'
  local tag="${CI_REGISTRY_IMAGE}/app-async:${CI_COMMIT_REF_NAME}"

      echo '[INFO] Remember that this job needs: build_lambdas' \
  &&  echo '[INFO] Remember that this job needs: build_django_apps' \
  &&  echo '[INFO] Computing Fluid Integrates version' \
  &&  echo -n "${FI_VERSION}" > 'version.txt' \
  &&  echo '[INFO] Logging in to AWS' \
  &&  aws_login "${ENVIRONMENT_NAME}" \
  &&  sops_env "secrets-${ENVIRONMENT_NAME}.yaml" 'default' \
        SSL_KEY \
        SSL_CERT \
        DRIVE_AUTHORIZATION \
        DRIVE_AUTHORIZATION_CLIENT \
  &&  helper_docker_build_and_push \
        "${tag}" \
        "${context}" \
        "${dockerfile}" \
        'CI_API_V4_URL' "${CI_API_V4_URL}" \
        'CI_COMMIT_REF_NAME' "${CI_COMMIT_REF_NAME}" \
        'CI_PROJECT_ID' "${CI_PROJECT_ID}" \
        'CI_REPOSITORY_URL' "${CI_REPOSITORY_URL}" \
        'ENV_NAME' "${ENVIRONMENT_NAME}" \
        'SSL_CERT' "${SSL_CERT}" \
        'SSL_KEY' "${SSL_KEY}" \
        'VERSION' "${FI_VERSION}"
}

function job_deploy_front {
        aws_login "${ENVIRONMENT_NAME}" \
    &&  sops_vars "${ENVIRONMENT_NAME}" \
    &&  ./manage.py collectstatic --no-input
}

function job_deploy_mobile {
      helper_use_pristine_workdir \
  &&  if  helper_have_any_file_changed \
            'mobile/'
      then
            echo '[INFO] Veryfing if we should set fs.inotify.max_user_watches' \
        &&  if test "${IS_LOCAL_BUILD}" = "${FALSE}"
            then
                  echo '[INFO] Setting: fs.inotify.max_user_watches=524288' \
              &&  echo 'fs.inotify.max_user_watches=524288' \
                    >> /etc/sysctl.conf \
              &&  sysctl -p
            else
                  echo '[INFO] Local build, skipping...'
            fi \
        &&  echo '[INFO] Logging in to AWS' \
        &&  aws_login "${ENVIRONMENT_NAME}" \
        &&  sops_env "secrets-${ENVIRONMENT_NAME}.yaml" 'default' \
              EXPO_USER \
              EXPO_PASS \
              ROLLBAR_ACCESS_TOKEN \
        &&  sops \
              --aws-profile default \
              --decrypt \
              --extract '["GOOGLE_SERVICES_APP"]' \
              --output 'mobile/google-services.json' \
              --output-type 'json' \
              "secrets-${ENVIRONMENT_NAME}.yaml" \
        &&  echo '[INFO] Installing deps' \
        &&  pushd mobile \
          &&  npm install \
          &&  npx expo login -u "${EXPO_USER}" -p "${EXPO_PASS}" \
          &&  echo '[INFO] Replacing versions' \
          &&  sed -i "s/integrates_version/${FI_VERSION}/g" ./app.json \
          &&  sed -i "s/\"versionCode\": 0/\"versionCode\": ${FI_VERSION_MOBILE}/g" ./app.json \
          &&  echo '[INFO] Publishing update' \
          &&  npx expo publish \
                --release-channel "${CI_COMMIT_REF_NAME}" --non-interactive \
          &&  if test "${ENVIRONMENT_NAME}" = 'production'
              then
                    echo '[INFO] Sending report to rollbar' \
                &&  curl "https://api.rollbar.com/api/1/deploy" \
                      --form "access_token=${ROLLBAR_ACCESS_TOKEN}" \
                      --form 'environment=production' \
                      --form "revision=${CI_COMMIT_SHA}" \
                      --form "local_username=${CI_COMMIT_REF_NAME}"
              fi \
        &&  popd
      else
            echo '[INFO] No relevant files were modified, skipping deploy' \
        &&  return 0
      fi
}

function _job_functional_tests {
      echo '[INFO] Logging in to AWS' \
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

function job_functional_tests_local {
  _job_functional_tests
}

function job_functional_tests_dev {
  CI='true' _job_functional_tests
}

function job_functional_tests_prod {
  CI_COMMIT_REF_NAME='master' _job_functional_tests
}

function job_renew_certificates {
  local certificate='ssl-review-apps'
  local certificate_issuer='letsencrypt'
  local secret_name='ssl-certificate'
  local RA_ACCESS_KEY
  local files=(
    review-apps/tls.yaml
  )
  local vars_to_replace_in_manifest=(
    CI_PROJECT_NAME
    DNS_ZONE_ID
    RA_ACCESS_KEY
  )

  if helper_is_today_wednesday
  then
    # shellcheck disable=SC2034
        aws_login 'development' \
    &&  echo '[INFO] Setting context' \
    &&  kubectl config \
          set-context "$(kubectl config current-context)" \
          --namespace="${CI_PROJECT_NAME}" \
    &&  echo '[INFO] Computing secrets' \
    &&  RA_ACCESS_KEY="${AWS_ACCESS_KEY_ID}" \
    &&  echo '[INFO] Replacing secrets' \
    &&  for file in "${files[@]}"
        do
          for var in "${vars_to_replace_in_manifest[@]}"
          do
                rpl "__${var}__" "${!var}" "${file}" \
            |&  grep 'Replacing' \
            |&  sed -E 's/with.*$//g' \
            ||  return 1
          done
        done \
    &&  echo '[INFO] Deleting current resources' \
    &&  kubectl delete secret "${secret_name}" \
    &&  kubectl delete issuer "${certificate_issuer}" \
    &&  kubectl delete certificate "${certificate}" \
    &&  echo '[INFO] Applying: review-apps/tls.yaml' \
    &&  kubectl apply -f 'review-apps/tls.yaml' \
    &&  while ! kubectl describe certificate "${certificate}" \
          | tr -s ' ' \
          | grep 'Status: True'
        do
              echo '[INFO] Still issuing certificate, sleeping 10 seconds...' \
          &&  sleep 10 \
          ||  return 1
        done
  else
        echo '[INFO] Skipping, this is only meant to be run on wednesday' \
    &&  return 0
  fi
}

function job_serve_dynamodb_local {
  local port=8022

      echo '[INFO] Launching DynamoDB local' \
  &&  {
        java \
          -Djava.library.path="${STARTDIR}/.DynamoDB/DynamoDBLocal_lib" \
          -jar "${STARTDIR}/.DynamoDB/DynamoDBLocal.jar" \
          -inMemory \
          -port "${port}" \
          -sharedDb \
        &
      } \
  &&  echo '[INFO] Waiting 5 seconds to leave DynamoDB start' \
  &&  sleep 5 \
  &&  echo '[INFO] Populating DynamoDB local' \
  &&  bash ./deploy/containers/common/vars/provision_local_db.sh \
  &&  echo "[INFO] DynamoDB is ready and listening on port ${port}!" \
  &&  echo "[INFO] Hit Ctrl+C to exit" \
  &&  fg %1
}

function job_send_new_release_email {
      CI_COMMIT_REF_NAME=master aws_login 'production' \
  &&  sops_env "secrets-production.yaml" default \
        MANDRILL_APIKEY \
        MANDRILL_EMAIL_TO \
  &&  curl -Lo \
        "${TEMP_FILE1}" \
        'https://static-objects.gitlab.net/fluidattacks/public/raw/master/shared-scripts/mail.py' \
  &&  echo "send_mail('new_version', MANDRILL_EMAIL_TO,
        context={'project': PROJECT, 'project_url': '$CI_PROJECT_URL',
          'version': _get_version_date(), 'message': _get_message()},
        tags=['general'])" >> "${TEMP_FILE1}" \
  &&  python3 "${TEMP_FILE1}"
}

function job_serve_front {
      pushd front \
    &&  npm install \
    &&  npm start \
  &&  popd \
  ||  return 1
}

function job_serve_redis {
  local port=6379

      echo "[INFO] Serving redis on port ${port}" \
  &&  redis-server --port "${port}"
}

function job_serve_back_async_dev {
  local app='fluidintegrates.asgi:application'
  local host='0.0.0.0'
  local port='9090'
  local root_path='/integrates'
  local workers='4'

      helper_set_dev_secrets \
  &&  echo "[INFO] Serving async back on port ${port}" \
  &&  uvicorn \
        --host="${host}" \
        --port="${port}" \
        --root-path="${root_path}" \
        --ssl-certfile="${srcDerivationsCerts}/fluidla.crt" \
        --ssl-keyfile="${srcDerivationsCerts}/fluidla.key" \
        --header="Access-Control-Allow-Origin:*" \
        --header="Access-Control-Allow-Headers:*" \
        --workers="${workers}" \
        --reload \
        "${app}"
}

function job_serve_back_dev {
  local app='fluidintegrates.asgi:application'
  local host='0.0.0.0'
  local port='8080'
  local root_path='/integrates'
  local workers='4'

      helper_set_dev_secrets \
  &&  echo "[INFO] Serving back on port ${port}" \
  &&  uvicorn \
        --host="${host}" \
        --port="${port}" \
        --root-path="${root_path}" \
        --ssl-certfile="${srcDerivationsCerts}/fluidla.crt" \
        --ssl-keyfile="${srcDerivationsCerts}/fluidla.key" \
        --workers="${workers}" \
        --reload \
        "${app}"
}

function job_lint_back {
      prospector -F -s high -u django -i node_modules app \
  &&  prospector -F -s high -u django -i node_modules django-apps/integrates-back/backend/ \
  &&  prospector -F -s high -u django -i node_modules django-apps/integrates-back-async/backend/ \
  &&  prospector -F -s veryhigh -u django -i node_modules fluidintegrates \
  &&  prospector -F -s veryhigh lambda \
  &&  mypy --ignore-missing-imports \
        django-apps/integrates-back/backend/mailer.py \
        django-apps/integrates-back/backend/scheduler.py \
        django-apps/integrates-back/backend/services.py \
        django-apps/integrates-back/backend/util.py \
        django-apps/integrates-back/backend/exceptions.py \
        django-apps/integrates-back/backend/decorators.py \
        django-apps/integrates-back/backend/entity/resource.py \
        django-apps/integrates-back/backend/entity/user.py \
        django-apps/integrates-back/backend/entity/vulnerability.py \
        django-apps/integrates-back/backend/typing.py \
        django-apps/integrates-back/backend/domain/* \
        django-apps/integrates-back/backend/dal/* \
        django-apps/integrates-back/backend/utils/* \
  &&  npx graphql-schema-linter \
        --except 'enum-values-all-caps,enum-values-have-descriptions,fields-are-camel-cased,fields-have-descriptions,input-object-values-are-camel-cased,relay-page-info-spec,types-have-descriptions' \
        django-apps/integrates-back-async/backend/api/schemas/*
}

function job_lint_build_system {
  # SC1090: Can't follow non-constant source. Use a directive to specify location.
  # SC2016: Expressions don't expand in single quotes, use double quotes for that.
  # SC2153: Possible misspelling: TEMP_FILE2 may not be assigned, but TEMP_FILE1 is.
  # SC2154: var is referenced but not assigned.

      nix-linter --recursive . \
  && echo '[OK] Nix code is compliant'
      shellcheck --external-sources build.sh \
  && find 'build' -name '*.sh' -exec \
      shellcheck --external-sources --exclude=SC1090,SC2016,SC2153,SC2154 {} + \
  && echo '[OK] Shell code is compliant'
}

function job_lint_front {
      pushd front \
    &&  npm install \
    &&  npm run audit \
    &&  npm run lint \
  &&  popd \
  ||  return 1
}

function job_lint_mobile {
      pushd mobile \
    &&  npm install \
    &&  npm run lint \
  &&  popd \
  ||  return 1
}

function job_infra_backup_deploy {
  export TF_VAR_db_user
  export TF_VAR_db_password

      echo '[INFO] Logging in to AWS production' \
  &&  CI_COMMIT_REF_NAME=master aws_login production \
  &&  sops_env 'secrets-production.yaml' 'default' \
        DB_USER \
        DB_PASSWD \
  &&  TF_VAR_db_user="${DB_USER}" \
  &&  TF_VAR_db_password="${DB_PASSWD}" \
  &&  pushd deploy/backup/terraform \
    &&  terraform init \
    &&  terraform apply -auto-approve -refresh=true \
  &&  popd \
  || return 1
}

function job_infra_backup_test {
      echo '[INFO] Logging in to AWS development' \
  &&  aws_login development \
  &&  pushd deploy/backup/terraform \
    &&  terraform init \
    &&  tflint --deep --module \
    &&  terraform plan -refresh=true \
  &&  popd \
  || return 1
}

function job_infra_cache_db_deploy {
      echo '[INFO] Logging in to AWS production' \
  &&  CI_COMMIT_REF_NAME=master aws_login production \
  &&  pushd deploy/cache-db/terraform \
    &&  terraform init \
    &&  terraform apply -auto-approve -refresh=true \
  &&  popd \
  || return 1
}

function job_infra_cache_db_test {
      echo '[INFO] Logging in to AWS development' \
  &&  aws_login development \
  &&  pushd deploy/cache-db/terraform \
    &&  terraform init \
    &&  tflint --deep --module \
    &&  terraform plan -refresh=true \
  &&  popd \
  || return 1
}

function job_infra_django_db_deploy {
  export TF_VAR_db_user
  export TF_VAR_db_password

      echo '[INFO] Logging in to AWS production' \
  &&  CI_COMMIT_REF_NAME=master aws_login production \
  &&  sops_env 'secrets-production.yaml' 'default' \
        DB_USER \
        DB_PASSWD \
  &&  TF_VAR_db_user="${DB_USER}" \
  &&  TF_VAR_db_password="${DB_PASSWD}" \
  &&  pushd deploy/django-db/terraform \
    &&  terraform init \
    &&  terraform apply -auto-approve -refresh=true \
  &&  popd \
  || return 1
}

function job_infra_django_db_test {
  export TF_VAR_db_user
  export TF_VAR_db_password

      echo '[INFO] Logging in to AWS development' \
  &&  aws_login development \
  &&  sops_env 'secrets-development.yaml' 'default' \
        DB_USER \
        DB_PASSWD \
  &&  TF_VAR_db_user="${DB_USER}" \
  &&  TF_VAR_db_password="${DB_PASSWD}" \
  &&  pushd deploy/django-db/terraform \
    &&  terraform init \
    &&  tflint --deep --module \
    &&  terraform plan -refresh=true \
  &&  popd \
  || return 1
}

function job_infra_resources_deploy {
      echo '[INFO] Logging in to AWS production' \
  &&  CI_COMMIT_REF_NAME=master aws_login production \
  &&  pushd deploy/terraform-resources \
    &&  terraform init \
    &&  terraform apply -auto-approve -refresh=true \
  &&  popd \
  || return 1
}

function job_infra_resources_test {
      echo '[INFO] Logging in to AWS development' \
  &&  aws_login development \
  &&  pushd deploy/terraform-resources \
    &&  terraform init \
    &&  tflint --deep --module \
    &&  terraform plan -refresh=true \
  &&  popd \
  || return 1
}

function job_infra_secret_management_deploy {
      echo '[INFO] Logging in to AWS production' \
  &&  CI_COMMIT_REF_NAME=master aws_login production \
  &&  pushd deploy/secret-management/terraform \
    &&  terraform init \
    &&  terraform apply -auto-approve -refresh=true \
  &&  popd \
  || return 1
}

function job_infra_secret_management_test {
      echo '[INFO] Logging in to AWS development' \
  &&  aws_login development \
  &&  pushd deploy/secret-management/terraform \
    &&  terraform init \
    &&  tflint --deep --module \
    &&  terraform plan -refresh=true \
  &&  popd \
  || return 1
}

function job_rotate_jwt_token {
  local integrates_repo_id='4620828'
  local var_name='JWT_TOKEN'
  local var_value
  local bytes_of_entropy='32'
  local set_as_masked='true'
  local set_as_protected='false'

      echo "[INFO] Extracting ${bytes_of_entropy} bytes of pseudo random entropy" \
  &&  var_value=$(head -c "${bytes_of_entropy}" /dev/urandom | base64) \
  &&  echo '[INFO] Extracting secrets' \
  &&  aws_login "${ENVIRONMENT_NAME}" \
  &&  sops_env "secrets-${ENVIRONMENT_NAME}.yaml" 'default' \
        GITLAB_API_TOKEN \
  &&  echo '[INFO] Updating var in GitLab' \
  &&  set_project_variable \
        "${GITLAB_API_TOKEN}" \
        "${integrates_repo_id}" \
        "${var_name}" \
        "${var_value}" \
        "${set_as_protected}" \
        "${set_as_masked}"
}

function job_test_back {
  local processes_to_kill=()
  local port_dynamo='8022'
  local port_redis='6379'

  function kill_processes {
    for process in "${processes_to_kill[@]}"
    do
          echo "[INFO] Killing PID: ${process}" \
      &&  (
            set +o errexit
            kill -9 "${process}"
          )
    done
  }

  # shellcheck disable=SC2015
      helper_set_dev_secrets \
  &&  echo '[INFO] Launching Redis' \
  &&  {
        redis-server --port "${port_redis}" \
          &
        processes_to_kill+=( "$!" )
      } \
  &&  echo '[INFO] Launching DynamoDB local' \
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
  &&  pytest \
        -n auto \
        --ds='fluidintegrates.settings' \
        --dist='loadscope' \
        --verbose \
        --maxfail='20' \
        --cov='fluidintegrates' \
        --cov='app' \
        --cov="${pyPkgIntegratesBack}/site-packages/backend" \
        --cov-report='term' \
        --cov-report='html:build/coverage/html' \
        --cov-report='xml:build/coverage/results.xml' \
        --cov-report='annotate:build/coverage/annotate' \
        --disable-warnings \
        'test' \
  &&  cp -a 'build/coverage/results.xml' "coverage.xml" \
  &&  {
        kill_processes
        return 0
      } \
  ||  {
        kill_processes
        return 1
      }
}

function job_test_back_async {
  local processes_to_kill=()
  local port_dynamo='8022'
  local port_redis='6379'

  function kill_processes {
    for process in "${processes_to_kill[@]}"
    do
          echo "[INFO] Killing PID: ${process}" \
      &&  (
            set +o errexit
            kill -9 "${process}"
          )
    done
  }

  # shellcheck disable=SC2015
      helper_set_dev_secrets \
  &&  echo '[INFO] Launching Redis' \
  &&  {
        redis-server --port "${port_redis}" \
          &
        processes_to_kill+=( "$!" )
      } \
  &&  echo '[INFO] Launching DynamoDB local' \
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
  &&  pytest \
        -n auto \
        --ds='fluidintegrates.settings' \
        --dist='loadscope' \
        --verbose \
        --maxfail='20' \
        --cov='fluidintegrates' \
        --cov='app' \
        --cov="${pyAsyncPkgIntegratesBack}/site-packages/backend" \
        --cov-report='term' \
        --disable-warnings \
        'test_async' \
  &&  {
        kill_processes
        return 0
      } \
  ||  {
        kill_processes
        return 1
      }
}

function job_test_front {
      pushd front \
    &&  npm install --unsafe-perm \
    &&  npm test \
    &&  mv coverage/lcov.info coverage.lcov \
  &&  popd \
  ||  return 1
}

function job_test_mobile {
      pushd mobile \
    &&  npm install --unsafe-perm \
    &&  npm test \
  &&  popd \
  ||  return 1
}

function job_deploy_k8s_back_ephemeral {
  local B64_AWS_ACCESS_KEY_ID
  local B64_AWS_SECRET_ACCESS_KEY
  local B64_JWT_TOKEN
  local DATE
  local DEPLOYMENT_NAME
  local files=(
    review-apps/variables.yaml
    review-apps/ingress.yaml
    review-apps/deploy-integrates.yaml
  )
  local vars_to_replace_in_manifest=(
    DATE
    B64_AWS_ACCESS_KEY_ID
    B64_AWS_SECRET_ACCESS_KEY
    B64_JWT_TOKEN
    DEPLOYMENT_NAME
  )

  # shellcheck disable=SC2034
      aws_login 'development' \
  &&  helper_use_pristine_workdir \
  &&  echo "[INFO] Setting namespace preferences..." \
  &&  kubectl config \
        set-context "$(kubectl config current-context)" \
        --namespace="${CI_PROJECT_NAME}" \
  &&  echo '[INFO] Computing environment variables' \
  &&  B64_AWS_ACCESS_KEY_ID=$(
        echo -n "${AWS_ACCESS_KEY_ID}" | base64 --wrap=0) \
  &&  B64_AWS_SECRET_ACCESS_KEY=$(
        echo -n "${AWS_SECRET_ACCESS_KEY}" | base64 --wrap=0) \
  &&  B64_JWT_TOKEN=$(
        echo -n "${JWT_TOKEN}" | base64 --wrap=0) \
  &&  DATE="$(date)" \
  &&  DEPLOYMENT_NAME="${CI_COMMIT_REF_SLUG}" \
  &&  for file in "${files[@]}"
      do
        for var in "${vars_to_replace_in_manifest[@]}"
        do
              rpl "__${var}__" "${!var}" "${file}" \
          |&  grep 'Replacing' \
          |&  sed -E 's/with.*$//g' \
          ||  return 1
        done
      done \
  &&  echo '[INFO] Applying: review-apps/variables.yaml' \
  &&  kubectl apply -f 'review-apps/variables.yaml' \
  &&  echo '[INFO] Applying: review-apps/ingress.yaml' \
  &&  kubectl apply -f 'review-apps/ingress.yaml' \
  &&  echo '[INFO] Applying: review-apps/deploy-integrates.yaml' \
  &&  kubectl apply -f 'review-apps/deploy-integrates.yaml' \
  &&  kubectl rollout status "deploy/review-${CI_COMMIT_REF_SLUG}" --timeout=5m
}

function job_deploy_k8s_back {
  local B64_AWS_ACCESS_KEY_ID
  local B64_AWS_SECRET_ACCESS_KEY
  local B64_JWT_TOKEN
  local DATE
  local files=(
    deploy/integrates-k8s.yaml
  )
  local vars_to_replace_in_manifest=(
    DATE
    B64_AWS_ACCESS_KEY_ID
    B64_AWS_SECRET_ACCESS_KEY
    B64_JWT_TOKEN
  )

  # shellcheck disable=SC2034
      CI_COMMIT_REF_NAME='master' aws_login 'production' \
  &&  helper_use_pristine_workdir \
  &&  sops_env 'secrets-production.yaml' 'default' \
        ROLLBAR_ACCESS_TOKEN \
        NEW_RELIC_API_KEY \
        NEW_RELIC_APP_ID \
  &&  echo "[INFO] Setting namespace preferences..." \
  &&  kubectl config \
        set-context "$(kubectl config current-context)" \
        --namespace='serves' \
  &&  echo '[INFO] Computing environment variables' \
  &&  B64_AWS_ACCESS_KEY_ID=$(
        echo -n "${AWS_ACCESS_KEY_ID}" | base64 --wrap=0) \
  &&  B64_AWS_SECRET_ACCESS_KEY=$(
        echo -n "${AWS_SECRET_ACCESS_KEY}" | base64 --wrap=0) \
  &&  B64_JWT_TOKEN=$(
        echo -n "${JWT_TOKEN}" | base64 --wrap=0) \
  &&  DATE="$(date)" \
  &&  for file in "${files[@]}"
      do
        for var in "${vars_to_replace_in_manifest[@]}"
        do
              rpl "__${var}__" "${!var}" "${file}" \
          |&  grep 'Replacing' \
          |&  sed -E 's/with.*$//g' \
          ||  return 1
        done
      done \
  &&  echo '[INFO] Applying: deploy/integrates-k8s.yaml' \
  &&  kubectl apply -f 'deploy/integrates-k8s.yaml' \
  &&  if ! kubectl rollout status --timeout=10m 'deploy/integrates-app'
      then
            echo '[INFO] Undoing deployment' \
        &&  kubectl rollout undo 'deploy/integrates-app' \
        &&  return 1
      fi \
  &&  if ! kubectl rollout status --timeout=10m 'deploy/integrates-app-async'
      then
            echo '[INFO] Undoing deployment' \
        &&  kubectl rollout undo 'deploy/integrates-app-async' \
        &&  return 1
      fi \
  &&  curl "https://api.rollbar.com/api/1/deploy" \
        --form "access_token=${ROLLBAR_ACCESS_TOKEN}" \
        --form 'environment=production' \
        --form "revision=${CI_COMMIT_SHA}" \
        --form "local_username=${CI_COMMIT_REF_NAME}" \
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

function job_deploy_k8s_stop_ephemeral {
      echo "[INFO] Setting namespace preferences..." \
  &&  kubectl config \
        set-context "$(kubectl config current-context)" \
        --namespace="${CI_PROJECT_NAME}" \
  &&  echo '[INFO] Deleting deployments' \
  &&  kubectl delete deployment "review-${CI_COMMIT_REF_SLUG}" \
  &&  kubectl delete service "service-${CI_COMMIT_REF_SLUG}" \
  &&  kubectl delete ingress "review-${CI_COMMIT_REF_SLUG}" \
  &&  kubectl delete deployment "review-async-${CI_COMMIT_REF_SLUG}" \
  &&  kubectl delete service "service-async-${CI_COMMIT_REF_SLUG}" \
  &&  kubectl delete ingress "review-async-${CI_COMMIT_REF_SLUG}"
}
