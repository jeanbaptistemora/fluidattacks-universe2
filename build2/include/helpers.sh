# shellcheck shell=bash

function helper_use_pristine_workdir {
  export WORKDIR
  export STARTDIR

  function helper_teardown_workdir {
        echo "[INFO] Deleting: ${WORKDIR}" \
    &&  rm -rf "${WORKDIR}"
  }
  trap 'helper_teardown_workdir' 'EXIT'

      echo '[INFO] Creating a pristine workdir' \
  &&  rm -rf "${WORKDIR}" \
  &&  mkdir -p "${WORKDIR}" \
  &&  echo '[INFO] Copying files to workdir' \
  &&  cp -r "${STARTDIR}/." "${WORKDIR}" \
  &&  echo '[INFO] Entering the workdir' \
  &&  pushd "${WORKDIR}" \
  &&  echo '[INFO] Running: git clean -xdf' \
  &&  git clean -xdf \
  ||  return 1
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

function helper_list_declared_jobs {
  declare -F \
    | sed 's/declare -f //' \
    | grep -P '^job_[a-z_]+' \
    | sed 's/job_//' \
    | sort
}

function helper_list_touched_files {
  local path

  git show --format= --name-only HEAD | while read -r path
  do
    if test -e "${path}"
    then
      echo "${path}"
    fi
  done
}

function helper_file_exists {
  local path="${1}"

      if [ -f "${path}" ]
      then
            return 0
      else
            echo "[ERROR] ${path} does not exist" \
        &&  return 1
      fi
}

function helper_build_nix_caches_parallel {
  local n_provisioners
  local n_provisioners_per_group
  local n_provisioners_remaining
  export lower_limit
  export upper_limit

      n_provisioners=$(find build/provisioners/ -type f | wc -l) \
  &&  n_provisioners_per_group=$(( n_provisioners/CI_NODE_TOTAL )) \
  &&  n_provisioners_remaining=$(( n_provisioners%CI_NODE_TOTAL )) \
  &&  if [ "${n_provisioners_remaining}" -gt '0' ]
      then
        n_provisioners_per_group=$(( n_provisioners_per_group+=1 ))
      fi \
  &&  lower_limit=$(( (CI_NODE_INDEX-1)*n_provisioners_per_group )) \
  &&  upper_limit=$(( CI_NODE_INDEX*n_provisioners_per_group-1 )) \
  &&  upper_limit=$((
        upper_limit > n_provisioners-1 ? n_provisioners-1 : upper_limit
      ))
}

function helper_aws_login {
      echo '[INFO] Logging into AWS' \
  &&  aws configure set aws_access_key_id "${AWS_ACCESS_KEY_ID}" \
  &&  aws configure set aws_secret_access_key "${AWS_SECRET_ACCESS_KEY}"
}

function helper_terraform_login {
  export TF_VAR_aws_access_key
  export TF_VAR_aws_secret_key

      helper_aws_login \
  &&  echo '[INFO] Logging into Terraform' \
  &&  TF_VAR_aws_access_key="${AWS_ACCESS_KEY_ID}" \
  &&  TF_VAR_aws_secret_key="${AWS_SECRET_ACCESS_KEY}"
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

function helper_terraform_apply {
  local target_dir="${1}"

      helper_terraform_init "${target_dir}" \
  &&  pushd "${target_dir}" \
    &&  echo '[INFO] Running terraform apply' \
    &&  terraform apply -auto-approve -refresh=true \
  &&  popd \
  || return 1
}

function helper_test_commit_msg_commitlint {
  local commit_diff
  local commit_hashes
  local parser_url='https://gitlab.com/autonomicmind/default/-/raw/master/commitlint-configs/challenges/parser-preset.js'
  local rules_url='https://gitlab.com/autonomicmind/default/-/raw/master/commitlint-configs/challenges/commitlint.config.js'

      helper_use_pristine_workdir \
  &&  curl -LOJ "${parser_url}" \
  &&  curl -LOJ "${rules_url}" \
  &&  npm install @commitlint/{config-conventional,cli} \
  &&  git fetch --prune > /dev/null \
  &&  if [ "${IS_LOCAL_BUILD}" = "${TRUE}" ]
      then
            commit_diff="origin/master..${CI_COMMIT_REF_NAME}"
      else
            commit_diff="origin/master..origin/${CI_COMMIT_REF_NAME}"
      fi \
  &&  commit_hashes="$(git log --pretty=%h "${commit_diff}")" \
  &&  for commit_hash in ${commit_hashes}
      do
            echo  '[INFO] Running Commitlint' \
        &&  git log -1 --pretty=%B "${commit_hash}" | npx commitlint \
        ||  return 1
      done
}
