# shellcheck shell=bash

function check_last_job_succeeded {
  export GITLAB_API_TOKEN
  local gitlab_repo_id="${1}"
  local job_name="${2}"
  local job_status=''
  local job_url=''
  local page='0'
  local job_data=''

      echo '[INFO] Iterating GitLab jobs' \
  &&  for page in $(seq 0 100)
      do
            echo "[INFO] Checking page ${page} for job: ${job_name}" \
        &&  if job_data=$( \
                  curl \
                      --globoff \
                      --silent \
                      --header "private-token: ${GITLAB_API_TOKEN}" \
                      "https://gitlab.com/api/v4/projects/${gitlab_repo_id}/jobs?page=${page}" \
                    | jq -er ".[] | select(.name == \"${job_name}\")")
            then
                  job_url=$(echo "${job_data}" | jq -er '.web_url') \
              &&  echo "[INFO] Got the job: ${job_url}" \
              &&  break
            else
              continue
            fi
      done \
  &&  if test -z "${job_data}"
      then
            echo '[INFO] Job was not found, was it renamed?' \
        &&  return 1
      fi \
  &&  job_status=$(echo "${job_data}" | jq -er '.status') \
  &&  if test "${job_status}" = "success"
      then
            echo "[INFO] Job status is: ${job_status}, continuing" \
        &&  return 0
      else
            echo "[INFO] Job status is different that succeeded: ${job_status}, continuing" \
        &&  return 1
      fi
}

function deploy_integrates {
  local gitlab_repo_id="${1}"
  local pipeline_token="${2}"

  curl \
    -X POST \
    -F token="${pipeline_token}" \
    -F 'variables[CI_COMMIT_TITLE]=integrates' \
    -F ref=master \
    "https://gitlab.com/api/v4/projects/${gitlab_repo_id}/trigger/pipeline"
}

function main {
  local gitlab_repo_id='20741933'
  local integrates_job_name='integrates/back/deploy/prod'

      user-rotate-keys-development \
  &&  check_last_job_succeeded \
        "${gitlab_repo_id}" \
        "${integrates_job_name}" \
  &&  aws_login_prod '__envProduct__' \
  &&  sops_export_vars '__envSecretsPath__' \
        PRODUCT_PIPELINE_TOKEN \
  &&  user-rotate-keys-production \
  &&  deploy_integrates \
        "${gitlab_repo_id}" \
        "${PRODUCT_PIPELINE_TOKEN}"
}

main "${@}"
