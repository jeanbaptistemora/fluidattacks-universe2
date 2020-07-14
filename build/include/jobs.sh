# shellcheck shell=bash

source "${srcEnv}"
source "${srcIncludeHelpers}"
source "${srcExternalGitlabVariables}"
source "${srcExternalSops}"

function job_build_front {
      pushd front \
    &&  npm install \
    &&  < ../build/patches/jquery-comments.diff \
        patch -p1 --binary node_modules/jquery-comments_brainkit/js/jquery-comments.js \
    &&  npm run build \
  &&  popd \
  &&  sed --in-place \
        "s/integrates_version/v. ${FI_VERSION}/g" \
        'app/static/dashboard/app-bundle.min.js'
}

function job_build_mobile_android {
  export EXPO_ANDROID_KEYSTORE_PASSWORD
  export EXPO_ANDROID_KEY_PASSWORD
  export TURTLE_ANDROID_DEPENDENCIES_DIR="${HOME}/.turtle/androidDependencies"
  export JAVA_OPTS="
    -Xmx7G
    -XX:+HeapDumpOnOutOfMemoryError
    -XX:+UnlockExperimentalVMOptions
    -XX:+UseCGroupMemoryLimitForHeap
    -XX:+UseG1GC
  "
  export GRADLE_OPTS="
    -Dorg.gradle.configureondemand=true
    -Dorg.gradle.daemon=false
    -Dorg.gradle.jvmargs=\"${JAVA_OPTS}\"
    -Dorg.gradle.parallel=true
    -Dorg.gradle.project.android.aapt2FromMavenOverride=${TURTLE_ANDROID_DEPENDENCIES_DIR}/sdk/build-tools/28.0.3/aapt2
  "
  export GRADLE_DAEMON_DISABLED="1"

  if  helper_have_any_file_changed \
    'mobile/app.json' \
    'mobile/assets/icon.png' \
    'mobile/assets/splash.png'
  then
        echo '[INFO] Logging in to AWS' \
    &&  aws_login "${ENVIRONMENT_NAME}" \
    &&  sops_env "secrets-${ENVIRONMENT_NAME}.yaml" 'default' \
          EXPO_USER \
          EXPO_PASS \
    &&  sops \
          --aws-profile default \
          --decrypt \
          --extract '["GOOGLE_SERVICES_APP"]' \
          --output 'mobile/google-services.json' \
          --output-type 'json' \
          "secrets-development.yaml" \
    &&  EXPO_ANDROID_KEYSTORE_PASSWORD=${EXPO_PASS} \
    &&  EXPO_ANDROID_KEY_PASSWORD=${EXPO_PASS} \
    &&  pushd mobile \
      &&  echo '[INFO] Installing deps' \
      &&  echo '[INFO] Using NodeJS '"$(node -v)"'' \
      &&  echo '[INFO] Using Java '"$(java -version 2>&1)"'' \
      &&  npm install \
      &&  npx --no-install expo login \
            --username "${EXPO_USER}" \
            --password "${EXPO_PASS}" \
      &&  aws s3 cp \
            --recursive \
            "s3://fluidintegrates.build/mobile/certs" \
            ./certs \
      &&  echo '[INFO] Patching android sdk' \
      &&  rm -rf "${HOME}/.turtle/" \
      &&  mkdir -p "${TURTLE_ANDROID_DEPENDENCIES_DIR}/sdk" \
      &&  cp -r --no-preserve=mode,ownership \
            "${androidSdk}"/libexec/android-sdk/* \
            "${TURTLE_ANDROID_DEPENDENCIES_DIR}/sdk" \
      &&  touch "${TURTLE_ANDROID_DEPENDENCIES_DIR}/sdk/.ready" \
      &&  echo '[INFO] Building android app' \
      &&  npx --no-install turtle build:android \
            --username "${EXPO_USER}" \
            --password "${EXPO_PASS}" \
            --keystore-alias fluidintegrates-keystore \
            --keystore-path ./certs/keystore-dev.jks \
            --output output/integrates.aab \
            --release-channel "${CI_COMMIT_REF_NAME}" \
            --type app-bundle \
      &&  rm google-services.json \
      &&  rm -rf ./certs \
    &&  popd \
    ||  return 1
  else
        echo '[INFO] No relevant files were modified, skipping build' \
    &&  return 0
  fi
}

function job_build_mobile_ios {
  export EXPO_APPLE_PASSWORD
  export EXPO_IOS_DIST_P12_PASSWORD

      echo '[INFO] Logging in to AWS' \
  &&  aws_login "${ENVIRONMENT_NAME}" \
  &&  sops_env "secrets-${ENVIRONMENT_NAME}.yaml" 'default' \
        APPLE_DIST_CERT_PASSWORD \
        APPLE_ID \
        APPLE_PASSWORD \
        APPLE_PUSH_ID \
        APPLE_TEAM_ID \
        EXPO_USER \
        EXPO_PASS \
  &&  EXPO_APPLE_PASSWORD="${APPLE_PASSWORD}" \
  &&  EXPO_IOS_DIST_P12_PASSWORD="${APPLE_DIST_CERT_PASSWORD}" \
  &&  pushd mobile \
    &&  echo '[INFO] Installing deps' \
    &&  echo '[INFO] Using NodeJS '"$(node -v)"'' \
    &&  npm install \
    &&  npx --no-install expo login \
          --username "${EXPO_USER}" \
          --password "${EXPO_PASS}" \
    &&  aws s3 cp \
          --recursive \
          "s3://fluidintegrates.build/mobile/certs" \
          ./certs \
    &&  echo '[INFO] Building iOS app' \
    &&  npx --no-install expo-cli build:ios \
          --apple-id "${APPLE_ID}" \
          --dist-p12-path ./certs/apple_ios_distribution.p12 \
          --no-publish \
          --provisioning-profile-path ./certs/apple_prov_profile.mobileprovision \
          --push-id "${APPLE_PUSH_ID}" \
          --push-p8-path ./certs/apple_apns.p8 \
          --release-channel "${CI_COMMIT_REF_NAME}" \
          --team-id "${APPLE_TEAM_ID}" \
          --type archive \
    &&  curl -sSo output/integrates.ipa "$(npx expo-cli url:ipa)" \
    &&  rm -rf ./certs \
  &&  popd \
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

      _job_build_lambdas 'send_mail_notification' \
  &&  _job_build_lambdas 'project_to_pdf'
}

function job_coverage_report {
      env_prepare_python_packages \
  &&  echo '[INFO] Logging in to AWS' \
  &&  aws_login "${ENVIRONMENT_NAME}" \
  &&  sops_env "secrets-${ENVIRONMENT_NAME}.yaml" 'default' \
        CODECOV_TOKEN \
  &&  codecov -b "${CI_COMMIT_REF_NAME}"
}

function job_clean_registries {
  local registry_name='app'
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

function job_build_nix_caches {
  local context='.'
  local dockerfile='build/Dockerfile'
  local provisioners

      helper_use_pristine_workdir \
  &&  provisioners=(./build/provisioners/*) \
  &&  helper_build_nix_caches_parallel \
  &&  for (( i="${lower_limit}";i<="${upper_limit}";i++ ))
      do
            provisioner=$(basename "${provisioners[${i}]}") \
        &&  provisioner="${provisioner%.*}" \
        &&  helper_docker_build_and_push \
              "${CI_REGISTRY_IMAGE}/nix:${provisioner}" \
              "${context}" \
              "${dockerfile}" \
              'PROVISIONER' "${provisioner}" \
        ||  return 1
      done
}

function job_build_container_app {
  local context='.'
  local dockerfile='deploy/containers/app/Dockerfile'
  local tag="${CI_REGISTRY_IMAGE}/app:${CI_COMMIT_REF_NAME}"

      echo '[INFO] Remember that this job needs: build_lambdas' \
  &&  helper_build_django_apps \
  &&  echo '[INFO] Computing Fluid Integrates version' \
  &&  echo -n "${FI_VERSION}" > 'version.txt' \
  &&  echo '[INFO] Logging in to AWS' \
  &&  aws_login "${ENVIRONMENT_NAME}" \
  &&  sops_env "secrets-${ENVIRONMENT_NAME}.yaml" 'default' \
        SSL_KEY \
        SSL_CERT \
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
      env_prepare_python_packages \
  &&  env_prepare_django_static_external \
  &&  aws_login "${ENVIRONMENT_NAME}" \
  &&  sops_vars "${ENVIRONMENT_NAME}" \
  &&  ./manage.py collectstatic --no-input
}

function job_deploy_mobile_ota {
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
          &&  echo '[INFO] Using NodeJS '"$(node -v)"'' \
          &&  npm install \
          &&  npx --no-install expo login \
                --username "${EXPO_USER}" \
                --password "${EXPO_PASS}" \
          &&  echo '[INFO] Replacing versions' \
          &&  sed -i "s/integrates_version/${FI_VERSION}/g" ./app.json \
          &&  sed -i "s/\"versionCode\": 0/\"versionCode\": ${FI_VERSION_MOBILE}/g" ./app.json \
          &&  echo '[INFO] Launching expo bundler' \
          &&  { npx --no-install expo start --non-interactive & } \
          &&  EXPO_PID=$! \
          &&  echo '[INFO] Waiting 10 seconds to leave the bundler start' \
          &&  sleep 10 \
          &&  echo '[INFO] Publishing update' \
          &&  npx --no-install expo publish \
                --non-interactive \
                --release-channel "${CI_COMMIT_REF_NAME}" \
          &&  kill -9 "${EXPO_PID}" \
          &&  if test "${ENVIRONMENT_NAME}" = 'production'
              then
                    echo '[INFO] Sending report to rollbar' \
                &&  curl "https://api.rollbar.com/api/1/deploy" \
                      --form "access_token=${ROLLBAR_ACCESS_TOKEN}" \
                      --form 'environment=mobile-production' \
                      --form "revision=${CI_COMMIT_SHA}" \
                      --form "local_username=${CI_COMMIT_AUTHOR}"
              fi \
        &&  popd \
        ||  return 1
      else
            echo '[INFO] No relevant files were modified, skipping deploy' \
        &&  return 0
      fi
}

function job_deploy_mobile_playstore {
  export LANG=en_US.UTF-8

  if  helper_have_any_file_changed \
    'mobile/app.json'
  then
        echo '[INFO] Logging in to AWS' \
    &&  aws_login "${ENVIRONMENT_NAME}" \
    &&  sops \
          --aws-profile default \
          --decrypt \
          --extract '["PLAYSTORE_CREDENTIALS"]' \
          --output 'mobile/playstore-credentials.json' \
          --output-type 'json' \
          "secrets-${ENVIRONMENT_NAME}.yaml" \
    &&  pushd mobile \
      &&  echo '[INFO] Installing deps' \
      &&  bundle install \
      &&  echo '[INFO] Deploying to Google Play Store' \
      &&  bundle exec fastlane supply \
            --aab ./output/integrates.aab \
            --json_key ./playstore-credentials.json \
            --package_name "com.fluidattacks.integrates" \
            --track production \
      &&  rm playstore-credentials.json \
    &&  popd \
    ||  return 1
  else
        echo '[INFO] No relevant files were modified, skipping deploy' \
    &&  return 0
  fi
}

function job_deploy_permissions_matrix {
  export PYTHONPATH="${pyPkgPandas}/lib/python3.7/site-packages"
  export PYTHONPATH="${pyPkgNumpy}/lib/python3.7/site-packages:${PYTHONPATH}"
  export PYTHONPATH="${pyPkgMagic}/lib/python3.7/site-packages:${PYTHONPATH}"
  export PYTHONPATH=".:${PYTHONPATH}"
  export DJANGO_SETTINGS_MODULE='fluidintegrates.settings'

      env_prepare_python_packages \
  &&  helper_set_dev_secrets \
  &&  echo '[INFO] Deploying permissions matrix' \
  &&  python3 deploy/permissions-matrix/matrix.py
}

function job_django_console {
 export DJANGO_SETTINGS_MODULE='fluidintegrates.settings'

      env_prepare_python_packages \
  &&  env_prepare_ruby_modules \
  &&  env_prepare_node_modules \
  &&  "helper_set_dev_secrets" \
  && ./manage.py shell
}

function job_functional_tests_local {
  helper_functional_tests
}

function job_functional_tests_dev {
  CI='true' helper_functional_tests
}

function job_functional_tests_prod {
  CI_COMMIT_REF_NAME='master' helper_functional_tests
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

function job_reset {
  local files_to_delete=(
    'app/static/dashboard/'
    'app/backend/reports/images/*'
    'django-apps/integrates-back-async/backend/reports/tpls/*'
    'django-apps/integrates-back-async/backend/reports/results/results_pdf/*'
    'django-apps/integrates-back-async/backend/reports/results/results_excel/*'
    'build/coverage'
    'django-apps/*/*.egg-info'
    'front/coverage'
    'geckodriver.log'
    'mobile/coverage'
    'front/coverage.lcov'
    'front/node_modules'
    'lambda/.venv.*'
    'mobile/.expo/'
    'mobile/google-services.json'
    'TEMP_FD'
    'test_async/dynamo_data/bb_executions.json.now'
    'version.txt'
    '*.xlsx'
    '.tmp'
    '.DynamoDB'
  )
  local globs_to_delete=(
    '*.coverage*'
    '*package-lock.json'
    '*__pycache__*'
    '*.terraform'
  )

  for file in "${files_to_delete[@]}"
  do
    # I want word splitting to exploit globbing
    # shellcheck disable=SC2086
        echo "[INFO] Deleting: ${file}" \
    &&  rm -rf ${file}
  done

  for glob in "${globs_to_delete[@]}"
  do
        echo "[INFO] Deleting: ${glob}" \
    &&  find . -wholename "${glob}" -exec rm -rf {} +
  done
}

function job_serve_dynamodb_local {
  local port=8022

      env_prepare_dynamodb_local \
  &&  echo '[INFO] Launching DynamoDB local' \
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
      env_prepare_python_packages \
  &&  CI_COMMIT_REF_NAME=master aws_login 'production' \
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

function job_serve_mobile {
        echo '[INFO] Logging in to AWS' \
    &&  aws_login "${ENVIRONMENT_NAME}" \
    &&  sops_env "secrets-${ENVIRONMENT_NAME}.yaml" 'default' \
          EXPO_USER \
          EXPO_PASS \
    &&  sops \
          --aws-profile default \
          --decrypt \
          --extract '["GOOGLE_SERVICES_APP"]' \
          --output 'mobile/google-services.json' \
          --output-type 'json' \
          "secrets-development.yaml" \
    &&  pushd mobile \
    &&  npm install \
    &&  npx --no-install expo login \
            --username "${EXPO_USER}" \
            --password "${EXPO_PASS}" \
    &&  npm start -- --non-interactive \
  &&  popd \
  ||  return 1
}

function job_serve_redis {
  local port=6379

      echo "[INFO] Serving redis on port ${port}" \
  &&  redis-server --port "${port}"
}

function job_serve_back_dev {
  helper_serve_back dev
}

function job_cron_show {
  export DJANGO_SETTINGS_MODULE='fluidintegrates.settings'

      env_prepare_python_packages \
  &&  helper_set_dev_secrets \
  &&  python3 manage.py crontab add \
  &&  python3 manage.py crontab show
}

function job_cron_run {
  export DJANGO_SETTINGS_MODULE='fluidintegrates.settings'
  local cron_job="${1}"

      env_prepare_python_packages \
  &&  helper_set_dev_secrets \
  &&  python3 manage.py crontab run "${cron_job}"
}

function job_serve_back_prod {
  helper_serve_back prod
}

function _job_make_migration {
  local env="${1}"
  local stage="${2}"
  local migration_file="${3}"
  export DJANGO_SETTINGS_MODULE='fluidintegrates.settings'

      env_prepare_python_packages \
  &&  "helper_set_${env}_secrets" \
  &&  PYTHONPATH="${PWD}:${PYTHONPATH}" \
      STAGE="${stage}" \
      python3 "${migration_file}" \

}

function job_make_migration_dev_test {
  local migration_file="${1}"

  _job_make_migration 'dev' 'test' "${migration_file}" \
    | tee "${migration_file}.dev_test.out"
}

function job_make_migration_prod_test {
  local migration_file="${1}"

  _job_make_migration 'prod' 'test' "${migration_file}"
}

function _execute_analytics_generator {
  local generator="${1}"
  local results_dir="${generator//.py/}"

      mkdir -p "${results_dir}" \
  &&  echo "[INFO] Running: ${generator}" \
  &&  {
            RESULTS_DIR="${results_dir}" python3 "${generator}" \
        ||  RESULTS_DIR="${results_dir}" python3 "${generator}" \
        ||  RESULTS_DIR="${results_dir}" python3 "${generator}"
      } \

}

function _job_analytics_make_documents {
  export CI_COMMIT_REF_NAME
  export CI_NODE_INDEX
  export CI_NODE_TOTAL
  export DJANGO_SETTINGS_MODULE='fluidintegrates.settings'
  export PYTHONPATH="${PWD}:${PWD}/analytics:${PYTHONPATH}"
  export TEMP_FILE1
  local remote_bucket='fluidintegrates.analytics'
  local num_of_generators

      find 'analytics/generators' -wholename '*.py' \
        | LC_ALL=C sort > "${TEMP_FILE1}" \
  &&  num_of_generators=$(wc -l < "${TEMP_FILE1}") \
  &&  echo "Found ${num_of_generators} generators to execute" \
  &&  echo "Processing batch: ${CI_NODE_INDEX} of ${CI_NODE_TOTAL}" \
  &&  split --number="l/${CI_NODE_INDEX}/${CI_NODE_TOTAL}" "${TEMP_FILE1}" \
        | while read -r generator
          do
                _execute_analytics_generator "${generator}" \
            ||  return 1
          done \
  &&  echo '[INFO] Uploading documents' \
  &&  aws s3 sync \
        'analytics/generators' "s3://${remote_bucket}/${CI_COMMIT_REF_NAME}/documents" \

}

function _job_analytics_make_snapshots {
  export CI_COMMIT_REF_NAME
  export DJANGO_SETTINGS_MODULE='fluidintegrates.settings'
  export PYTHONPATH="${PWD}:${PWD}/analytics:${PYTHONPATH}"
  local remote_bucket='fluidintegrates.analytics'

      echo '[INFO] Collecting static results' \
  &&  RESULTS_DIR='analytics/collector/reports' \
      python3 analytics/collector/generate_reports.py \
  &&  echo '[INFO] Uploading static results' \
  &&  aws s3 sync \
        'analytics/collector' "s3://${remote_bucket}/${CI_COMMIT_REF_NAME}/snapshots" \

}

function job_analytics_make_documents_dev {
      env_prepare_python_packages \
  &&  helper_set_dev_secrets \
  &&  if test "${IS_LOCAL_BUILD}" = "${FALSE}"
      then
        helper_set_local_dynamo_and_redis
      fi \
  &&  _job_analytics_make_documents
}

function job_analytics_make_documents_prod {
      env_prepare_python_packages \
  &&  helper_set_prod_secrets \
  &&  _job_analytics_make_documents
}

function job_analytics_make_documents_prod_schedule {
  job_analytics_make_documents_prod
}

function job_analytics_make_snapshots_prod_schedule {
      env_prepare_python_packages \
  &&  helper_set_prod_secrets \
  &&  _job_analytics_make_snapshots
}

function job_make_migration_dev_apply {
  local migration_file="${1}"

  _job_make_migration 'dev' 'apply' "${migration_file}" \
    | tee "${migration_file}.dev_apply.out"
}

function job_make_migration_prod_apply {
  local migration_file="${1}"

  _job_make_migration 'prod' 'apply' "${migration_file}"
}

function _job_subscriptions_trigger_user_to_entity_report {
  export DJANGO_SETTINGS_MODULE='fluidintegrates.settings'
  export PYTHONPATH="${PWD}:${PWD}/analytics:${PYTHONPATH}"

      echo '[INFO] Waking up: trigger_user_to_entity_report' \
  &&  python3 \
        'django-apps/integrates-back-async/cli/subscriptions.py' \
        'backend.domain.subscriptions.trigger_user_to_entity_report' \

}

function job_subscriptions_trigger_user_to_entity_report_dev {
      env_prepare_python_packages \
  &&  helper_set_dev_secrets \
  &&  if test "${IS_LOCAL_BUILD}" = "${FALSE}"
      then
        helper_set_local_dynamo_and_redis
      fi \
  &&  _job_subscriptions_trigger_user_to_entity_report \

}

function job_subscriptions_trigger_user_to_entity_report_prod_schedule {
      env_prepare_python_packages \
  &&  helper_set_prod_secrets \
  &&  _job_subscriptions_trigger_user_to_entity_report \

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
    &&  terraform plan -lock=false -refresh=true \
  &&  popd \
  || return 1
}

function job_infra_database_deploy {
  export TF_VAR_db_user
  export TF_VAR_db_password

      echo '[INFO] Logging in to AWS production' \
  &&  CI_COMMIT_REF_NAME=master aws_login production \
  &&  sops_env 'secrets-production.yaml' 'default' \
        DB_USER \
        DB_PASSWD \
  &&  TF_VAR_db_user="${DB_USER}" \
  &&  TF_VAR_db_password="${DB_PASSWD}" \
  &&  pushd deploy/database/terraform \
    &&  terraform init \
    &&  terraform apply -auto-approve -refresh=true \
  &&  popd \
  || return 1
}

function job_infra_database_test {
      echo '[INFO] Logging in to AWS development' \
  &&  aws_login development \
  &&  pushd deploy/database/terraform \
    &&  terraform init \
    &&  tflint --deep --module \
    &&  terraform plan -lock=false -refresh=true \
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
    &&  terraform plan -lock=false -refresh=true \
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
    &&  terraform plan -lock=false -refresh=true \
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
    &&  terraform plan -lock=false -refresh=true \
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
    &&  terraform plan -lock=false -refresh=true \
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
  local common_args=(
    -n auto
    --ds 'fluidintegrates.settings'
    --dist 'loadscope'
    --verbose
    --maxfail '20'
    --cov 'fluidintegrates'
    --cov 'app'
    --cov "${pyPkgIntegratesBack}/site-packages/backend"
    --cov-report 'term'
    --cov-report 'html:build/coverage/html'
    --cov-report 'xml:build/coverage/results.xml'
    --cov-report 'annotate:build/coverage/annotate'
    --disable-warnings
  )
  local extra_args=()
  local markers=(
    'not (changes_db or changes_sessions)'
    'changes_db'
    'changes_sessions'
  )

  # shellcheck disable=SC2015
      env_prepare_python_packages \
  &&  helper_set_dev_secrets \
  &&  helper_set_local_dynamo_and_redis \
  &&  for i in "${!markers[@]}"
      do
            echo "[INFO] Running marker: ${markers[i]}" \
        &&  if [[ "${i}" != 0 ]]
            then
              extra_args=( --cov-append )
            fi \
        &&  pytest \
              -m "${markers[i]}" \
              "${common_args[@]}" \
              "${extra_args[@]}" \
              'test_async' \
        ||  return 1
      done \
  &&  cp -a 'build/coverage/results.xml' "coverage.xml"
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
    &&  mv coverage/lcov.info coverage.lcov \
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
  &&  curl "https://api.rollbar.com/api/1/deploy" \
        --form "access_token=${ROLLBAR_ACCESS_TOKEN}" \
        --form 'environment=production' \
        --form "revision=${CI_COMMIT_SHA}" \
        --form "local_username=${CI_COMMIT_AUTHOR}" \
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
  &&  kubectl delete ingress "review-${CI_COMMIT_REF_SLUG}"
}
