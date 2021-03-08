# shellcheck shell=bash

function get_deps_from_lock {
  jq -r '.dependencies | to_entries[] | .key + "@" + .value.version' < "${1}" \
    | sort
}

function get_files_to_patch {
  local path="${1}"
  local regex="${2}"
  local file

      file="$(mktemp)" \
  &&  grep -lrP "${regex}" "${path}" > "${file}" \
  &&  echo "${file}"
}

# Use npm install with --force flag for packages that would fail to install
# due to OS/arch issues (fsevents), but removing them from the dependencies
# would install them anyway due to being an inherited dependency
# from another package, thus creating an Integrity Check error
function main {
  local dependencies
  local files_to_patch=()
  local shebang_regex='#!(\s*)/usr/bin/env(\s*)node'

      mkdir "${out}" \
  &&  echo "[INFO] Installing: ${dependencies[*]}" \
  &&  copy "${envPackageJsonFile}" "${out}/package.json" \
  &&  pushd "${out}" \
    &&  HOME=. npm install --force --ignore-scripts=false --verbose \
  &&  popd \
  &&  echo '[INFO] Freezing' \
  &&  get_deps_from_lock "${out}/package-lock.json" > "${out}/requirements" \
  &&  if test "$(cat "${out}/requirements")" = "$(cat "${envRequirementsFile}")"
      then
        echo '[INFO] Integrity check passed'
      else
            echo '[ERROR] Integrity check failed' \
        &&  echo '[INFO] The following dependencies are missing from your configuration file:' \
        &&  comm -1 -3 "${envRequirementsFile}" "${out}/requirements" \
        &&  return 1
      fi \
  &&  mapfile -t files_to_patch < "$(get_files_to_patch "${out}" "${shebang_regex}")" \
  &&  for file in "${files_to_patch[@]}"
      do
            sed -Ei "s|${shebang_regex}|#! $(command -v node)|g" "${file}" \
        ||  return 1
      done \
  ||  return 1
}

main "${@}"
