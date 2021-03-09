# shellcheck shell=bash

function main {
      echo '[INFO] Creating virtualenv' \
  &&  python -m venv "${out}" \
  &&  echo '[INFO] Activating virtualenv' \
  &&  source "${out}/bin/activate" \
  &&  echo '[INFO] Installing' \
  &&  HOME=. python -m pip install \
        --requirement "${envRequirementsFile}" \
        --no-cache-dir \
  &&  echo '[INFO] Freezing' \
  &&  python -m pip freeze | sort --ignore-case > "${out}/installed" \
  &&  sed -E 's|^(.*)\[.*?\](.*)$|\1\2|g' "${envRequirementsFile}" > "${out}/desired" \
  &&  if test "$(cat "${out}/desired")" = "$(cat "${out}/installed")"
      then
        echo '[INFO] Integrity check passed'
      else
            echo '[ERROR] Integrity check failed' \
        &&  echo '[INFO] You need to specify all dependencies:' \
        &&  git diff --no-index "${out}/desired" "${out}/installed" \
        &&  return 1
      fi \
  &&  rm -f "${out}/desired" \
  &&  rm -f "${out}/installed" \

}

main "${@}"
