# shellcheck shell=bash

function main {
  mkdir -p "${out}" \
    && graphql-schema-linter \
      --except 'relay-page-info-spec' \
      "${envIntegratesApiSchema}/**/*.graphql" \
      "${envIntegratesApiSchema}/types/**/*.graphql"
}

main "${@}"
