# shellcheck shell=bash

function main {
  local env="${1:-}"

  true \
    && case "${env}" in
      dev) aws_login_dev_new ;;
      dev-mobile) aws_login_dev_new ;;
      eph) aws_login_dev_new ;;
      prod) aws_login_prod 'integrates' ;;
      prod-local) aws_login_prod 'integrates' ;;
      *) abort '[ERROR] First argument must be one of: dev, dev-mobile, eph, prod, prod-local' ;;
    esac \
    && case "${env}" in
      dev) sops_export_vars __argSecretsDev__ "${INTEGRATES_SECRETS_LIST[@]}" ;;
      dev-mobile) sops_export_vars __argSecretsDev__ "${INTEGRATES_SECRETS_LIST[@]}" ;;
      eph) sops_export_vars __argSecretsDev__ "${INTEGRATES_SECRETS_LIST[@]}" ;;
      prod) sops_export_vars __argSecretsProd__ "${INTEGRATES_SECRETS_LIST[@]}" ;;
      prod-local) sops_export_vars __argSecretsProd__ "${INTEGRATES_SECRETS_LIST[@]}" \
        && export DEBUG=True \
        && export REDIS_SERVER=localhost ;;
      *) abort '[ERROR] First argument must be one of: dev, dev-mobile, eph, prod, prod-lcoal' ;;
    esac \
    && export CI_COMMIT_REF_NAME \
    && export CI_COMMIT_SHA \
    && export MACHINE_QUEUES='__argManifestQueues__' \
    && export MACHINE_FINDINGS='__argManifestFindings__' \
    && export INTEGRATES_DB_MODEL_PATH='__argIntegrates__/arch/database-design.json' \
    && export INTEGRATES_CHARTS_LOGO_PATH='__argIntegrates__/back/src/reports/resources/themes/logo.png' \
    && export INTEGRATES_MAILER_TEMPLATES='__argIntegrates__/back/src/mailer/email_templates' \
    && export STARTDIR="${PWD}" \
    && export TZ=UTC \
    && if test -z "${CI_COMMIT_REF_NAME:-}"; then
      # Local environments specific
      CI_COMMIT_REF_NAME="$(get_abbrev_rev . HEAD)"
    fi \
    && if test -z "${CI_COMMIT_SHA:-}"; then
      # Local environments specific
      CI_COMMIT_SHA="$(get_commit_from_rev . HEAD)"
    fi \
    && if ! test -e 'integrates'; then
      # Kubernetes specific
      mkdir 'integrates' \
        && copy '__argIntegrates__' 'integrates'
    fi
}

main "${@}"
