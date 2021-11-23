# shellcheck shell=bash
alias timedoc-tokens="observes-bin-service-timedoctor-tokens"
alias job-last-success="observes-bin-service-job-last-success"

function refresh_token {
  export analytics_auth_timedoctor
  local db_creds

  db_creds=$(mktemp) \
    && aws_login_prod 'observes' \
    && sops_export_vars 'observes/secrets-prod.yaml' \
      analytics_auth_redshift \
    && echo '[INFO] Generating secret files' \
    && echo "${analytics_auth_redshift}" > "${db_creds}" \
    && analytics_auth_timedoctor=$(
      get_project_variable \
        "${PRODUCT_API_TOKEN}" \
        "${CI_PROJECT_ID}" \
        "analytics_auth_timedoctor"
    ) \
    && echo '[INFO] Updating token...' \
    && timedoc-tokens update-token \
      --creds "${analytics_auth_timedoctor}" \
    && echo '[INFO] Done! Token created for current project' \
    && job-last-success single-job \
      --auth "${db_creds}" \
      --job 'timedoctor_refresh_token'
}

refresh_token
