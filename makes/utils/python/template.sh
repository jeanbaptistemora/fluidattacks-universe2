# shellcheck shell=bash

function make_python_path {
  local version="${1}"

  for element in "${@:2}"
  do
        export PYTHONPATH="${element}/lib/python${version}/site-packages:${PYTHONPATH:-}" \
    &&  export PATH="${element}/bin:${PATH:-}" \
    ||  return 1
  done
}

function make_python_path_plain {
  for element in "${@}"
  do
        export PYTHONPATH="${element}:${PYTHONPATH:-}" \
    ||  return 1
  done
}
