# shellcheck shell=bash

function check_content_file_name {
  local target="${1}"
  local msg='File must follow the naming convention'

  if echo "${target}" | grep -Pv '^[a-z0-9-/.]+\.[a-z0-9]+$'
  then
    abort "[ERROR] ${msg}: ${target}"
  fi
}

function main {
      find "${envAirs}" -wholename '*.adoc' \
        | grep --file "${envExclude}" --fixed-strings --invert-match \
        | sort \
        | while read -r path
          do
                echo "[INFO] Verifying: ${path}" \
            &&  check_adoc_fluid_attacks_name "${path}" \
            &&  check_adoc_keywords_casing "${path}" \
            &&  check_adoc_main_title "${path}" \
            &&  check_adoc_max_columns "${path}" \
            &&  check_adoc_min_keywords "${path}" \
            &&  check_adoc_patterns "${path}" \
            &&  check_adoc_tag_exists "${path}" 'description' \
            &&  check_adoc_word_count "${path}" '1' '4500' \
            &&  check_adoc_words_case "${path}" \
            ||  return 1
          done \
  &&  find "${envAirs}/content" -type f \
        | sort \
        | while read -r path
          do
                echo "[INFO] Verifying: ${path}" \
            &&  check_content_file_name "${path}" \
            ||  return 1
          done \
  &&  touch "${out}" \
  ||  return 1
}

main "${@}"
