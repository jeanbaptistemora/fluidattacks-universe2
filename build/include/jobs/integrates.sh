# shellcheck shell=bash


# Mobile

# This job is used locally and should be migrated to makes
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

# Back

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
