#! /usr/bin/env bash

function main {
  local repo="${1}"             # fusion/xxx
  local date="${2}"             # 2021-08-01
  local branch="${3}"           # trunk
  local commit_to_search="${4}" # xxxxxxx
  export TZ='UTC'
  local git=(git -C "${repo}" -P)

  pushd "$(mktemp -d)" \
    && "${git[@]}" checkout "${branch}" \
    && date_min="$(date --date "${date}" --rfc-3339 seconds)" \
    && date_max="$(date --date "${date}+1month" --rfc-3339 seconds)" \
    && echo "From: ${date_min}, to: ${date_max}" \
    && "${git[@]}" log \
      --after="${date_min}" \
      --before="${date_max}" \
      --format='%H' \
      --no-merges \
      --reverse \
      > commits.lst \
    && mapfile -t commits < commits.lst \
    && "${git[@]}" config advice.detachedHead false \
    && touch last \
    && for commit in "${commits[0]}^1" "${commits[@]}"; do
      echo --- \
        && echo Inspecting "${commit}" \
        && "${git[@]}" checkout --quiet "${commit}" \
        && "${git[@]}" ls-files \
        | xargs -n 1 "${git[@]}" blame \
          | grep -a "${commit_to_search}" \
            > this \
        && { git -P diff --no-index last this || true; } \
        && mv this last
    done
}

main "${@}"
