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

function initialize {
  local build_dir

      build_dir="$(mktemp -d)" \
  &&  cd "${build_dir}" \
  &&  echo "[INFO] Build directory: ${PWD}" \
  ||  return 1
}

function success {
  touch "${out}"
}
