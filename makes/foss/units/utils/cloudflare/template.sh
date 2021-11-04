# shellcheck shell=bash

function cloudflare_purge_cache {
  local cloudflare_api_token=${1}
  local domain=${2}
  shift 2
  local urls=("${@}")
  local api_url="https://api.cloudflare.com/client/v4"
  local zones

  zones=$(
    curl \
      -X GET "${api_url}/zones?name=${domain}&status=active" \
      -H "Authorization: Bearer ${cloudflare_api_token}" \
      -H "Content-Type: application/json" \
      | jq -r ".result[] | .id"
  ) \
    && echo "[INFO] Purging cloudflare cache" \
    && for zone in ${zones}; do
      curl \
        -X POST "${api_url}/zones/${zone}/purge_cache" \
        -H "Authorization: Bearer ${cloudflare_api_token}" \
        -H "Content-Type: application/json" \
        --data '{"files":'"$(echo "${urls[@]}" | jq -R 'split(" ")')"'}'
    done \
    || return 1
}
