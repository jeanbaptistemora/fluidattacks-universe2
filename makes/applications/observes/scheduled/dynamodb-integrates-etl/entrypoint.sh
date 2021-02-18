# shellcheck shell=bash

function get_tables {
  local tables_path="${1}"
  local target="${2}"

    jq -r ".tables[]" < "${tables_path}" > "${target}"
}

function dynamodb_etl {
  local tables_path

      tables_file=$(mktemp) \
  &&  tables_path="./observes/conf/awsdynamodb.json" \
  &&  get_tables "${tables_path}" "${tables_file}" \
  &&  while read -r table
      do
            echo "[INFO] Submitting: ${table}"
            if test "${table,,}" = "fi_vulnerabilities"
            then
                  aws-batch-dynamodb-etl-big "${table}" ||  return 1
            else
                  aws-batch-dynamodb-etl "${table}" ||  return 1
            fi
      done < "${tables_file}"
}

dynamodb_etl
