# shellcheck shell=bash

function check_adoc_main_title {
  local target="${1}"
  local msg='Files must contain exactly one title'

      titles_count="$(grep -Pc '^=\s.*$' "${target}" || true)" \
  &&  if test "${titles_count}" = '1'
      then
        echo "[INFO] PASSED: ${msg}: ${target}"
      else
        abort "[ERROR] ${msg}: ${target}"
      fi
}
