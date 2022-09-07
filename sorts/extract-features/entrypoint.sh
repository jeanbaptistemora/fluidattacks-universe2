# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function upload_sorts_results_to_s3 {
  local group="${1}"
  local target="s3://sorts/features/"

  : \
    && aws_login "prod_sorts" "3600" \
    && echo "[INFO] Uploading Sorts feature extraction results to S3" \
    && aws_s3_sync "${PWD}" "${target}" --exclude "*" --include "${group}*.csv" \
    && rm -rf "${group}"*".csv"
}

function extract_features {
  export INTEGRATES_API_TOKEN
  local group="${1}"
  local success

  { clone_services_repository "${group}" || true; } \
    && if ! test -e "groups/${group}/fusion"; then
      echo '[WARNING] No repositories to test' \
        && return 0
    fi \
    && echo '[INFO] Running sorts:' \
    && if sorts --get-file-data "groups/${group}"; then
      echo "[INFO] Succesfully processed: ${group}" \
        && success='true'
    else
      echo "[ERROR] While running sorts on: ${group}" \
        && success='false'
    fi \
    && upload_sorts_results_to_s3 "${group}" \
    && rm -rf "groups/${group}/fusion" \
    && test "${success}" = 'true'
}

function main {
  local groups_file

  : \
    && aws_login "prod_sorts" "3600" \
    && sops_export_vars 'sorts/secrets.yaml' \
      'MIXPANEL_API_TOKEN_SORTS' \
      'REDSHIFT_DATABASE' \
      'REDSHIFT_HOST' \
      'REDSHIFT_PASSWORD' \
      'REDSHIFT_PORT' \
      'REDSHIFT_USER' \
    && use_git_repo_services \
    && groups_file="$(mktemp)" \
    && ls -1 groups > "${groups_file}" \
    && execute_chunk_parallel extract_features "${groups_file}" "15" "gitlab"

}

main "${@}"
