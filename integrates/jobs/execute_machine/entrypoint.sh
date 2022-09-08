# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function main() {
  local dynamo_item

  dynamo_item="$(aws dynamodb get-item \
    --table-name "fi_async_processing" \
    --key "{\"pk\":{\"S\": \"${2}\"}}")" \
    && echo "${dynamo_item}" \
    | jq '.Item.additional_info.S' -r \
      | jq -c -r '.roots[]' \
      | while read -r root; do
        echo "Cloning -> ${root}" \
          && melts drills \
            --pull-repos "$(echo "${dynamo_item}" | jq -c -r '.Item.entity.S')" \
            --name "${root}"
      done
}

main "${@}"
