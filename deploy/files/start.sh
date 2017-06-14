#!/bin/bash

echo "Starting FLUIDIntegrates"
INTEGRATES_PATH="/usr/src/app"
exec python ${INTEGRATES_PATH}/manage.py runsslserver 0.0.0.0:8000 --certificate ${INTEGRATES_PATH}/config/fluidla.crt --key ${INTEGRATES_PATH}/config/fluidla.key
