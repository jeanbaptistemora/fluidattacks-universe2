# shellcheck shell=bash

source "${makeDerivation}"

function main {
      echo '[INFO] Creating virtualenv' \
  &&  python -m venv "${out}" \
  &&  echo '[INFO] Activating virtualenv' \
  &&  source "${out}/bin/activate" \
  &&  echo '[INFO] Installing' \
  &&  python -m pip install \
        --requirement "${envRequirementsFile}" \
        --no-cache-dir \
  &&  echo '[INFO] Freezing' \
  &&  python -m pip freeze > "${out}/requirements" \
  &&  if test "$(cat "${out}/requirements")" = "$(cat "${envRequirementsFile}")"
      then
        echo '[INFO] Integrity check passed'
      else
            echo '[ERROR] Integrity check failed' \
        &&  echo '[INFO] You need to pin all dependencies:' \
        &&  while read -r requirement
            do
              echo "\"${requirement}\""
            done < "${out}/requirements" \
        &&  return 1
      fi \
  &&  rm -f "${out}/requirements" \

}

main "${@}"
