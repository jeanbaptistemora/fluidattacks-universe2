# shellcheck shell=bash

source '__envSearchPaths__'
source '__envUtilsGitlab__'

function __get_key {
  local path="${1}"
  local result

      result="$(echo '__envKeys__' | jq -r "${path}")" \
  &&  if [ "${result}" != 'null' ]
      then
            echo "${result}" \
        &&  return 0
      else
        return 1
      fi
}

function __get_aws_keys {

  __get_key 'keys[]' | tr '\n' ' '
}

function __get_key_attrs {
  local key="${1}"

  __get_key ".\"${key}\" | keys[]" | tr '\n' ' '
}

function __update_key {
  local key="${1}"
  local attrs=()

      IFS=' ' read -ra attrs <<< "$(__get_key_attrs "${key}")" \
  &&  for attr in "${attrs[@]}"
      do
            gitlab_id="$(__get_key ".\"${key}\".\"${attr}\".gitlab.id")" \
        &&  gitlab_masked="$(__get_key ".\"${key}\".\"${attr}\".gitlab.masked")" \
        &&  gitlab_protected="$(__get_key ".\"${key}\".\"${attr}\".gitlab.protected")" \
        &&  output_id="$(__get_key ".\"${key}\".\"${attr}\".output.id")" \
        &&  output_val="$(terraform output "${output_id}")" \
        &&  set_project_variable \
              "${GITLAB_API_TOKEN}" \
              '__envGitlabProjectId__' \
              "${gitlab_id}" "${output_val}" \
              "${gitlab_protected}" "${gitlab_masked}" \
        ||  return 1
      done
}

function main {
  local keys=()

      IFS=' ' read -ra keys <<< "$(__get_aws_keys)" \
  &&  '__envTerraformTaint__' "${keys[@]}" \
  &&  pushd '__envTarget__' \
    &&  for key in "${keys[@]}"
        do
              __update_key "${key}" \
          ||  return 1
        done \
  &&  popd \
  ||  return 1
}

main "${@}"
