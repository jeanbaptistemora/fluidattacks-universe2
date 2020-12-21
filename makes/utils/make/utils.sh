# shellcheck shell=bash

# Shell hardening
set -o errexit
set -o pipefail
set -o nounset
set -o functrace
set -o errtrace
set -o monitor
set -o posix

# https://reproducible-builds.org/docs/source-date-epoch/
# https://nixos.org/nixpkgs/manual/#faq (15.17.3.3)
unset SOURCE_DATE_EPOCH

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
