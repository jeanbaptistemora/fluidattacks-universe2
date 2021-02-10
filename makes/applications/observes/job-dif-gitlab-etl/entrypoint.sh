# shellcheck shell=bash

source '__envUtilsBashLibAws__'
source '__envUtilsBashLibSops__'


function job_gitlab_etl {
  local dif_gitlab_etl

  local db_creds
  local projects
  dif_gitlab_etl="__envDifGitlabEtl__" \
  &&  projects=(
        'autonomicmind/default'
        'autonomicmind/challenges'
        'fluidattacks/services'
        'fluidattacks/product'
      ) \
  &&  db_creds=$(mktemp) \
  &&  aws_login_prod 'observes' \
  &&  sops_export_vars 'observes/secrets-prod.yaml' \
        analytics_auth_redshift \
  &&  echo '[INFO] Generating secret files' \
  &&  echo "${analytics_auth_redshift}" > "${db_creds}" \
  &&  "${dif_gitlab_etl}" start-etl "${projects[@]}" "${db_creds}"
}

job_gitlab_etl
