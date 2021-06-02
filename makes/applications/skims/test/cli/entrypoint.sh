# shellcheck shell=bash

function assert {
  if "${@}"
  then
        echo "[INFO] Successfully run: ${*}" \
    &&  return 0
  else
        echo "[ERROR] While running: ${*}" \
    &&  return 1
  fi
}

function main {
  local output

      output="$(mktemp)" \
  &&  assert skims expected-code-date --group continuoustest --finding-code F117 |& tee "${output}" \
    &&  assert grep -HnP '^(0|1622\d+)$' "${output}" \
    &&  assert grep -HnP 'Success' "${output}" \
  &&  assert skims language --group continuoustest |& tee "${output}" \
    &&  assert grep -HnP '^EN$' "${output}" \
    &&  assert grep -HnP 'Success' "${output}" \

}

main "${@}"
