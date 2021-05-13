# shellcheck shell=bash

function lint_python_package {
  # If you do `import XXX` in your python code and the structure is like this:
  #   /path/to/XXX
  #   /path/to/XXX/__init__.py
  #   /path/to/XXX/business_code.py
  # then package_path is /path/to/XXX
  local package_path="${1}"

  local current_python_dir
  local python_dirs
  local python_dir

      package_name="$(basename "${1#*-}")" \
  &&  echo "[INFO] Running mypy over: ${package_path}, package ${package_name}" \
  &&  if ! test -e "${package_path}/py.typed"
      then
            echo '[ERROR] This is not a mypy package (py.typed missing)' \
        &&  return 1
      fi \
  &&  tmpdir="$(mktemp -d)" \
  &&  copy "${package_path}" "${tmpdir}/${package_name}" \
  &&  pushd "${tmpdir}" \
    &&  mypy --config-file '__envSettingsMypy__' "${package_name}" \
    &&  python_dirs=() \
    &&  current_python_dir="" \
    &&  find . -name '*.py' > tmp \
    &&  while IFS= read -r python_file
        do
              python_dir="$(dirname "${python_file}")" \
          &&  if [ ! "${python_dir}" == "${current_python_dir}" ] && [ ! -f "${python_dir}/__init__.py" ]
              then
                    python_dirs+=( "${python_dir}" )
              fi \
          &&  current_python_dir="${python_dir}" \
          ||  return 1
        done < tmp \
    &&  for dir in "${python_dirs[@]}"
        do
              echo "[INFO] Running mypy over: ${package_path}, folder ${dir}" \
          &&  mypy --config-file '__envSettingsMypy__' "${dir}" \
          ||  return 1
        done \
  &&  popd \
  &&  echo "[INFO] Running prospector over: ${package_path}, package ${package_name}" \
  &&  if ! test -e "${package_path}/__init__.py"
      then
            echo '[ERROR] This is not a python package, a package has __init__.py' \
        &&  return 1
      fi \
  &&  pushd "${tmpdir}" \
    &&  prospector --profile '__envSettingsProspector__' "${package_name}" \
  &&  popd \
  ||  return 1
}

function lint_python_imports {
  local config="${1}"
  # If you do `import XXX` in your python code and the structure is like this:
  #   /path/to/XXX
  #   /path/to/XXX/__init__.py
  #   /path/to/XXX/business_code.py
  # Then site-packages path is /path/to
  local site_packages_path="${2}"

      pushd "${site_packages_path}" \
    &&  python '__envSettingsImports__' "${site_packages_path}" "${config}" \
    &&  lint-imports --config "${config}" \
  &&  popd \
  ||  return 1
}
