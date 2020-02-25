# shellcheck shell=bash

source "${srcExternalGitlabVariables}"
source "${srcExternalSops}"
source "${srcDotDotToolboxOthers}"

function helper_get_gitlab_var {
  local gitlab_var_name="${1}"
  local gitlab_api_token="${2}"

      echo "[INFO] Retrieving var from GitLab: ${gitlab_var_name}" 1>&2 \
  &&  curl \
        --silent \
        --header "private-token: ${gitlab_api_token}" \
        "${GITLAB_API_URL}/${gitlab_var_name}" \
      | jq -r '.value'
}

function helper_indent_2 {
  sed 's/^/  /g'
}

function helper_aws_login {
      echo '[INFO] Logging into AWS' \
  &&  aws configure set aws_access_key_id "${AWS_ACCESS_KEY_ID}" \
  &&  aws configure set aws_secret_access_key "${AWS_SECRET_ACCESS_KEY}"
}

function helper_docker_build_and_push {
  local tag="${1}"
  local context="${2}"
  local dockerfile="${3}"
  local build_arg_1_key="${4:-build_arg_1_key}"
  local build_arg_1_val="${5:-build_arg_1_val}"

      echo "[INFO] Logging into: ${CI_REGISTRY}" \
  &&  docker login \
        --username "${CI_REGISTRY_USER}" \
        --password "${CI_REGISTRY_PASSWORD}" \
      "${CI_REGISTRY}" \
  &&  echo "[INFO] Pulling: ${tag}" \
  &&  { docker pull "${tag}" || true; } \
  &&  echo "[INFO] Building: ${tag}" \
  &&  docker build \
          --tag "${tag}" \
          --file "${dockerfile}" \
          --build-arg "${build_arg_1_key}=${build_arg_1_val}" \
        "${context}" \
  &&  echo "[INFO] Pushing: ${tag}" \
  &&  docker push "${tag}"
}

function helper_list_declared_jobs {
  declare -F | sed 's/declare -f //' | grep -P '^job_[a-z_]+' | sed 's/job_//' | sort
}

function helper_list_vars_with_regex {
  local regex="${1}"
  printenv | grep -oP "${regex}" | sort
}

function helper_list_touched_files_in_last_commit {
  local path

  git show --format= --name-only HEAD \
    | while read -r path
      do
        if test -e "${path}"
        then
          echo "${path}"
        fi
      done
}

function helper_run_break_build {
  local kind="${1}"

      docker pull fluidattacks/break-build \
  &&  pushd "${STARTDIR}" \
    &&  if test "${IS_LOCAL_BUILD}"
        then
          docker run fluidattacks/break-build \
              "--${kind}" \
              --id "${BREAK_BUILD_ID}" \
              --secret "${BREAK_BUILD_SECRET}" \
              --no-image-rm \
            | bash
        else
          docker run fluidattacks/break-build \
              "--${kind}" \
              --id "${BREAK_BUILD_ID}" \
              --secret "${BREAK_BUILD_SECRET}" \
              --no-image-rm \
              --gitlab-docker-socket-binding \
            | bash
        fi \
  &&  popd \
  || return 1
}

function helper_terraform_login {
  export TF_VAR_aws_access_key
  export TF_VAR_aws_secret_key

      helper_aws_login \
  &&  echo '[INFO] Logging into Terraform' \
  &&  TF_VAR_aws_access_key="${AWS_ACCESS_KEY_ID}" \
  &&  TF_VAR_aws_secret_key="${AWS_SECRET_ACCESS_KEY}"
}

function helper_terraform_apply {
  local target_dir="${1}"

      helper_terraform_init "${target_dir}" \
  &&  pushd "${target_dir}" \
    &&  echo '[INFO] Running terraform apply' \
    &&  terraform apply -auto-approve -refresh=true \
  &&  popd \
  || return 1
}

function helper_terraform_init {
  local target_dir="${1}"

      helper_terraform_login \
  &&  pushd "${target_dir}" \
    &&  echo '[INFO] Running terraform init' \
    &&  terraform init \
  &&  popd \
  || return 1
}

function helper_terraform_lint {
  local target_dir="${1}"

      helper_terraform_init "${target_dir}" \
  &&  pushd "${1}" \
    &&  echo '[INFO] Running terraform linter' \
    &&  tflint --deep --module \
  &&  popd \
  || return 1
}

function helper_terraform_plan {
  local target_dir="${1}"

      helper_terraform_init "${target_dir}" \
  &&  pushd "${target_dir}" \
    &&  echo '[INFO] Running terraform plan' \
    &&  terraform plan -refresh=true \
  &&  popd \
  || return 1
}

function helper_terraform_taint {
  local target_dir="${1}"
  local marked_value="${2}"

      helper_terraform_init "${target_dir}" \
  &&  pushd "${target_dir}" \
    &&  terraform refresh \
    &&  echo "[INFO] Running terraform taint: ${marked_value}" \
    &&  terraform taint "${marked_value}" \
  &&  popd \
  || return 1
}

function helper_terraform_output {
  local target_dir="${1}"
  local output_name="${2}"

      helper_terraform_init "${target_dir}" 1>&2 \
  &&  pushd "${target_dir}" 1>&2 \
    &&  echo "[INFO] Running terraform output: ${output_name}" 1>&2 \
    &&  terraform output "${output_name}" \
  &&  popd 1>&2 \
  || return 1
}

function helper_user_provision_rotate_keys {
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
  local resource_to_taint_number

      resource_to_taint_number="$( \
        helper_get_resource_to_taint_number)" \
  &&  helper_terraform_taint \
        "${terraform_dir}" \
        "${resource_to_taint}-${resource_to_taint_number}" \
  &&  helper_terraform_apply \
        "${terraform_dir}" \
  &&  output_key_id_value=$( \
        helper_terraform_output \
          "${terraform_dir}" \
          "${output_key_id_name}-${resource_to_taint_number}") \
  &&  output_secret_key_value=$( \
        helper_terraform_output \
          "${terraform_dir}" \
          "${output_secret_key_name}-${resource_to_taint_number}")  \
  &&  set_project_variable \
        "${GITLAB_API_TOKEN}" "${gitlab_repo_id}" \
        "${gitlab_key_id_name}" "${output_key_id_value}" \
        "${gitlab_protected}" "${gitlab_masked}" \
  &&  set_project_variable \
        "${GITLAB_API_TOKEN}" "${gitlab_repo_id}" \
        "${gitlab_secret_key_name}" "${output_secret_key_value}" \
        "${gitlab_protected}" "${gitlab_masked}"
}

function helper_deploy_integrates {
  local integrates_id='4620828'

      aws_login \
  &&  sops_env \
        secrets-prod.yaml \
        default \
        INTEGRATES_PIPELINE_TOKEN \
  &&  curl \
        -X POST \
        -H "Content-Type: application/json" \
        -d '{"token":"'"${INTEGRATES_PIPELINE_TOKEN}"'", "ref":"master", "variables": {"TRIGGER_MASTER": "1"}}' \
        "https://gitlab.com/api/v4/projects/${integrates_id}/trigger/pipeline"
}

function helper_get_resource_to_taint_number {

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
