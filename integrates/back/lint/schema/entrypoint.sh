# shellcheck shell=bash

function main {
  local schema_path="integrates/back/src/api/**/*.graphql"

  graphql-schema-linter \
    --except 'relay-page-info-spec' \
    "${schema_path}" \
    && export CI_COMMIT_REF_NAME \
    && if test -z "${CI_COMMIT_REF_NAME:-}"; then
      CI_COMMIT_REF_NAME="$(get_abbrev_rev . HEAD)"
    fi \
    && git fetch origin trunk \
    && graphql-inspector diff \
      "git:origin/trunk:${schema_path}" \
      "git:origin/${CI_COMMIT_REF_NAME}:${schema_path}" \
      --rule suppressRemovalOfDeprecatedField
}

main "${@}"
