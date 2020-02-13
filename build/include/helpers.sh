# shellcheck shell=bash

function helper_indent_2 {
  sed 's/^/  /g'
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
  &&  popd
}

function helper_terraform_apply {
  local target_dir="${1}"
  local bucket="${2}"

      helper_terraform_init "${target_dir}" "${bucket}" \
  &&  pushd "${target_dir}" \
    &&  echo '[INFO] Running terraform apply' \
    &&  terraform apply -auto-approve -refresh=true \
  &&  popd
}

function helper_terraform_init {
  local target_dir="${1}"
  local bucket="${2}"

      source toolbox/others.sh \
  &&  echo '[INFO] Logging in to aws' \
  &&  aws_login \
  &&  pushd "${target_dir}" \
    &&  echo '[INFO] Running terraform init' \
    &&  terraform init --backend-config="bucket=${bucket}" \
  &&  popd
}

function helper_terraform_lint {
  local target_dir="${1}"
  local bucket="${2}"

      helper_terraform_init "${target_dir}" "${bucket}" \
  &&  pushd "${1}" \
    &&  echo '[INFO] Running terraform linter' \
    &&  tflint --deep --module \
  &&  popd
}

function helper_terraform_plan {
  local target_dir="${1}"
  local bucket="${2}"

      helper_terraform_init "${target_dir}" "${bucket}" \
  &&  pushd "${target_dir}" \
    &&  echo '[INFO] Running terraform plan' \
    &&  terraform plan -refresh=true \
  &&  popd
}

function helper_terraform_taint {
  local target_dir="${1}"
  local bucket="${2}"
  local marked_value="${3}"

      helper_terraform_init "${target_dir}" "${bucket}" \
  &&  pushd "${target_dir}" \
    &&  terraform refresh \
    &&  echo "[INFO] Running terraform taint: ${marked_value}" \
    &&  terraform taint "${marked_value}" \
  &&  popd
}

function helper_terraform_output {
  local target_dir="${1}"
  local bucket="${2}"
  local output_name="${3}"

      helper_terraform_init "${target_dir}" "${bucket}" 1>&2 \
  &&  pushd "${target_dir}" 1>&2 \
    &&  echo "[INFO] Running terraform output: ${output_name}" 1>&2 \
    &&  terraform output "${output_name}" \
  &&  popd 1>&2
}

function helper_user_provision_rotate_keys {
  local terraform_dir="${1}"
  local bucket="${2}"
  local resource_to_taint="${3}"
  local output_key_id_name="${4}"
  local output_key_id_value
  local output_secret_key_name="${5}"
  local output_secret_key_value
  local gitlab_repo_id="${6}"
  local gitlab_key_id_name="${7}"
  local gitlab_secret_key_name="${8}"
  local gitlab_masked="${9}"
  local gitlab_protected="${10}"

      helper_terraform_taint \
        "${terraform_dir}" \
        "${bucket}" \
        "${resource_to_taint}" \
  &&  helper_terraform_apply \
        "${terraform_dir}" \
        "${bucket}" \
  &&  output_key_id_value=$( \
        helper_terraform_output \
          "${terraform_dir}" "${bucket}" "${output_key_id_name}") \
  &&  output_secret_key_value=$( \
        helper_terraform_output \
          "${terraform_dir}" "${bucket}" "${output_secret_key_name}")  \
  &&  set_project_variable \
        "${GITLAB_API_TOKEN}" "${gitlab_repo_id}" \
        "${gitlab_key_id_name}" "${output_key_id_value}" \
        "${gitlab_protected}" "${gitlab_masked}" \
  &&  set_project_variable \
        "${GITLAB_API_TOKEN}" "${gitlab_repo_id}" \
        "${gitlab_secret_key_name}" "${output_secret_key_value}" \
        "${gitlab_protected}" "${gitlab_masked}"
}
