# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function serve {
  local buckets_by_branch=(
    'fluidintegrates.analytics'
  )
  local buckets_by_group=(
    'fluidintegrates.evidences'
    'fluidintegrates.forces'
    'fluidintegrates.resources'
    'continuous-repositories'
  )
  local buckets_by_root=(
    'fluidintegrates.reports'
  )
  local bill_bucket='continuous-data'
  local buckets=(
    "${bill_bucket}"
    "${buckets_by_branch[@]}"
    "${buckets_by_group[@]}"
    "${buckets_by_root[@]}"
  )
  local host='127.0.0.1'
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
    && for bucket in "${buckets[@]}"; do
      __argMinioCli__ mb --ignore-existing "storage/${bucket}" \
        || return 1
    done \
    && if test "${POPULATE}" != 'false'; then
      for project in "${TEST_PROJECTS[@]}"; do
        for bucket in "${buckets_by_group[@]}"; do
          aws_s3_sync \
            "s3://${bucket}/${project}" \
            "${state_path}/${bucket}/${project}" \
            --delete \
            || return 1
        done
      done \
        && if test -z "${CI_COMMIT_REF_NAME:-}"; then
          CI_COMMIT_REF_NAME="$(get_abbrev_rev . HEAD)"
        fi \
        && if test "${CI_COMMIT_REF_NAME}" != "trunk"; then
          for bucket in "${buckets_by_branch[@]}"; do
            aws_s3_sync \
              "s3://${bucket}/${CI_COMMIT_REF_NAME}" \
              "${state_path}/${bucket}/${CI_COMMIT_REF_NAME}" \
              --delete \
              || return 1
          done
        fi \
        && bill_date="$(date +'%Y/%m')" \
        && aws_s3_sync \
          "s3://${bill_bucket}/bills/test" \
          "${state_path}/${bill_bucket}/bills/${bill_date}" \
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
