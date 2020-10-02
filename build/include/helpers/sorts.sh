# shellcheck shell=bash

function helper_sorts_install_dependencies {
  export PYTHONPATH="${PWD}/sorts/.venv/lib64/python3.8/site-packages:${PYTHONPATH}"

  # If the lock does not exist
  if ! test -e sorts/poetry.lock
  then
          helper_common_poetry_install_deps sorts
  fi
}
