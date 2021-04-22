# shellcheck shell=bash

function refresh_token {
  export analytics_auth_timedoctor
  local db_creds

      db_creds=$(mktemp) \
  &&  aws_login_prod 'observes' \
  &&  sops_export_vars 'observes/secrets-prod.yaml' \
        analytics_auth_redshift \
  &&  echo '[INFO] Generating secret files' \
  &&  echo "${analytics_auth_redshift}" > "${db_creds}" \
  &&  analytics_auth_timedoctor=$( \
        get_project_variable \
          "${PRODUCT_API_TOKEN}" \
          "${CI_PROJECT_ID}" \
          "analytics_auth_timedoctor"
      ) \
  &&  echo '[INFO] Updating token...' \
  &&  observes-bin-service-timedoctor-tokens --timedoctor-refresh \
  &&  echo '[INFO] Done! Token created for current project' \
  &&  observes-bin-service-job-last-success single-job \
        --auth "${db_creds}" \
        --job 'timedoctor_refresh_token'
}

refresh_token
