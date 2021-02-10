# shellcheck shell=bash

source "${envBashLibCommon}"

function get_deps_from_lock {
  jq -r '.dependencies | to_entries[] | .key + "@" + .value.version' < "${1}" \
    | sort
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
    &&  { HOME=. npm audit || true; } \
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
  &&  shopt -s nullglob \
  &&  for bin in "${out}"/node_modules/**/{bin,src}/*
      do
            if test -f "${bin}"
            then
              sed -i "s|#!/usr/bin/env node|#!${envNode}/bin/node|g" "${bin}"
            fi \
        ||  return 1
      done \
  ||  return 1
}

main "${@}"
