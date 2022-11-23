# shellcheck shell=bash

function main {
  export TF_VAR_projects

  source __argIntegratesBackEnv__/template "prod" \
    && groups_file="$(mktemp)" \
    && python '__argScriptGroups__' "${groups_file}" \
    && TF_VAR_projects="$(cat "${groups_file}")"
}

main "${@}"
