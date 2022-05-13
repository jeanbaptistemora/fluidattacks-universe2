# shellcheck shell=bash

function abort {
  echo "${*}" \
    && exit 1 \
    || exit 1
}

function copy {
  cp --no-target-directory --recursive "${@}" \
    && chmod --recursive +w "${@: -1}"
}

function execute_chunk_parallel {
  local function_to_call="${1}"
  local todo_list="${2}"
  local total="${3}"
  local runtime="${4}"
  local index

  : \
    && if [ "${runtime}" = "batch" ]; then
      index=$(("${AWS_BATCH_JOB_ARRAY_INDEX}" + 1))
    elif [ "${runtime}" = "gitlab" ]; then
      index="${CI_NODE_INDEX}"
    else
      error "Runtime must be either 'batch' or 'gitlab'."
    fi \
    && info "Found $(wc -l "${todo_list}") items to process" \
    && info "Processing batch: ${index} of ${total}" \
    && split --number="l/${index}/${total}" "${todo_list}" \
    | while read -r item; do
      "${function_to_call}" "${item}" \
        || return 1
    done
}
