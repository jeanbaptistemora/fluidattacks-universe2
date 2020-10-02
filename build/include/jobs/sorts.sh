# shellcheck shell=bash

function job_sorts_lint {
  local args_mypy=(
    --config-file 'settings.cfg'
  )
  local args_prospector=(
    # Some day when sorts has https://readthedocs.org
    # --doc-warnings
    --full-pep8
    --strictness veryhigh
    --test-warnings
  )

      helper_sorts_install_dependencies \
  &&  pushd sorts \
    &&  echo '[INFO] Checking static typing' \
    &&  poetry run mypy "${args_mypy[@]}" sorts/ \
    &&  poetry run mypy "${args_mypy[@]}" test/ \
    &&  echo "[INFO] Linting" \
    &&  poetry run prospector "${args_prospector[@]}" sorts/ \
    &&  poetry run prospector "${args_prospector[@]}" test/ \
  &&  popd \
  ||  return 1
}
