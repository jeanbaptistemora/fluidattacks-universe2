# shellcheck shell=bash

function main {

  mkdir -p "${out}" \
    && copy "${envNodeRequirements}/node_modules" "${out}/node_modules" \
    && pushd "${out}" \
    && npx --no-install graphql-schema-linter \
      --except 'fields-are-camel-cased,input-object-values-are-camel-cased,relay-page-info-spec' \
      "${envIntegratesApiSchema}/**/*.graphql" \
      "${envIntegratesApiSchema}/types/**/*.graphql" \
    && popd \
    || return 1
}

main "${@}"
