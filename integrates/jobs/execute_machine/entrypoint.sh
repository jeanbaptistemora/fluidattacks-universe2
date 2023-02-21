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
    && dynamo_item="$(aws dynamodb get-item \
      --table-name "fi_async_processing" \
      --key "${dynamo_key}")" \
    && retries="$(echo "${dynamo_item}" \
      | jq '.Item | if has("retries") then .retries.N else 0 end' -r)" \
    && aws dynamodb update-item \
      --table-name "fi_async_processing" \
      --key "${dynamo_key}" \
      --update-expression "SET retries=:retries" \
      --expression-attribute-values "{\":retries\": {\"N\": \"$((retries + 1))\"}}" \
    && group_name="$(echo "${dynamo_item}" \
      | jq '.Item.entity.S' -r)" \
    && checks="$(echo "${dynamo_item}" \
      | jq '.Item.additional_info.S' -r \
      | jq -c -r '.checks')" \
    && chown -R "${USER}" "$(pwd)" \
    && git config --global --add safe.directory '*' \
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
          && pushd "groups/${group_name}/fusion/${root}/" \
          && if ! git reset --hard; then
            echo "Can not reset ${root}"
            continue
          fi \
          && popd \
          && python3 __argScript__ generate-configs \
            --group-name "${group_name}" \
            --root-nickname "${root}" \
            --checks "${checks}" \
            --working-dir "groups/${group_name}/fusion/${root}" \
            --api-token "${INTEGRATES_API_TOKEN}" \
          && aws s3 cp \
            --recursive \
            "groups/${group_name}/fusion/${root}/execution_configs/" \
            s3://machine.data/configs \
          && find "groups/${group_name}/fusion/${root}/execution_configs/" \
            -name "*.yaml" \
          | while read -r file_config; do
            pushd "groups/${group_name}/fusion/${root}" \
              && popd \
              && skims scan --group "${group_name}" "${file_config}" \
              && filename="$(basename "${file_config}")" \
              && execution_id="${filename%.*}" \
              && execution_result="groups/${group_name}/fusion/${root}/execution_results/${execution_id}.sarif" \
              && if test -f "${execution_result}"; then
                aws s3 cp "${execution_result}" s3://machine.data/results/ \
                  && python3 __argScript__ submit-task \
                    --execution-id "${execution_id}"
              fi
          done
      done \
    && aws dynamodb delete-item \
      --table-name "fi_async_processing" \
      --key "${dynamo_key}" \
    && if test -n "${CI}"; then
      nix-store --gc
    fi
}

main "${@}"
