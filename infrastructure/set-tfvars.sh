#!/usr/bin/env bash

echo 'ciIP = "'"$RUNNER_IP"'"'                > vars/aws.tfvars
echo 'db_user = "'"$DB_USER"'"'               >> vars/aws.tfvars
echo 'db_pass = "'"$DB_PASS"'"'               >> vars/aws.tfvars
echo 'db_name = "'"$DB_NAME"'"'               >> vars/aws.tfvars
echo 'engine_ver = "'"$ENGINE_VER"'"'         >> vars/aws.tfvars
echo 'acc_key = "'"$AWS_ACCESS_KEY_ID"'"'     >> vars/aws.tfvars
echo 'sec_key = "'"$AWS_SECRET_ACCESS_KEY"'"' >> vars/aws.tfvars

echo 'bucket = "'"$FS_S3_BUCKET_NAME"'"'    >> terraform.tfvars
echo 'webBucket = "'"$FW_S3_BUCKET_NAME"'"' >> terraform.tfvars
echo 'fiBucket = "'"$FI_S3_BUCKET_NAME"'"'  >> terraform.tfvars
echo 'db_id = "'"$SNAP_ID"'"'               >> terraform.tfvars

echo "$SSO_XML" > vars/SSO.xml
echo "$SSO_FINANCE_XML" > vars/SSOFinance.xml

echo "$FI_SSH_KEY" | base64 -d > vars/FLUID_Serves.pem

mkdir -p $(helm home)
echo "$HELM_KEY" | base64 -d > $(helm home)/key.pem
echo "$HELM_CERT" | base64 -d > $(helm home)/cert.pem
echo "$CA_CERT" | base64 -d > $(helm home)/ca.pem
