# shellcheck shell=bash

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
  declare -F | sed 's/declare -f //' | grep -P '^job_[a-z_]+' | sed 's/job_//' | sort
}

function helper_list_vars_with_regex {
  local regex="${1}"
  printenv | grep -oP "${regex}" | sort
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

function helper_set_dev_secrets {
  export AWS_ACCESS_KEY_ID
  export AWS_SECRET_ACCESS_KEY
  export AWS_DEFAULT_REGION

      AWS_ACCESS_KEY_ID="${DEV_AWS_ACCESS_KEY_ID}" \
  &&  AWS_SECRET_ACCESS_KEY="${DEV_AWS_SECRET_ACCESS_KEY}" \
  &&  AWS_DEFAULT_REGION='us-east-1' \
  &&  aws configure set aws_access_key_id "${AWS_ACCESS_KEY_ID}" \
  &&  aws configure set aws_secret_access_key "${AWS_SECRET_ACCESS_KEY}" \
  &&  aws configure set region 'us-east-1'
}

function helper_set_prod_secrets {
  export AWS_ACCESS_KEY_ID
  export AWS_SECRET_ACCESS_KEY
  export AWS_DEFAULT_REGION

      AWS_ACCESS_KEY_ID=${PROD_AWS_ACCESS_KEY_ID} \
  &&  AWS_SECRET_ACCESS_KEY=${PROD_AWS_SECRET_ACCESS_KEY} \
  &&  AWS_DEFAULT_REGION='us-east-1' \
  &&  aws configure set aws_access_key_id "${AWS_ACCESS_KEY_ID}" \
  &&  aws configure set aws_secret_access_key "${AWS_SECRET_ACCESS_KEY}" \
  &&  aws configure set region 'us-east-1'
}

function helper_terraform_login {
  export TF_VAR_aws_access_key="$AWS_ACCESS_KEY_ID"
  export TF_VAR_aws_secret_key="$AWS_SECRET_ACCESS_KEY"
}

function helper_terraform_test {
  local dir="${1}"

      helper_terraform_login \
  &&  pushd "${dir}" || return 1 \
  &&  terraform init \
  &&  terraform plan -refresh=true \
  &&  tflint --deep --module \
  &&  popd || return 1
}

function helper_terraform_apply {
  local dir="${1}"

      helper_terraform_login \
  &&  pushd "${dir}" || return 1 \
  &&  terraform init \
  &&  terraform apply -auto-approve -refresh=true \
  &&  popd || return 1
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

function helper_adoc_max_columns {
  local file="${1}"
  local max_columns="${2}"
  local regex

      helper_file_exists "${file}" \
  &&  normalized_file="$(helper_adoc_normalize "${file}")" \
  &&  regex=".{${max_columns},}" \
  &&  if ! echo "${normalized_file}" | grep -Pq "${regex}"
      then
            return 0
      else
            echo "${normalized_file}" | grep -P "${regex}"
            echo "[ERROR] ${file} must be wrapped at column ${max_columns}" \
        &&  return 1
      fi
}

function helper_adoc_tag_exists {
  file="${1}"
  tag="${2}"

      helper_file_exists "${file}" \
  &&  if grep -q "${tag}" "${file}"
      then
            return 0
      else
            echo "[ERROR] ${file} does not have a ${tag} tag." \
        &&  return 1
      fi
}

function helper_adoc_regex_direct {
  local file="${1}"
  local regex="${2}"
  local error="${3}"

      helper_file_exists "${file}" \
  &&  if ! pcregrep -MH "${regex}" "${file}"
      then
            return 0
      else
            echo "[ERROR] ${file}: ${error}" \
        &&  return 1
      fi
}

function helper_adoc_regex_normalized {
  local file="${1}"
  local regex="${2}"
  local error="${3}"
  local normalized_file

      helper_file_exists "${file}" \
  &&  normalized_file="$(helper_adoc_normalize "${file}")" \
  &&  if ! echo "${normalized_file}" | pcregrep -MH "${regex}"
      then
            return 0
      else
            echo "[ERROR] ${file}: ${error}" \
        &&  return 1
      fi
}

function helper_adoc_normalize {
  local file="${1}"
  local content

  local blocks_regex='^(----|\+\+\+\+|\.\.\.\.)((.|\n)*?)^(----|\+\+\+\+|\.\.\.\.)'
  local link_regex='link:.*\['
  local internal_ref_regex='<<.*>>'
  local inline_anchors_regex='\[\[.*\]]'
  local images_regex='image:*.*\[.*\]'
  local tooltip_regex='tooltip:.*\['
  local button_regex='\[button\]\#'
  local inner_regex='\[inner\]\#'
  local source_regex='^\[source.*'
  local metadata_regex='^:[a-zA-Z0-9-]+:.*'
  local block_title_regex='^\.[a-zA-Z0-9].*'
  local hard_break_regex='^\+$'

      helper_file_exists "${file}" \
  &&  content="$(cat "${file}")" \
  &&  content="$(echo "${content}" | pcregrep -Mv "${blocks_regex}")" \
  &&  content="$(echo "${content}" | sed -r \
              -e "s/${link_regex}//g" \
              -e "s/${internal_ref_regex}//g" \
              -e "s/${inline_anchors_regex}//g" \
              -e "s/${images_regex}//g" \
              -e "s/${tooltip_regex}//g" \
              -e "s/${button_regex}//g" \
              -e "s/${inner_regex}//g" \
              -e "/${source_regex}/d" \
              -e "/${metadata_regex}/d" \
              -e "/${block_title_regex}/d" \
              -e "/${hard_break_regex}/d" \
              )" \
  &&  echo "${content}"
}

function helper_word_count {
  local file="${1}"
  local min_words="${2}"
  local max_words="${3}"
  local words
  local regex='[0-9]+(?= words,)'

      helper_file_exists "${file}" \
  &&  words="$(style "${file}" | grep -Po "${regex}")" \
  &&  if [ "${words}" -ge "${min_words}" ] && [ "${words}" -le "${max_words}" ]
      then
            return 0
      else
            echo "[ERROR] ${file} must have [${min_words}-${max_words}] words. It currently has ${words}"
      fi
}

function helper_test_lix {
  local file="${1}"
  local max_lix="${2}"
  local file_lix
  local file_style

      helper_file_exists "${file}" \
  &&  file_style="$(helper_adoc_normalize "${file}" | style)" \
  &&  if [ "${file_style}" != 'No sentences found.' ]
      then
            file_lix="$(echo "${file_style}" | pcregrep -o1 'Lix: (\d\d)')" \
        &&  if [ "${file_lix}" -le "${max_lix}" ]
            then
                  return 0
            else
                  echo "[ERROR] ${file} has Lix greater than ${max_lix}: ${file_lix}" \
              &&  return 1
            fi
      else
            echo "[INFO] ${file} seems to be empty. Skipping lix test" \
        &&  return 0
      fi
}
