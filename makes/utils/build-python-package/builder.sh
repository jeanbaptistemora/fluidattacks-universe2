# shellcheck shell=bash

function main {
      echo '[INFO] Creating virtualenv' \
  &&  python -m venv "${out}" \
  &&  echo '[INFO] Activating virtualenv' \
  &&  source "${out}/bin/activate" \
  &&  echo '[INFO] Installing' \
  &&  pushd "$(mktemp -d)" \
    &&  copy "${envPackagePath}" . \
    &&  python -m pip install --no-cache-dir . \
  &&  popd \
  ||  return 1
}

main "${@}"
