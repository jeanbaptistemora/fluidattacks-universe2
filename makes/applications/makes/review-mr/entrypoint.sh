# shellcheck shell=bash

function main {
  local config='.reviews.toml'
  export CI_PROJECT_ID
  export CI_MERGE_REQUEST_IID
  export REVIEWS_TOKEN

  reviews "${config}"
}

main "${@}"
