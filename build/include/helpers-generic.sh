# shellcheck shell=bash

source "${srcIncludeHelpers}"

function helper_generic_forbidden_extensions {
  local invalid_extensions='asc'
  local found_files

      found_files="$(find content/ -type f -regex  ".*\(${invalid_extensions}\)$")" \
  &&  if [ "${found_files}" == '' ]
      then
            return 0
      else
            echo '[ERROR] invalid/unsopported files found:' \
        &&  echo "${found_files}" \
        && return 1
      fi
}

function helper_generic_file_name {
  local file="${1}"
  local regex='^[a-z0-9-]+\.[a-z0-9]+\.*[a-z0-9]*$'
  local filename

      helper_file_exists "${file}" \
  &&  filename="$(basename "${file}")" \
  &&  if [[ ${filename} =~ ${regex} ]]
      then
            return 0
      else
            echo "[ERROR] ${filename} does not match the ${regex} convention" \
        &&  return 1
      fi
}

function helper_generic_adoc_main_title {
  local file="${1}"
  local titles

      helper_file_exists "${file}" \
  &&  titles="$(grep -Pc '^=\s.*$' "${file}")" || titles='0' \
  &&  if [ "${titles}" = '1' ]
      then
            return 0
      else
            echo "[ERROR] ${file} must have only one main title" \
        &&  return 1
      fi
}

function helper_generic_adoc_min_keywords {
  local file="${1}"
  local tag=':keywords:'
  local min_keywords='6'
  local keywords

      helper_file_exists "${file}" \
  &&  helper_adoc_tag_exists "${file}" "${tag}" \
  &&  keywords="$(grep -Po '(?<=^:keywords:).*' "${file}" | tr ',' '\n' | wc -l)" \
  &&  if [ "${keywords}" -ge "${min_keywords}" ]
      then
            return 0
      else
            echo "[ERROR] ${file} has less than ${min_keywords} keywords" \
        &&  return 1
      fi
}

function helper_generic_adoc_keywords_uppercase {
  local file="${1}"
  local tag=":keywords:"
  local keywords
  local invalid_keywords

      helper_file_exists "${file}" \
  &&  helper_adoc_tag_exists "${file}" "${tag}" \
  &&  keywords="$(grep -Po '(?<=^:keywords:).*' "${file}" | tr ',' '\n' | sed -e 's/^\s*//g')" \
  &&  invalid_keywords="$( echo "${keywords}" | grep -Pvc '^[A-Z]')" || invalid_keywords='0' \
  &&  if [ "${invalid_keywords}" = '0' ]
      then
            return 0
      else
            echo "[ERROR] All keywords in ${file} must begin with an upper case" \
        && return 1
      fi
}

function helper_generic_adoc_fluid_attacks_name {
  local file="${1}"
  local normalized_file

  local regex_fluid_no_attacks='Fluid(?! Attacks)'
  local regex_fluidsignal_group='Fluidsignal Group'
  local regex_fluidsignal_formstack='fluidsignal(?!\.formstack)'
  local regex_fluid_lowercase_1='fluid attacks'
  local regex_fluid_lowercase_2='fluid(?!.)'
  local regex_fluid_uppercase_1='FLUID(?!.)'
  local regex_fluid_uppercase_2='FLUIDAttacks'
  local regex_fluid_uppercase_3='FLUID Attacks'

      helper_file_exists "${file}" \
  &&  normalized_file="$(helper_adoc_normalize "${file}")" \
  &&  if ! echo "${normalized_file}" | pcregrep \
         -e "${regex_fluid_no_attacks}" \
         -e "${regex_fluidsignal_group}" \
         -e "${regex_fluidsignal_formstack}" \
         -e "${regex_fluid_lowercase_1}" \
         -e "${regex_fluid_lowercase_2}" \
         -e "${regex_fluid_uppercase_1}" \
         -e "${regex_fluid_uppercase_2}" \
         -e "${regex_fluid_uppercase_3}"
      then
        return 0
      else
            echo "[ERROR] Incorrect reference to 'Fluid Attacks' found in ${file}" \
        &&  return 1
      fi
}

function helper_generic_adoc_spelling {
  local file="${1}"
  local normalized_file
  local case_insensitive
  local case_sensitive
  local words=(
    'HTML'
    'Java'
    'Red Hat'
    'JavaScript'
    'COBOL'
    'AsciiDoc'
    'OpenSSL'
    'RPG'
    'MySQL'
    'SQLi'
    'bWAPP'
    'Python'
    'GlassFish'
    'OWASP'
    'Apache'
    'C Sharp'
    'OSCP'
    'OSWP'
    'CEH'
    'Linux'
    'Scala'
  )
      helper_file_exists "${file}" \
  &&  normalized_file="$(helper_adoc_normalize "${file}")" \
  &&  for word in "${words[@]}"
      do
            case_insensitive="$(echo "${normalized_file}" | grep -oi " ${word} ")" || true \
        &&  case_sensitive="$(echo "${normalized_file}" | grep -o " ${word} ")" || true \
        &&  if [ "${case_insensitive}" = "${case_sensitive}" ]
            then
                  continue
            else
                  echo "[ERROR] Spelling error in ${file}: Only '${word}' allowed" \
              &&  return 1
            fi
      done
}

function helper_generic_adoc_others {
  local file="${1}"
  local tests_direct=(
    'blank_space_header'
    'numbered_references'
    'title_before_image'
    'slug_max_chars'
    'four_dashes_code_block'
    'no_start_used'
    'slug_ends_with_slash'
    'image_alt_name'
    'title_no_double_quotes'
    'separate_code_from_paragraph'
    'title_length_limit'
    'metadata_lowercase'
    'no_monospace_header'
    'description_char_range'
    'local_relative_paths'
    'only_autonomic_com'
    'caption_forbidden_titles'
    'only_local_images'
  )
  local tests_normalized=(
    'link_before_url'
    'shortname_in_url'
  )
  declare -A data=(
    [regex_blank_space_header]='^=\s+.+\n.+'
    [error_blank_space_header]='Headers must be followed by a blank line'
    [regex_numbered_references]='^== Referenc.+\n\n[a-zA-Z]'
    [error_numbered_references]='References must be numbered'
    [regex_title_before_image]='image::.+\n\.[a-zA-Z]'
    [error_title_before_image]='Title must go before image'
    [regex_slug_max_chars]='^:slug: .{44,}'
    [error_slug_max_chars]='Slug length has a maximum of 44 characters'
    [regex_four_dashes_code_block]='^-{5,}'
    [error_four_dashes_code_block]='Code blocks must only have four dashes (----)'
    [regex_no_start_used]='\[start'
    [error_no_start_used]='Start attribute must not be used. Use a + sign instead'
    [regex_slug_ends_with_slash]='^:slug:.*[a-z0-9-]$'
    [error_slug_ends_with_slash]=':slug: tag must end with a slash /'
    [regex_image_alt_name]='^image::.+\[\]'
    [error_image_alt_name]='Images must have an alt description'
    [regex_title_no_double_quotes]='^={1,6} .*"'
    [error_title_no_double_quotes]='Do not use double quotes (") in titles'
    [regex_separate_code_from_paragraph]='^[a-zA-Z0-9].*\n.*\[source'
    [error_separate_code_from_paragraph]='Source code must be separated from a paragraph using a + sign'
    [regex_title_length_limit]='^= .{60,}'
    [error_title_length_limit]='Title must not exceed 60 characters'
    [regex_metadata_lowercase]='^:[A-Z]:'
    [error_metadata_lowercase]='All metadata must be lowercase'
    [regex_no_monospace_header]='^=+ \+.+\+.*'
    [error_no_monospace_header]='Headers must not have monospaces'
    [regex_description_char_range]='(?<=^:description: )(.{0,249}|.{301,})$'
    [error_description_char_range]='Descriptions must be in the 250-300 character range'
    [regex_local_relative_paths]='link:http(s)?://fluidattacks.com/web'
    [error_local_relative_paths]='Local URLs must use relative paths'
    [regex_only_autonomic_com]='autonomicmind.co(?!m)'
    [error_only_autonomic_com]='Use autonomicmind.com instead of autonomicmind.co'
    [regex_caption_forbidden_titles]='^\.(image|table|figure) \d+'
    [error_caption_forbidden_titles]='Captions must not contain "image", "table" or "figure"'
    [regex_only_local_images]='image::?https?://.*$'
    [error_only_local_images]='Only local images allowed'
    [regex_link_before_url]='(\s|\w|^|\()http(s)?://'
    [error_link_before_url]='All urls must be preceded by a "link:"'
    [regex_shortname_in_url]='link:http(s)?://'
    [error_shortname_in_url]='Urls must always have a shortname between brackets []'
  )

      helper_file_exists "${file}" \
  &&  for test in "${tests_direct[@]}"
      do
            helper_adoc_regex_direct \
              "${file}" \
              "${data[regex_${test}]}" \
              "${data[error_${test}]}" \
        ||  return 1
      done \
  &&  for test in "${tests_normalized[@]}"
      do
            helper_adoc_regex_normalized \
              "${file}" \
              "${data[regex_${test}]}" \
              "${data[error_${test}]}" \
        ||  return 1
      done
}
