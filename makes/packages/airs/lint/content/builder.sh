# shellcheck shell=bash

function main {
      find "${envAirs}" -wholename '*.adoc' | while read -r path
      do
            check_adoc_main_title "${path}" \
        ||  return 1
      done \
  &&  touch "${out}" \
  ||  return 1
}

main "${@}"
