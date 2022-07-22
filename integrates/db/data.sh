# shellcheck shell=bash

function get_git_email {
  HOME="${HOME_IMPURE}" git config user.email
}

function main {
  local email="${GITLAB_USER_EMAIL:-$(get_git_email)}"
  local out="integrates/db/.data"
  local i=0
  local included_facets=(
    credentials_historic_state
    credentials_metadata
    credentials_state
    enrollment_metadata
    event_historic_state
    event_metadata
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
    root_secret
    git_environment_secret
    git_root_environment_url
    git_root_historic_cloning
    git_root_historic_state
    git_root_metadata
    group_historic_state
    group_historic_policies
    group_metadata
    group_unreliable_indicators
    ip_root_historic_state
    ip_root_metadata
    machine_git_root_execution
    organization_access
    organization_historic_policies
    organization_historic_state
    organization_metadata
    portfolio_metadata
    root_services_toe_lines
    stakeholder_metadata
    toe_input_metadata
    toe_lines_metadata
    url_root_historic_state
    url_root_metadata
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
          "${out}/database-design" | sed "s/__adminEmail__/${email}/g" \
          > "${out}/database-design${i}.json" \
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
