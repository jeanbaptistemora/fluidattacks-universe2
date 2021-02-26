# shellcheck shell=bash

function abort {
      echo "${1}" \
  &&  exit 1 \
  ||  exit 1
}

function copy {
  cp \
    --no-preserve 'mode' \
    --no-target-directory \
    --recursive \
    "${@}"
}

function copy2 {
      cp --no-target-directory --recursive "${@}" \
  &&  chmod --recursive +w "${@: -1}"
}

function ensure_env_vars {
  for var_name in "${@}"
  do
    if test -z "${!var_name:-}"
    then
          echo "[ERROR] Missing environment variable: ${var_name}" \
      &&  return 1
    fi
  done
}

function execute_chunk_parallel {
  export CI_NODE_INDEX
  export CI_NODE_TOTAL
  local function_to_call="${1}"
  local todo_list="${2}"

      echo "Found $(wc -l "${todo_list}") items to process" \
  &&  echo "Processing batch: ${CI_NODE_INDEX} of ${CI_NODE_TOTAL}" \
  &&  split --number="l/${CI_NODE_INDEX}/${CI_NODE_TOTAL}" "${todo_list}" \
        | while read -r item
          do
                "${function_to_call}" "${item}" \
            ||  return 1
          done
}
