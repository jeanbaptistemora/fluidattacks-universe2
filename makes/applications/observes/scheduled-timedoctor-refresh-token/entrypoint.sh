# shellcheck shell=bash

function refresh_token {
  export analytics_auth_timedoctor

      aws_login_prod 'observes' \
  &&  analytics_auth_timedoctor=$( \
        get_project_variable \
          "${GITLAB_API_TOKEN}" \
          "${CI_PROJECT_ID}" \
          "analytics_auth_timedoctor"
      ) \
  &&  echo '[INFO] Updating token...' \
  &&  observes-service-timedoctor-tokens --timedoctor-refresh \
  &&  echo '[INFO] Done! Token created for current project'
}

refresh_token
