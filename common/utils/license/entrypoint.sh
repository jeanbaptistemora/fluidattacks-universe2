# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function get_files {
  reuse lint \
    | awk '/# MISSING COPYRIGHT AND LICENSING INFORMATION/{f=1;next}/# SUMMARY/{f=0}f' \
    | grep '^\*' \
    | sed -E 's|^\* ||g' \
    || return 1
}

function add_custom_license {
  local input="${1}"
  local files
  local files_array
  local args=(
    --copyright="Fluid Attacks <development@fluidattacks.com>"
    --license="MPL-2.0"
    --copyright-style spdx
    --force-dot-license
  )

  files_array="$(mktemp)"
  echo "${input}" \
    | sed "s| *$||g" \
    | tr " " "\n" \
      > "${files_array}"
  while read -r line; do
    reuse addheader "${args[@]}" "${line}"
  done < "${files_array}" \
    && echo "[INFO] Formatted files successfully!" \
    || return 1
}

function add_headers {
  local files
  local files_array

  files="$(get_files)"
  echo '[INFO] Adding License and Copyright headers to files' \
    && if [[ ${files} == "" ]]; then
      echo "[INFO] Nothing to format here! All files are licensed"
    elif [[ ${files} == *"airs/front/content"* ]] || [[ ${files} == *"docs/src/docs"* ]]; then
      add_custom_license "${files}" ".md" \
        && files_array="$(echo "${files}" | grep -v ".md")" \
        && add_custom_license "${files_array}" "" \
        && exit 1 || exit 1
    elif [[ ${files} == *".yaml"* ]]; then
      files_array="$(echo "${files}" | grep ".yaml")" \
        && add_custom_license "${files_array}" ".yaml" \
        && exit 1 || exit 1
    elif [[ ${files} == *".yml"* ]]; then
      files_array="$(echo "${files}" | grep ".yml")" \
        && add_custom_license "${files}" ".yml" \
        && exit 1 || exit 1
    elif reuse addheader \
      --copyright="Fluid Attacks <development@fluidattacks.com>" \
      --license="MPL-2.0" \
      --copyright-style spdx \
      "${files}" &> /dev/null; then
      echo "[INFO] Formatted files successfully!" \
        && exit 1 || exit 1
    else
      echo "[CRITICAL] Unrecognized file extension, please follow the template in the docs https://docs.fluidattacks.com/development/licencing-and-copyright#license-and-copyright-headers" \
        && exit 1 || exit 1
    fi \
    || return 1
}

function main {

  if reuse lint; then
    echo "[INFO] Nothing to format here! All files are licensed"
  else
    add_headers
  fi \
    || return 1
}

main "${@}"
