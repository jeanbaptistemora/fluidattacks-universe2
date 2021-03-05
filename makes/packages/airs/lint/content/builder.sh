# shellcheck shell=bash

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
            &&  check_adoc_min_keywords "${path}" \
            &&  check_adoc_words_case "${path}" \
            ||  return 1
          done \
  &&  touch "${out}" \
  ||  return 1
}

main "${@}"
