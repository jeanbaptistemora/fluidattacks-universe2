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

function job_observes_dynamo {
      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_observes_dynamo \
  ||  return 1
}

function job_observes_services_toe {
      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_observes_services_toe \
  ||  return 1
}

function job_observes_intercom {
      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_observes_intercom \
  ||  return 1
}

function job_observes_mandrill {
      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_observes_mandrill \
  ||  return 1
}

function job_observes_gitlab {
      helper_use_observes_workdir \
  &&  env_prepare_python_packages \
  &&  helper_observes_gitlab \
  ||  return 1
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

function job_observes_code {
  export GITLAB_API_USER
  export GITLAB_API_TOKEN
  local mock_integrates_api_token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.xxx'
  local services_url="https://${GITLAB_API_USER}:${GITLAB_API_TOKEN}@gitlab.com/fluidattacks/services.git"

      env_prepare_python_packages \
  &&  helper_observes_aws_login prod \
  &&  helper_common_sops_env 'observes/secrets-prod.yaml' 'default' \
        'REDSHIFT_DATABASE' \
        'REDSHIFT_HOST' \
        'REDSHIFT_PASSWORD' \
        'REDSHIFT_PORT' \
        'REDSHIFT_USER' \
  &&  if ! test -e .services
      then
            echo '[INFO] Cloning services' \
        &&  git clone --branch master --single-branch --depth 1 "${services_url}" '.services'
      fi \
  &&  shopt -s nullglob \
  &&  pushd '.services' \
    &&  aws s3 ls 's3://continuous-repositories/' \
          | sed 's|.*PRE ||g;s|/||g' \
          | while read -r group
            do
                  echo "[INFO] Working on ${group}" \
              &&  echo "[INFO] Cloning ${group}" \
              &&  CI=true \
                  CI_COMMIT_REF_NAME='master' \
                  INTEGRATES_API_TOKEN="${mock_integrates_api_token}" \
                  PROD_AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" \
                  PROD_AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" \
                  melts drills --pull-repos "${group}" \
              &&  echo "[INFO] Apending mailmaps" \
              &&  for repo in "groups/${group}/fusion/"*
                  do
                        cp -f '.groups-mailmap' "${repo}/.mailmap" \
                    ||  return 1
                  done \
              &&  echo "[INFO] Executing ${group}" \
              &&  python3 "${STARTDIR}/observes/code/__init__.py" \
                    --namespace "${group}" \
                    "groups/${group}/fusion/"* \
              &&  rm -rf "groups/${group}/fusion/" \

            done \
  &&  popd \
  ||  return 1

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

function job_observes_services_repositories_cache {
  # Please don't add pristine workdir

      env_prepare_python_packages \
  &&  helper_observes_services_repositories_cache \
  ||  return 1
}

function job_observes_services_repositories_cache_new {
  # Please don't add pristine workdir

      env_prepare_python_packages \
  &&  helper_observes_services_repositories_cache_new \
  ||  return 1
}

function job_observes_test_infra {
  local target='observes/infra/terraform'

      helper_use_pristine_workdir \
  &&  helper_observes_aws_login dev \
  &&  helper_common_terraform_plan \
        "${target}" \
  ||  return 1
}

function job_observes_apply_infra {
  local target='observes/infra/terraform'

      helper_use_pristine_workdir \
  &&  helper_observes_aws_login prod \
  &&  helper_common_terraform_apply \
        "${target}" \
  ||  return 1
}

function job_observes_lint_code {

      pushd observes \
  &&  env_prepare_python_packages \
  &&  helper_observes_lint_code_python \
  &&  popd \
  ||  return 1
}
