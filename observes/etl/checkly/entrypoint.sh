# shellcheck shell=bash

function start_etl {
  local db_creds
  local state_dir
  local state_file

  db_creds=$(mktemp) \
    && state_dir=$(mktemp -d) \
    && state_folder="s3://observes.state/checkly_etl" \
    && state_file="universe.json" \
    && aws_login "prod_observes" "3600" \
    && echo '[INFO] Generating secret files' \
    && redshift_env_vars \
    && json_db_creds "${db_creds}" \
    && sops_export_vars 'observes/secrets/prod.yaml' \
      checkly_api_user \
      checkly_api_key \
      bugsnag_notifier_key \
    && echo '[INFO] Getting state' \
    && aws_s3_sync "${state_folder}" "${state_dir}" --exclude "*" --include "${state_file}" \
    && echo '[INFO] Running tap' \
    && tap-checkly stream \
      --api-user "${checkly_api_user}" \
      --api-key "${checkly_api_key}" \
      --state "${state_dir}/${state_file}" \
      --all-streams \
      > .singer \
    && echo '[INFO] Running target' \
    && target-redshift destroy-and-upload \
      --schema-name 'checkly' \
      --s3-state "${state_folder}/${state_file}" \
      --persistent-tables "check_results,check_results_api,check_results_browser,check_results_browser_pages" \
      < .singer \
    && success-indicators single-job \
      --job 'checkly' \
    && rm .singer
}

start_etl
