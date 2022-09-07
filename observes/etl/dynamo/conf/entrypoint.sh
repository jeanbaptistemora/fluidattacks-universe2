# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

export DYNAMO_ETL_BIN=__argSendTableETL__
export DYNAMO_ETL_BIG_BIN=__argSendBigTableETL__
export DYNAMO_PARALLEL=__argSendParallelTableETL__
export DYNAMO_PREPARE=__argSendPrepare__

function execute {
  local selection="${1}"
  echo "[INFO] Executing job: ${selection}"
  dynamo-etl run "${selection}"
}

export_notifier_key \
  && execute "${@}"
