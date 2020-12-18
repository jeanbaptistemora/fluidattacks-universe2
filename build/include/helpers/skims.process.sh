# shellcheck shell=bash

function helper_skims_process_group {
  local success='true'

  # Make sure these exports are declared in `skims_process_group_on_aws`
  export GITLAB_API_TOKEN
  export GITLAB_API_USER
  export INTEGRATES_API_TOKEN
  export SERVICES_PROD_AWS_ACCESS_KEY_ID
  export SERVICES_PROD_AWS_SECRET_ACCESS_KEY
  export SKIMS_PROD_AWS_ACCESS_KEY_ID
  export SKIMS_PROD_AWS_SECRET_ACCESS_KEY

      helper_common_use_services \
  &&  helper_skims_aws_login prod \
  &&  echo '[INFO] Cloning repositories' \
  &&  { helper_common_pull_services_repositories "${group}" || true; } \
  &&  shopt -s nullglob \
  &&  for namespace in "groups/${group}/fusion/"*
      do
            namespace="$(basename "${namespace}")" \
        &&  echo "[INFO] Running skims: ${group} ${namespace}" \
        &&  helper_skims_get_group_config_as_json "${group}" "${namespace}" \
              | helper_common_json_to_yaml \
              | tee "${TEMP_FILE1}" \
        &&  helper_skims_pull_cache "${group}" "${namespace}" \
        &&  if "${product}/bin/skims" "${TEMP_FILE1}"
            then
              echo "[INFO] Succesfully processed: ${group} ${namespace}"
            else
                  echo "[ERROR] While running skims on: ${group} ${namespace}" \
              &&  success='false'
            fi \
        &&  helper_skims_push_cache "${group}" "${namespace}" \
        ||  continue
      done \
  &&  shopt -u nullglob \
  &&  helper_common_remove_services_repositories "${group}" \
  &&  test "${success}" = 'true'
}

function helper_skims_pull_cache {
  local group="${1}"
  local namespace="${2}"
  local source="s3://skims.data/cache/${group}/${namespace}"
  local target="${HOME}/.skims"

      echo "[INFO] Moving skims state from ${source} to ${target}" \
  &&  mkdir -p "${target}" \
  &&  aws s3 sync --delete --quiet "${source}" "${target}"
}

function helper_skims_push_cache {
  local group="${1}"
  local namespace="${2}"
  local source="s3://skims.data/cache/${group}/${namespace}"
  local source="${HOME}/.skims"

      echo "[INFO] Moving skims state from ${source} to ${target}" \
  &&  aws s3 sync --delete --quiet "${source}" "${target}" \
  &&  rm -rf "${source}"
}

function helper_skims_get_group_config_as_json {
  local group="${1}"
  local namespace="${2}"

  jq -e -n -r \
    --arg 'language' "$(yq -r .language < "groups/${group}/config/config.yml")" \
    --arg 'namespace' "${namespace}" \
    --arg 'working_dir' "groups/${group}/fusion/${namespace}" \
    '{
      language: $language,
      namespace: $namespace,
      path: {
        include: [
          "glob(*)"
        ],
        exclude: [
          "glob(**/.git)",
          "glob(**/*.min.js)",
          "glob(**/*bootstrap*)",
          "glob(**/*cordova*)",
          "glob(**/*dynatrace*)",
          "glob(**/*ibmmfpf.js*)",
          "glob(**/*jquery*)",
          "glob(**/*sjcl*)",
          "glob(**/cryptojs/components/core.js)",
          "glob(**/modernizr.js)",
          "glob(**/UI/AutocompleteGenerico)",
          "glob(**/UI/Tabs)",
          "glob(**/.vscode)",
          "glob(**/.idea)",
          "glob(**/*.pydevproject)",
          "glob(**/*.swp)",
          "glob(**/*.launch)",
          "glob(**/.cproject)",
          "glob(**/.buildpath)"
        ]
      },
      timeout: 14400,
      working_dir: $working_dir
    }'
}
