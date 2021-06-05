# shellcheck shell=bash

function job_code_amend_authors {

  aws_login_prod 'observes' \
    && sops_export_vars 'observes/secrets-prod.yaml' \
      'REDSHIFT_DATABASE' \
      'REDSHIFT_HOST' \
      'REDSHIFT_PASSWORD' \
      'REDSHIFT_PORT' \
      'REDSHIFT_USER' \
    && use_git_repo_services \
    && observes-bin-code-etl amend-authors \
      '.groups-mailmap' \
    && popd \
    || return 1
}

job_code_amend_authors "${@}"
