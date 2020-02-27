# shellcheck shell=bash

source "${srcIncludeHelpers}"
source "${srcExternalGitlabVariables}"
source "${srcExternalSops}"
source "${srcExternalSops}"
source "${srcCiScriptsHelpersOthers}"
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

function job_build_lambdas {

  function _job_build_lambdas {
    local lambda_name="${1}"
    local lambda_zip_file
    local current_path="${PWD}/lambda"
    local path_to_lambda="${current_path}/${lambda_name}"
    local path_to_lambda_venv="${current_path}/.venv.${lambda_name}"

    # shellcheck disable=SC1091
        lambda_zip_file="$(mktemp -d)/${lambda_name}.zip" \
    &&  echo '[INFO] Deleting previous virtual environment if exists' \
    &&  rm -rf "${path_to_lambda_venv}" \
    &&  echo '[INFO] Creating virtual environment' \
    &&  python3 -m venv "${path_to_lambda_venv}" \
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
      &&  pushd "${path_to_lambda_venv}/lib/python3.8/site-packages" \
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

function job_deploy_container_nix_cache {
  local context='.'
  local dockerfile='build/Dockerfile'
  local tag="${CI_REGISTRY_IMAGE}:nix"

      helper_use_pristine_workdir \
  &&  helper_docker_build_and_push \
        "${tag}" \
        "${context}" \
        "${dockerfile}"
}

function job_deploy_container_deps_base {
  local context='.'
  local dockerfile='deploy/containers/deps-base/Dockerfile'
  local tag="${CI_REGISTRY_IMAGE}/deps-base:${CI_COMMIT_REF_NAME}"

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

function job_deploy_container_deps_development {
  local context='.'
  local dockerfile='deploy/containers/deps-development/Dockerfile'
  local tag="${CI_REGISTRY_IMAGE}/deps-development:${CI_COMMIT_REF_NAME}"
  local build_arg_1='CI_COMMIT_REF_NAME'

      helper_use_pristine_workdir \
  &&  helper_docker_build_and_push \
        "${tag}" \
        "${context}" \
        "${dockerfile}" \
        "${build_arg_1}" "${!build_arg_1}"
}

function job_deploy_container_deps_production {
  local context='.'
  local dockerfile='deploy/containers/deps-production/Dockerfile'
  local tag="${CI_REGISTRY_IMAGE}/deps-production:${CI_COMMIT_REF_NAME}"
  local build_arg_1='CI_COMMIT_REF_NAME'

      helper_use_pristine_workdir \
  &&  helper_docker_build_and_push \
        "${tag}" \
        "${context}" \
        "${dockerfile}" \
        "${build_arg_1}" "${!build_arg_1}"
}

function job_deploy_container_app {
  local environment_name
  local fi_version
  local context='.'
  local dockerfile='deploy/containers/app/Dockerfile'
  local tag="${CI_REGISTRY_IMAGE}/app:${CI_COMMIT_REF_NAME}"

      echo '[INFO] Remember that this job needs: build_lambdas' \
  &&  echo '[INFO] Remember that this job needs: build_django_apps' \
  &&  echo '[INFO] Computing Fluid Integrates version' \
  &&  fi_version=$(app_version) \
  &&  echo -n "${fi_version}" > 'version.txt' \
  &&  echo "[INFO] Version: ${fi_version}" \
  &&  if test "${CI_COMMIT_REF_NAME}" = 'master'
      then
        environment_name="production"
      else
        environment_name="development"
      fi \
  &&  echo '[INFO] Logging in to AWS' \
  &&  aws_login "${environment_name}" \
  &&  sops_env "secrets-${environment_name}.yaml" 'default' \
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
        'ENV_NAME' "${environment_name}" \
        'SSL_CERT' "${SSL_CERT}" \
        'SSL_KEY' "${SSL_KEY}" \
        'VERSION' "${fi_version}"
}

function job_serve_dynamodb_local {
  local port=8022

      echo '[INFO] Launching DynamoDB local' \
  &&  {
        java \
          -Djava.library.path=./.DynamoDB/DynamoDBLocal_lib \
          -jar ./.DynamoDB/DynamoDBLocal.jar \
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
        "${app}"
}

function job_lint_back {
      prospector -F -s high -u django -i node_modules app \
  &&  prospector -F -s high -u django -i node_modules django-apps \
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
        django-apps/integrates-back/backend/dal/* \
        django-apps/integrates-back/backend/utils/*
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
          -Djava.library.path=./.DynamoDB/DynamoDBLocal_lib \
          -jar ./.DynamoDB/DynamoDBLocal.jar \
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
        --cov="${pyPkgIntegratesBack}/site-packages/back-end" \
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

function job_test_front {
      pushd front \
    &&  npm install \
    &&  npm test \
  &&  popd \
  ||  return 1
}
