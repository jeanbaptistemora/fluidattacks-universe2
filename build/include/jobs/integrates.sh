# shellcheck shell=bash


# Mobile

function job_integrates_mobile_build_android {
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
    -Dorg.gradle.project.android.aapt2FromMavenOverride=${TURTLE_ANDROID_DEPENDENCIES_DIR}/sdk/build-tools/30.0.3/aapt2
  "
  export GRADLE_DAEMON_DISABLED="1"

      if  helper_common_has_any_file_changed \
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
                --non-interactive \
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

function job_integrates_mobile_build_ios {
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
          --non-interactive \
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
          --non-interactive \
    &&  mkdir -p output \
    &&  curl -sSo output/integrates.ipa "$(npx expo-cli url:ipa)" \
    &&  rm -rf ./certs \
    &&  popd \
  ||  return 1
}

function job_integrates_mobile_deploy_ota_development {
  local env='development'
  local release_channel="${CI_COMMIT_REF_NAME}"

      pushd integrates \
    &&  helper_integrates_aws_login "${env}" \
    &&  helper_integrates_mobile_deploy_ota \
          "${env}" \
          "${release_channel}" \
  &&  popd \
  ||  return 1
}

function job_integrates_mobile_deploy_ota_production {
  local env='production'
  local release_channel='master'

      pushd integrates \
    &&  helper_integrates_aws_login "${env}" \
    &&  helper_integrates_mobile_deploy_ota \
          "${env}" \
          "${release_channel}" \
  &&  popd \
  ||  return 1
}

function job_integrates_mobile_deploy_playstore {
  export LANG=en_US.UTF-8

      if  helper_common_has_any_file_changed \
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

function job_integrates_mobile_test_functional_local {
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

function job_integrates_mobile_test_unit {
      pushd "${STARTDIR}/integrates/mobile" \
    &&  npm install --unsafe-perm \
    &&  npm test \
    &&  mv coverage/lcov.info coverage.lcov \
  &&  popd \
  ||  return 1
}

function job_integrates_mobile_lint {
      pushd integrates/mobile \
    &&  npm install \
    &&  npm run lint \
  &&  popd \
  ||  return 1
}


# Front

function job_integrates_front_build_production {
      pushd integrates \
    &&  helper_integrates_front_build \
  &&  popd \
  ||  return 1
}

function job_integrates_front_deploy_development {
  local branch="${CI_COMMIT_REF_NAME}"
  local env='development'

      pushd integrates \
    &&  helper_integrates_front_deploy \
          "${branch}" \
          "${env}" \
  &&  popd \
  ||  return 1
}

function job_integrates_front_deploy_production {
  local branch='master'
  local env='production'

      pushd integrates \
    &&  helper_integrates_front_deploy \
          "${branch}" \
          "${env}" \
  &&  popd \
  ||  return 1
}

function job_integrates_front_lint_styles {
  local err_count
        pushd integrates/front \
      &&  npm install \
      &&  echo "[INFO] Running Stylelint to lint CSS files" \
      &&  if npm run lint:stylelint
          then
            echo '[INFO] All styles are ok!'
          else
                err_count="$(npx stylelint '**/*.css' | wc -l || true)" \
            &&  echo "[ERROR] ${err_count} errors found in styles!" \
            &&  return 1
          fi \
    && popd \
    || return 1
}


# Back

function job_integrates_back_build_production {
  helper_integrates_back_build 'master'
}

function job_integrates_back_build_development {
  helper_integrates_back_build "${CI_COMMIT_REF_NAME}"
}

function job_integrates_back_deploy_development {
  local env='development'
  export BRANCH
  export DATE
  export DEPLOYMENT_NAME
  export B64_INTEGRATES_DEV_AWS_ACCESS_KEY_ID
  export B64_INTEGRATES_DEV_AWS_SECRET_ACCESS_KEY
  export B64_CI_COMMIT_REF_NAME

  local region='us-east-1'
  local cluster='integrates-cluster'
  local namespace='ephemeral'
  local deployment="${CI_COMMIT_REF_NAME}"
  local timeout='10m'
  local files_path='deploy/ephemeral'

      helper_common_use_pristine_workdir \
  &&  helper_integrates_aws_login "${env}" \
  &&  pushd integrates \
    &&  BRANCH="${CI_COMMIT_REF_NAME}" \
    &&  DATE="$(date)" \
    &&  DEPLOYMENT_NAME="${deployment}" \
    &&  B64_INTEGRATES_DEV_AWS_ACCESS_KEY_ID=$(helper_integrates_to_b64 "${INTEGRATES_DEV_AWS_ACCESS_KEY_ID}") \
    &&  B64_INTEGRATES_DEV_AWS_SECRET_ACCESS_KEY=$(helper_integrates_to_b64 "${INTEGRATES_DEV_AWS_SECRET_ACCESS_KEY}") \
    &&  B64_CI_COMMIT_REF_NAME=$(helper_integrates_to_b64 "${CI_COMMIT_REF_NAME}") \
    &&  helper_integrates_back_deploy \
          "${region}" \
          "${cluster}" \
          "${namespace}" \
          "${deployment}" \
          "${timeout}" \
          "${files_path}" \
  &&  popd \
  ||  return 1
}

function job_integrates_back_deploy_production {
  local env='production'
  export DATE
  export B64_INTEGRATES_PROD_AWS_ACCESS_KEY_ID
  export B64_INTEGRATES_PROD_AWS_SECRET_ACCESS_KEY
  export B64_CI_COMMIT_REF_NAME

  local region='us-east-1'
  local cluster='integrates-cluster'
  local namespace='production'
  local deployment='master'
  local timeout='10m'
  local files_path='deploy/production'

      helper_common_use_pristine_workdir \
  &&  helper_integrates_aws_login "${env}" \
  &&  pushd integrates \
    &&  DATE="$(date)" \
    &&  B64_INTEGRATES_PROD_AWS_ACCESS_KEY_ID=$(helper_integrates_to_b64 "${INTEGRATES_PROD_AWS_ACCESS_KEY_ID}") \
    &&  B64_INTEGRATES_PROD_AWS_SECRET_ACCESS_KEY=$(helper_integrates_to_b64 "${INTEGRATES_PROD_AWS_SECRET_ACCESS_KEY}") \
    &&  B64_CI_COMMIT_REF_NAME=$(helper_integrates_to_b64 'master') \
    &&  helper_integrates_back_deploy \
          "${region}" \
          "${cluster}" \
          "${namespace}" \
          "${deployment}" \
          "${timeout}" \
          "${files_path}" \
    &&  helper_integrates_back_deploy_newrelic \
    &&  helper_integrates_back_deploy_checkly \
  &&  popd \
  ||  return 1
}

function job_integrates_back_clean_development_environments {
  local cluster='integrates-cluster'
  local namespace='ephemeral'
  local region='us-east-1'

      helper_common_use_pristine_workdir \
  &&  pushd integrates \
  &&  echo "[INFO] Setting namespace preferences..." \
  &&  helper_integrates_aws_login 'development' \
  &&  helper_common_update_kubeconfig "${cluster}" "${region}" \
  &&  echo '[INFO] Deleting ephemeral environments' \
  &&  kubectl delete --all deployment -n "${namespace}" \
  &&  kubectl delete --all secret -n "${namespace}" \
  &&  kubectl delete --all service -n "${namespace}" \
  &&  kubectl delete --all ingress -n "${namespace}" \
  &&  popd \
  ||  return 1
}

function job_integrates_back_test_e2e {
  local args_pytest=(
    --capture tee-sys
    --disable-pytest-warnings
    --exitfirst
    --maxfail 20
    --show-capture no
    --verbose
    --reruns 10
    --test-group-count "${CI_NODE_TOTAL}"
    --test-group "${CI_NODE_INDEX}"
    -n 2
  )

      pushd integrates \
    &&  env_prepare_python_packages \
    &&  helper_integrates_aws_login 'development' \
    &&  helper_common_sops_env 'secrets-development.yaml' 'default' \
          TEST_E2E_USER \
          STARLETTE_SESSION_KEY \
    &&  pushd test_e2e \
      &&  pytest "${args_pytest[@]}" < /dev/null \
    &&  popd \
  &&  popd \
  ||  return 1
}

function job_integrates_back_test_unit {
  local common_args=(
    -n auto
    --dist 'loadscope'
    --verbose
    --maxfail '20'
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
    'not changes_db'
    'changes_db'
  )

  # shellcheck disable=SC2015
      pushd integrates \
  &&  env_prepare_python_packages \
  &&  helper_integrates_set_dev_secrets \
  &&  helper_integrates_serve_dynamo \
  &&  helper_integrates_serve_minio \
  &&  sleep 10 \
  &&  helper_integrates_serve_redis \
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

function job_integrates_back_test_functional {
  local common_args=(
    --verbose
    --cov "${pyPkgIntegratesBack}/site-packages/backend"
    --cov-report 'term'
    --cov-report 'html:build/coverage/functional/html'
    --cov-report 'xml:build/coverage/functional/results.xml'
    --cov-report 'annotate:build/coverage/functional/annotate'
    --disable-warnings
  )
  local markers=(
    'priority'
    'not priority'
  )

  # shellcheck disable=SC2015
      pushd integrates \
  &&  env_prepare_python_packages \
  &&  helper_integrates_set_dev_secrets \
  &&  helper_integrates_serve_dynamo \
  &&  helper_integrates_serve_minio \
  &&  sleep 10 \
  &&  helper_integrates_serve_redis \
  &&  for marker in "${markers[@]}"
      do
            echo "[INFO] Running marker: ${marker}" \
        &&  pytest \
              -m "${marker}" \
              "${common_args[@]}" \
              'test_async/functional_test' \
        ||  return 1
      done \
  &&  popd \
  ||  return 1
}

function job_integrates_back_build_lambdas_production {
      pushd integrates \
    &&  helper_integrates_back_build_lambda 'send_mail_notification' \
    &&  helper_integrates_back_build_lambda 'project_to_pdf' \
  &&  popd \
  || return 1
}

function job_integrates_back_build_lambdas_development {
  job_integrates_back_build_lambdas_production
}

function job_integrates_back_lint {
      pushd integrates \
  &&  env_prepare_python_packages \
  &&  mypy --strict --ignore-missing-imports analytics/ \
        back/migrations/ \
        back \
  &&  mypy --strict --ignore-missing-imports --follow-imports=skip \
        back/packages/integrates-back/backend/decorators.py \
        back/packages/integrates-back/backend/api/ \
        back/packages/integrates-back/backend/authz/ \
        back/packages/integrates-back/backend/dal/ \
        back/packages/integrates-back/backend/utils/ \
  &&  mypy --ignore-missing-imports --follow-imports=skip \
        back/packages/integrates-back \
  &&  prospector -F -s veryhigh analytics/ \
  &&  prospector -F -s veryhigh back \
  &&  prospector -F -s veryhigh lambda \
  &&  prospector -F -s veryhigh deploy/permissions-matrix \
  &&  npx graphql-schema-linter \
        --except 'enum-values-have-descriptions,fields-are-camel-cased,fields-have-descriptions,input-object-values-are-camel-cased,relay-page-info-spec,types-have-descriptions,arguments-have-descriptions' \
        back/packages/integrates-back/backend/api/schema/**/*.graphql \
        back/packages/integrates-back/backend/api/schema/types/**/*.graphql \
  &&  popd \
  || return 1
}

function job_integrates_back_lint_e2e {
  local modules=(
    src/
    src/tests/
  )

      pushd integrates/test_e2e \
    &&  env_prepare_python_packages \
    &&  mypy --config-file settings.cfg "${modules[@]}" \
    &&  prospector --profile profile.yaml . \
  &&  popd \
  ||  return 1
}

function job_integrates_back_lint_graphics {
      env_prepare_node_modules \
  &&  pushd integrates/back/app/templates/static/graphics \
        &&  eslint --config .eslintrc --fix . \
  &&  popd \
  ||  return 1
}

# Analytics

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
  export PYTHONPATH="${PWD}:${PWD}/analytics:${PYTHONPATH}"
  export TEMP_FILE1
  local remote_bucket='fluidintegrates.analytics'

      find 'analytics/generators' -wholename '*.py' | LC_ALL=C sort > "${TEMP_FILE1}" \
  &&  helper_common_execute_chunk_parallel \
        "_execute_analytics_generator" \
        "${TEMP_FILE1}" \
  &&  echo '[INFO] Uploading documents' \
  &&  aws s3 sync \
        'analytics/generators' "s3://${remote_bucket}/${CI_COMMIT_REF_NAME}/documents" \

}

function _job_integrates_analytics_make_snapshots {
  export CI_COMMIT_REF_NAME
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
            helper_integrates_serve_dynamo \
        &&  helper_integrates_serve_redis \
        &&  helper_integrates_serve_minio
      fi \
  &&  _job_integrates_analytics_make_documents \
  &&  popd \
  ||  return 1
}

function job_integrates_analytics_make_documents_prod {
      pushd "${STARTDIR}/integrates" \
  &&  env_prepare_python_packages \
  &&  helper_bootstrap_prod_ci \
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
  &&  helper_bootstrap_prod_ci \
  &&  _job_integrates_analytics_make_snapshots \
  &&  popd \
  ||  return 1
}


# Others

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

function job_integrates_deploy_permissions_matrix {
  export PYTHONPATH="${pyPkgPandas}/lib/python3.7/site-packages"
  export PYTHONPATH="${pyPkgNumpy}/lib/python3.7/site-packages:${PYTHONPATH}"
  export PYTHONPATH="${pyPkgMagic}/lib/python3.7/site-packages:${PYTHONPATH}"
  export PYTHONPATH=".:${PYTHONPATH}"

      pushd "${STARTDIR}/integrates" \
  &&  env_prepare_python_packages \
  &&  helper_integrates_set_dev_secrets \
  &&  sleep 3 \
  &&  helper_integrates_serve_redis \
  &&  echo '[INFO] Deploying permissions matrix' \
  &&  python3 deploy/permissions-matrix/matrix.py \
  &&  popd \
  ||  return 1
}

function job_integrates_probes_liveness {
  local aws_creds="${1}"
  local localhost_endpoint="${2}"
  local internet_endpoint="${3}"

      helper_integrates_probe_aws_credentials "${aws_creds}" \
  &&  helper_integrates_probe_curl "${localhost_endpoint}" \
  &&  helper_integrates_probe_curl "${internet_endpoint}"
}

function job_integrates_probes_readiness {
  local aws_creds="${1}"
  local localhost_endpoint="${2}"

      helper_integrates_probe_aws_credentials "${aws_creds}" \
  &&  helper_integrates_probe_curl "${localhost_endpoint}"
}

function job_integrates_serve_components {
  local aws_creds="${1}"

  trap 'helper_common_kill_attached_processes 5' SIGINT

      pushd integrates \
    &&  helper_integrates_aws_login "${aws_creds}" \
    &&  for arg in "${@:1}"
        do
              if echo "${arg}" | grep -qP '^http'
              then
                    for internal_args in $(helper_common_string_to_lines "${arg}" '/')
                    do
                          back_args+=( "${internal_args}" ) \
                      ||  return 1
                    done \
                &&  helper_integrates_serve_back "${back_args[@]}"
              elif [[ "${arg}" == 'redis'  ]]
              then
                helper_integrates_serve_redis
              elif [[ "${arg}" == 'dynamo' ]]
              then
                helper_integrates_serve_dynamo
              elif [[ "${arg}" == 'minio' ]]
              then
                helper_integrates_serve_minio
              elif [[ "${arg}" == 'front' ]]
              then
                helper_integrates_serve_front
              elif [[ "${arg}" == 'mobile' ]]
              then
                helper_integrates_serve_mobile
              fi \
          ||  return 1
        done \
    &&  wait \
  &&  popd \
  ||  return 1
}


function _job_integrates_make_migration {
  local env="${1}"
  local stage="${2}"
  local migration_file="${3}"

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

function job_integrates_reset {
  local files_to_delete=(
    'app/static/dashboard/'
    'app/backend/reports/images/*'
    'back/packages/integrates-back/backend/reports/tpls/*'
    'back/packages/integrates-back/backend/reports/results/results_pdf/*'
    'back/packages/integrates-back/backend/reports/results/results_excel/*'
    'build/coverage'
    'back/packages/*/*.egg-info'
    'front/coverage'
    'geckodriver.log'
    'mobile/coverage'
    'front/coverage.lcov'
    'front/node_modules'
    'lambda/.venv.*'
    'mobile/.expo/'
    'mobile/google-services.json'
    'TEMP_FD'
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
