# shellcheck shell=bash

function _replace {
  local src="${1}"
  local from="${2}"
  local to="${3}"

  find "${src}" -type f -exec sed -i "s|${from}|${to}|gI" {} +
}

function deploy {
  local aws_role="${1}"
  local env="${2}"
  local branch="${3}"
  local bugsnag_key='99a64555a50340cfa856f6623c6bf35d'
  local deployment_date
  local bucket_name="integrates.front.${env}.fluidattacks.com"
  local base_url="${bucket_name}/${branch}"
  local cached_urls=(
    "https://${base_url}/static/dashboard/runtime-bundle.min.js"
    "https://${base_url}/static/dashboard/vendors-bundle.min.js"
    "https://${base_url}/static/dashboard/vendors-style.min.css"
    "https://${base_url}/static/dashboard/app-bundle.min.js"
  )
  export CI_COMMIT_SHA
  export CI_COMMIT_SHORT_SHA

  : \
    && aws_login "${aws_role}" "3600" \
    && pushd integrates \
    && sops_export_vars "secrets/${env}.yaml" \
      CLOUDFLARE_API_TOKEN \
    && mkdir -p app \
    && copy "__argCompiledFront__/output/app" app \
    && if test -z "${CI_COMMIT_SHA:-}"; then
      CI_COMMIT_SHA="$(get_commit_from_rev . HEAD)"
    fi \
    && if test -z "${CI_COMMIT_SHORT_SHA:-}"; then
      CI_COMMIT_SHORT_SHA="${CI_COMMIT_SHA:0:8}"
    fi \
    && deployment_date="$(date -u '+%FT%H:%M:%SZ')" \
    && _replace app '__CI_COMMIT_REF_NAME__' "${branch}" \
    && _replace app '__CI_COMMIT_SHA__' "${CI_COMMIT_SHA}" \
    && _replace app '__CI_COMMIT_SHORT_SHA__' "${CI_COMMIT_SHORT_SHA}" \
    && _replace app '__INTEGRATES_BUCKET_NAME__' "${bucket_name}" \
    && _replace app '__INTEGRATES_DEPLOYMENT_DATE__' "${deployment_date}" \
    && aws_s3_sync \
      app \
      "s3://${base_url}/" \
      --delete \
    && bugsnag-announce "${bugsnag_key}" "${env}" \
    && cloudflare_purge_cache \
      "${CLOUDFLARE_API_TOKEN}" \
      "fluidattacks.com" \
      "${cached_urls[@]}" \
    && popd \
    || return 1
}
