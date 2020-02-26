# shellcheck shell=bash

function helper_use_pristine_workdir {
  export WORKDIR="${PWD}.ephemeral"
  export STARTDIR="${PWD}"

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

function helper_docker_build_and_push {
  local tag="${1}"
  local context="${2}"
  local dockerfile="${3}"
  local build_arg_1_key="${4:-build_arg_1_key}"
  local build_arg_1_val="${5:-build_arg_1_val}"
  local build_args=(
    --tag "${tag}"
    --file "${dockerfile}"
    --build-arg "${build_arg_1_key}=${build_arg_1_val}"
  )

      helper_use_pristine_workdir \
  &&  echo "[INFO] Logging into: ${CI_REGISTRY}" \
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
  &&  docker push "${tag}"
}

function helper_get_gitlab_var {
  local gitlab_var_name="${1}"
      echo "[INFO] Retrieving var from GitLab: ${gitlab_var_name}" 1>&2 \
  &&  curl \
        --silent \
        --header "private-token: ${GITLAB_TOKEN}" \
        "${GITLAB_API_URL}/${gitlab_var_name}" \
      | jq -r '.value'
}

function helper_list_declared_jobs {
  declare -F | sed 's/declare -f //' | grep -P '^job_[a-z_]+' | sed 's/job_//' | sort
}

function helper_list_vars_with_regex {
  local regex="${1}"
  printenv | grep -oP "${regex}" | sort
}

function helper_set_dev_secrets {
  export JWT_TOKEN
  export AWS_ACCESS_KEY_ID
  export AWS_SECRET_ACCESS_KEY
  export AWS_DEFAULT_REGION

      JWT_TOKEN=$(helper_get_gitlab_var JWT_TOKEN) \
  &&  AWS_ACCESS_KEY_ID=$(helper_get_gitlab_var DEV_AWS_ACCESS_KEY_ID) \
  &&  AWS_SECRET_ACCESS_KEY=$(helper_get_gitlab_var DEV_AWS_SECRET_ACCESS_KEY) \
  &&  AWS_DEFAULT_REGION='us-east-1' \
  &&  aws configure set aws_access_key_id "${AWS_ACCESS_KEY_ID}" \
  &&  aws configure set aws_secret_access_key "${AWS_SECRET_ACCESS_KEY}" \
  &&  aws configure set region 'us-east-1' \
  &&  echo '[INFO] Exporting development secrets' \
  &&  sops_vars development
}
