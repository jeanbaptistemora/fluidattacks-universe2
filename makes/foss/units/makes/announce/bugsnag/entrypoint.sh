# shellcheck shell=bash

function main {
  local api_key="${1}"
  local release_stage="${2}"

  bugsnag-build-reporter \
    --api-key "${api_key}" \
    --app-version "${CI_COMMIT_SHORT_SHA}" \
    --builder-name "${CI_COMMIT_AUTHOR}" \
    --release-stage "${release_stage}" \
    --source-control-provider 'gitlab' \
    --source-control-repository 'https://gitlab.com/fluidattacks/product' \
    --source-control-revision "${CI_COMMIT_SHA}"
}

main "${@}"
