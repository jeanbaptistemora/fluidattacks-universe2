# shellcheck shell=bash

export DYNAMO_ETL_BIN=__argSendTableETL__
export DYNAMO_ETL_BIG_BIN=__argSendBigTableETL__
export DYNAMO_PARALLEL=__argSendParallelTableETL__
export DYNAMO_PREPARE=__argSendPrepare__
export DYNAMO_DETERMINE_SCHEMA=__argDynamoSchema__

dynamo-etl "${@}"
