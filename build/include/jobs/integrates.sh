# shellcheck shell=bash

function job_integrates_build_front {
      pushd "${STARTDIR}/integrates" \
  &&  pushd front \
  &&  npm install \
  &&  < ../../build/patches/jquery-comments.diff \
        patch -p1 --binary node_modules/jquery-comments_brainkit/js/jquery-comments.js \
  &&  npm run build \
  &&  popd \
  &&  sed --in-place \
        "s/integrates_version/${FI_VERSION}/g" \
        'app/static/dashboard/app-bundle.min.js' \
  &&  popd \
  || return 1
}

function job_integrates_build_mobile_android {
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
        'integrates/mobile/app.json' \
        'integrates/mobile/assets/icon.png' \
        'integrates/mobile/assets/splash.png'
      then
            pushd "${STARTDIR}/integrates" \
        &&  echo '[INFO] Logging in to AWS' \
        &&  helper_integrates_aws_login "${ENVIRONMENT_NAME}" \
        &&  helper_common_sops_env "secrets-${ENVIRONMENT_NAME}.yaml" 'default' \
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
      fi \
  &&  popd \
  ||  return 1
}

function job_integrates_build_mobile_ios {
  export EXPO_APPLE_PASSWORD
  export EXPO_IOS_DIST_P12_PASSWORD

      pushd "${STARTDIR}/integrates" \
  &&  echo '[INFO] Logging in to AWS' \
  &&  helper_integrates_aws_login "${ENVIRONMENT_NAME}" \
  &&  helper_common_sops_env "secrets-${ENVIRONMENT_NAME}.yaml" 'default' \
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

function job_integrates_build_lambdas {

  function _job_integrates_build_lambdas {
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
      pushd "${STARTDIR}/integrates" \
  &&  _job_integrates_build_lambdas 'send_mail_notification' \
  &&  _job_integrates_build_lambdas 'project_to_pdf' \
  &&  popd \
  || return 1
}

function job_integrates_coverage_report {
      pushd "${STARTDIR}/integrates" \
  &&  env_prepare_python_packages \
  &&  echo '[INFO] Logging in to AWS' \
  &&  helper_integrates_aws_login "${ENVIRONMENT_NAME}" \
  &&  helper_common_sops_env "secrets-${ENVIRONMENT_NAME}.yaml" 'default' \
        CODECOV_TOKEN \
  &&  codecov -b "${CI_COMMIT_REF_NAME}" \
  &&  popd \
  || return 1
}

function job_integrates_clean_registries {
  local registry_name='app'
  local registry_id

      pushd "${STARTDIR}/integrates" \
  &&  if helper_is_today_first_day_of_month
      then
            echo '[INFO] Cleaning registries' \
        &&  CI_COMMIT_REF_NAME='master' helper_integrates_aws_login 'production' \
        &&  helper_common_sops_env 'secrets-production.yaml' 'default' \
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
      fi \
  &&  popd \
  ||  return 1
}

function job_integrates_build_container_app {
  local context='.'
  local dockerfile='deploy/containers/app/Dockerfile'
  local tag="${CI_REGISTRY_IMAGE}/app:${CI_COMMIT_REF_NAME}"

      pushd "${STARTDIR}/integrates" \
  &&  echo '[INFO] Remember that this job needs: build_lambdas' \
  &&  helper_build_django_apps \
  &&  echo '[INFO] Computing Fluid Integrates version' \
  &&  echo -n "${FI_VERSION}" > 'version.txt' \
  &&  echo '[INFO] Logging in to AWS' \
  &&  helper_integrates_aws_login "${ENVIRONMENT_NAME}" \
  &&  helper_common_sops_env "secrets-${ENVIRONMENT_NAME}.yaml" 'default' \
        SSL_KEY \
        SSL_CERT \
  &&  cp ../build/include/helpers/common.sh . \
  &&  cp ../build/include/helpers/integrates.sh . \
  &&  helper_docker_build_and_push \
        "${tag}" \
        "${context}" \
        "${dockerfile}" \
        'CI_API_V4_URL' "${CI_API_V4_URL}" \
        'CI_COMMIT_AUTHOR' "${CI_COMMIT_AUTHOR}" \
        'CI_COMMIT_REF_NAME' "${CI_COMMIT_REF_NAME}" \
        'CI_COMMIT_SHA' "${CI_COMMIT_SHA}" \
        'CI_PROJECT_ID' "${CI_PROJECT_ID}" \
        'CI_REPOSITORY_URL' "${CI_REPOSITORY_URL}" \
        'ENV_NAME' "${ENVIRONMENT_NAME}" \
        'SSL_CERT' "${SSL_CERT}" \
        'SSL_KEY' "${SSL_KEY}" \
        'VERSION' "${FI_VERSION}" \
  &&  popd \
  || return 1
}

function job_integrates_deploy_front {
      pushd "${STARTDIR}/integrates" \
  &&  env_prepare_python_packages \
  &&  env_prepare_django_static_external \
  &&  helper_integrates_aws_login "${ENVIRONMENT_NAME}" \
  &&  sops_vars "${ENVIRONMENT_NAME}" \
  &&  ./manage.py collectstatic --no-input \
  &&  popd \
  ||  return 1
}

function job_integrates_deploy_mobile_ota {
  export EXPO_USE_DEV_SERVER="true"

      pushd integrates \
    &&  echo '[INFO] Logging in to AWS' \
    &&  helper_integrates_aws_login "${ENVIRONMENT_NAME}" \
    &&  helper_common_sops_env "secrets-${ENVIRONMENT_NAME}.yaml" 'default' \
          EXPO_USER \
          EXPO_PASS \
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
      &&  echo '[INFO] Publishing update' \
      &&  npx --no-install expo publish \
            --non-interactive \
            --release-channel "${CI_COMMIT_REF_NAME}" \
      &&  echo '[INFO] Sending build info to bugsnag' \
      &&  npx bugsnag-build-reporter \
            --api-key c7b947a293ced0235cdd8edc8c09dad4 \
            --app-version "${FI_VERSION}" \
            --release-stage "mobile-${ENVIRONMENT_NAME}" \
            --builder-name "${CI_COMMIT_AUTHOR}" \
            --source-control-provider gitlab \
            --source-control-repository https://gitlab.com/fluidattacks/product.git \
            --source-control-revision "${CI_COMMIT_SHA}/integrates/mobile" \
    &&  popd \
    ||  return 1 \
  &&  popd \
  ||  return 1
}

function job_integrates_deploy_mobile_playstore {
  export LANG=en_US.UTF-8

      if  helper_have_any_file_changed \
        'integrates/mobile/app.json'
      then
            pushd "${STARTDIR}/integrates" \
        &&  echo '[INFO] Logging in to AWS' \
        &&  helper_integrates_aws_login "${ENVIRONMENT_NAME}" \
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
      fi \
  &&  popd \
  ||  return 1
}

function job_integrates_deploy_permissions_matrix {
  export PYTHONPATH="${pyPkgPandas}/lib/python3.7/site-packages"
  export PYTHONPATH="${pyPkgNumpy}/lib/python3.7/site-packages:${PYTHONPATH}"
  export PYTHONPATH="${pyPkgMagic}/lib/python3.7/site-packages:${PYTHONPATH}"
  export PYTHONPATH=".:${PYTHONPATH}"
  export DJANGO_SETTINGS_MODULE='fluidintegrates.settings'

      pushd "${STARTDIR}/integrates" \
  &&  env_prepare_python_packages \
  &&  helper_integrates_set_dev_secrets \
  &&  echo '[INFO] Deploying permissions matrix' \
  &&  python3 deploy/permissions-matrix/matrix.py \
  &&  popd \
  ||  return 1
}

function job_integrates_django_console {
 export DJANGO_SETTINGS_MODULE='fluidintegrates.settings'

      pushd "${STARTDIR}/integrates" \
  &&  env_prepare_python_packages \
  &&  env_prepare_ruby_modules \
  &&  env_prepare_node_modules \
  &&  helper_integrates_set_dev_secrets \
  &&  ./manage.py shell \
  &&  popd \
  ||  return 1
}

function job_integrates_functional_tests_back {
  local common_args=(
    --ds 'fluidintegrates.settings'
    --verbose
    --disable-warnings
  )

  # shellcheck disable=SC2015
      pushd "${STARTDIR}/integrates" \
  &&  env_prepare_python_packages \
  &&  helper_integrates_set_dev_secrets \
  &&  helper_set_local_dynamo_and_redis \
  &&  pytest \
        "${common_args[@]}" \
        'test_async/functional_test' \
  ||  return 1 \
  &&  popd \
  ||  return 1
}

function job_integrates_functional_tests_mobile_local {
  export CI_COMMIT_REF_NAME
  local expo_apk_url="https://d1ahtucjixef4r.cloudfront.net/Exponent-2.16.1.apk"

  function teardown {
    kill %1
  }

      pushd "${STARTDIR}/integrates/mobile/e2e" \
  &&  env_prepare_python_packages \
  &&  env_prepare_node_modules \
  &&  curl -sSo expoClient.apk "${expo_apk_url}" \
  &&  echo '[INFO] Looking for available android devices...' \
  &&  echo '[INFO] Make sure to enable USB debugging and set' \
            'your mobile device to file transfer mode' \
  &&  "${ANDROID_SDK_ROOT}/platform-tools/adb" wait-for-device \
  &&  { appium --default-capabilities capabilities/android.json & } \
  &&  echo '[INFO] Waiting 5 seconds to leave appium start' \
  &&  sleep 5 \
  &&  trap 'teardown' EXIT \
  &&  pytest ./ \
        --exitfirst \
        --verbose \
  &&  popd \
  ||  return 1
}

function job_integrates_functional_tests_mobile {
  local expo_apk_url="https://d1ahtucjixef4r.cloudfront.net/Exponent-2.16.1.apk"
  local project_arn
  local device_pool_arn
  local apk_arn
  local test_pkg_arn
  local test_spec_arn
  local run_name

      pushd "${STARTDIR}/integrates/mobile/e2e" \
  &&  echo '[INFO] Logging in to AWS' \
  &&  helper_integrates_aws_login "${ENVIRONMENT_NAME}" \
  &&  aws configure set region 'us-west-2' \
  &&  project_arn=$(
        aws devicefarm list-projects \
        | jq -r '.projects | .[] | select(.name == "integrates-mobile") | .arn'
      ) \
  &&  run_name="${CI_COMMIT_REF_NAME}_$(date -Iseconds)" \
  &&  echo '[INFO] Preparing device pool' \
  &&  device_pool_arn=$(
        aws devicefarm create-device-pool \
          --max-devices 1 \
          --name devicePool \
          --project-arn "${project_arn}" \
          --rules file://devicefarm/devices.json \
        | jq -r '.devicePool | .arn'
      ) \
  &&  echo '[INFO] Preparing apk' \
  &&  curl -sSo expoClient.apk "${expo_apk_url}" \
  &&  helper_upload_to_devicefarm \
        apk_arn \
        "${run_name}" \
        expoClient.apk \
        ANDROID_APP \
  &&  echo '[INFO] Preparing test package' \
  &&  zip -r9 devicefarm/tests.zip tests/ requirements.txt \
  &&  helper_upload_to_devicefarm \
        test_pkg_arn \
        "${run_name}" \
        devicefarm/tests.zip \
        APPIUM_PYTHON_TEST_PACKAGE \
  &&  echo '[INFO] Preparing test spec' \
  &&  yq write -i \
        devicefarm/spec.yml \
        'phases.test.commands[+]' \
        "$(cat devicefarm/test.sh)" \
  &&  sed -i \
        "s/__CI_COMMIT_REF_NAME__/${CI_COMMIT_REF_NAME}/g" \
        devicefarm/spec.yml \
  &&  helper_upload_to_devicefarm \
        test_spec_arn \
        "${run_name}" \
        devicefarm/spec.yml \
        APPIUM_PYTHON_TEST_SPEC \
  &&  helper_run_test_devicefarm \
        "${apk_arn}" \
        "${device_pool_arn}" \
        "${project_arn}" \
        "${run_name}" \
        "${test_pkg_arn}" \
        "${test_spec_arn}" \
  &&  popd \
  ||  return 1
}

function job_integrates_functional_tests_local {
      pushd "${STARTDIR}/integrates" \
  &&  helper_integrates_functional_tests \
  &&  popd \
  ||  return 1
}

function job_integrates_functional_tests_dev {
      pushd "${STARTDIR}/integrates" \
  &&  CI='true' helper_integrates_functional_tests \
  &&  popd \
  ||  return 1
}

function job_integrates_functional_tests_prod {
      pushd "${STARTDIR}/integrates" \
  &&  CI_COMMIT_REF_NAME='master' helper_integrates_functional_tests \
  &&  popd \
  ||  return 1
}

function job_integrates_renew_certificates {
  local certificate='ssl-review-apps'
  local certificate_issuer='letsencrypt'
  local secret_name='ssl-certificate'
  local RA_ACCESS_KEY
  local files=(
    deploy/ephemeral/tls.yaml
  )
  local vars_to_replace_in_manifest=(
    DNS_ZONE_ID
    RA_ACCESS_KEY
  )

      pushd "${STARTDIR}/integrates" \
  &&  if helper_is_today_wednesday
      then
        # shellcheck disable=SC2034
            helper_integrates_aws_login 'development' \
        &&  echo '[INFO] Setting context' \
        &&  helper_common_update_kubeconfig FluidServes us-east-1 \
        &&  kubectl config \
              set-context "$(kubectl config current-context)" \
              --namespace=integrates \
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
        &&  echo '[INFO] Applying: deploy/ephemeral/tls.yaml' \
        &&  kubectl apply -f 'deploy/ephemeral/tls.yaml' \
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
      fi \
  &&  popd \
  ||  return 1
}

function job_integrates_reset {
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
    'skims/coverage'
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
    '*.mypy_cache'
    '*.pytest_cache'
    '*.terraform'
  )

      pushd "${STARTDIR}/integrates" \
  &&  for file in "${files_to_delete[@]}"
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
      done \
  &&  popd \
  ||  return 1
}

function job_integrates_serve_dynamodb_local {
  local port=8022

      pushd "${STARTDIR}/integrates" \
  &&  env_prepare_dynamodb_local \
  &&  echo '[INFO] Launching DynamoDB local' \
  &&  {
        java \
          -Djava.library.path="${STARTDIR}/integrates/.DynamoDB/DynamoDBLocal_lib" \
          -jar "${STARTDIR}/integrates/.DynamoDB/DynamoDBLocal.jar" \
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
  &&  fg %1 \
  &&  popd \
  ||  return 1
}

function job_integrates_serve_front {
      pushd "${STARTDIR}/integrates/front" \
    &&  npm install \
    &&  npm start \
  &&  popd \
  ||  return 1
}

function job_integrates_serve_mobile {
      pushd "${STARTDIR}/integrates" \
  &&  echo '[INFO] Logging in to AWS' \
  &&  helper_integrates_aws_login "${ENVIRONMENT_NAME}" \
  &&  helper_common_sops_env "secrets-${ENVIRONMENT_NAME}.yaml" 'default' \
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
  &&  rm -rf ~/.expo ./.expo \
  &&  npx --no-install expo login \
          --username "${EXPO_USER}" \
          --password "${EXPO_PASS}" \
          --non-interactive \
  &&  npm start -- \
        --clear \
        --non-interactive \
  &&  popd \
  &&  popd \
  ||  return 1
}

function job_integrates_serve_redis {
  local port=6379

      pushd "${STARTDIR}/integrates" \
  &&  echo "[INFO] Serving redis on port ${port}" \
  &&  redis-server --port "${port}" \
  &&  popd \
  ||  return 1
}

function job_integrates_serve_back_dev {
      pushd "${STARTDIR}/integrates" \
  &&  helper_integrates_serve_back dev \
  &&  popd \
  ||  return 1
}

function job_integrates_cron_show {
  export DJANGO_SETTINGS_MODULE='fluidintegrates.settings'

      pushd "${STARTDIR}/integrates" \
  &&  env_prepare_python_packages \
  &&  helper_integrates_set_dev_secrets \
  &&  python3 manage.py crontab add \
  &&  python3 manage.py crontab show \
  &&  popd \
  ||  return 1
}

function job_integrates_cron_run {
  export DJANGO_SETTINGS_MODULE='fluidintegrates.settings'
  local cron_job="${1}"

      pushd "${STARTDIR}/integrates" \
  &&  env_prepare_python_packages \
  &&  helper_integrates_set_dev_secrets \
  &&  python3 manage.py crontab run "${cron_job}" \
  &&  popd \
  ||  return 1
}

function job_integrates_serve_back_prod {
      pushd "${STARTDIR}/integrates" \
  &&  helper_integrates_serve_back prod \
  &&  popd \
  ||  return 1
}

function _job_integrates_make_migration {
  local env="${1}"
  local stage="${2}"
  local migration_file="${3}"
  export DJANGO_SETTINGS_MODULE='fluidintegrates.settings'

      env_prepare_python_packages \
  &&  "helper_integrates_set_${env}_secrets" \
  &&  PYTHONPATH="${PWD}:${PYTHONPATH}" \
      STAGE="${stage}" \
      python3 "${migration_file}" \

}

function job_integrates_make_migration_dev_test {
  local migration_file="${1}"

      pushd "${STARTDIR}/integrates" \
  &&  _job_integrates_make_migration 'dev' 'test' "${migration_file}" \
        | tee "${migration_file}.dev_test.out" \
  &&  popd \
  ||  return 1
}

function job_integrates_make_migration_prod_test {
  local migration_file="${1}"

      pushd "${STARTDIR}/integrates" \
  &&  _job_integrates_make_migration 'prod' 'test' "${migration_file}" \
  &&  popd \
  ||  return 1
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

function _job_integrates_analytics_make_documents {
  export CI_COMMIT_REF_NAME
  export CI_NODE_INDEX
  export CI_NODE_TOTAL
  export DJANGO_SETTINGS_MODULE='fluidintegrates.settings'
  export PYTHONPATH="${PWD}:${PWD}/analytics:${PYTHONPATH}"
  export TEMP_FILE1
  local remote_bucket='fluidintegrates.analytics'

      find 'analytics/generators' -wholename '*.py' | LC_ALL=C sort > "${TEMP_FILE1}" \
  &&  helper_execute_chunk_parallel \
        "_execute_analytics_generator" \
        "${TEMP_FILE1}" \
  &&  echo '[INFO] Uploading documents' \
  &&  aws s3 sync \
        'analytics/generators' "s3://${remote_bucket}/${CI_COMMIT_REF_NAME}/documents" \

}

function _job_integrates_analytics_make_snapshots {
  export CI_COMMIT_REF_NAME
  export DJANGO_SETTINGS_MODULE='fluidintegrates.settings'
  export PYTHONPATH="${PWD}:${PWD}/analytics:${PYTHONPATH}"
  local remote_bucket='fluidintegrates.analytics'

      echo '[INFO] Collecting static results' \
  &&  RESULTS_DIR='analytics/collector/reports' \
      python3 analytics/collector/generate_reports.py \
  &&  echo '[INFO] Uploading static results' \
  &&  aws s3 sync \
        'analytics/collector' "s3://${remote_bucket}/${CI_COMMIT_REF_NAME}/snapshots"
}

function job_integrates_analytics_make_documents_dev {
      pushd "${STARTDIR}/integrates" \
  &&  env_prepare_python_packages \
  &&  helper_integrates_set_dev_secrets \
  &&  if test "${IS_LOCAL_BUILD}" = "${FALSE}"
      then
        helper_set_local_dynamo_and_redis
      fi \
  &&  _job_integrates_analytics_make_documents \
  &&  popd \
  ||  return 1
}

function job_integrates_analytics_make_documents_prod {
      pushd "${STARTDIR}/integrates" \
  &&  env_prepare_python_packages \
  &&  helper_integrates_set_prod_secrets \
  &&  _job_integrates_analytics_make_documents \
  &&  popd \
  ||  return 1
}

function job_integrates_analytics_make_documents_prod_schedule {
      pushd "${STARTDIR}/integrates" \
  &&  job_integrates_analytics_make_documents_prod \
  &&  popd \
  ||  return 1
}

function job_integrates_analytics_make_snapshots_prod_schedule {
      pushd "${STARTDIR}/integrates" \
  &&  env_prepare_python_packages \
  &&  helper_integrates_set_prod_secrets \
  &&  _job_integrates_analytics_make_snapshots \
  &&  popd \
  ||  return 1
}

function job_integrates_make_migration_dev_apply {
  local migration_file="${1}"

  pushd "${STARTDIR}/integrates" \
  &&  _job_integrates_make_migration 'dev' 'apply' "${migration_file}" \
        | tee "${migration_file}.dev_apply.out" \
  &&  popd \
  ||  return 1
}

function job_integrates_make_migration_prod_apply {
  local migration_file="${1}"

      pushd "${STARTDIR}/integrates" \
  &&  _job_integrates_make_migration 'prod' 'apply' "${migration_file}" \
  &&  popd \
  ||  return 1
}

function _job_integrates_subscriptions_trigger_user_to_entity_report {
  helper_invoke_py backend.domain.subscriptions.trigger_user_to_entity_report

}

function job_integrates_subscriptions_trigger_user_to_entity_report_dev {
      pushd "${STARTDIR}/integrates" \
  &&  helper_bootstrap_dev_ci \
  &&  _job_integrates_subscriptions_trigger_user_to_entity_report \
  &&  popd \
  ||  return 1
}

function job_integrates_subscriptions_trigger_user_to_entity_report_prod_schedule {
      pushd "${STARTDIR}/integrates" \
  &&  helper_bootstrap_prod_ci \
  &&  _job_integrates_subscriptions_trigger_user_to_entity_report \
  &&  popd \
  ||  return 1
}

function job_integrates_scheduler_dev {
  local module="backend.scheduler.${1}"

      pushd "${STARTDIR}/integrates" \
  &&  helper_bootstrap_dev_ci \
  &&  helper_invoke_py "${module}" \
  &&  popd \
  ||  return 1
}

function job_integrates_scheduler_prod {
  local module="backend.scheduler.${1}"

      pushd "${STARTDIR}/integrates" \
  &&  helper_bootstrap_prod_ci \
  &&  helper_invoke_py "${module}" \
  &&  popd \
  ||  return 1
}

function job_integrates_infra_backup_deploy {
  export TF_VAR_db_user
  export TF_VAR_db_password

      pushd "${STARTDIR}/integrates" \
  &&  echo '[INFO] Logging in to AWS production' \
  &&  CI_COMMIT_REF_NAME=master helper_integrates_aws_login production \
  &&  helper_common_sops_env 'secrets-production.yaml' 'default' \
        DB_USER \
        DB_PASSWD \
  &&  TF_VAR_db_user="${DB_USER}" \
  &&  TF_VAR_db_password="${DB_PASSWD}" \
  &&  pushd deploy/backup/terraform \
    &&  terraform init \
    &&  terraform apply -auto-approve -refresh=true \
  &&  popd \
  &&  popd \
  || return 1
}

function job_integrates_infra_backup_test {
      pushd "${STARTDIR}/integrates" \
  &&  echo '[INFO] Logging in to AWS development' \
  &&  helper_integrates_aws_login development \
  &&  pushd deploy/backup/terraform \
    &&  terraform init \
    &&  tflint --deep --module \
    &&  terraform plan -lock=false -refresh=true \
  &&  popd \
  &&  popd \
  || return 1
}

function job_integrates_infra_database_deploy {
  export TF_VAR_db_user
  export TF_VAR_db_password

      pushd "${STARTDIR}/integrates" \
  &&  echo '[INFO] Logging in to AWS production' \
  &&  CI_COMMIT_REF_NAME=master helper_integrates_aws_login production \
  &&  helper_common_sops_env 'secrets-production.yaml' 'default' \
        DB_USER \
        DB_PASSWD \
  &&  TF_VAR_db_user="${DB_USER}" \
  &&  TF_VAR_db_password="${DB_PASSWD}" \
  &&  pushd deploy/database/terraform \
    &&  terraform init \
    &&  terraform apply -auto-approve -refresh=true \
  &&  popd \
  &&  popd \
  || return 1
}

function job_integrates_infra_database_test {
      pushd "${STARTDIR}/integrates" \
  &&  echo '[INFO] Logging in to AWS development' \
  &&  helper_integrates_aws_login development \
  &&  pushd deploy/database/terraform \
    &&  terraform init \
    &&  tflint --deep --module \
    &&  terraform plan -lock=false -refresh=true \
  &&  popd \
  &&  popd \
  || return 1
}

function job_integrates_infra_cache_db_deploy {
      pushd "${STARTDIR}/integrates" \
  &&  echo '[INFO] Logging in to AWS production' \
  &&  CI_COMMIT_REF_NAME=master helper_integrates_aws_login production \
  &&  pushd deploy/cache-db/terraform \
    &&  terraform init \
    &&  terraform apply -auto-approve -refresh=true \
  &&  popd \
  &&  popd \
  || return 1
}

function job_integrates_infra_cache_db_test {
      pushd "${STARTDIR}/integrates" \
  &&  echo '[INFO] Logging in to AWS development' \
  &&  helper_integrates_aws_login development \
  &&  pushd deploy/cache-db/terraform \
    &&  terraform init \
    &&  tflint --deep --module \
    &&  terraform plan -lock=false -refresh=true \
  &&  popd \
  &&  popd \
  || return 1
}

function job_integrates_infra_django_db_deploy {
  export TF_VAR_db_user
  export TF_VAR_db_password

      pushd "${STARTDIR}/integrates" \
  &&  echo '[INFO] Logging in to AWS production' \
  &&  CI_COMMIT_REF_NAME=master helper_integrates_aws_login production \
  &&  helper_common_sops_env 'secrets-production.yaml' 'default' \
        DB_USER \
        DB_PASSWD \
  &&  TF_VAR_db_user="${DB_USER}" \
  &&  TF_VAR_db_password="${DB_PASSWD}" \
  &&  pushd deploy/django-db/terraform \
    &&  terraform init \
    &&  terraform apply -auto-approve -refresh=true \
  &&  popd \
  &&  popd \
  || return 1
}

function job_integrates_infra_django_db_test {
  export TF_VAR_db_user
  export TF_VAR_db_password

      pushd "${STARTDIR}/integrates" \
  &&  echo '[INFO] Logging in to AWS development' \
  &&  helper_integrates_aws_login development \
  &&  helper_common_sops_env 'secrets-development.yaml' 'default' \
        DB_USER \
        DB_PASSWD \
  &&  TF_VAR_db_user="${DB_USER}" \
  &&  TF_VAR_db_password="${DB_PASSWD}" \
  &&  pushd deploy/django-db/terraform \
    &&  terraform init \
    &&  tflint --deep --module \
    &&  terraform plan -lock=false -refresh=true \
  &&  popd \
  &&  popd \
  || return 1
}

function job_integrates_infra_devicefarm_deploy {
      pushd "${STARTDIR}/integrates" \
  &&  echo '[INFO] Logging in to AWS production' \
  &&  CI_COMMIT_REF_NAME=master helper_integrates_aws_login production \
  &&  pushd deploy/devicefarm/terraform \
    &&  terraform init \
    &&  terraform apply -auto-approve -refresh=true \
  &&  popd \
  &&  popd \
  || return 1
}

function job_integrates_infra_devicefarm_test {
      pushd "${STARTDIR}/integrates" \
  &&  echo '[INFO] Logging in to AWS development' \
  &&  helper_integrates_aws_login development \
  &&  pushd deploy/devicefarm/terraform \
    &&  terraform init \
    &&  tflint --deep --module \
    &&  terraform plan -lock=false -refresh=true \
  &&  popd \
  &&  popd \
  || return 1
}

function job_integrates_infra_resources_deploy {
      pushd "${STARTDIR}/integrates" \
  &&  echo '[INFO] Logging in to AWS production' \
  &&  CI_COMMIT_REF_NAME=master helper_integrates_aws_login production \
  &&  pushd deploy/terraform-resources \
    &&  terraform init \
    &&  terraform apply -auto-approve -refresh=true \
  &&  popd \
  &&  popd \
  || return 1
}

function job_integrates_infra_resources_test {
      pushd "${STARTDIR}/integrates" \
  &&  echo '[INFO] Logging in to AWS development' \
  &&  helper_integrates_aws_login development \
  &&  pushd deploy/terraform-resources \
    &&  terraform init \
    &&  tflint --deep --module \
    &&  terraform plan -lock=false -refresh=true \
  &&  popd \
  || return 1
}

function job_integrates_infra_secret_management_deploy {
      pushd "${STARTDIR}/integrates" \
  &&  echo '[INFO] Logging in to AWS production' \
  &&  CI_COMMIT_REF_NAME=master helper_integrates_aws_login production \
  &&  pushd deploy/secret-management/terraform \
    &&  terraform init \
    &&  terraform apply -auto-approve -refresh=true \
  &&  popd \
  &&  popd \
  || return 1
}

function job_integrates_infra_secret_management_test {
      pushd "${STARTDIR}/integrates" \
  &&  echo '[INFO] Logging in to AWS development' \
  &&  helper_integrates_aws_login development \
  &&  pushd deploy/secret-management/terraform \
    &&  terraform init \
    &&  tflint --deep --module \
    &&  terraform plan -lock=false -refresh=true \
  &&  popd \
  &&  popd \
  || return 1
}

function job_integrates_infra_cluster_deploy {
  local target='deploy/cluster/terraform'

      helper_use_pristine_workdir \
  &&  pushd integrates \
  &&  echo '[INFO] Logging in to AWS production' \
  &&  CI_COMMIT_REF_NAME=master helper_integrates_aws_login production \
  &&  pushd "${target}" \
  &&  terraform init \
  &&  terraform apply -auto-approve -refresh=true \
  &&  popd \
  &&  popd \
  || return 1
}

function job_integrates_infra_cluster_test {
  local target='deploy/cluster/terraform'

      helper_use_pristine_workdir \
  &&  pushd integrates \
  &&  echo '[INFO] Logging in to AWS development' \
  &&  helper_integrates_aws_login development \
  &&  pushd "${target}" \
  &&  terraform init \
  &&  tflint --deep --module \
  &&  terraform plan -lock=false -refresh=true \
  &&  popd \
  &&  popd \
  || return 1
}

function job_integrates_rotate_jwt_token {
  local integrates_repo_id='20741933'
  local var_name='JWT_TOKEN'
  local var_value
  local bytes_of_entropy='32'
  local set_as_masked='true'
  local set_as_protected='false'

      pushd "${STARTDIR}/integrates" \
  &&  echo "[INFO] Extracting ${bytes_of_entropy} bytes of pseudo random entropy" \
  &&  var_value=$(head -c "${bytes_of_entropy}" /dev/urandom | base64) \
  &&  echo '[INFO] Extracting secrets' \
  &&  helper_integrates_aws_login "${ENVIRONMENT_NAME}" \
  &&  helper_common_sops_env "secrets-${ENVIRONMENT_NAME}.yaml" 'default' \
        GITLAB_API_TOKEN \
  &&  echo '[INFO] Updating var in GitLab' \
  &&  helper_common_set_project_variable \
        "${GITLAB_API_TOKEN}" \
        "${integrates_repo_id}" \
        "${var_name}" \
        "${var_value}" \
        "${set_as_protected}" \
        "${set_as_masked}" \
  &&  popd \
  || return 1
}

function job_integrates_test_back {
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
    --ignore 'test_async/functional_test'
  )
  local extra_args=()
  local markers=(
    'not (changes_db or changes_sessions)'
    'changes_db'
    'changes_sessions'
  )

  # shellcheck disable=SC2015
      pushd "${STARTDIR}/integrates" \
  &&  env_prepare_python_packages \
  &&  helper_integrates_set_dev_secrets \
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
  &&  cp -a 'build/coverage/results.xml' "coverage.xml" \
  &&  popd \
  ||  return 1
}

function job_integrates_test_front {
      pushd "${STARTDIR}/integrates/front" \
    &&  npm install --unsafe-perm \
    &&  npm test \
    &&  mv coverage/lcov.info coverage.lcov \
  &&  popd \
  ||  return 1
}

function job_integrates_test_mobile {
      pushd "${STARTDIR}/integrates/mobile" \
    &&  npm install --unsafe-perm \
    &&  npm test \
    &&  mv coverage/lcov.info coverage.lcov \
  &&  popd \
  ||  return 1
}

function job_integrates_deploy_k8s_back_ephemeral {
  local B64_AWS_ACCESS_KEY_ID
  local B64_AWS_SECRET_ACCESS_KEY
  local B64_JWT_TOKEN
  local DATE
  local DEPLOYMENT_NAME
  local files=(
    deploy/ephemeral/variables.yaml
    deploy/ephemeral/ingress.yaml
    deploy/ephemeral/deploy-integrates.yaml
  )
  local vars_to_replace_in_manifest=(
    DATE
    B64_AWS_ACCESS_KEY_ID
    B64_AWS_SECRET_ACCESS_KEY
    B64_JWT_TOKEN
    DEPLOYMENT_NAME
  )

  # shellcheck disable=SC2034
      helper_use_pristine_workdir \
  &&  pushd "${STARTDIR}/integrates" \
  &&  helper_integrates_aws_login 'development' \
  &&  echo "[INFO] Setting namespace preferences..." \
  &&  helper_common_update_kubeconfig FluidServes us-east-1 \
  &&  kubectl config \
        set-context "$(kubectl config current-context)" \
        --namespace=integrates \
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
  &&  echo '[INFO] Applying: deploy/ephemeral/variables.yaml' \
  &&  kubectl apply -f 'deploy/ephemeral/variables.yaml' \
  &&  echo '[INFO] Applying: deploy/ephemeral/ingress.yaml' \
  &&  kubectl apply -f 'deploy/ephemeral/ingress.yaml' \
  &&  echo '[INFO] Applying: deploy/ephemeral/deploy-integrates.yaml' \
  &&  kubectl apply -f 'deploy/ephemeral/deploy-integrates.yaml' \
  &&  kubectl rollout status "deploy/review-${CI_COMMIT_REF_SLUG}" --timeout=5m \
  &&  popd \
  ||  return 1
}

function job_integrates_deploy_k8s_back {
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
      helper_use_pristine_workdir \
  &&  pushd "${STARTDIR}/integrates" \
  &&  CI_COMMIT_REF_NAME='master' helper_integrates_aws_login 'production' \
  &&  helper_common_sops_env 'secrets-production.yaml' 'default' \
        CHECKLY_CHECK_ID \
        CHECKLY_TRIGGER_ID \
        NEW_RELIC_API_KEY \
        NEW_RELIC_APP_ID \
  &&  echo "[INFO] Setting namespace preferences..." \
  &&  helper_common_update_kubeconfig FluidServes us-east-1 \
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
          }" \
  &&  curl "https://api.checklyhq.com/check-groups/${CHECKLY_CHECK_ID}/trigger/${CHECKLY_TRIGGER_ID}" \
        --request 'GET' \
        --data 'deployment=true' \
        --data 'repository=product/integrates' \
        --data "sha=${CI_COMMIT_SHA}" \
  &&  popd \
  ||  return 1
}

function job_integrates_deploy_k8s_stop_ephemeral {
      pushd "${STARTDIR}/integrates" \
  &&  echo "[INFO] Setting namespace preferences..." \
  &&  helper_integrates_aws_login 'development' \
  &&  helper_common_update_kubeconfig FluidServes us-east-1 \
  &&  kubectl config \
        set-context "$(kubectl config current-context)" \
        --namespace=integrates \
  &&  echo '[INFO] Deleting deployments' \
  &&  kubectl delete deployment "review-${CI_COMMIT_REF_SLUG}" \
  &&  kubectl delete service "service-${CI_COMMIT_REF_SLUG}" \
  &&  kubectl delete ingress "review-${CI_COMMIT_REF_SLUG}" \
  &&  popd \
  ||  return 1
}
