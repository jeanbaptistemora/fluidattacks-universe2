# shellcheck shell=bash

source "${makeDerivation}"

function main {
      echo '[INFO] Creating virtualenv' \
  &&  python -m venv "${out}" \
  &&  echo '[INFO] Activating virtualenv' \
  &&  source "${out}/bin/activate" \
  &&  echo '[INFO] Installing' \
  &&  use_ephemeral_dir \
    &&  copy "${envPackagePath}" . \
    &&  python -m pip install --no-cache-dir .
}

main "${@}"
