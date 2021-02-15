# shellcheck shell=bash

function get_key {
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

function get_array_length {
  local array_path="${1}"

  get_key "${array_path} | length"
}

function get_aws_keys {

  get_key 'keys[]' | tr '\n' ' '
}

function get_key_attrs {
  local key="${1}"

  get_key ".\"${key}\" | keys[]" | tr '\n' ' '
}

function get_attr_gitlab_project_ids {
  local key="${1}"
  local attr="${2}"

  get_key ".\"${key}\".\"${attr}\".gitlab.project_ids[]" | tr '\n' ' '
}

function update_key {
  local key="${1}"
  local attrs=()

      IFS=' ' read -ra attrs <<< "$(get_key_attrs "${key}")" \
  &&  for attr in "${attrs[@]}"
      do
            output_id="$(get_key ".\"${key}\".\"${attr}\".output.id")" \
        &&  output_val="$(terraform output "${output_id}")" \
        &&  gitlab_length="$(get_array_length ".\"${key}\".\"${attr}\".gitlab")" \
        &&  for ((i=0; i<gitlab_length; i++))
            do
                  project_id="$(get_key ".\"${key}\".\"${attr}\".gitlab[${i}].project_id")" \
              &&  key_id="$(get_key ".\"${key}\".\"${attr}\".gitlab[${i}].key_id")" \
              &&  masked="$(get_key ".\"${key}\".\"${attr}\".gitlab[${i}].masked")" \
              &&  protected="$(get_key ".\"${key}\".\"${attr}\".gitlab[${i}].protected")" \
              &&  set_project_variable \
                    "${GITLAB_API_TOKEN}" \
                    "${project_id}" \
                    "${key_id}" "${output_val}" \
                    "${protected}" "${masked}" \
              ||  return 1
            done \
        ||  return 1
      done
}

function main {
  local keys=()

      IFS=' ' read -ra keys <<< "$(get_aws_keys)" \
  &&  '__envTerraformTaint__' "${keys[@]}" \
  &&  '__envTerraformApply__' \
  &&  pushd '__envTarget__' \
    &&  for key in "${keys[@]}"
        do
              update_key "${key}" \
          ||  return 1
        done \
  &&  popd \
  ||  return 1
}

main "${@}"
