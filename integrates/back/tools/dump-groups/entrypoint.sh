# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function main {
  export TF_VAR_projects

  source __argIntegratesBackEnv__/template "prod" \
    && groups_file="$(mktemp)" \
    && python '__argScriptGroups__' "${groups_file}" \
    && TF_VAR_projects="$(cat "${groups_file}")"
}

main "${@}"
