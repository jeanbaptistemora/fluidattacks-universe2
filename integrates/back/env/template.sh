# shellcheck shell=bash

function main {
  local env="${1:-}"

  : \
    && case "${env}" in
      dev) aws_login_dev ;;
      eph) : ;;
      prod) : ;;
      prod-local) aws_login_prod 'integrates' ;;
      *) error 'First argument must be one of: dev, eph, prod, prod-local' ;;
    esac \
    && case "${env}" in
      dev) sops_export_vars __argSecretsDev__ "${INTEGRATES_SECRETS_LIST[@]}" ;;
      eph) sops_export_vars __argSecretsDev__ "${INTEGRATES_SECRETS_LIST[@]}" ;;
      prod) sops_export_vars __argSecretsProd__ "${INTEGRATES_SECRETS_LIST[@]}" ;;
      prod-local) sops_export_vars __argSecretsProd__ "${INTEGRATES_SECRETS_LIST[@]}" \
        && export DEBUG=True \
        && export REDIS_SERVER=localhost ;;
      *) error 'First argument must be one of: dev, eph, prod, prod-local' ;;
    esac \
    && export CI_COMMIT_REF_NAME \
    && export CI_COMMIT_SHA \
    && export MACHINE_QUEUES='__argManifestQueues__' \
    && export MACHINE_FINDINGS='__argManifestFindings__' \
    && export INTEGRATES_DB_MODEL_PATH='__argIntegrates__/arch/database-design.json' \
    && export INTEGRATES_REPORTS_LOGO_PATH='__argIntegrates__/back/src/reports/resources/themes/background.png' \
    && export INTEGRATES_MAILER_TEMPLATES='__argIntegrates__/back/src/mailer/email_templates' \
    && export INTEGRATES_CRITERIA_REQUIREMENTS='__argCriteriaRequirements__' \
    && export INTEGRATES_CRITERIA_VULNERABILITIES='__argCriteriaVulnerabilities__' \
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
