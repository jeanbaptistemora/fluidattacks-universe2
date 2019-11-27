#!/usr/bin/env bash
#
# Lambda package builder

build_lambda() {
    set -x
    LAMBDA_FUNCTION=$1
    CURR_PATH=${PWD}/lambda

    python3 -m venv ${CURR_PATH}/${LAMBDA_FUNCTION}-venv
    cd ${CURR_PATH}/${LAMBDA_FUNCTION}-venv
    source bin/activate
    pip3 install -U setuptools==41.4.0 wheel==0.33.6
    if [[ -f ${CURR_PATH}/${LAMBDA_FUNCTION}/requirements.txt ]]; then
        pip3 install -r ${CURR_PATH}/${LAMBDA_FUNCTION}/requirements.txt
    fi
    deactivate
    cd ${CURR_PATH}/${LAMBDA_FUNCTION}-venv/lib/python3.7/site-packages/
    zip -r9 /tmp/${LAMBDA_FUNCTION}.zip .
    cd ${CURR_PATH}/${LAMBDA_FUNCTION}
    zip -g /tmp/${LAMBDA_FUNCTION}.zip lambda_${LAMBDA_FUNCTION}.py
    mv /tmp/${LAMBDA_FUNCTION}.zip ${CURR_PATH}/packages/
    cd ${CURR_PATH}

}

build_lambda send_mail_new_vulnerabilities