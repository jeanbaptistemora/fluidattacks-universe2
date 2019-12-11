#!/usr/bin/env bash
#
# Lambda package builder

build_lambda() {
    LAMBDA_FUNCTION=$1
    OLD_PWD=${PWD}
    CURR_PATH=${OLD_PWD}/lambda

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
    zip -r -g /tmp/${LAMBDA_FUNCTION}.zip * 
    mv /tmp/${LAMBDA_FUNCTION}.zip ${CURR_PATH}/packages/
    cd ${OLD_PWD}

}

build_lambda send_mail_new_vulnerabilities
build_lambda project_to_pdf
