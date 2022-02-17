# shellcheck shell=bash

export DYNAMO_ETL_BIN=__argSendTableETL__
export DYNAMO_ETL_BIG_BIN=__argSendBigTableETL__

function execute {
  local selection="${1}"
  import="from dynamo_etl_conf.jobs import Jobs;"
  echo "[INFO] Executing job: ${selection}"
  case "${selection}" in
    FORCES)
      python -c "${import} Jobs().forces().compute()"
      ;;
    CORE)
      python -c "${import} Jobs().core().compute()"
      ;;
    GROUP)
      python -c "${import} Jobs().standard_group().compute()"
      ;;
    *)
      echo "[ERROR] Invalid job selection" && return 1
      ;;
  esac
}

execute "${@}"
