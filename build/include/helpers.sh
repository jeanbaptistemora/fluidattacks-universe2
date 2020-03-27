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

function helper_image_blog_cover_dimensions {
  local path="${1}"
  local dimensions

      helper_file_exists "${path}" \
  &&  dimensions="$(identify -format "%wx%h" "${path}")" \
  &&  if [ "${dimensions}" = '600x280' ]
      then
            return 0
      else
            echo "[ERROR] ${path} does not have a size of 600x280" \
        && return 1
      fi
}

function helper_image_optimized {
  local path="${1}"

      helper_file_exists "${path}" \
  &&  if optipng "${path}" 2>&1 | tail -n2 | grep -q 'already optimized.'
      then
            return 0
      else
            echo "[ERROR] ${path} is not optimized" \
        &&  return 1
      fi
}

function helper_image_size {
  local path="${1}"
  local size_bytes

      helper_file_exists "${path}" \
  &&  size_bytes="$(stat -c %s "${path}")" \
  &&  if [ "${size_bytes}" -le '1000000' ]
      then
            return 0
      else
            echo "[ERROR] ${path} size is over 1mb" \
        &&  return 1
      fi
}

function helper_image_valid {
  local path="${1}"
  local valid_extensions='image/\(png\|svg+xml\|gif\)'

      helper_file_exists "${path}" \
  &&  if file --mime-type "${path}" | grep -q "${valid_extensions}"
      then
            return 0
      else
            echo "[ERROR] ${path} must be a valid format: ${valid_extensions}" \
        &&  return 1
      fi
}

function helper_generic_forbidden_extensions {
  local invalid_extensions='asc'
  local found_files

      found_files="$(find content/ -type f -regex  ".*\(${invalid_extensions}\)$")" \
  &&  if [ "${found_files}" == '' ]
      then
            return 0
      else
            echo '[ERROR] invalid/unsopported files found:' \
        &&  echo "${found_files}" \
        && return 1
      fi
}

function helper_generic_file_name {
  local file="${1}"
  local regex='^[a-z0-9-]+\.[a-z0-9]+\.*[a-z0-9]*$'
  local filename

      helper_file_exists "${file}" \
  &&  filename="$(basename "${file}")" \
  &&  if [[ ${filename} =~ ${regex} ]]
      then
            return 0
      else
            echo "[ERROR] ${filename} does not match the ${regex} convention" \
        &&  return 1
      fi
}

function helper_generic_adoc_main_title {
  local file="${1}"
  local titles

      helper_file_exists "${file}" \
  &&  titles="$(grep -Pc '^=\s.*$' "${file}")" || titles='0' \
  &&  if [ "${titles}" = '1' ]
      then
            return 0
      else
            echo "[ERROR] ${file} must have only one main title" \
        &&  return 1
      fi
}

function helper_generic_adoc_min_keywords {
  local file="${1}"
  local tag=':keywords:'
  local min_keywords='6'
  local keywords

      helper_file_exists "${file}" \
  &&  helper_adoc_tag_exists "${file}" "${tag}" \
  &&  keywords="$(grep -Po '(?<=^:keywords:).*' "${file}" | tr ',' '\n' | wc -l)" \
  &&  if [ "${keywords}" -ge "${min_keywords}" ]
      then
            return 0
      else
            echo "[ERROR] ${file} has less than ${min_keywords} keywords" \
        &&  return 1
      fi
}

function helper_generic_adoc_keywords_uppercase {
  local file="${1}"
  local tag=":keywords:"
  local keywords
  local invalid_keywords

      helper_file_exists "${file}" \
  &&  helper_adoc_tag_exists "${file}" "${tag}" \
  &&  keywords="$(grep -Po '(?<=^:keywords:).*' "${file}" | tr ',' '\n' | sed -e 's/^\s*//g')" \
  &&  invalid_keywords="$( echo "${keywords}" | grep -Pvc '^[A-Z]')" || invalid_keywords='0' \
  &&  if [ "${invalid_keywords}" = '0' ]
      then
            return 0
      else
            echo "[ERROR] All keywords in ${file} must begin with an upper case" \
        && return 1
      fi
}

function helper_generic_adoc_fluid_attacks_name {
  local file="${1}"
  local normalized_file

  local regex_fluid_no_attacks='Fluid(?! Attacks)'
  local regex_fluidsignal_group='Fluidsignal Group'
  local regex_fluidsignal_formstack='fluidsignal(?!\.formstack)'
  local regex_fluid_lowercase_1='fluid attacks'
  local regex_fluid_lowercase_2='fluid(?!.)'
  local regex_fluid_uppercase_1='FLUID(?!.)'
  local regex_fluid_uppercase_2='FLUIDAttacks'
  local regex_fluid_uppercase_3='FLUID Attacks'

      helper_file_exists "${file}" \
  &&  normalized_file="$(helper_adoc_normalize "${file}")" \
  &&  if ! echo "${normalized_file}" | pcregrep \
         -e "${regex_fluid_no_attacks}" \
         -e "${regex_fluidsignal_group}" \
         -e "${regex_fluidsignal_formstack}" \
         -e "${regex_fluid_lowercase_1}" \
         -e "${regex_fluid_lowercase_2}" \
         -e "${regex_fluid_uppercase_1}" \
         -e "${regex_fluid_uppercase_2}" \
         -e "${regex_fluid_uppercase_3}"
      then
        return 0
      else
            echo "[ERROR] Incorrect reference to 'Fluid Attacks' found in ${file}" \
        &&  return 1
      fi
}

function helper_generic_adoc_spelling {
  local file="${1}"
  local normalized_file
  local case_insensitive
  local case_sensitive
  local words=(
    'HTML'
    'Java'
    'Red Hat'
    'JavaScript'
    'COBOL'
    'AsciiDoc'
    'OpenSSL'
    'RPG'
    'MySQL'
    'SQLi'
    'bWAPP'
    'Python'
    'GlassFish'
    'OWASP'
    'Apache'
    'C Sharp'
    'OSCP'
    'OSWP'
    'CEH'
    'Linux'
    'Scala'
  )
      helper_file_exists "${file}" \
  &&  normalized_file="$(helper_adoc_normalize "${file}")" \
  &&  for word in "${words[@]}"
      do
            case_insensitive="$(echo "${normalized_file}" | grep -oi " ${word} ")" || true \
        &&  case_sensitive="$(echo "${normalized_file}" | grep -o " ${word} ")" || true \
        &&  if [ "${case_insensitive}" = "${case_sensitive}" ]
            then
                  continue
            else
                  echo "[ERROR] Spelling error in ${file}: Only '${word}' allowed" \
              &&  return 1
            fi
      done
}

function helper_generic_adoc_others {
  local file="${1}"
  local tests_direct=(
    'blank_space_header'
    'numbered_references'
    'title_before_image'
    'slug_max_chars'
    'four_dashes_code_block'
    'no_start_used'
    'slug_ends_with_slash'
    'image_alt_name'
    'title_no_double_quotes'
    'separate_code_from_paragraph'
    'title_length_limit'
    'metadata_lowercase'
    'no_monospace_header'
    'description_char_range'
    'local_relative_paths'
    'only_autonomic_com'
    'caption_forbidden_titles'
    'only_local_images'
  )
  local tests_normalized=(
    'link_before_url'
    'shortname_in_url'
  )
  declare -A data=(
    [regex_blank_space_header]='^=\s+.+\n.+'
    [error_blank_space_header]='Headers must be followed by a blank line'
    [regex_numbered_references]='^== Referenc.+\n\n[a-zA-Z]'
    [error_numbered_references]='References must be numbered'
    [regex_title_before_image]='image::.+\n\.[a-zA-Z]'
    [error_title_before_image]='Title must go before image'
    [regex_slug_max_chars]='^:slug: .{44,}'
    [error_slug_max_chars]='Slug length has a maximum of 44 characters'
    [regex_four_dashes_code_block]='^-{5,}'
    [error_four_dashes_code_block]='Code blocks must only have four dashes (----)'
    [regex_no_start_used]='\[start'
    [error_no_start_used]='Start attribute must not be used. Use a + sign instead'
    [regex_slug_ends_with_slash]='^:slug:.*[a-z0-9-]$'
    [error_slug_ends_with_slash]=':slug: tag must end with a slash /'
    [regex_image_alt_name]='^image::.+\[\]'
    [error_image_alt_name]='Images must have an alt description'
    [regex_title_no_double_quotes]='^={1,6} .*"'
    [error_title_no_double_quotes]='Do not use double quotes (") in titles'
    [regex_separate_code_from_paragraph]='^[a-zA-Z0-9].*\n.*\[source'
    [error_separate_code_from_paragraph]='Source code must be separated from a paragraph using a + sign'
    [regex_title_length_limit]='^= .{60,}'
    [error_title_length_limit]='Title must not exceed 60 characters'
    [regex_metadata_lowercase]='^:[A-Z]:'
    [error_metadata_lowercase]='All metadata must be lowercase'
    [regex_no_monospace_header]='^=+ \+.+\+.*'
    [error_no_monospace_header]='Headers must not have monospaces'
    [regex_description_char_range]='(?<=^:description: )(.{0,249}|.{301,})$'
    [error_description_char_range]='Descriptions must be in the 250-300 character range'
    [regex_local_relative_paths]='link:http(s)?://fluidattacks.com/web'
    [error_local_relative_paths]='Local URLs must use relative paths'
    [regex_only_autonomic_com]='autonomicmind.co(?!m)'
    [error_only_autonomic_com]='Use autonomicmind.com instead of autonomicmind.co'
    [regex_caption_forbidden_titles]='^\.(image|table|figure) \d+'
    [error_caption_forbidden_titles]='Captions must not contain "image", "table" or "figure"'
    [regex_only_local_images]='image::?https?://.*$'
    [error_only_local_images]='Only local images allowed'
    [regex_link_before_url]='(\s|\w|^|\()http(s)?://'
    [error_link_before_url]='All urls must be preceded by a "link:"'
    [regex_shortname_in_url]='link:http(s)?://'
    [error_shortname_in_url]='Urls must always have a shortname between brackets []'
  )

      helper_file_exists "${file}" \
  &&  for test in "${tests_direct[@]}"
      do
            helper_adoc_regex_direct \
              "${file}" \
              "${data[regex_${test}]}" \
              "${data[error_${test}]}" \
        ||  return 1
      done \
  &&  for test in "${tests_normalized[@]}"
      do
            helper_adoc_regex_normalized \
              "${file}" \
              "${data[regex_${test}]}" \
              "${data[error_${test}]}" \
        ||  return 1
      done
}

function helper_blog_adoc_category {
  local file="${1}"
  local category
  local regex='(?<=^:category: ).+$'
  local valid_categories=(
    'aix'
    'apache'
    'aspnet'
    'attacks'
    'certifications'
    'challenges'
    'cobol'
    'csharp'
    'documentation'
    'glassfish'
    'hacking'
    'html'
    'identity'
    'interview'
    'java'
    'javascript'
    'linux'
    'machine-learning'
    'math'
    'opinions'
    'philosophy'
    'php'
    'politics'
    'programming'
    'python'
    'redhat'
    'rpg'
    'scala'
    'social-engineering'
    'techniques'
    'verilog'
    'windows'
    'yii'
  )

      helper_file_exists "${file}" \
  &&  helper_adoc_tag_exists "${file}" ':category:' \
  &&  category="$(grep -Po "${regex}" "${file}")" \
  &&  if echo " ${valid_categories[*]} " | grep -q " ${category} "
      then
            return 0
      else
            echo "[ERROR] Category '${category}' in ${file} is not valid" \
        &&  echo "Valid categories: ${valid_categories[*]}" \
        &&  return 1
      fi
}

function helper_blog_adoc_tags {
  local file="${1}"
  local tags
  local regex='(?<=^:tags: ).+$'
  local valid_tags=(
    'android'
    'application'
    'blue team'
    'bug'
    'business'
    'cbc'
    'challenge'
    'cloud'
    'code'
    'company'
    'credential'
    'csv'
    'cybersecurity'
    'dependency'
    'detect'
    'devops'
    'discovery'
    'documentation'
    'economics'
    'encryption'
    'engineering'
    'eslint'
    'ethical hacking'
    'experiment'
    'exploit'
    'flaw'
    'forensics'
    'functional'
    'fuzzing'
    'git'
    'health'
    'healthcare'
    'htb'
    'imperative'
    'information'
    'injection'
    'interview'
    'investigation'
    'investment'
    'javascript'
    'jwt'
    'libssh'
    'linters'
    'machine learning'
    'math'
    'mistake'
    'multiparadigm'
    'mypy'
    'openssl'
    'operations'
    'password'
    'pentesting'
    'policies'
    'protect'
    'pwn'
    'pythagoras'
    'python'
    'red team'
    'revert'
    'risk'
    'saml'
    'scanner'
    'security'
    'security testing'
    'social engineering'
    'software'
    'solve'
    'sql'
    'ssl'
    'standard'
    'stateless'
    'technology'
    'test'
    'testing'
    'tls'
    'training'
    'trends'
    'vector'
    'vulnerability'
    'web'
    'wep'
    'wifi'
    'windows'
    'xml'
    'xpath'
    'xss'
  )

      helper_file_exists "${file}" \
  &&  helper_adoc_tag_exists "${file}" ':tags:' \
  &&  tags="$(grep -Po "${regex}" "${file}" | tr ',' ' ')" \
  &&  for tag in ${tags}
      do
            if echo " ${valid_tags[*]} " | grep -q " ${tag} "
            then
                  continue
            else
                  echo "[ERROR] Tag '${tag}' in ${file} is not valid" \
              &&  echo "Valid tags: ${valid_tags[*]}" \
              &&  return 1
            fi
      done
}

function helper_blog_adoc_others {
  local file="${1}"
  local tests=(
    'title_length_limit'
    'subtitle_length_limit'
    'source_unsplash'
  )
  declare -A data=(
    [regex_title_length_limit]='^= .{35,}'
    [error_title_length_limit]='Title must not exceed 35 characters'
    [regex_subtitle_length_limit]='(?<=^:subtitle: ).{56,}'
    [error_subtitle_length_limit]='Subtitles must not exceed 55 characters'
    [regex_source_unsplash]='(?<=^:source: )((?!https://unsplash).*$)'
    [error_source_unsplash]='The cover image is not from unsplash'
  )

      helper_file_exists "${file}" \
  &&  for test in "${tests[@]}"
      do
            helper_adoc_regex_direct \
              "${file}" \
              "${data[regex_${test}]}" \
              "${data[error_${test}]}" \
        ||  return 1
      done
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

function helper_get_lix {
  local file="${1}"

      helper_file_exists "${file}" \
  &&  helper_adoc_normalize "${file}" | style | pcregrep -o1 'Lix: (\d\d)'
}
