# shellcheck shell=bash

function get_git_email {
  HOME="${HOME_IMPURE}" git config user.email
}

function main {
  local email="${GITLAB_USER_EMAIL:-$(get_git_email)}"
  local out="integrates/db/.data"
  local i=0

  : \
    && rm -rf "${out}" \
    && mkdir -p "${out}" \
    && echo '[INFO] Populating from database design...' \
    && jq -c \
      '{integrates_vms: [.DataModel[].TableFacets[] | select(.FacetName) | {PutRequest: {Item: .TableData[]}}]}' \
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
