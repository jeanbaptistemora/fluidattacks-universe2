# shellcheck shell=bash

function main {
  export CI_COMMIT_REF_NAME

  if test '__argShouldMock__' == '1'; then
    sops_export_vars __argSecretsFile__ "INTEGRATES_API_TOKEN" \
      && integrates-mock '__argDbData__'
  fi \
    && CI_COMMIT_REF_NAME="$(get_abbrev_rev "${PWD}" HEAD)"
}

main "${@}"
