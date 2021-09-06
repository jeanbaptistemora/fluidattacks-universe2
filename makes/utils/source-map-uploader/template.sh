# shellcheck shell=bash

function source_map_uploader {
  local api_key="${1}"
  local base_url="${2}"
  local directory="${3}"

  bugsnag-source-maps upload-browser \
    --api-key "${api_key}" \
    --app-version "${CI_COMMIT_SHORT_SHA}" \
    --base-url "${base_url}" \
    --directory "${directory}"
}
