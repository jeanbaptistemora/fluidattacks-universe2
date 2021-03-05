# shellcheck shell=bash

function check_adoc_keywords_casing {
  local target="${1}"
  local msg="Keywords must be: Like This"

      { grep -Po '(?<=^:keywords: ).*' "${target}" || true; } \
        | sed -E 's|,\s*|\n|g;s| |\n|g' \
        > list \
  &&  mapfile -t words < list \
  &&  for word in "${words[@]}"
      do
        if test "$(echo "${word}" | grep -cPv '^[A-Z]+[a-z]*$')" -gt 0
        then
          abort "[ERROR] ${msg}: ${word}: ${target}"
        fi
      done
}

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

function check_adoc_patterns {
  local target="${1}"
  declare -A msgs=(
    [caption_forbidden_titles]='Captions must not contain "image", "table" or "figure"'
    [only_local_images]='Only local images are allowed'
    [only_autonomic_com]='Use autonomicmind.com'
  )
  declare -A patterns=(
    [caption_forbidden_titles]='^\.(image|table|figure) \d+'
    [only_local_images]='image::?https?://'
    [only_autonomic_com]='autonomicmind.co(?!m)'
  )

  for test in "${!patterns[@]}"
  do
    if pcregrep -MH "${patterns[${test}]}" "${target}"
    then
      abort "[ERROR] ${msgs[${test}]}: ${target}"
    fi
  done
}
