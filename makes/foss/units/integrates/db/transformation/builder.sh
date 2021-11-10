# shellcheck shell=bash

function main {
  mkdir "${out}"
  export STATE_PATH="${out}"
  local email="${1:-integratesmanager@gmail.com}"
  local db_design="${envNewDbDesign}/database-design.json"
  local TMP_ITEMS='.tmp_integrates_vms'
  local i=0
  local included_facets=(
    git_root_metadata
    git_root_state
    git_root_historic_state
    git_root_cloning
    git_root_historic_cloning
    ip_root_metadata
    ip_root_state
    ip_root_historic_state
    machine_git_root_execution
    root_toe_input
    root_services_toe_lines
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
  )
  local facets=''

  facets=$(echo "${included_facets[@]}" | jq -R 'split(" ")') \
    && echo '[INFO] Populating from new database design...' \
    && jq -c --arg facets "${facets}" \
      '{integrates_vms: [.DataModel[].TableFacets[] | select(.FacetName as $fn | $facets | index($fn) ) | {PutRequest: {Item: .TableData[]}}]}' \
      "${db_design}" > "${STATE_PATH}/${TMP_ITEMS}" \
    && items_len=$(jq '.integrates_vms | length' "${STATE_PATH}/${TMP_ITEMS}") \
    && echo "items qy: ${items_len}" \
    && while [ $((i * 25)) -lt "$items_len" ]; do
      local ilow=$((i * 25)) \
        && local ihigh=$(((i + 1) * 25)) \
        && jq -c "{integrates_vms: .integrates_vms[$ilow:$ihigh]}" \
          "${STATE_PATH}/${TMP_ITEMS}" > "${STATE_PATH}/integrates_vms${i}.json" \
        && ((i++))
    done \
    && rm "${STATE_PATH}/${TMP_ITEMS}"
  echo "[INFO] Admin email: ${email}" \
    && sed "s/2020-09-04.*/$(date -u +%Y-%m-%dT%H:%M:%S.000000%z)\"/g" \
      < "${envDbData}/forces.json" \
    | sed "s/33e5d863252940edbfb144ede56d56cf/aaa/g" \
      | sed "s/a125217504d447ada2b81da3e4bdab0e/bbb/g" \
        > "${STATE_PATH}/forces.now.json" \
    && for data in "${envDbData}/"*'.json'; do
      sed "s/__adminEmail__/${email}/g" "${data}" \
        > "${STATE_PATH}/$(basename "${data}")"
    done
}

main "${@}"
