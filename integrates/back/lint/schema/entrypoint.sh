# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function main {
  local schema_path="integrates/back/src/api/schema/**/*.graphql"

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
