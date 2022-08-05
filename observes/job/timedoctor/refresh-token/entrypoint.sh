# shellcheck shell=bash
alias timedoc-tokens="observes-service-timedoctor-tokens-bin"

function refresh_token {
  export analytics_auth_timedoctor
  local db_creds

  db_creds=$(mktemp) \
    && sops_export_vars 'observes/secrets/prod.yaml' \
      bugsnag_notifier_key \
    && echo '[INFO] Generating secret files' \
    && json_db_creds "${db_creds}" \
    && analytics_auth_timedoctor=$(
      get_project_variable \
        "${UNIVERSE_API_TOKEN}" \
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
