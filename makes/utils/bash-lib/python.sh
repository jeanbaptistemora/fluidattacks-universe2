# shellcheck shell=bash

function make_python_path {
  for element in "${@}"
  do
        echo "[INFO] Exporting python paths: ${element}" \
    &&  export PYTHONPATH="${element}/lib/python3.8/site-packages:${PYTHONPATH:-}" \
    &&  export PATH="${element}/bin:${PATH:-}" \
    ||  return 1
  done
}
