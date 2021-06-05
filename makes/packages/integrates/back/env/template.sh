# shellcheck shell=bash

function main {
  local env="${1:-}"
  local api_status="${2:-}"

  if test "${env}" == 'dev'; then
    aws_login_dev 'integrates' \
      && sops_export_vars __envSecretsDev__ "${INTEGRATES_SECRETS_LIST[@]}"
  elif test "${env}" == 'dev-mobile'; then
    aws_login_dev 'integrates' \
      && sops_export_vars __envSecretsDev__ "${INTEGRATES_SECRETS_LIST[@]}"
  elif test "${env}" == 'eph'; then
    aws_login_dev 'integrates' \
      && sops_export_vars __envSecretsDev__ "${INTEGRATES_SECRETS_LIST[@]}"
  elif test "${env}" == 'prod'; then
    aws_login_prod 'integrates' \
      && sops_export_vars __envSecretsProd__ "${INTEGRATES_SECRETS_LIST[@]}"
  else
    echo '[ERROR] First argument must be one of: dev, dev-mobile, eph, prod' \
      && return 1
  fi \
    && if ! { test "${api_status}" == '' || test "${api_status}" == 'migration'; }; then
      echo '[ERROR] Second argument must be one of: , migration' \
        && return 1
    fi \
    && export API_STATUS="${api_status}" \
    && export INTEGRATES_DB_MODEL_PATH='__envIntegrates__/arch/database-design.json' \
    && export INTEGRATES_CHARTS_LOGO_PATH='__envIntegrates__/back/src/reports/resources/themes/logo.png' \
    && export INTEGRATES_MAILER_TEMPLATES='__envIntegrates__/back/src/mailer/email_templates' \
    && export STARTDIR="${PWD}" \
    && if ! test -e 'integrates'; then
      # Kubernetes specific
      mkdir 'integrates' \
        && copy '__envIntegrates__' 'integrates'
    fi
}

main "${@}"
