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
          "${GITLAB_API_TOKEN}" \
          "${CI_PROJECT_ID}" \
          "analytics_auth_timedoctor"
      ) \
  &&  echo '[INFO] Updating token...' \
  &&  observes-service-timedoctor-tokens --timedoctor-refresh \
  &&  echo '[INFO] Done! Token created for current project' \
  &&  observes-update-sync-date "timedoctor_refresh_token" \
        --auth-file "${db_creds}"
}

refresh_token
