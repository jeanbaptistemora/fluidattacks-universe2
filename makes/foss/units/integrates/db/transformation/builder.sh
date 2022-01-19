# shellcheck shell=bash

function main {
  local email="" # Place your email here to become an admin
  local i=0
  local included_facets=(
    credentials_metadata
    credentials_historic_state
    credentials_state
    git_root_metadata
    git_root_state
    git_root_historic_state
    git_root_cloning
    git_root_historic_cloning
    ip_root_metadata
    ip_root_state
    ip_root_historic_state
    machine_git_root_execution
    root_services_toe_lines
    toe_input_metadata
    toe_lines_metadata
    url_root_metadata
    url_root_state
    url_root_historic_state
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
    vulnerability_metadata
    vulnerability_historic_state
    vulnerability_historic_treatment
    vulnerability_historic_verification
    vulnerability_historic_zero_risk
  )
  local facets=''

  facets=$(echo "${included_facets[@]}" | jq -R 'split(" ")') \
    && mkdir "${out}" \
    && echo '[INFO] Populating from new database design...' \
    && jq -c --arg facets "${facets}" \
      '{integrates_vms: [.DataModel[].TableFacets[] | select(.FacetName as $fn | $facets | index($fn) ) | {PutRequest: {Item: .TableData[]}}]}' \
      "${envNewDbDesign}" > "${out}/database-design" \
    && items_len=$(jq '.integrates_vms | length' "${out}/database-design") \
    && echo "items qy: ${items_len}" \
    && while [ $((i * 25)) -lt "$items_len" ]; do
      local ilow=$((i * 25)) \
        && local ihigh=$(((i + 1) * 25)) \
        && jq -c "{integrates_vms: .integrates_vms[$ilow:$ihigh]}" \
          "${out}/database-design" > "${out}/database-design${i}.json" \
        && ((i++))
    done \
    && if test -z "${email}"; then
      echo "[INFO] Admin email for new DB: test@fluidattacks.com"
      echo "[INFO] Admin email for old DB: integratesmanager@gmail.com"
    else
      echo "[INFO] Admin email for new DB: ${email}"
      echo "[INFO] Admin email for old DB: ${email}"
    fi \
    && for data in "${out}/database-design"*.json; do
      if test -n "${email}"; then
        sed -i "s/test@fluidattacks.com/${email}/g" "${data}"
      fi
    done \
    && for data in "${envDbData}/"*'.json'; do
      if test -z "${email}"; then
        sed "s/__adminEmail__/integratesmanager@gmail.com/g" "${data}" \
          > "${out}/$(basename "${data}")"
      else
        sed "s/__adminEmail__/${email}/g" "${data}" \
          > "${out}/$(basename "${data}")"
      fi
    done
}

main "${@}"
