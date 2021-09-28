# shellcheck shell=bash

function assert {
  if "${@}"; then
    info Successfully run: "${*}"
  else
    critical While running: "${*}"
  fi
}

function main {
  local output

  output="$(mktemp)" \
    && assert skims expected-code-date --finding-code F117 --group continuoustest --namespace services |& tee "${output}" \
    && assert grep -HnP '^(0|1622\d+)$' "${output}" \
    && assert grep -HnP 'Success' "${output}" \
    && assert skims language --group continuoustest |& tee "${output}" \
    && assert grep -HnP '^EN$' "${output}" \
    && assert grep -HnP 'Success' "${output}"
}

main "${@}"
