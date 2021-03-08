# shellcheck shell=bash

function _replace {
  local src="${1}"
  local from="${2}"
  local to="${3}"

  find "${src}" -type f -exec sed -i "s|${from}|${to}|g" {} +
}

function deploy {
  local env="${1}"
  local endpoint="${2}"
  local branch="${3}"
  local front_path="${4}"
  local bugsnag_key='99a64555a50340cfa856f6623c6bf35d'
  local deployment_date
  export CI_COMMIT_SHA
  export CI_COMMIT_SHORT_SHA

      "aws_login_${env}" integrates \
  &&  pushd integrates \
    &&  mkdir -p app/static \
    &&  copy "${front_path}/output/app/static" app/static \
    &&  deployment_date="$(date -u '+%FT%H:%M:%SZ')" \
    &&  _replace app '__CI_COMMIT_SHA__' "${CI_COMMIT_SHA}" \
    &&  _replace app '__CI_COMMIT_SHORT_SHA__' "${CI_COMMIT_SHORT_SHA}" \
    &&  _replace app '__INTEGRATES_DEPLOYMENT_DATE__' "${deployment_date}" \
    &&  aws_s3_sync \
          app \
          "s3://integrates.front.${endpoint}.fluidattacks.com/${branch}/" \
          --delete \
    &&  makes-announce-bugsnag "${bugsnag_key}" "${endpoint}" \
  &&  popd \
  ||  return 1
}
