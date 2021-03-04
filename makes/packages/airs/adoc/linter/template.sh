# shellcheck shell=bash

function check_adoc_main_title {
  local target="${1}"
  local msg='File must contain exactly one title'

      titles_count="$(grep -Pc '^=\s.*$' "${target}" || true)" \
  &&  if test "${titles_count}" = '1'
      then
        echo "[INFO] PASSED: ${msg}: ${target}"
      else
        abort "[ERROR] ${msg}: ${target}"
      fi
}

function check_adoc_min_keywords {
  local target="${1}"
  local min_keywords='5'
  local msg="File must contain at least ${min_keywords} keywords"

      keywords="$( \
        { grep -Po '^:keywords:.*' "${target}" || true; } \
          | tr ',' '\n' \
          | wc -l \
      )" \
  &&  if test "${keywords}" -ge "${min_keywords}"
      then
        echo "[INFO] PASSED: ${msg}: ${target}"
      else
        abort "[ERROR] ${msg}: ${target}"
      fi
}

function check_adoc_fluid_attacks_name {
  local target="${1}"
  local msg='Fluid Attacks must be spelled as Fluid Attacks'

  if pcregrep \
      -e '\bfluid attacks' \
      -e '\bFLUID Attacks' \
      -e '\bfluidsignal(?!\.formstack)' \
      -e '\bFluidsignal Group' \
      -e '\bfluid(?!.)' \
      -e '\bFluid(?! Attacks)' \
      -e '\bFLUID(?!.)' \
      -e '\bFLUIDAttacks' \
      "${target}"
  then
    echo "[ERROR] ${msg}: ${target}"
  else
    echo "[INFO] PASSED: ${msg}: ${target}"
  fi
}
