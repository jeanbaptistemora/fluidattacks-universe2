# shellcheck shell=bash

function check_content_file_name {
  local target="${1}"
  local msg='File must follow the naming convention'

  if echo "${target}" | grep -Pv '^[a-z0-9-/.]+\.[a-z0-9]+$'; then
    abort "[ERROR] ${msg}: ${target}"
  fi
}

function find_md {
  local target="${1}"

  find "${target}" -type f -wholename '*.md' \
    | (grep --file "${envExclude}" --fixed-strings --invert-match || cat) \
    | sort
}

function main {
  find_md "${envAirs}" | while read -r path; do
    echo "[INFO] Verifying: ${path}" \
      && check_md_fluid_attacks_name "${path}" \
      && check_md_keywords_casing "${path}" \
      && check_md_lix "${path}" '75' \
      && check_md_main_title "${path}" \
      && check_md_min_keywords "${path}" \
      && check_md_patterns "${path}" \
      && check_md_tag_exists "${path}" 'description' \
      && check_md_word_count "${path}" '1' '4500' \
      && check_md_words_case "${path}" \
      || return 1
  done \
    && find "${envAirs}/front/content" -type f | sort | while read -r path; do
      echo "[INFO] Verifying: ${path}" \
      && check_content_file_name "${path}" \
        || return 1
    done \
    && find_md "${envAirs}/front/content/blog" | while read -r path; do
      echo "[INFO] Verifying: ${path}" \
      && check_md_blog_categories "${path}" \
        && check_md_blog_patterns "${path}" \
        && check_md_blog_tags "${path}" \
        && check_md_lix "${path}" '52' \
        && check_md_tag_exists "${path}" 'alt' \
        && check_md_tag_exists "${path}" 'source' \
        && check_md_tag_exists "${path}" 'subtitle' \
        && check_md_word_count "${path}" '800' '1200' \
        || return 1
    done \
    && touch "${out}" \
    || return 1
}

main "${@}"
