# shellcheck shell=bash

function serve {
  local buckets_by_branch=(
    'fluidintegrates.analytics'
  )
  local buckets_by_group=(
    'fluidintegrates.evidences'
    'fluidintegrates.forces'
    'fluidintegrates.resources'
  )
  local buckets_by_root=(
    'fluidintegrates.reports'
  )
  local buckets=(
    "${buckets_by_branch[@]}"
    "${buckets_by_group[@]}"
    "${buckets_by_root[@]}"
  )
  local host='localhost'
  local port='9000'
  local state_path='.Storage'

  aws_login_dev_new \
    && sops_export_vars __argDevSecrets__ \
      TEST_PROJECTS \
    && mkdir -p "${state_path}" \
    && echo -e "${TEST_PROJECTS//,/\\n}" > "${state_path}/projects" \
    && mapfile -t TEST_PROJECTS < "${state_path}/projects" \
    && kill_port "${port}" 29000 \
    && {
      MINIO_ACCESS_KEY='test' \
        MINIO_SECRET_KEY='testtest' \
        __argMinioLocal__ server "${state_path}" --address "${host}:${port}" &
    } \
    && wait_port 10 "${host}:${port}" \
    && sleep 3 \
    && __argMinioCli__ alias set storage "http://${host}:${port}" 'test' 'testtest' \
    && __argMinioCli__ admin user add storage "${AWS_ACCESS_KEY_ID}" "${AWS_SECRET_ACCESS_KEY}" \
    && __argMinioCli__ admin policy set storage readwrite user="${AWS_ACCESS_KEY_ID}" \
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
        && for bucket in "${buckets_by_branch[@]}"; do
          aws_s3_sync \
            "s3://${bucket}/${CI_COMMIT_REF_NAME}" \
            "${state_path}/${bucket}/${CI_COMMIT_REF_NAME}" \
            --delete \
            || return 1
        done
    fi \
    && done_port 29000 \
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
