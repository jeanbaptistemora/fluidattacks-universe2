# shellcheck shell=bash

source '__envUtilsBashLibAws__'
source '__envUtilsBashLibSops__'

function job_mixpanel_integrates {
  local conf="${1}"
  local db_creds
  local mixpanel_creds

  local tap_json
  local tap_mixpanel
  local target_redshift

  tap_json="__envTapJson__" \
  &&  tap_mixpanel="__envTapMixpanel__" \
  &&  target_redshift="__envTargetRedshift__" \
  &&  update_sync_date="__envUpdateSyncDate__" \
  &&  db_creds=$(mktemp) \
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
  &&  "${tap_mixpanel}" -a "${mixpanel_creds}" -c "${conf}" | "${tap_json}" \
        > .singer \
  &&  "${target_redshift}" \
        --auth "${db_creds}" \
        --drop-schema \
        --schema-name "mixpanel_integrates" \
        < .singer \
  &&  "${update_sync_date}" mixpanel-integrates "${db_creds}"
}

job_mixpanel_integrates "./observes/conf/mixpanel_integrates.json"
