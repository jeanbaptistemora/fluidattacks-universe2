# shellcheck shell=bash

function check_adoc_blog_categories {
  local target="${1}"
  local valid_categories=(
    attacks
    challenges
    documentation
    hacking
    identity
    interview
    machine-learning
    math
    opinions
    philosophy
    politics
    programming
    social-engineering
    techniques
  )

  check_adoc_tag_exists "${path}" 'page-category' \
    && grep -Po '(?<=^:page-category: ).+$' "${target}" \
    | sed -E 's|,\s*|\n|g' \
      > list \
    && mapfile -t categories < list \
    && for category in "${categories[@]}"; do
      if ! echo "${valid_categories[*]}" | grep -q "${category}"; then
        abort "[ERROR] Tag: ${category}, is not valid: ${target}, pick one from: ${valid_categories[*]}"
      fi
    done
}

function check_adoc_blog_patterns {
  local target="${1}"
  declare -A msgs=(
    [source_unsplash]='The cover image is not from unsplash'
    [subtitle_length_limit]='Subtitles must not exceed 55 characters'
    [title_length_limit]='Title must not exceed 35 characters'
  )
  declare -A patterns=(
    [source_unsplash]='(?<=^:source: )((?!https://unsplash).*$)'
    [subtitle_length_limit]='(?<=^:page-subtitle: ).{56,}'
    [title_length_limit]='^= .{36,}'
  )

  for test in "${!patterns[@]}"; do
    if pcregrep -MH "${patterns[${test}]}" "${target}"; then
      abort "[ERROR] ${msgs[${test}]}: ${target}"
    fi
  done
}

function check_adoc_blog_tags {
  local target="${1}"
  local valid_tags=(
    android
    application
    backdoor
    blue-team
    bug
    business
    cbc
    challenge
    cloud
    code
    company
    credential
    csv
    cybersecurity
    dependency
    detect
    devops
    discovery
    documentation
    economics
    encryption
    engineering
    eslint
    ethical-hacking
    experiment
    exploit
    flaw
    functional
    fuzzing
    git
    hacking
    health
    healthcare
    hevd
    htb
    imperative
    information
    injection
    interview
    investment
    javascript
    jwt
    kernel
    libssh
    linters
    machine-learning
    math
    mistake
    multiparadigm
    mypy
    openssl
    operations
    osce
    osee
    password
    pentesting
    policies
    protect
    pwn
    python
    red-team
    revert
    risk
    saml
    scanner
    security-testing
    social-engineering
    software
    sql
    ssl
    standard
    stateless
    technology
    test
    tls
    training
    trends
    vector
    vulnerability
    vulnserver
    web
    wep
    wifi
    windows
    xml
    xpath
    xss
  )

  check_adoc_tag_exists "${path}" 'page-tags' \
    && grep -Po '(?<=^:page-tags: ).+$' "${target}" \
    | sed -E 's|,\s*|\n|g' \
      > list \
    && mapfile -t tags < list \
    && for tag in "${tags[@]}"; do
      if ! echo "${valid_tags[*]}" | grep -q "${tag}"; then
        abort "[ERROR] Tag: ${tag}, is not valid: ${target}, pick one from: ${valid_tags[*]}"
      fi
    done
}

function check_adoc_keywords_casing {
  local target="${1}"
  local msg="Keywords must be: Like This"

  { grep -Po '(?<=^:page-keywords: ).*' "${target}" || true; } \
    | sed -E 's|,\s*|\n|g;s| |\n|g' \
      > list \
    && mapfile -t words < list \
    && for word in "${words[@]}"; do
      if test "$(echo "${word}" | grep -cPv '^[A-ZÁÉÍÓÚÑ]+[a-záéíóúñ]*$')" -gt 0 && ! test "$(grep -cP "^${word}$" __argAcceptedKeywordsFile__)" -gt 0; then
        abort "[ERROR] ${msg}: ${word}: ${target}"
      fi
    done
}

function check_adoc_lix {
  local target="${1}"
  local max_lix="${2}"
  local msg="Document Lix must be under ${max_lix}"
  local lix

  lix="$(
    sed 's|link:.*\[|[|g' "${target}" \
      | sed 's|image:.*\[|[|g' \
      | sed 's|https://.*\[|[|g' \
      | sed 's|http://.*\[|[|g' \
      | sed 's|\[role=.*||g' \
      | grep -vh '^:' \
      | style \
      | grep -oP '(?<=Lix: )[0-9]+'
  )" \
    && if test "${lix}" -gt "${max_lix}"; then
      abort "[ERROR] ${msg}, current: ${lix}: ${target}"
    fi
}

function check_adoc_main_title {
  local target="${1}"
  local msg='File must contain exactly one title'

  titles_count="$(grep -Pc '^=\s.*$' "${target}" || true)" \
    && if test "${titles_count}" != '1'; then
      abort "[ERROR] ${msg}: ${target}"
    fi
}

function check_adoc_max_columns {
  local target="${1}"
  local msg='File must be at most 80 columns'

  if grep -v '^:' "${target}" \
    | grep -v '\(link:\|image::\|https://\|http://\)' \
    | grep -P "^.{81,}"; then
    abort "[ERROR] ${msg}: ${target}"
  fi
}

function check_adoc_min_keywords {
  local target="${1}"
  local min_keywords='5'
  local msg="File must contain at least ${min_keywords} keywords"

  keywords="$(
    { grep -Po '^:page-keywords:.*' "${target}" || true; } \
      | tr ',' '\n' \
      | wc -l
  )" \
    && if test "${keywords}" -lt "${min_keywords}"; then
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
    "${target}"; then
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

  for word in "${words[@]}"; do
    case_insensitive="$(grep -ioP "( |^)${word}( |$)" "${target}" || true)" \
      && case_sensitive="$(grep -oP "( |^)${word}( |$)" "${target}" || true)" \
      && if test "${case_insensitive}" != "${case_sensitive}"; then
        abort "[ERROR] ${msg}: ${word}: ${target}"
      fi \
      || return 1
  done
}

function check_adoc_patterns {
  local target="${1}"
  declare -A msgs=(
    [blank_space_header]='Headers must be followed by a blank line'
    [caption_forbidden_titles]='Captions must not contain "image", "table" or "figure"'
    [description_char_range]='Descriptions must be in the 50-160 character range'
    [four_dashes_code_block]='Code blocks must only have four dashes (----)'
    [image_alt_name]='Images must have an alt description'
    [local_relative_paths]='Local URLs must use relative paths'
    [metadata_lowercase]='All metadata must be lowercase'
    [no_monospace_header]='Headers must not have monospaces'
    [no_start_used]='Start attribute must not be used. Use a + sign instead'
    [numbered_references]='References must be numbered'
    [only_external_images]='Only images uploaded to Cloudinary or an external free source are allowed'
    [only_autonomic_com]='Use autonomicmind.com'
    [separate_code_from_paragraph]='Source code must be separated from a paragraph using a + sign'
    [slug_ends_with_slash]=':slug: tag must end with a slash /'
    [slug_max_chars]='Slug length has a maximum of 44 characters'
    [title_before_image]='Title must go before image'
    [title_length_limit]='Title must not exceed 60 characters'
    [title_no_double_quotes]='Do not use double quotes (") in titles'
  )
  declare -A patterns=(
    [blank_space_header]='^=\s+.+\n.+'
    [caption_forbidden_titles]='^\.(image|table|figure) \d+'
    [description_char_range]='(?<=^:page-description: )(.{0,49}|.{161,})$'
    [four_dashes_code_block]='^-{5,}'
    [image_alt_name]='^image::.+\[\]'
    [local_relative_paths]='link:http(s)?://fluidattacks.com'
    [metadata_lowercase]='^:[A-Z]:'
    [no_monospace_header]='^=+ \+.+\+.*'
    [no_start_used]='\[start'
    [numbered_references]='^== Referenc.+\n\n[a-zA-Z]'
    [only_external_images]='image::?../'
    [only_autonomic_com]='autonomicmind.co(?!m)'
    [separate_code_from_paragraph]='^[a-zA-Z0-9].*\n.*\[source'
    [slug_ends_with_slash]='^:page-slug:.*[a-z0-9-]$'
    [slug_max_chars]='^:page-slug: .{44,}'
    [title_before_image]='image::.+\n\.[a-zA-Z]'
    [title_length_limit]='^= .{60,}'
    [title_no_double_quotes]='^={1,6} .*"'
  )

  for test in "${!patterns[@]}"; do
    if pcregrep -MH "${patterns[${test}]}" "${target}"; then
      abort "[ERROR] ${msgs[${test}]}: ${target}"
    fi
  done
}

function check_adoc_tag_exists {
  local target="${1}"
  local tag="${2}"
  local msg="Tag must exists: ${2}"

  if ! grep -q ":${tag}:" "${target}"; then
    abort "[ERROR] ${msg}: ${target}"
  fi
}

function check_adoc_word_count {
  local target="${1}"
  local min_words="${2}"
  local max_words="${3}"
  local msg="Document must have between ${min_words} and ${max_words} words"
  local words

  words="$(
    sed 's|link:.*\[|[|g' "${target}" \
      | sed 's|image:.*\[|[|g' \
      | sed 's|https://.*\[|[|g' \
      | sed 's|http://.*\[|[|g' \
      | sed 's|\[role=.*||g' \
      | grep -vh '^:' \
      | style \
      | grep -oP '[0-9]+(?= words,)'
  )" \
    && if test "${words}" -lt "${min_words}" || test "${words}" -gt "${max_words}"; then
      abort "[ERROR] ${msg}: ${target} ${words}"
    fi
}
