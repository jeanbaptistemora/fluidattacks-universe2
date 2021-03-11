# shellcheck shell=bash

source '__envUtilsBashLibAws__'
source '__envUtilsBashLibSops__'
source '__envUtilsBashLibGit__'

export PATH="__envCodeEtlBin__:${PATH:-}"

function job_code_amend_authors {
  export GITLAB_API_USER
  export GITLAB_API_TOKEN

      aws_login_prod 'observes' \
  &&  sops_export_vars 'observes/secrets-prod.yaml' \
        'REDSHIFT_DATABASE' \
        'REDSHIFT_HOST' \
        'REDSHIFT_PASSWORD' \
        'REDSHIFT_PORT' \
        'REDSHIFT_USER' \
  &&  use_git_repo_services \
    &&  code-etl amend-authors \
          '.groups-mailmap' \
  &&  popd \
  ||  return 1
}

job_code_amend_authors "${@}"
