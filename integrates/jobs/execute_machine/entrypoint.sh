# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function main() {
  local dynamo_item
  local group_name
  local checks

  dynamo_item="$(aws dynamodb get-item \
    --table-name "fi_async_processing" \
    --key "{\"pk\":{\"S\": \"${2}\"}}")" \
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
          && python3 __argScript__ \
            --group-name "${group_name}" \
            --language="EN" \
            --root-nickname "${root}" \
            --checks "${checks}" \
            --working-dir "groups/${group_name}/fusion/${root}" \
          && aws s3 cp \
            --recursive \
            "groups/${group_name}/fusion/${root}/execution_configs/" \
            s3://skims.data/configs \
          && find "groups/${group_name}/fusion/${root}/execution_configs/" \
            -name "*.yaml" \
          | while IFS=$'\n' read -r file_config; do
            skims scan "groups/${group_name}/fusion/${root}/execution_configs/${file_config}"
          done \
          && aws s3 cp \
            --recursive \
            "groups/${group_name}/fusion/${root}/execution_results/" \
            s3://skims.data/results/
      done
}

main "${@}"
