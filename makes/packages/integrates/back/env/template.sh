# shellcheck shell=bash

function main {
  local env="${1:-}"
  local api_status="${2:-}"

  true \
    && case "${env}" in
      dev) aws_login_dev 'integrates' ;;
      dev-mobile) aws_login_dev 'integrates' ;;
      eph) aws_login_dev 'integrates' ;;
      prod) aws_login_prod 'integrates' ;;
      prod-local) aws_login_prod 'integrates' ;;
      *) abort '[ERROR] First argument must be one of: dev, dev-mobile, eph, prod, prod-local' ;;
    esac \
    && case "${env}" in
      dev) sops_export_vars __envSecretsDev__ "${INTEGRATES_SECRETS_LIST[@]}" ;;
      dev-mobile) sops_export_vars __envSecretsDev__ "${INTEGRATES_SECRETS_LIST[@]}" ;;
      eph) sops_export_vars __envSecretsDev__ "${INTEGRATES_SECRETS_LIST[@]}" ;;
      prod) sops_export_vars __envSecretsProd__ "${INTEGRATES_SECRETS_LIST[@]}" ;;
      prod-local) sops_export_vars __envSecretsProd__ "${INTEGRATES_SECRETS_LIST[@]}" \
        && export DEBUG=True \
        && export REDIS_SERVER=localhost ;;
      *) abort '[ERROR] First argument must be one of: dev, dev-mobile, eph, prod, prod-lcoal' ;;
    esac \
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
