# shellcheck shell=bash

function copy {
  cp \
    --no-preserve 'mode' \
    --no-target-directory \
    --recursive \
    "${@}"
}

function make_executable {
  chmod +x "${@}"
}

function remove {
  rm -rf "${@}"
}

function success {
  touch "${out}"
}

function use_ephemeral_dir {
  local build_dir

      build_dir="$(mktemp -d)" \
  &&  pushd "${build_dir}" \
  ||  return 1
}
