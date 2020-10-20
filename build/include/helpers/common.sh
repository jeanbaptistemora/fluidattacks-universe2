# shellcheck shell=bash

function helper_common_json_to_yaml {
  yq -y .
}

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

function helper_common_use_pristine_workdir {
  export WORKDIR
  export STARTDIR

  function helper_teardown_workdir {
        echo "[INFO] Deleting: ${WORKDIR}" \
    &&  pushd "${STARTDIR}" \
    &&  git worktree remove -f "${WORKDIR}" \
    &&  rm -rf "${WORKDIR}"
  }

      echo '[INFO] Creating a pristine workdir' \
  &&  rm -rf "${WORKDIR}" \
  &&  git worktree add -f "${WORKDIR}" "${CI_COMMIT_REF_NAME}" \
  &&  pushd "${WORKDIR}" \
  &&  trap 'helper_teardown_workdir' 'EXIT' \
  ||  return 1
}

function helper_common_use_repo {
  local source="${1}"
  local target="${2}"

  if test -e "${target}"
  then
        echo "[INFO] Updating local repository copy at: ${target}" \
    &&  pushd "${target}" \
      &&  git remote set-url origin "${source}" \
      &&  git fetch \
      &&  git reset --hard HEAD \
    ||  return 1
  else
        echo "[INFO] Creating local repository copy at: ${target}" \
    &&  git clone --depth 1 --single-branch "${source}" "${target}" \
    &&  pushd "${target}" \
    ||  return 1
  fi
}

function helper_common_use_services {
  export STARTDIR
  export GITLAB_API_TOKEN
  export GITLAB_API_USER
  local source="https://${GITLAB_API_USER}:${GITLAB_API_TOKEN}@gitlab.com/fluidattacks/services.git"
  local target="${STARTDIR}/../services"

  helper_common_use_repo "${source}" "${target}"
}

function helper_common_list_services_groups {
  local store="${1}"

      helper_common_use_services \
    &&  ls -1 groups/ > "${store}" \
  &&  popd \
  ||  return 1
}

function helper_common_get_projects {
  export PROJECTS=(
    'autonomicmind/default'
    'autonomicmind/challenges'
    'fluidattacks/services'
    'fluidattacks/product'
  )
}

function helper_common_docker_build_and_push {
  local tag="${1}"
  local context="${2}"
  local dockerfile="${3}"
  local use_cache="${4}"
  local build_arg_1_key="${5:-build_arg_1_key}"
  local build_arg_1_val="${6:-build_arg_1_val}"
  local build_arg_2_key="${7:-build_arg_2_key}"
  local build_arg_2_val="${8:-build_arg_2_val}"
  local build_arg_3_key="${9:-build_arg_3_key}"
  local build_arg_3_val="${10:-build_arg_3_val}"
  local build_arg_4_key="${11:-build_arg_4_key}"
  local build_arg_4_val="${12:-build_arg_4_val}"
  local build_arg_5_key="${13:-build_arg_5_key}"
  local build_arg_5_val="${14:-build_arg_5_val}"
  local build_arg_6_key="${15:-build_arg_6_key}"
  local build_arg_6_val="${16:-build_arg_6_val}"
  local build_arg_7_key="${17:-build_arg_7_key}"
  local build_arg_7_val="${18:-build_arg_7_val}"
  local build_arg_8_key="${19:-build_arg_8_key}"
  local build_arg_8_val="${20:-build_arg_8_val}"
  local build_arg_9_key="${21:-build_arg_9_key}"
  local build_arg_9_val="${22:-build_arg_9_val}"
  local build_arg_10_key="${23:-build_arg_10_key}"
  local build_arg_10_val="${24:-build_arg_10_val}"
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
  &&  if test "${use_cache}" == 'true' && docker pull "${tag}"
      then
        build_args+=( --cache-from "${tag}" )
      fi \
  &&  echo "[INFO] Building: ${tag}" \
  &&  DOCKER_BUILDKIT='1' docker build "${build_args[@]}" "${context}" \
  &&  echo "[INFO] Pushing: ${tag}" \
  &&  docker push "${tag}" \
  &&  echo "[INFO] Deleting local copy of: ${tag}" \
  &&  docker image remove "${tag}"
}

function helper_common_execute_chunk_parallel {
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

function helper_common_get_gitlab_var {
  local gitlab_var_name="${1}"
      echo "[INFO] Retrieving var from GitLab: ${gitlab_var_name}" 1>&2 \
  &&  curl \
        --silent \
        --header "private-token: ${GITLAB_API_TOKEN}" \
        "${GITLAB_API_URL}/${gitlab_var_name}" \
      | jq -r '.value'
}

function helper_common_get_touched_files_in_last_commit {
  git diff --name-only "${CI_COMMIT_BEFORE_SHA}" "${CI_COMMIT_SHA}" \
    | while read -r path
      do
        ! test -e "${path}" || echo "${path}"
      done
}

function helper_common_has_any_file_changed {
  local file
  local files=( "$@" )
  local canon_file_a
  local canon_file_b

      helper_common_get_touched_files_in_last_commit > "${TEMP_FD}" \
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

function helper_common_is_today_first_day_of_month {
  test "$(date +%d)" == '01'
}

function helper_common_list_declared_jobs {
  local product="${1:-}"

  declare -F \
    | sed 's/declare -f //' \
    | grep -P '^job_[a-z_]+' \
    | sed 's/job_//' \
    | grep -P "${product}" \
    | sort
}

function helper_common_list_vars_with_regex {
  local regex="${1}"
  printenv | grep -oP "${regex}" | sort
}

function helper_common_registry_id {
  # Get the id of a gitlab registry
  # e.g helper_common_registry_id deps-base

  local registry_name="$1"
  local integrates_id='20741933'
  local check_url

      check_url="https://gitlab.com/api/v4/projects/${integrates_id}/registry/repositories" \
  &&  wget -O - "${check_url}" 2> /dev/null | jq ".[] | select (.name == \"${registry_name}\") | .id"
}

function helper_common_registry_delete {
  # Delete registry
  # e.g: helper_common_registry_delete deps-production TOKEN

  local registry_name="$1"
  local token="$2"
  local registry_id
  local delete_url

      registry_id=$(helper_common_registry_id "${registry_name}") \
  &&  delete_url="https://gitlab.com/api/v4/projects/20741933/registry/repositories/${registry_id}" \
  &&  curl --request DELETE --header "PRIVATE-TOKEN: ${token}" "${delete_url}"
}

function helper_common_minutes_of_month {
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

function helper_common_terraform_plan_new {
  local target_dir="${1}"
  local config="${2}"

      helper_common_terraform_init "${target_dir}" \
  &&  pushd "${target_dir}" \
    &&  echo '[INFO] Running terraform plan' \
    &&  tflint --config "${config}" \
    &&  terraform plan -lock=false -refresh=true \
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

function helper_common_update_kubeconfig {
  local cluster_name="${1}"
  local region="${2}"

  aws eks update-kubeconfig --name "${cluster_name}" --region "${region}"
}

function helper_common_poetry_compute_version {
  poetry run python -c 'if True:
    import time
    now=time.gmtime()
    minutes_month=(
      (now.tm_mday - 1) * 1440
      + now.tm_hour * 60
      + now.tm_min
    )
    print(time.strftime(f"%y.%m.{minutes_month}"))
  '
}

function helper_common_poetry_install_deps {
  local path="${1}"
  export PYTHONPATH="${PWD}/${path}/.venv/lib64/python3.8/site-packages:${PYTHONPATH}"

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

function helper_common_start_localstack {
  local time='0'
  local timeout='60'
  local services='s3'

      echo '[INFO] Starting localstack' \
  &&  docker stop localstack_main || true \
  &&  ENTRYPOINT=-d SERVICES="${services}" localstack start \
  &&  while ! docker logs localstack_main | grep -q 'Ready.'
      do
            sleep 1 \
        &&  time=$(( time + 1 )) \
        &&  if [ "${time}" = "${timeout}" ]
            then
                  echo "[ERROR] Timeout reached. Looks like container did not start properly" \
              &&  return 1
            fi
      done
}

function helper_common_array_contains_element {
  local e match="$1"
  shift
  for e; do [[ "$e" == "$match" ]] && return 0; done
  return 1
}

function helper_common_run_on_aws {
  export EXTERNAL_ENV_VARS
  export NIX_PATH
  export STARTDIR
  local job_definition
  local vcpus="${1}"
  local memory="${2}"
  local attempts="${3}"
  local timeout="${4}"
  local jobname="${5}"
  local jobqueue="${6}"
  local command=('./build.sh' "${@:7}")
  local maxmemory

      maxmemory=$(( "${vcpus}" * 4 * 900 )) \
  &&  if test "${memory}" -gt "${maxmemory}"
      then
            echo "[ERROR] Memory must be at most ${maxmemory} given ${vcpus} vcpus" \
        &&  return 1
      fi \
  &&  if test "${vcpus}" -gt '2'
      then
            echo "[ERROR] Decrease VCPUs consumption" \
        &&  return 1
      fi \
  &&  echo "[INFO] Running on AWS:" \
  &&  for arg in "${command[@]}"; do echo "       ${arg}"; done \
  &&  echo "[INFO] Memory: ${memory} MB" \
  &&  echo "[INFO] VCPU: ${vcpus} units" \
  &&  echo "[INFO] Attempts: ${attempts}" \
  &&  echo "[INFO] Timeout: ${timeout} seconds" \
  &&  NIX_PATH='/root/.nix-defexpr/channels' \
      job_definition=$( \
        python "${STARTDIR}/build/include/helpers/create_aws_batch_job_definition.py" \
          "${vcpus}" \
          "${memory}" \
          "${command[@]}" \
      ) \
  &&  aws batch submit-job \
        --container-overrides "${job_definition}" \
        --job-name "${jobname}" \
        --job-queue "${jobqueue}" \
        --job-definition 'default' \
        --retry-strategy "attempts=${attempts}" \
        --timeout "attemptDurationSeconds=${timeout}"
}

function helper_common_kill_attached_processes {
  local sleep_time="${1}"

  for process in $(jobs -p)
  do
    echo "[INFO] Killing PID: ${process}"
    kill -15 "${process}" || true
  done
  sleep "${sleep_time}"
}
