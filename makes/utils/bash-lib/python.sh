# shellcheck shell=bash

function make_python_path {
  for element in "${@}"
  do
        echo "[INFO] Exporting to PYTHONPATH: ${element}" \
    &&  export PYTHONPATH="${element}:${PYTHONPATH:-}" \
    &&  export PATH="${element}/bin:${PATH:-}" \
    ||  return 1
  done
}
