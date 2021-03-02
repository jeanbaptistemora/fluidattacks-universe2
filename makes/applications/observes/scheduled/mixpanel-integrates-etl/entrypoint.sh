# shellcheck shell=bash

function job_mixpanel_integrates {
  local conf="${1}"
  local db_creds
  local mixpanel_creds

      db_creds=$(mktemp) \
  &&  mixpanel_creds=$(mktemp) \
  &&  aws_login_prod 'observes' \
  &&  sops_export_vars 'observes/secrets-prod.yaml' \
        mixpanel_integrates_api_secret \
        mixpanel_integrates_api_token \
        analytics_auth_redshift \
  &&  {
        echo '{'
        echo "\"API_secret\":\"${mixpanel_integrates_api_secret}\","
        echo "\"token\":\"${mixpanel_integrates_api_token}\""
        echo '}'
      } > "${mixpanel_creds}" \
  &&  echo '[INFO] Starting mixpanel ETL' \
  &&  echo "${analytics_auth_redshift}" > "${db_creds}" \
  &&  echo '[INFO] Running tap' \
  &&  observes-tap-mixpanel -a "${mixpanel_creds}" -c "${conf}" | observes-tap-json \
        > .singer \
  &&  observes-target-redshift \
        --auth "${db_creds}" \
        --drop-schema \
        --schema-name "mixpanel_integrates" \
        < .singer \
  &&  observes-update-sync-date single-job \
          --auth "${db_creds}" \
          --job 'mixpanel_integrates'
}

job_mixpanel_integrates "./observes/conf/mixpanel_integrates.json"
