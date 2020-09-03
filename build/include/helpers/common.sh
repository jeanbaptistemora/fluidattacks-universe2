# shellcheck shell=bash

function helper_common_sops_env {
  local file
  local decrypted_json
  local profile
  local variable_name

  # Export variables from sops yaml file
  # e.g: helper_common_sops_env secrets-production.yaml serves-admin var1 var2 var3 var4
  # note: needs jq

      file="${1}" \
  &&  profile="${2}" \
  &&  decrypted_json=$( \
        sops \
          --aws-profile "${profile}" \
          --decrypt \
          --output-type json \
          "${file}") \
  &&  shift 2 \
  &&  for variable_name in "${@}"; do
            echo "Exporting: ${variable_name}" \
        &&  variable_value=$( \
              echo "${decrypted_json}" \
                | jq -r ".${variable_name}") \
        &&  export "${variable_name//./__}=${variable_value}"
      done
}

function helper_use_pristine_workdir {
  export WORKDIR
  export STARTDIR

  function helper_teardown_workdir {
        echo "[INFO] Deleting: ${WORKDIR}" \
    &&  rm -rf "${WORKDIR}"
  }

      echo '[INFO] Creating a pristine workdir' \
  &&  rm -rf "${WORKDIR}" \
  &&  mkdir -p "${WORKDIR}" \
  &&  echo '[INFO] Copying files to workdir' \
  &&  cp -r "${STARTDIR}/." "${WORKDIR}" \
  &&  echo '[INFO] Entering the workdir' \
  &&  pushd "${WORKDIR}" \
  &&  echo '[INFO] Running: git clean -xdf' \
  &&  git clean -xdf \
  &&  trap 'helper_teardown_workdir' 'EXIT' \
  ||  return 1
}

function helper_use_regular_workdir {
  export STARTDIR

      echo '[INFO] Entering the workdir' \
  &&  pushd "${STARTDIR}" \
  ||  return 1
}

function helper_get_projects {
  export PROJECTS=(
    'autonomicmind/default'
    'autonomicmind/challenges'
    'fluidattacks/services'
    'fluidattacks/product'
    'fluidattacks/web'
  )
}

function helper_docker_build_and_push {
  local tag="${1}"
  local context="${2}"
  local dockerfile="${3}"
  local build_arg_1_key="${4:-build_arg_1_key}"
  local build_arg_1_val="${5:-build_arg_1_val}"
  local build_arg_2_key="${6:-build_arg_2_key}"
  local build_arg_2_val="${7:-build_arg_2_val}"
  local build_arg_3_key="${8:-build_arg_3_key}"
  local build_arg_3_val="${9:-build_arg_3_val}"
  local build_arg_4_key="${10:-build_arg_4_key}"
  local build_arg_4_val="${11:-build_arg_4_val}"
  local build_arg_5_key="${12:-build_arg_5_key}"
  local build_arg_5_val="${13:-build_arg_5_val}"
  local build_arg_6_key="${14:-build_arg_6_key}"
  local build_arg_6_val="${15:-build_arg_6_val}"
  local build_arg_7_key="${16:-build_arg_7_key}"
  local build_arg_7_val="${17:-build_arg_7_val}"
  local build_arg_8_key="${18:-build_arg_8_key}"
  local build_arg_8_val="${19:-build_arg_8_val}"
  local build_arg_9_key="${20:-build_arg_9_key}"
  local build_arg_9_val="${21:-build_arg_9_val}"
  local build_arg_10_key="${22:-build_arg_10_key}"
  local build_arg_10_val="${23:-build_arg_10_val}"
  local build_args=(
    --tag "${tag}"
    --file "${dockerfile}"
    --build-arg "${build_arg_1_key}=${build_arg_1_val}"
    --build-arg "${build_arg_2_key}=${build_arg_2_val}"
    --build-arg "${build_arg_3_key}=${build_arg_3_val}"
    --build-arg "${build_arg_4_key}=${build_arg_4_val}"
    --build-arg "${build_arg_5_key}=${build_arg_5_val}"
    --build-arg "${build_arg_6_key}=${build_arg_6_val}"
    --build-arg "${build_arg_7_key}=${build_arg_7_val}"
    --build-arg "${build_arg_8_key}=${build_arg_8_val}"
    --build-arg "${build_arg_9_key}=${build_arg_9_val}"
    --build-arg "${build_arg_10_key}=${build_arg_10_val}"
  )

      echo "[INFO] Logging into: ${CI_REGISTRY}" \
  &&  docker login \
        --username "${CI_REGISTRY_USER}" \
        --password "${CI_REGISTRY_PASSWORD}" \
      "${CI_REGISTRY}" \
  &&  echo "[INFO] Pulling: ${tag}" \
  &&  if docker pull "${tag}"
      then
        build_args+=( --cache-from "${tag}" )
      fi \
  &&  echo "[INFO] Building: ${tag}" \
  &&  docker build "${build_args[@]}" "${context}" \
  &&  echo "[INFO] Pushing: ${tag}" \
  &&  docker push "${tag}" \
  &&  echo "[INFO] Deleting local copy of: ${tag}" \
  &&  docker image remove "${tag}"
}

function helper_execute_chunk_parallel {
  local function_to_call
  local todo_list

  function_to_call="${1:-}"
  todo_list="${2:-}"

      echo "Found $(wc -l "${todo_list}") items to process" \
  &&  echo "Processing batch: ${CI_NODE_INDEX} of ${CI_NODE_TOTAL}" \
  &&  split --number="l/${CI_NODE_INDEX}/${CI_NODE_TOTAL}" "${todo_list}" \
        | while read -r item
          do
                "${function_to_call}" "${item}" \
            ||  return 1
          done
}

function helper_get_gitlab_var {
  local gitlab_var_name="${1}"
      echo "[INFO] Retrieving var from GitLab: ${gitlab_var_name}" 1>&2 \
  &&  curl \
        --silent \
        --header "private-token: ${GITLAB_API_TOKEN}" \
        "${GITLAB_API_URL}/${gitlab_var_name}" \
      | jq -r '.value'
}

function helper_get_gitlab_registry_id {
  local registry_name="${1}"

  wget -O - "https://gitlab.com/api/v4/projects/${CI_PROJECT_ID}/registry/repositories" \
    | jq ".[] | select (.name == \"${registry_name}\") | .id"
}

function helper_get_touched_files_in_last_commit {
  git diff --name-only "${CI_COMMIT_BEFORE_SHA}" "${CI_COMMIT_SHA}" \
    | while read -r path
      do
        ! test -e "${path}" || echo "${path}"
      done
}

function helper_have_any_file_changed {
  local file
  local files=( "$@" )
  local canon_file_a
  local canon_file_b

      helper_get_touched_files_in_last_commit > "${TEMP_FD}" \
  &&  while read -r touched_file
      do
        for file in "${files[@]}"
        do
              canon_file_a=$(readlink -f "${touched_file}") \
          &&  canon_file_b=$(readlink -f "${file}") \
          &&  if [[ "${canon_file_a}" == "${canon_file_b}"* ]]
              then
                echo "${canon_file_a}"
                echo "${canon_file_b}"
                return 0
              else
                continue
              fi
        done || :
      done < "${TEMP_FD}" \
  &&  return 1
}

function helper_common_list_touched_files {
  local path

  git show --format= --name-only HEAD | while read -r path
  do
    if test -e "${path}"
    then
      echo "${path}"
    fi
  done
}

function helper_is_today_wednesday {
  test "$(date +%A)" == 'Wednesday'
}

function helper_is_today_first_day_of_month {
  test "$(date +%d)" == '01'
}

function helper_list_declared_jobs {
  declare -F | sed 's/declare -f //' | grep -P '^job_[a-z_]+' | sed 's/job_//' | sort
}

function helper_list_vars_with_regex {
  local regex="${1}"
  printenv | grep -oP "${regex}" | sort
}

function reg_registry_id {
  # Get the id of a gitlab registry
  # e.g reg_registry_id deps-base

  local registry_name="$1"
  local integrates_id='20741933'
  local check_url

      check_url="https://gitlab.com/api/v4/projects/${integrates_id}/registry/repositories" \
  &&  wget -O - "${check_url}" 2> /dev/null | jq ".[] | select (.name == \"${registry_name}\") | .id"
}

function reg_registry_delete {
  # Delete registry
  # e.g: reg_registry_delete deps-production TOKEN

  local registry_name="$1"
  local token="$2"
  local registry_id
  local delete_url

      registry_id=$(reg_registry_id "${registry_name}") \
  &&  delete_url="https://gitlab.com/api/v4/projects/20741933/registry/repositories/${registry_id}" \
  &&  curl --request DELETE --header "PRIVATE-TOKEN: ${token}" "${delete_url}"
}

function minutes_of_month {
  # Returns minutes that have passed during the current month

  local minutes_of_passed_days
  local minutes_of_passed_hours
  local minutes_of_current_hour
  local minutes_of_month

      minutes_of_passed_days=$((
        ($(date +%d | sed 's/^0//') -1) * 1440
      )) \
  &&  minutes_of_passed_hours=$((
        $(date +%H | sed 's/^0//') * 60
      )) \
  &&  minutes_of_current_hour=$((
        $(date +%M | sed 's/^0//')
      )) \
  &&  minutes_of_month=$((
        minutes_of_passed_days +
        minutes_of_passed_hours +
        minutes_of_current_hour
      )) \
  &&  echo "${minutes_of_month}"
}

function helper_common_terraform_login {
  export TF_VAR_aws_access_key
  export TF_VAR_aws_secret_key

      echo '[INFO] Logging into Terraform' \
  &&  TF_VAR_aws_access_key="${AWS_ACCESS_KEY_ID}" \
  &&  TF_VAR_aws_secret_key="${AWS_SECRET_ACCESS_KEY}"
}

function helper_common_terraform_init {
  local target_dir="${1}"

      helper_common_terraform_login \
  &&  pushd "${target_dir}" \
    &&  echo '[INFO] Running terraform init' \
    &&  terraform init \
  &&  popd \
  || return 1
}

function helper_common_terraform_plan {
  local target_dir="${1}"

      helper_common_terraform_init "${target_dir}" \
  &&  pushd "${target_dir}" \
    &&  echo '[INFO] Running terraform plan' \
    &&  terraform plan -lock=false -refresh=true \
    &&  tflint --deep --module \
  &&  popd \
  || return 1
}

function helper_common_terraform_apply {
  local target_dir="${1}"

      helper_common_terraform_init "${target_dir}" \
  &&  pushd "${target_dir}" \
    &&  echo '[INFO] Running terraform apply' \
    &&  terraform apply -auto-approve -refresh=true \
  &&  popd \
  || return 1
}

function helper_common_poetry_install_deps {
  local path="${1}"
  export PYTHONPATH="${PWD}/skims/.venv/lib64/python3.8/site-packages:${PYTHONPATH}"

      pushd "${path}" \
    &&  { test -e poetry.lock || poetry install; } \
  &&  popd \
  ||  return 1
}

function helper_common_poetry_install {
  local path="${1}"

      pushd "${path}" \
    &&  poetry update \
    &&  poetry install \
  &&  popd \
  ||  return 1
}
