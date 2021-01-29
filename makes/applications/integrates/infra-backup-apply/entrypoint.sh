# shellcheck shell=bash

source '__envUtilsAws__'
source '__envUtilsSops__'

function main {
      aws_login_prod integrates \
  &&  sops_export_vars 'integrates/secrets-production.yaml' 'default' \
        DB_USER \
        DB_PASSWD \
  &&  TF_VAR_db_user="${DB_USER}" \
      TF_VAR_db_password="${DB_PASSWD}" \
      '__envTerraformApply__'
}

main "${@}"
