# shellcheck shell=bash

source '__envUtilsBashLibPython__'

function lint_python_module {
  # If you do `import XXX` in your python code and the structure is like this:
  #   /path/to/XXX
  #   /path/to/XXX/__init__.py
  #   /path/to/XXX/business_code.py
  # then module_path is /path/to/XXX
  local module_path="${1}"

      make_python_path '3.8' \
        '__envPythonRequirements__' \
  &&  module_name="$(basename "${1#*-}")" \
  &&  echo "[INFO] Running mypy over: ${module_path}, module ${module_name}" \
  &&  if ! test -e "${module_path}/py.typed"
      then
            echo '[ERROR] This is not a mypy module, a module has py.typed' \
        &&  return 1
      fi \
  &&  tmpdir="$(mktemp -d)" \
  &&  copy "${module_path}" "${tmpdir}/${module_name}" \
  &&  pushd "${tmpdir}" \
    &&  mypy --config-file '__envSettingsMypy__' "${module_name}" \
  &&  popd \
  &&  echo "[INFO] Running prospector over: ${module_path}, module ${module_name}" \
  &&  if ! test -e "${module_path}/__init__.py"
      then
            echo '[ERROR] This is not a python module, a module has __init__.py' \
        &&  return 1
      fi \
  &&  pushd "${tmpdir}" \
    &&  prospector --profile '__envSettingsProspector__' "${module_name}" \
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

      make_python_path '3.8' \
        '__envPythonRequirements__' \
  && pushd "${site_packages_path}" \
    &&  lint-imports --config "${config}" \
  &&  popd \
  ||  return 1
}
