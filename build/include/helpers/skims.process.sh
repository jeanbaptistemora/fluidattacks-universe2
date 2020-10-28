# shellcheck shell=bash

function helper_skims_process_group {
  local success

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
  &&  { helper_skims_pull_repositories "${group}" ||  true; } \
  &&  if ! test -e "groups/${group}/fusion"
      then
            echo '[WARNING] No repositories to test' \
        &&  return 0
      fi \
  &&  echo '[INFO] Running skims:' \
  &&  helper_skims_get_group_config_as_json "${group}" \
        | helper_common_json_to_yaml \
        | tee "${TEMP_FILE1}" \
  &&  helper_skims_pull_cache "${group}" \
  &&  if "${product}/bin/skims" --group "${group}" "${TEMP_FILE1}"
      then
            echo "[INFO] Succesfully processed: ${group}" \
        &&  success='true'
      else
            echo "[ERROR] While running skims on: ${group}" \
        &&  success='false'
      fi \
  &&  helper_skims_remove_repositories "${group}" \
  &&  helper_skims_push_cache "${group}" \
  &&  test "${success}" = 'true'
}

function helper_skims_pull_cache {
  local group="${1}"
  local source="s3://skims.data/cache/${group}"
  local target="${HOME}/.skims"

      echo "[INFO] Moving skims state from ${source} to ${target}" \
  &&  mkdir -p "${target}" \
  &&  aws s3 sync --delete --quiet "${source}" "${target}"
}

function helper_skims_pull_repositories {
  export SERVICES_PROD_AWS_ACCESS_KEY_ID
  export SERVICES_PROD_AWS_SECRET_ACCESS_KEY
  local group="${1}"

  CI='true' \
  CI_COMMIT_REF_NAME='master' \
  PROD_AWS_ACCESS_KEY_ID="${SERVICES_PROD_AWS_ACCESS_KEY_ID}" \
  PROD_AWS_SECRET_ACCESS_KEY="${SERVICES_PROD_AWS_SECRET_ACCESS_KEY}" \
  "${product}/bin/melts" drills --pull-repos "${group}"
}

function helper_skims_remove_repositories {
  local group="${1}"

      echo "[INFO] Removing repositories" \
  &&  rm -rf "groups/${group}/fusion"
}

function helper_skims_push_cache {
  local group="${1}"
  local target="s3://skims.data/cache/${group}"
  local source="${HOME}/.skims"

      echo "[INFO] Moving skims state from ${source} to ${target}" \
  &&  aws s3 sync --delete --quiet "${source}" "${target}" \
  &&  rm -rf "${source}"
}

function helper_skims_get_group_config_as_json {
  local group="${1}"

  jq -e -n -r \
    --arg 'chdir' "groups/${group}/fusion" \
    --arg 'language' "$(
        yq -r .language < "groups/${group}/config/config.yml"
      )" \
    '{
      chdir: $chdir,
      language: $language,
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
          "glog(**/*.pydevproject)",
          "glog(**/*.swp)",
          "glog(**/*.launch)",
          "glog(**/.cproject)",
          "glog(**/.buildpath)"
        ]
      },
      timeout: 14400
    }'
}
