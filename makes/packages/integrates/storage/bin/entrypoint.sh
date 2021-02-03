# shellcheck shell=bash

source '__envUtilsAws__'
source '__envUtilsSops__'

function main {
  local buckets_by_branch=(
    'fluidintegrates.analytics'
  )
  local buckets_by_group=(
    'fluidintegrates.evidences'
    'fluidintegrates.forces'
    'fluidintegrates.reports'
    'fluidintegrates.resources'
  )
  local host='localhost'
  local port='9000'
  local state_path='.Storage'

      aws_login_dev integrates \
  &&  sops_export_vars 'integrates/secrets-development.yaml' 'default' \
        TEST_PROJECTS \
  &&  mkdir -p "${state_path}" \
  &&  echo "${TEST_PROJECTS}" > "${state_path}/projects" \
  &&  read -a TEST_PROJECTS -d , -r < "${state_path}/projects" \
  &&  __envKillPidListeningOnPort__ "${port}" \
  &&  { MINIO_ACCESS_KEY='test' \
        MINIO_SECRET_KEY='testtest' \
        __envMinioLocal__ server "${state_path}" --address "${host}:${port}" &
      } \
  &&  __envWait__ 10 "${host}:${port}" \
  &&  sleep 1 \
  &&  __envMinioCli__ alias set storage "http://${host}:${port}" 'test' 'testtest' \
  &&  __envMinioCli__ admin user add storage "${AWS_ACCESS_KEY_ID}" "${AWS_SECRET_ACCESS_KEY}" \
  &&  __envMinioCli__ admin policy set storage readwrite user="${AWS_ACCESS_KEY_ID}" \
  &&  for bucket in "${buckets_by_branch[@]}" "${buckets_by_group[@]}"
      do
            __envMinioCli__ mb --ignore-existing "storage/${bucket}" \
        ||  return 1
      done \
  &&  for project in "${TEST_PROJECTS[@]}"
      do
        for bucket in "${buckets_by_group[@]}"
        do
              aws_s3_sync \
                "s3://${bucket}/${project}" \
                "${state_path}/${bucket}/${project}" \
                --delete \
          ||  return 1
        done
      done \
  &&  for bucket in "${buckets_by_branch[@]}"
      do
            aws_s3_sync \
              "s3://${bucket}/${CI_COMMIT_REF_NAME}" \
              "${state_path}/${bucket}/${CI_COMMIT_REF_NAME}" \
              --delete \
        ||  return 1
      done \
  &&  echo '[INFO] Storage is ready' \
  &&  wait
}

main "${@}"
