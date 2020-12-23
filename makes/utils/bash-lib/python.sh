# shellcheck shell=bash

function make_python_path {
  version="${1}"

  for element in "${@:1}"
  do
        echo "[INFO] Exporting python${version} paths: ${element}" \
    &&  export PYTHONPATH="${element}/lib/python${version}/site-packages:${PYTHONPATH:-}" \
    &&  export PATH="${element}/bin:${PATH:-}" \
    ||  return 1
  done
}

function make_python_path_plain {
  for element in "${@}"
  do
        echo "[INFO] Exporting python paths: ${element}" \
    &&  export PYTHONPATH="${element}:${PYTHONPATH:-}" \
    ||  return 1
  done
}
