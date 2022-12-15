# shellcheck shell=bash

function main {
  local env="${1:-}"

  : \
    && case "${env}" in
      dev) aws_login "dev" "3600" ;;
      eph) : ;;
      prod) : ;;
      prod-local) aws_login "prod_integrates" "3600" ;;
      *) error 'First argument must be one of: dev, eph, prod, prod-local' ;;
    esac \
    && case "${env}" in
      dev)
        sops_export_vars __argSecretsDev__ "${INTEGRATES_SECRETS_LIST[@]}" \
          && export AWS_S3_PATH_PREFIX="${CI_COMMIT_REF_NAME}/"
        ;;
      eph)
        sops_export_vars __argSecretsDev__ "${INTEGRATES_SECRETS_LIST[@]}" \
          && export AWS_S3_PATH_PREFIX="${CI_COMMIT_REF_NAME}/"
        ;;
      prod) sops_export_vars __argSecretsProd__ "${INTEGRATES_SECRETS_LIST[@]}" ;;
      prod-local) sops_export_vars __argSecretsProd__ "${INTEGRATES_SECRETS_LIST[@]}" \
        && export DEBUG=True ;;
      *) error 'First argument must be one of: dev, eph, prod, prod-local' ;;
    esac \
    && export CI_COMMIT_REF_NAME \
    && export CI_COMMIT_SHA \
    && export MACHINE_QUEUES='__argManifestQueues__' \
    && export MACHINE_FINDINGS='__argManifestFindings__' \
    && export INTEGRATES_DB_MODEL_PATH='__argIntegrates__/arch/database-design.json' \
    && export INTEGRATES_REPORTS_LOGO_PATH='__argIntegrates__/back/src/reports/resources/themes/background.png' \
    && export INTEGRATES_MAILER_TEMPLATES='__argIntegrates__/back/src/mailer/email_templates' \
    && export INTEGRATES_CRITERIA_COMPLIANCE='__argCriteriaCompliance__' \
    && export INTEGRATES_CRITERIA_REQUIREMENTS='__argCriteriaRequirements__' \
    && export INTEGRATES_CRITERIA_VULNERABILITIES='__argCriteriaVulnerabilities__' \
    && export SKIMS_FLUID_WATERMARK='__argSrcSkimsStatic__/img/logo_fluid_attacks_854x329.png' \
    && export SKIMS_ROBOTO_FONT='__argSrcSkimsVendor__/fonts/roboto_mono_from_google/regular.ttf' \
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
