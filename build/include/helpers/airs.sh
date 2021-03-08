# shellcheck shell=bash

function helper_airs_set_lc_all {
  export LC_ALL='en_US.UTF-8'
}

function helper_airs_list_touched_files {
  local path

  git show --format= --name-only HEAD | while read -r path
  do
    if test -e "${path}"
    then
      echo "${path}"
    fi
  done
}

function helper_airs_aws_login {
  local user="${1}"
  export AWS_ACCESS_KEY_ID
  export AWS_SECRET_ACCESS_KEY


      if [ "${user}" = 'development' ]
      then
            AWS_ACCESS_KEY_ID="${AIRS_DEV_AWS_ACCESS_KEY_ID}" \
        &&  AWS_SECRET_ACCESS_KEY="${AIRS_DEV_AWS_SECRET_ACCESS_KEY}"
      elif [ "${user}" = 'production' ]
      then
            AWS_ACCESS_KEY_ID="${AIRS_PROD_AWS_ACCESS_KEY_ID}" \
        &&  AWS_SECRET_ACCESS_KEY="${AIRS_PROD_AWS_SECRET_ACCESS_KEY}"
      else
            echo '[ERROR] either prod or dev must be passed as arg' \
        &&  return 1
      fi \
  &&  echo "[INFO] Logging into AWS with ${user} credentials" \
  &&  aws configure set aws_access_key_id "${AWS_ACCESS_KEY_ID}" \
  &&  aws configure set aws_secret_access_key "${AWS_SECRET_ACCESS_KEY}" \
  &&  aws configure set region 'us-east-1'
}

function helper_airs_git_sparse_checkout {
  local files="${1}"
  local version="${2}"
  local install_path="${3}"
  local url_repo="${4}"

      mkdir -p "${install_path}" \
  &&  pushd "${install_path}" || return 1 \
  &&  git init \
  &&  git remote add origin "${url_repo}" \
  &&  git config core.sparsecheckout true \
  &&  echo "${files}" | tr ' ' '\n' > .git/info/sparse-checkout \
  &&  git pull origin master \
  &&  git reset --hard "${version}" \
  &&  rm -rf .git/ \
  &&  popd || return 1
}
