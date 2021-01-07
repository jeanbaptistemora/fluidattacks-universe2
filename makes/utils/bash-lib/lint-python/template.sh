# shellcheck shell=bash

source '__envUtilsBashLibPython__'

function lint_python {
  local path="${1}"

      make_python_path '3.8' \
        '__envPythonRequirements__' \
  &&  pkg_dir="$(__envDirname__ "${path}")" \
  &&  pkg_name="$(__envBasename__ "${path}")" \
  &&  echo "[INFO] Running mypy over: ${path}" \
  &&  pushd "${pkg_dir}" \
    &&  mypy \
          --config-file '__envSettingsMypy__' \
          "${pkg_name}" \
  &&  popd \
  &&  echo "[INFO] Running prospector over: ${pkg}" \
  &&  prospector \
        --full-pep8 \
        --profile '__envSettingsProspector__' \
        --test-warnings \
        "${path}" \
  ||  return 1
}
