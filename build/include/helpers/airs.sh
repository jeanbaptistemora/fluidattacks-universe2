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

function helper_airs_file_exists {
  local path="${1}"

      if [ -f "${path}" ]
      then
            return 0
      else
            echo "[ERROR] ${path} does not exist" \
        &&  return 1
      fi
}

function helper_airs_adoc_max_columns {
  local file="${1}"
  local max_columns="${2}"
  local regex

      helper_airs_file_exists "${file}" \
  &&  normalized_file="$(helper_airs_adoc_normalize "${file}")" \
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

function helper_airs_adoc_tag_exists {
  file="${1}"
  tag="${2}"

      helper_airs_file_exists "${file}" \
  &&  if grep -q "${tag}" "${file}"
      then
            return 0
      else
            echo "[ERROR] ${file} does not have a ${tag} tag." \
        &&  return 1
      fi
}

function helper_airs_adoc_regex_direct {
  local file="${1}"
  local regex="${2}"
  local error="${3}"

      helper_airs_file_exists "${file}" \
  &&  if ! pcregrep -MH "${regex}" "${file}"
      then
            return 0
      else
            echo "[ERROR] ${file}: ${error}" \
        &&  return 1
      fi
}

function helper_airs_adoc_normalize {
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
  local numbered_list_regex='^\. .*'

      helper_airs_file_exists "${file}" \
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
              -e "s/${numbered_list_regex}//g" \
              -e "/${source_regex}/d" \
              -e "/${metadata_regex}/d" \
              -e "/${block_title_regex}/d" \
              -e "/${hard_break_regex}/d" \
              )" \
  &&  echo "${content}"
}

function helper_airs_word_count {
  local file="${1}"
  local min_words="${2}"
  local max_words="${3}"
  local file_style
  local words
  local regex='[0-9]+(?= words,)'

      helper_airs_file_exists "${file}" \
  &&  file_style="$(helper_airs_adoc_normalize "${file}" | style)" \
  &&  if [ "${file_style}" != 'No sentences found.' ]
      then
            words="$(echo "${file_style}" | grep -Po "${regex}")" \
        &&  if [ "${words}" -ge "${min_words}" ] && [ "${words}" -le "${max_words}" ]
            then
                  echo "[OK] ${file} must have [${min_words}-${max_words}] words. It currently has ${words}" \
              &&  return 0
            else
                  echo "[ERROR] ${file} must have [${min_words}-${max_words}] words. It currently has ${words}" \
              &&  return 1
            fi
      else
            echo "[INFO] ${file} seems to be empty. Skipping words test" \
        &&  return 0
      fi
}

function helper_airs_test_lix {
  local file="${1}"
  local max_lix="${2}"
  local file_lix
  local file_style
  local regex='Lix: (\d\d)'

      helper_airs_file_exists "${file}" \
  &&  file_style="$(helper_airs_adoc_normalize "${file}" | style)" \
  &&  if [ "${file_style}" != 'No sentences found.' ]
      then
            file_lix="$(echo "${file_style}" | pcregrep -o1 "${regex}")" \
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
