# shellcheck shell=bash

function check_content_file_name {
  local target="${1}"
  local msg='File must follow the naming convention'

  if echo "${target}" | grep -Pv '^[a-z0-9-/.]+\.[a-z0-9]+$'; then
    abort "[ERROR] ${msg}: ${target}"
  fi
}

function find_adoc {
  local target="${1}"

  find "${target}" -type f -wholename '*.adoc' \
    | (grep --file "${envExclude}" --fixed-strings --invert-match || cat) \
    | sort
}

function main {
  find_adoc "${envAirs}" | while read -r path; do
    echo "[INFO] Verifying: ${path}" \
      && check_adoc_fluid_attacks_name "${path}" \
      && check_adoc_keywords_casing "${path}" \
      && check_adoc_lix "${path}" '65' \
      && check_adoc_main_title "${path}" \
      && check_adoc_max_columns "${path}" \
      && check_adoc_min_keywords "${path}" \
      && check_adoc_patterns "${path}" \
      && check_adoc_tag_exists "${path}" 'page-description' \
      && check_adoc_word_count "${path}" '1' '4500' \
      && check_adoc_words_case "${path}" \
      || return 1
  done \
    && find "${envAirs}/front/content" -type f | sort | while read -r path; do
      echo "[INFO] Verifying: ${path}" \
      && check_content_file_name "${path}" \
        || return 1
    done \
    && find_adoc "${envAirs}/front/content/blog" | while read -r path; do
      echo "[INFO] Verifying: ${path}" \
      && check_adoc_blog_categories "${path}" \
        && check_adoc_blog_patterns "${path}" \
        && check_adoc_blog_tags "${path}" \
        && check_adoc_lix "${path}" '50' \
        && check_adoc_tag_exists "${path}" 'page-alt' \
        && check_adoc_tag_exists "${path}" 'source' \
        && check_adoc_tag_exists "${path}" 'page-subtitle' \
        && check_adoc_word_count "${path}" '800' '1200' \
        || return 1
    done \
    && touch "${out}" \
    || return 1
}

main "${@}"
