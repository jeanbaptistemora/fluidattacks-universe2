# shellcheck shell=bash
function start_etl {
  local db_creds
  local analytics_zoho_tables=(
    Candidates
    Periods
  )

      db_creds=$(mktemp) \
  &&  aws_login_prod 'observes'  \
  &&  sops_export_vars 'observes/secrets-prod.yaml' \
        analytics_zoho_email \
        analytics_zoho_token \
        analytics_zoho_space \
        analytics_auth_redshift \
  &&  echo '[INFO] Generating secret files' \
  &&  echo "${analytics_auth_redshift}" > "${db_creds}" \
  &&  echo '[INFO] Running converter and streamer' \
  &&  for table in "${analytics_zoho_tables[@]}"
      do
            echo "  [INFO] Table: ${table}" \
        &&  observes-bin-tap-zoho-analytics \
              --email "${analytics_zoho_email}" \
              --token "${analytics_zoho_token}" \
              --space "${analytics_zoho_space}" \
              --table "${table}" \
              --target "${table}" \
              > .jsonstream \
        || return 1
      done \
  &&  echo '[INFO] Running tap' \
  &&  observes-tap-json  \
        --date-formats '%Y-%m-%d %H:%M:%S' \
        > .singer \
        < .jsonstream \
  &&  echo '[INFO] Running target' \
  &&  observes-target-redshift \
        --auth "${db_creds}" \
        --drop-schema \
        --schema-name 'zoho' \
        < .singer
}

start_etl
