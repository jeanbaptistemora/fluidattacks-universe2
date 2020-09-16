# shellcheck shell=bash

function helper_skims_process_group {
  local success

  # Make sure these exports are declared in `skims_queue_group_processing`
  export GITLAB_API_TOKEN
  export GITLAB_API_USER
  export INTEGRATES_API_TOKEN
  export SERVICES_PROD_AWS_ACCESS_KEY_ID
  export SERVICES_PROD_AWS_SECRET_ACCESS_KEY
  export SKIMS_PROD_AWS_ACCESS_KEY_ID
  export SKIMS_PROD_AWS_SECRET_ACCESS_KEY

      helper_use_services \
  &&  helper_skims_aws_login prod \
  &&  echo '[INFO] Cloning repositories' \
  &&  {
        _pull_repos "${group}" \
    &&  if ! test -e "groups/${group}/fusion"
        then
              echo '[WARNING] No repositories to test' \
          &&  return 0
        fi \
    ||  true;
  } \
  &&  echo '[INFO] Running skims:' \
  &&  _get_group_config_as_json "${group}" \
        | helper_common_json_to_yaml \
        | tee "${TEMP_FILE1}" \
  &&  if "${product}/bin/skims" --group "${group}" "${TEMP_FILE1}"
      then
            echo "[INFO] Succesfully processed: ${group}" \
        &&  success='true'
      else
            echo "[ERROR] While running skims on: ${group}" \
        &&  success='false'
      fi \
  &&  test "${success}" = 'true'
}

function _pull_repos {
  export SERVICES_PROD_AWS_ACCESS_KEY_ID
  export SERVICES_PROD_AWS_SECRET_ACCESS_KEY
  local group="${1}"

  CI='true' \
  CI_COMMIT_REF_NAME='master' \
  PROD_AWS_ACCESS_KEY_ID="${SERVICES_PROD_AWS_ACCESS_KEY_ID}" \
  PROD_AWS_SECRET_ACCESS_KEY="${SERVICES_PROD_AWS_SECRET_ACCESS_KEY}" \
  "${product}/bin/melts" drills --pull-repos "${group}"
}

function _get_group_config_as_json {
  local group="${1}"

  jq -e -n -r \
    --arg 'chdir' "groups/${group}/fusion" \
    --arg 'language' "$(
        yq -r .language < "groups/${group}/config/config.yml"
      )" \
    '{
      chdir: $chdir,
      console_snippets: false,
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
          "glob(**/test)",
          "glob(**/UI/AutocompleteGenerico)",
          "glob(**/UI/Tabs)"
        ]
      },
      timeout: 14400
    }'
}
