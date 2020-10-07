# shellcheck shell=bash

function job_observes_formstack {
      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_observes_formstack \
  ||  return 1
}

function job_observes_dynamodb {
      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_observes_dynamodb "./observes/conf/awsdynamodb.json" "dynamodb" \
  ||  return 1
}

function job_observes_dynamodb_forces {
      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_observes_dynamodb \
      "./observes/conf/awsdynamodb_forces.json" \
      "dynamodb_forces" \
  ||  return 1
}

function job_observes_dynamodb_forces_on_aws {
  local vcpus='2'
  local memory='7200'
  local attempts='10'
  local timeout='18000'
  local jobname="observes_dynamodb_forces"
  local jobqueue='default'

      helper_observes_aws_login prod \
  &&  helper_common_run_on_aws \
        "${vcpus}" \
        "${memory}" \
        "${attempts}" \
        "${timeout}" \
        "${jobname}" \
        "${jobqueue}" \
        'observes_dynamodb_forces'
}

function job_observes_services_toe {
      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_observes_services_toe \
  ||  return 1
}

function job_observes_gitlab {
      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_observes_gitlab \
  ||  return 1
}

function job_observes_gitlab_on_aws {
  local vcpus='1'
  local memory='900'
  local attempts='10'
  local timeout='18000'
  local jobname="observes_gitlab"
  local jobqueue='default-uninterruptible'

      helper_observes_aws_login prod \
  &&  helper_common_run_on_aws \
        "${vcpus}" \
        "${memory}" \
        "${attempts}" \
        "${timeout}" \
        "${jobname}" \
        "${jobqueue}" \
        'observes_gitlab'
}

function job_observes_timedoctor {
      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_observes_timedoctor \
  ||  return 1
}

function job_observes_zoho {
      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_observes_zoho \
  ||  return 1
}

function job_observes_code_upload_all_groups_on_aws {
  local groups_file="${TEMP_FILE1}"

      helper_list_services_groups "${groups_file}" \
  &&  while read -r group
      do
            echo "[INFO] Submitting: ${group}" \
        &&  job_observes_code_upload_group_on_aws "${group}" \
        ||  return 1
      done < "${groups_file}"

}

function job_observes_code_upload_group {
  local mock_integrates_api_token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.xxx'
  local group="${1}"

      if test -z "${group}"
      then
            echo '[INFO] Please set the first argument to the group name' \
        &&  return 1
      fi \
  &&  env_prepare_python_packages \
  &&  helper_observes_aws_login prod \
  &&  helper_common_sops_env 'observes/secrets-prod.yaml' 'default' \
        'REDSHIFT_DATABASE' \
        'REDSHIFT_HOST' \
        'REDSHIFT_PASSWORD' \
        'REDSHIFT_PORT' \
        'REDSHIFT_USER' \
  &&  helper_use_services \
    &&  echo "[INFO] Working on ${group}" \
    &&  echo "[INFO] Cloning ${group}" \
    &&  if  CI=true \
            CI_COMMIT_REF_NAME='master' \
            INTEGRATES_API_TOKEN="${mock_integrates_api_token}" \
            PROD_AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" \
            PROD_AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" \
            melts drills --pull-repos "${group}"
        then
              echo "[INFO] Apending mailmaps" \
          &&  shopt -s nullglob \
          &&  for repo in "groups/${group}/fusion/"*
              do
                    cp -f '.groups-mailmap' "${repo}/.mailmap" \
                ||  return 1
              done \
          &&  echo "[INFO] Executing ${group}" \
          &&  python3 "${STARTDIR}/observes/code/upload.py" \
                --namespace "${group}" \
                "groups/${group}/fusion/"* \
          &&  shopt -u nullglob \
          &&  rm -rf "groups/${group}/fusion/" \

        fi \
  &&  popd \
  ||  return 1

}

function job_observes_batch_stability {
      env_prepare_python_packages \
  &&  helper_observes_aws_login prod \
  &&  python3 observes/batch/stability.py
}

function job_observes_code_upload_group_on_aws {
  local group="${1}"
  local vcpus='1'
  local memory='1800'
  local attempts='10'
  local timeout='7200'
  local jobname="observes_code_upload_group__${group}"
  local jobqueue='default'

      if test -z "${group}"
      then
            echo '[INFO] Please set the first argument to the group name' \
        &&  return 1
      fi \
  &&  helper_observes_aws_login prod \
  &&  helper_common_run_on_aws \
        "${vcpus}" \
        "${memory}" \
        "${attempts}" \
        "${timeout}" \
        "${jobname}" \
        "${jobqueue}" \
        'observes_code_upload_group' "${group}"
}

function job_observes_code_amend_authors {
  export GITLAB_API_USER
  export GITLAB_API_TOKEN

      env_prepare_python_packages \
  &&  helper_observes_aws_login prod \
  &&  helper_common_sops_env 'observes/secrets-prod.yaml' 'default' \
        'REDSHIFT_DATABASE' \
        'REDSHIFT_HOST' \
        'REDSHIFT_PASSWORD' \
        'REDSHIFT_PORT' \
        'REDSHIFT_USER' \
  &&  helper_use_services \
    &&  python3 "${STARTDIR}/observes/code/ammend_authors.py" \
          --mailmap '.groups-mailmap' \
  &&  popd \
  ||  return 1
}

function job_observes_code_amend_authors_on_aws {
  local vcpus='1'
  local memory='900'
  local attempts='10'
  local timeout='18000'
  local jobname='observes_code_amend_authors'
  local jobqueue='default'

      helper_observes_aws_login prod \
  &&  helper_common_run_on_aws \
        "${vcpus}" \
        "${memory}" \
        "${attempts}" \
        "${timeout}" \
        "${jobname}" \
        "${jobqueue}" \
        'observes_code_amend_authors'
}

function job_observes_code_compute_bills {
  export GITLAB_API_USER
  export GITLAB_API_TOKEN
  local bucket_month
  local bucket_day
  local folder

      env_prepare_python_packages \
  &&  helper_observes_aws_login prod \
  &&  helper_common_sops_env 'observes/secrets-prod.yaml' 'default' \
        'REDSHIFT_DATABASE' \
        'REDSHIFT_HOST' \
        'REDSHIFT_PASSWORD' \
        'REDSHIFT_PORT' \
        'REDSHIFT_USER' \
  &&  folder="$(mktemp -d)" \
  &&  bucket_month="s3://continuous-data/bills/$(date +%Y)/$(date +%m)" \
  &&  bucket_day="s3://continuous-data/bills/$(date +%Y)/$(date +%m)/$(date +%d)" \
  &&  echo "[INFO] Temporary results folder: ${folder}" \
  &&  python3 "${STARTDIR}/observes/code/compute_bills.py" \
        --folder "${folder}" \
        --year "$(date +%Y)" \
        --month "$(date +%m)" \
  &&  helper_services_aws_login prod \
  &&  echo "[INFO] Syncing data from: ${folder} to ${bucket_month}" \
  &&  aws s3 sync "${folder}" "${bucket_month}" \
  &&  echo "[INFO] Syncing data from: ${folder} to ${bucket_day}" \
  &&  aws s3 sync "${folder}" "${bucket_day}" \

}

function job_observes_code_mirror_all_groups_to_s3_on_aws {
  local groups_file="${TEMP_FILE1}"

      helper_list_services_groups "${groups_file}" \
  &&  while read -r group
      do
            echo "[INFO] Submitting: ${group}" \
        &&  job_observes_code_mirror_group_to_s3_on_aws "${group}" \
        ||  return 1
      done < "${groups_file}"
}

function job_observes_code_mirror_group_to_s3 {
  local mock_integrates_api_token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.xxx'
  local group="${1}"

      if test -z "${group}"
      then
            echo '[INFO] Please set the first argument to the group name' \
        &&  return 1
      fi \
  &&  helper_observes_aws_login prod \
  &&  helper_use_services \
    &&  echo "[INFO] Working on ${group}" \
    &&  echo "[INFO] Cloning ${group} from source Git repository" \
    &&  CI='true' \
        CI_COMMIT_REF_NAME='master' \
        INTEGRATES_API_TOKEN="${mock_integrates_api_token}" \
        PROD_AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" \
        PROD_AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" \
        melts resources --clone-from-customer-git "${group}" \
    &&  if find "groups/${group}/fusion/"* -maxdepth 0 -type d
        then
              echo '[INFO] Pushing repositories to S3' \
          &&  CI='true' \
              CI_COMMIT_REF_NAME='master' \
              INTEGRATES_API_TOKEN="${mock_integrates_api_token}" \
              PROD_AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" \
              PROD_AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" \
              melts drills --push-repos "${group}"
        else
              echo '[INFO] Unable to clone repositories from source' \
          &&  echo '[INFO] Skipping push to S3'
        fi \
    &&  rm -rf "groups/${group}/fusion/" \
  &&  popd \
  ||  return 1
}

function job_observes_code_mirror_group_to_s3_on_aws {
  local group="${1}"
  local vcpus='1'
  local memory='1800'
  local attempts='10'
  local timeout='3600'
  local jobname="observes_code_mirror_group_to_s3__${group}"
  local jobqueue='default'

      if test -z "${group}"
      then
            echo '[INFO] Please set the first argument to the group name' \
        &&  return 1
      fi \
  &&  helper_observes_aws_login prod \
  &&  helper_common_run_on_aws \
        "${vcpus}" \
        "${memory}" \
        "${attempts}" \
        "${timeout}" \
        "${jobname}" \
        "${jobqueue}" \
        'observes_code_mirror_group_to_s3' "${group}"
}

function job_observes_git_process {
  # If you move me take into account the artifacts in the .gitlab-ci.yaml

      env_prepare_python_packages \
  &&  helper_observes_git_process \
  ||  return 1
}

function job_observes_git_upload {
      env_prepare_python_packages \
  &&  helper_observes_git_upload \
  ||  return 1
}

function job_observes_timedoctor_refresh_token {
      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_observes_timedoctor_refresh_token \
  ||  return 1
}

function job_observes_timedoctor_backup {
      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_observes_timedoctor_backup \
  ||  return 1
}

function job_observes_timedoctor_manually_create_token {
      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_observes_timedoctor_manually_create_token \
  ||  return 1
}

function job_observes_test_infra {
  local target='infra/terraform'

      helper_use_pristine_workdir \
  &&  pushd observes \
    &&  helper_observes_aws_login dev \
    &&  helper_observes_terraform_plan "${target}" \
  &&  popd \
  ||  return 1
}

function job_observes_apply_infra {
  local target='infra/terraform'

      helper_use_pristine_workdir \
  &&  pushd observes \
    &&  helper_observes_aws_login prod \
    &&  helper_common_terraform_apply "${target}" \
  &&  popd \
  ||  return 1
}

function job_observes_lint_code {

      pushd observes \
  &&  env_prepare_python_packages \
  &&  helper_observes_lint_code_python \
  &&  popd \
  ||  return 1
}

function job_observes_code_lint {

      pushd observes \
    &&  env_prepare_python_packages \
    &&  helper_observes_lint_generic_package "./code/code" \
  &&  popd \
  ||  return 1
}

function job_observes_code_test {

      pushd observes \
    &&  env_prepare_python_packages \
    &&  helper_observes_test_generic_package "./code" \
  &&  popd \
  ||  return 1
}

function job_observes_gitlab_lint {

      pushd observes \
    &&  env_prepare_python_packages \
    &&  helper_observes_lint_generic_package "./singer/streamer_gitlab/streamer_gitlab" \
  &&  popd \
  ||  return 1
}

function job_observes_gitlab_test {

      pushd observes \
    &&  env_prepare_python_packages \
    &&  helper_observes_test_generic_package "./singer/streamer_gitlab" \
  &&  popd \
  ||  return 1
}
