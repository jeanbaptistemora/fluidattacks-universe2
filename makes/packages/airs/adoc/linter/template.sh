# shellcheck shell=bash

function check_adoc_main_title {
  local target="${1}"
  local msg='File must contain exactly one title'

      titles_count="$(grep -Pc '^=\s.*$' "${target}" || true)" \
  &&  if test "${titles_count}" != '1'
      then
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
  &&  if test "${keywords}" -lt "${min_keywords}"
      then
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
    abort "[ERROR] ${msg}: ${target}"
  fi
}

function check_adoc_words_case {
  local target="${1}"
  local words=(
    'AsciiDoc'
    'bWAPP'
    'CEH'
    'COBOL'
    'C Sharp'
    'GlassFish'
    'HTML'
    'Java'
    'JavaScript'
    'Linux'
    'MySQL'
    'OpenSSL'
    'OSCP'
    'OSWP'
    'OWASP'
    'Python'
    'Red Hat'
    'RPG'
    'Scala'
    'SQLi'
  )
  local msg='Spelling'

    for word in "${words[@]}"
    do
          case_insensitive="$(grep -ioP "( |^)${word}( |$)" "${target}" || true)" \
      &&  case_sensitive="$(grep -oP "( |^)${word}( |$)" "${target}" || true)" \
      &&  if test "${case_insensitive}" != "${case_sensitive}"
          then
            abort "[ERROR] ${msg}: ${word}: ${target}"
          fi \
      ||  return 1
    done
}
