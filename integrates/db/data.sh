# shellcheck shell=bash

function main {
  local email="${GITLAB_USER_EMAIL:-$(git config user.email)}"
  local out="integrates/db/.data"
  local i=0
  local included_facets=(
    credentials_historic_state
    credentials_metadata
    credentials_state
    finding_approval
    finding_creation
    finding_historic_state
    finding_historic_verification
    finding_id
    finding_metadata
    finding_state
    finding_submission
    finding_unreliable_indicators
    finding_verification
    git_root_historic_cloning
    git_root_historic_state
    git_root_metadata
    group_historic_state
    group_metadata
    group_unreliable_indicators
    ip_root_historic_state
    ip_root_metadata
    machine_git_root_execution
    organization_historic_policies
    organization_historic_state
    organization_metadata
    portfolio_metadata
    root_services_toe_lines
    toe_input_metadata
    toe_lines_metadata
    url_root_historic_state
    url_root_metadata
    user_metadata
    vulnerability_historic_state
    vulnerability_historic_treatment
    vulnerability_historic_verification
    vulnerability_historic_zero_risk
    vulnerability_metadata
  )
  local facets=''

  facets=$(echo "${included_facets[@]}" | jq -R 'split(" ")') \
    && rm -rf "${out}" \
    && mkdir -p "${out}" \
    && echo '[INFO] Populating from new database design...' \
    && jq -c --arg facets "${facets}" \
      '{integrates_vms: [.DataModel[].TableFacets[] | select(.FacetName as $fn | $facets | index($fn) ) | {PutRequest: {Item: .TableData[]}}]}' \
      "__argNewDbDesign__" > "${out}/database-design" \
    && items_len=$(jq '.integrates_vms | length' "${out}/database-design") \
    && echo "items qy: ${items_len}" \
    && while [ $((i * 25)) -lt "$items_len" ]; do
      local ilow=$((i * 25)) \
        && local ihigh=$(((i + 1) * 25)) \
        && jq -c "{integrates_vms: .integrates_vms[$ilow:$ihigh]}" \
          "${out}/database-design" > "${out}/database-design${i}.json" \
        && ((i++))
    done \
    && echo "[INFO] Admin email for new DB: ${email}" \
    && echo "[INFO] Admin email for old DB: ${email}" \
    && for data in "__argDbData__/"*'.json'; do
      sed "s/__adminEmail__/${email}/g" "${data}" \
        > "${out}/$(basename "${data}")"
    done
}

main "${@}"
