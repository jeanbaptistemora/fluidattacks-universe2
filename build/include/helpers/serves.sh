# shellcheck shell=bash

function helper_serves_deploy_integrates {
  local integrates_id='20741933'

      helper_serves_aws_login production \
  &&  helper_common_sops_env secret-management/production.yaml default \
        PRODUCT_PIPELINE_TOKEN \
  &&  curl \
        -X POST \
        -F token="${PRODUCT_PIPELINE_TOKEN}" \
        -F 'variables[CI_COMMIT_TITLE]=integrates' \
        -F ref=master \
        "https://gitlab.com/api/v4/projects/${integrates_id}/trigger/pipeline"
}

function helper_serves_aws_login {
  local user="${1}"
  export AWS_ACCESS_KEY_ID
  export AWS_SECRET_ACCESS_KEY


      if [ "${user}" = 'development' ]
      then
            AWS_ACCESS_KEY_ID="${SERVES_DEV_AWS_ACCESS_KEY_ID}" \
        &&  AWS_SECRET_ACCESS_KEY="${SERVES_DEV_AWS_SECRET_ACCESS_KEY}"
      elif [ "${user}" = 'production' ]
      then
            AWS_ACCESS_KEY_ID="${SERVES_PROD_AWS_ACCESS_KEY_ID}" \
        &&  AWS_SECRET_ACCESS_KEY="${SERVES_PROD_AWS_SECRET_ACCESS_KEY}"
      else
            echo '[ERROR] either "production" or "development" must be passed as arg' \
        &&  return 1
      fi \
  &&  echo "[INFO] Logging into AWS with ${user} credentials" \
  &&  aws configure set aws_access_key_id "${AWS_ACCESS_KEY_ID}" \
  &&  aws configure set aws_secret_access_key "${AWS_SECRET_ACCESS_KEY}"
}

function helper_serves_cloudflare_login {
  local user="${1}"
  export TF_VAR_cloudflare_email
  export TF_VAR_cloudflare_api_key

      helper_common_sops_env "secret-management/${user}.yaml" default \
        CLOUDFLARE_EMAIL \
        CLOUDFLARE_API_KEY \
  &&  TF_VAR_cloudflare_email="${CLOUDFLARE_EMAIL}" \
  &&  TF_VAR_cloudflare_api_key="${CLOUDFLARE_API_KEY}"
}

function helper_serves_terraform_taint {
  local target_dir="${1}"
  local marked_value="${2}"

      helper_common_terraform_init "${target_dir}" \
  &&  pushd "${target_dir}" \
    &&  terraform refresh \
    &&  echo "[INFO] Running terraform taint: ${marked_value}" \
    &&  terraform taint "${marked_value}" \
  &&  popd \
  || return 1
}

function helper_serves_terraform_output {
  local target_dir="${1}"
  local output_name="${2}"

      helper_common_terraform_init "${target_dir}" 1>&2 \
  &&  pushd "${target_dir}" 1>&2 \
    &&  echo "[INFO] Running terraform output: ${output_name}" 1>&2 \
    &&  terraform output "${output_name}" \
  &&  popd 1>&2 \
  || return 1
}

function helper_serves_infra_monolith {
  local first_argument="${1}"

      helper_serves_aws_login development \
  &&  pushd infrastructure/ \
    &&  helper_common_terraform_plan . \
    &&  if [ "${first_argument}" == "deploy" ]; then
              helper_serves_aws_login production \
          &&  helper_common_terraform_apply .
        fi \
  &&  popd \
  || return 1
}

function helper_serves_get_resource_to_taint_number {

  # Made specifically for nightly rotations.
  # It prints 1 if day is even and 2 if day is odd.

  local date
  local timestamp
  local days

      date="$(date +%y-%m-%d)" \
  &&  timestamp="$(date +%s --date="${date}")" \
  &&  days=$((timestamp / 60 / 60 / 24)) \
  &&  if [ $((days % 2)) == '0' ]
      then
        echo "1"
      else
        echo "2"
      fi
}

function helper_serves_check_last_job_succeeded {
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

function helper_serves_user_provision_rotate_keys {
  local terraform_dir="${1}"
  local resource_to_taint="${2}"
  local output_key_id_name="${3}"
  local output_key_id_value
  local output_secret_key_name="${4}"
  local output_secret_key_value
  local gitlab_repo_id="${5}"
  local gitlab_key_id_name="${6}"
  local gitlab_secret_key_name="${7}"
  local gitlab_masked="${8}"
  local gitlab_protected="${9}"
  local gitlab_repo_id_2="${10:-}"
  local gitlab_key_id_name_2="${11:-}"
  local gitlab_secret_key_name_2="${12:-}"
  local resource_to_taint_number

      resource_to_taint_number="$( \
        helper_serves_get_resource_to_taint_number)" \
  &&  helper_serves_aws_login production \
  &&  helper_serves_terraform_taint \
        "${terraform_dir}" \
        "${resource_to_taint}-${resource_to_taint_number}" \
  &&  helper_common_terraform_apply \
        "${terraform_dir}" \
  &&  output_key_id_value=$( \
        helper_serves_terraform_output \
          "${terraform_dir}" \
          "${output_key_id_name}-${resource_to_taint_number}") \
  &&  output_secret_key_value=$( \
        helper_serves_terraform_output \
          "${terraform_dir}" \
          "${output_secret_key_name}-${resource_to_taint_number}")  \
  &&  helper_common_set_project_variable \
        "${GITLAB_API_TOKEN}" "${gitlab_repo_id}" \
        "${gitlab_key_id_name}" "${output_key_id_value}" \
        "${gitlab_protected}" "${gitlab_masked}" \
  &&  helper_common_set_project_variable \
        "${GITLAB_API_TOKEN}" "${gitlab_repo_id}" \
        "${gitlab_secret_key_name}" "${output_secret_key_value}" \
        "${gitlab_protected}" "${gitlab_masked}" \
  &&  if test -n "${gitlab_repo_id_2}"
      then
            helper_common_set_project_variable \
              "${GITLAB_API_TOKEN}" "${gitlab_repo_id_2}" \
              "${gitlab_key_id_name_2}" "${output_key_id_value}" \
              "${gitlab_protected}" "${gitlab_masked}" \
        &&  helper_common_set_project_variable \
              "${GITLAB_API_TOKEN}" "${gitlab_repo_id_2}" \
              "${gitlab_secret_key_name_2}" "${output_secret_key_value}" \
              "${gitlab_protected}" "${gitlab_masked}"
      fi
}

function helper_serves_test_lint_code_shell {
  local path="${1}"

  find "${path}" -name '*.sh' -exec \
    shellcheck --external-sources --exclude=SC1090,SC2016,SC2153,SC2154 {} +
}

function helper_serves_terraform_plan {
  local target="${1}"
  local config

      config="$(readlink -f ../.tflint.hcl)" \
  &&  helper_common_terraform_plan_new "${target}" "${config}"
}
