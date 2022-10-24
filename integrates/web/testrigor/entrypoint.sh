# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function run_tests {
  local test_cases=()

  : \
    && for test_file in __argTests__/*.txt; do
      test_cases+=(
        "$(
          jq -n \
            --arg custom_steps "$(cat "${test_file}")" \
            --arg description "$(basename "${test_file}")" \
            '{"customSteps": $custom_steps, "description": $description}'
        )"
      )
    done \
    && baseline=$(jq -n '$ARGS.positional' --jsonargs "${test_cases[@]}") \
    && curl -X POST \
      -H "Content-type: application/json" \
      -H "auth-token: ${TESTRIGOR_AUTH_TOKEN}" \
      --data "{
        \"baselineMutations\": ${baseline},
        \"branch\": {
          \"commit\": \"${CI_COMMIT_SHA}\",
          \"name\": \"${CI_COMMIT_REF_NAME}\"
        },
        \"explicitMutations\": true,
        \"forceCancelPreviousTesting\": true,
        \"url\": \"https://${CI_COMMIT_REF_NAME}.app.fluidattacks.com/\"
      }" \
      "https://api.testrigor.com/api/v1/apps/${TESTRIGOR_SUITE_ID}/retest" \
    || return 1
}

function wait_for_completion {
  : \
    && while true; do
      : \
        && echo "Checking testRigor" \
        && response=$(
          curl -i -o - -s -X GET \
            "https://api.testrigor.com/api/v1/apps/${TESTRIGOR_SUITE_ID}/status" \
            -d "branchName=${CI_COMMIT_REF_NAME}" \
            -H "auth-token: ${TESTRIGOR_AUTH_TOKEN}" \
            -H "Accept: application/json"
        ) \
        && code=$(echo "$response" | grep HTTP | awk '{print $2}') \
        && case $code in
          4* | 5*)
            echo "Error calling API"
            return 1
            ;;
          200)
            echo "Test finished successfully"
            return 0
            ;;
          227 | 228)
            echo "Test is not finished yet"
            ;;
          230)
            echo "Test finished but failed"
            return 1
            ;;
          *)
            echo "Unknown status"
            return 1
            ;;
        esac \
        && sleep 10 \
        || return 1
    done \
    || return 1
}

function main {
  : \
    && sops_export_vars __argSecretsDev__ \
      TESTRIGOR_AUTH_TOKEN \
      TESTRIGOR_SUITE_ID \
    && run_tests \
    && wait_for_completion \
    || return 1
}

main "${@}"
