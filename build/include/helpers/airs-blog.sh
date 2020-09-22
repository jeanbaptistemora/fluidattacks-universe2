# shellcheck shell=bash

function helper_airs_blog_adoc_category {
  local file="${1}"
  local category
  local regex='(?<=^:category: ).+$'
  local valid_categories=(
    'aix'
    'apache'
    'aspnet'
    'attacks'
    'certifications'
    'challenges'
    'cobol'
    'csharp'
    'documentation'
    'glassfish'
    'hacking'
    'html'
    'identity'
    'interview'
    'java'
    'javascript'
    'linux'
    'machine-learning'
    'math'
    'opinions'
    'philosophy'
    'php'
    'politics'
    'programming'
    'python'
    'redhat'
    'rpg'
    'scala'
    'social-engineering'
    'techniques'
    'verilog'
    'windows'
    'yii'
  )

      helper_airs_file_exists "${file}" \
  &&  helper_airs_adoc_tag_exists "${file}" ':category:' \
  &&  category="$(grep -Po "${regex}" "${file}")" \
  &&  if echo " ${valid_categories[*]} " | grep -q " ${category} "
      then
            return 0
      else
            echo "[ERROR] Category '${category}' in ${file} is not valid" \
        &&  echo "Valid categories: ${valid_categories[*]}" \
        &&  return 1
      fi
}

function helper_airs_blog_adoc_tags {
  local file="${1}"
  local tags
  local regex='(?<=^:tags: ).+$'
  local valid_tags=(
    'android'
    'application'
    'backdoor'
    'blue team'
    'bug'
    'business'
    'cbc'
    'challenge'
    'cloud'
    'code'
    'company'
    'credential'
    'csv'
    'cybersecurity'
    'dependency'
    'detect'
    'devops'
    'discovery'
    'documentation'
    'economics'
    'encryption'
    'engineering'
    'eslint'
    'ethical hacking'
    'experiment'
    'exploit'
    'flaw'
    'forensics'
    'functional'
    'fuzzing'
    'git'
    'health'
    'healthcare'
    'hevd'
    'htb'
    'imperative'
    'information'
    'injection'
    'interview'
    'investigation'
    'investment'
    'javascript'
    'jwt'
    'kernel'
    'libssh'
    'linters'
    'linters'
    'machine learning'
    'math'
    'mistake'
    'multiparadigm'
    'mypy'
    'openssl'
    'operations'
    'osce'
    'osee'
    'password'
    'pentesting'
    'policies'
    'protect'
    'pwn'
    'pythagoras'
    'python'
    'red team'
    'revert'
    'risk'
    'saml'
    'scanner'
    'security'
    'security testing'
    'social engineering'
    'software'
    'solve'
    'sql'
    'ssl'
    'standard'
    'stateless'
    'technology'
    'test'
    'testing'
    'tls'
    'training'
    'trends'
    'vector'
    'vulnerability'
    'vulnserver'
    'web'
    'wep'
    'wifi'
    'windows'
    'xml'
    'xpath'
    'xss'
  )

      helper_airs_file_exists "${file}" \
  &&  helper_airs_adoc_tag_exists "${file}" ':tags:' \
  &&  tags="$(grep -Po "${regex}" "${file}" | tr ',' ' ')" \
  &&  for tag in ${tags}
      do
            if echo " ${valid_tags[*]} " | grep -q " ${tag} "
            then
                  continue
            else
                  echo "[ERROR] Tag '${tag}' in ${file} is not valid" \
              &&  echo "Valid tags: ${valid_tags[*]}" \
              &&  return 1
            fi
      done
}

function helper_airs_blog_adoc_others {
  local file="${1}"
  local tests=(
    'title_length_limit'
    'subtitle_length_limit'
    'source_unsplash'
  )
  declare -A data=(
    [regex_title_length_limit]='^= .{35,}'
    [error_title_length_limit]='Title must not exceed 35 characters'
    [regex_subtitle_length_limit]='(?<=^:subtitle: ).{56,}'
    [error_subtitle_length_limit]='Subtitles must not exceed 55 characters'
    [regex_source_unsplash]='(?<=^:source: )((?!https://unsplash).*$)'
    [error_source_unsplash]='The cover image is not from unsplash'
  )

      helper_airs_file_exists "${file}" \
  &&  for test in "${tests[@]}"
      do
            helper_airs_adoc_regex_direct \
              "${file}" \
              "${data[regex_${test}]}" \
              "${data[error_${test}]}" \
        ||  return 1
      done
}
