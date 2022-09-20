# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function main() {
  local dynamo_item
  local group_name
  local checks
  local dynamo_key

  aws_login "prod_integrates" "3600" \
    && ensure_gitlab_env_vars \
      INTEGRATES_API_TOKEN \
    && dynamo_key="{\"pk\":{\"S\": \"${2}\"}}" \
      dynamo_item="$(aws dynamodb get-item \
        --table-name "fi_async_processing" \
        --key "${dynamo_key}")" \
    && group_name="$(echo "${dynamo_item}" \
      | jq '.Item.entity.S' -r)" \
    && checks="$(echo "${dynamo_item}" \
      | jq '.Item.additional_info.S' -r \
      | jq -c -r '.checks')" \
    && echo "${dynamo_item}" \
    | jq '.Item.additional_info.S' -r \
      | jq -c -r '.roots[]' \
      | while read -r root; do
        echo "Cloning -> ${root}" \
          && if ! melts drills \
            --pull-repos "$(echo "${dynamo_item}" | jq -c -r '.Item.entity.S')" \
            --name "${root}"; then
            echo "Can not clone ${root}"
            continue
          fi \
          && if [ ! -d "groups/${group_name}/fusion/${root}/" ]; then
            continue
          fi \
          && python3 __argScript__ generate-configs \
            --group-name "${group_name}" \
            --root-nickname "${root}" \
            --checks "${checks}" \
            --working-dir "groups/${group_name}/fusion/${root}" \
            --api-token "${INTEGRATES_API_TOKEN}" \
          && aws s3 cp \
            --recursive \
            "groups/${group_name}/fusion/${root}/execution_configs/" \
            s3://skims.data/configs \
          && find "groups/${group_name}/fusion/${root}/execution_configs/" \
            -name "*.yaml" \
          | while read -r file_config; do
            pushd "groups/${group_name}/fusion/${root}" \
              && current_commit="$(git rev-parse HEAD)" \
              && popd \
              && python3 __argScript__ start-execution \
                --group-name "${group_name}" \
                --root-nickname "${root}" \
                --api-token "${INTEGRATES_API_TOKEN}" \
                --commit-hash "${current_commit}" \
              && skims scan --group "${group_name}" "${file_config}" \
              && filename="$(basename "${file_config}")" \
              && execution_id="${filename%.*}" \
              && execution_result="groups/${group_name}/fusion/${root}/execution_results/${execution_id}.sarif" \
              && if test -f "${execution_result}"; then
                aws s3 cp "${execution_result}" s3://skims.data/results/ \
                  && python3 __argScript__ submit-task \
                    --execution-id "${execution_id}" \
                  && python3 __argScript__ finish-execution \
                    --group-name "${group_name}" \
                    --root-nickname "${root}" \
                    --api-token "${INTEGRATES_API_TOKEN}" \
                    --checks "${checks}"
              fi
          done
      done \
    && aws dynamodb delete-item \
      --table-name "fi_async_processing" \
      --key "${dynamo_key}"
}

main "${@}"
