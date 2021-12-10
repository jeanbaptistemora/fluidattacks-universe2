# shellcheck shell=bash

function main {
  mkdir -p "${out}" \
    && graphql-schema-linter \
      --except 'fields-are-camel-cased,input-object-values-are-camel-cased,defined-types-are-used,relay-page-info-spec' \
      "${envIntegratesApiSchema}/**/*.graphql" \
      "${envIntegratesApiSchema}/types/**/*.graphql"
}

main "${@}"
