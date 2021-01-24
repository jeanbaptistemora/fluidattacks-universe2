# shellcheck shell=bash

function get_deps_from_lock {
  jq -r '.dependencies | to_entries[] | .key + "@" + .value.version' < "${1}" \
    | sort --ignore-case
}

function main {
  local dependencies

      echo '[INFO] Computing Dependencies' \
  &&  mapfile -t 'dependencies' < "${envRequirementsFile}" \
  &&  mkdir "${out}" \
  &&  echo "[INFO] Installing: ${dependencies[*]}" \
  &&  pushd "${out}" \
    &&  HOME=. npm install "${dependencies[@]}" \
  &&  popd \
  &&  echo '[INFO] Freezing' \
  &&  get_deps_from_lock "${out}/package-lock.json" > "${out}/requirements" \
  &&  if test "$(cat "${out}/requirements")" = "$(cat "${envRequirementsFile}")"
      then
        echo '[INFO] Integrity check passed'
      else
            echo '[ERROR] Integrity check failed' \
        &&  echo '[INFO] You need to specify all dependencies:' \
        &&  while read -r requirement
            do
              echo "\"${requirement}\""
            done < "${out}/requirements" \
        &&  return 1
      fi \
  ||  return 1
}

main "${@}"
