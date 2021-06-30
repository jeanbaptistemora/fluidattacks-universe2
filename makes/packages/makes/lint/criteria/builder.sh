# shellcheck shell=bash

function main {
  local paths=(
    requirements
    vulnerabilities
  )

  for path in "${paths[@]}"
  do
    echo "[INFO] Evaluating ${path}" \
      && ajv compile -s "${envSrc}/${path}/schema.json" \
      && ajv validate \
           -s "${envSrc}/${path}/schema.json" \
           -d "${envSrc}/${path}/data.yaml" \
      || return 1
  done \
    && touch "${out}"
}

main "${@}"
