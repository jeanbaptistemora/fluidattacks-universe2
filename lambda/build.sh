#!/usr/bin/env bash
#
# Lambda package builder
LAMBDA_FUNCTION=$1
CURR_PATH=${PWD}

python3 -m venv ${LAMBDA_FUNCTION}-venv
cd ${LAMBDA_FUNCTION}-venv
source bin/activate
pip3 install -U setuptools==41.4.0 wheel==0.33.6
if [[ -f ${CURR_PATH}/${LAMBDA_FUNCTION}/requirements.txt ]]; then
    pip3 install -r ${CURR_PATH}/${LAMBDA_FUNCTION}/requirements.txt
fi
cd lib/python3.7/site-packages/
zip -r9 ${CURR_PATH}/packages/${LAMBDA_FUNCTION}.zip .
cd ${CURR_PATH}/${LAMBDA_FUNCTION}
zip -g ../packages/${LAMBDA_FUNCTION}.zip lambda_${LAMBDA_FUNCTION}.py
cd ${CURR_PATH}
deactivate
