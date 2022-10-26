# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function serve {
  local main_bucket='integrates'
  local bucket_paths_by_group=(
    'evidences'
    'resources'
    'forces'
    'continuous-repositories'
  )
  local bucket_paths_by_branch=(
    'analytics'
  )
  local bucket_paths_by_root=(
    'reports'
  )
  local bill_bucket='continuous-data'
  local bucket_paths=(
    "${bill_bucket}"
    "${bucket_paths_by_group[@]}"
    "${bucket_paths_by_branch[@]}"
    "${bucket_paths_by_root[@]}"
  )
  local host='0.0.0.0'
  local port='9000'
  local state_path='.Storage'
  local bill_date

  : \
    && sops_export_vars __argDevSecrets__ \
      TEST_PROJECTS \
      MINIO_PASS \
      MINIO_USER \
    && mkdir -p "${state_path}" \
    && echo -e "${TEST_PROJECTS//,/\\n}" > "${state_path}/projects" \
    && mapfile -t TEST_PROJECTS < "${state_path}/projects" \
    && kill_port "${port}" \
    && {
      MINIO_ACCESS_KEY='test' \
        MINIO_SECRET_KEY='testtest' \
        __argMinioLocal__ server "${state_path}" --address "${host}:${port}" &
    } \
    && wait_port 10 "${host}:${port}" \
    && sleep 3 \
    && __argMinioCli__ alias set storage "http://${host}:${port}" 'test' 'testtest' \
    && __argMinioCli__ admin user add storage "${MINIO_USER}" "${MINIO_PASS}" \
    && __argMinioCli__ admin policy set storage readwrite user="${MINIO_USER}" \
    && for bucket_path in "${bucket_paths[@]}"; do
      __argMinioCli__ mc mb --ignore-existing "storage/${main_bucket}/${bucket_path}" \
        || return 1
    done \
    && if test "${POPULATE}" != 'false'; then
      for project in "${TEST_PROJECTS[@]}"; do
        for bucket_path in "${bucket_paths_by_group[@]}"; do
          aws_s3_sync \
            "s3://${main_bucket}/${bucket_path}/${project}" \
            "${state_path}/${main_bucket}/${bucket_path}/${project}" \
            --delete \
            || return 1
        done
      done \
        && if test -z "${CI_COMMIT_REF_NAME:-}"; then
          CI_COMMIT_REF_NAME="$(get_abbrev_rev . HEAD)"
        fi \
        && if test "${CI_COMMIT_REF_NAME}" != "trunk"; then
          for bucket_path in "${bucket_paths_by_branch[@]}"; do
            aws_s3_sync \
              "s3://${main_bucket}/${bucket_path}/${CI_COMMIT_REF_NAME}" \
              "${state_path}/${main_bucket}/${bucket_path}/${CI_COMMIT_REF_NAME}" \
              --delete \
              || return 1
          done
        fi \
        && bill_date="$(date +'%Y/%m')" \
        && aws_s3_sync \
          "s3://${main_bucket}/${bill_bucket}/bills/test" \
          "${state_path}/${main_bucket}/${bill_bucket}/bills/${bill_date}" \
          --delete
    fi \
    && done_port "${host}" 29000 \
    && echo '[INFO] Storage is ready' \
    && wait
}

function serve_daemon {
  kill_port 29000 \
    && { serve "${@}" & } \
    && wait_port 300 localhost:29000
}

function main {
  export POPULATE="${POPULATE:-true}"

  case "${DAEMON:-}" in
    true) serve_daemon "${@}" ;;
    *) serve "${@}" ;;
  esac
}

main "${@}"
