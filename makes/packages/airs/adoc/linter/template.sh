# shellcheck shell=bash

function check_adoc_main_title {
  local target="${1}"

      titles_count="$(grep -Pc '^=\s.*$' "${target}" || true)" \
  &&  if test "${titles_count}" = '1'
      then
        echo "[INFO] adoc_main_title: ${target}"
      else
        abort "[ERROR] adoc_main_title: ${target}"
      fi
}
