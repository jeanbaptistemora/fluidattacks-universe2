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
  local options=("${2}")
  local files
  local files_array
  local args=(
    --copyright="Fluid Attacks <development@fluidattacks.com>"
    --license="MPL-2.0"
    --copyright-style spdx
  )

  files_array="$(mktemp)"
  echo "${input}" \
    | sed "s| *$||g" \
    | tr " " "\n" \
      > "${files_array}"
  while read -r line; do
    reuse addheader "${args[@]}" "${options[@]}" "${line}"
  done < "${files_array}" \
    && echo "[INFO] Formatted files successfully!"
}

function add_headers {
  local files
  local files_array
  files="$(get_files)"

  echo '[INFO] Adding License and Copyright headers to files' \
    && if [[ ${files} == "" ]]; then
      echo "[INFO] Nothing to format here! All files are licensed"
    fi \
    && if [[ ${files} == *"airs/front/content"* ]] || [[ ${files} == *"docs/src/docs"* ]]; then
      files_array="$(echo "${files}" | grep ".md")" \
        && add_custom_license "${files_array}" "--force-dot-license" \
        && files_array="$(echo "${files}" | grep -E "airs/front/content|docs/src/docs" | grep -v ".md")" \
        && add_custom_license "${files_array}" "--force-dot-license"
    fi \
    && if [[ ${files} == *".yaml"* ]] || [[ ${files} == *".yml"* ]]; then
      files_array="$(echo "${files}" | grep -E ".yaml|.yml")" \
        && add_custom_license "${files_array}" "--force-dot-license"
    fi \
    && if [[ ${files} == *".yml"* ]]; then
      files_array="$(echo "${files}" | grep ".yml")" \
        && add_custom_license "${files_array}" "--force-dot-license"
    fi \
    && if [[ ${files} == *".ts"* ]] || [[ ${files} == *".js"* ]]; then
      files_array="$(echo "${files}" | grep -E ".ts|.js")" \
        && add_custom_license "${files_array}" "--multi-line"
    fi \
    && if add_custom_license "${files}" "--skip-existing" &> /dev/null; then
      echo "[INFO] Formatted files successfully!"
    else
      if [[ ${files} == *".cfg"* ]] || [[ ${files} == *".tf"* ]] || [[ ${files} == *".rb"* ]] || [[ ${files} == *".toml"* ]]; then
        files_array="$(echo "${files}" | grep -E ".cfg|.tf|.rb|.toml")" \
          && add_custom_license "${files_array}" "--style=python"
      else
        echo "[CRITICAL] there are some unrecognised extensions, please follow the template in the docs https://docs.fluidattacks.com/development/licencing-and-copyright#license-and-copyright-headers" \
          && exit 1 || exit 1
      fi
    fi

}

function main {

  if reuse lint; then
    echo "[INFO] Nothing to format here! All files are licensed"
  else
    add_headers \
      && echo "[WARNING] Some files are missing licensing information. When this command fails it adds the propper licensing notices to the files that need it, please commit those changes." \
      && exit 1 || exit 1
  fi \
    || return 1
}

main "${@}"
