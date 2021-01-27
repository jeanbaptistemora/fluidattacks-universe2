# shellcheck shell=bash

source "${envBashLibCommon}"

function get_deps_from_lock {
  jq -r '.dependencies | to_entries[] | .key + "@" + .value.version' < "${1}" \
    | sort --ignore-case
}

# Use npm install with --force flag for packages that would fail to install
# due to OS/arch issues (fsevents), but removing them from the dependencies
# would install them anyway due to being an inherited dependency
# from another package, thus creating an Integrity Check error
function main {
  local dependencies

      mkdir "${out}" \
  &&  echo "[INFO] Installing: ${dependencies[*]}" \
  &&  copy "${envPackageJsonFile}" "${out}/package.json" \
  &&  pushd "${out}" \
    &&  HOME=. npm install --force \
    &&  HOME=. npm audit \
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
