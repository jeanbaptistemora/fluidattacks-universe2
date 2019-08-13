#!/usr/bin/env bash

set -e

curl -o terraform.zip https://releases.hashicorp.com/terraform/0.12.6/terraform_0.12.6_linux_amd64.zip
unzip terraform.zip
rm terraform.zip
mv terraform /usr/local/bin/terraform

curl -Lo tflint.zip https://github.com/wata727/tflint/releases/download/v0.9.3/tflint_linux_amd64.zip
unzip tflint.zip
rm tflint.zip
install tflint /usr/local/bin/

stage="${1:-test}"

# Run Terraform Plan for IAM, AWS EKS, RDS and VPC infrastructure
cd infrastructure/
export TF_VAR_aws_access_key="$AWS_ACCESS_KEY_ID"
export TF_VAR_aws_secret_key="$AWS_SECRET_KEY_ID"
echo "$ONELOGIN_SSO" | base64 -d > SSO.xml
echo "$ONELOGIN_FINANCE_SSO" | base64 -d > SSOFinance.xml
terraform init --backend-config="bucket=${FS_S3_BUCKET_NAME}"
tflint
terraform plan -refresh=true

if [ "$stage" == "deployment" ]; then
  mkdir -p $(helm home)
  echo "$HELM_KEY" | base64 -d > $(helm home)/key.pem
  echo "$HELM_CERT" | base64 -d > $(helm home)/cert.pem
  echo "$HELM_CA" | base64 -d > $(helm home)/ca.pem
  VAULT_KMS_KEY=$(terraform output vaultKmsKey)
  export VAULT_KMS_KEY
  eks/manifests/deploy.sh
  if [ -n "${NEW_DEPLOY}" ]; then
    git clone https://github.com/checkr/s3-sync.git;
  fi
  if [ -n "${NEW_DEPLOY}" ]; then
    create-config.sh && cd s3-sync
    go run main.go sync --config ./config-prod.yaml;
  fi
fi

#Run Terraform Plan for Staging infrastructure
cd staging/
export AWS_INNOVATION_ACCESS_KEY_ID="$TF_VAR_aws_innovation_access_key"
export AWS_INNOVATION_SECRET_KEY_ID="$TF_VAR_aws_innovation_secret_key"
terraform init --backend-config="bucket=${FS_S3_BUCKET_NAME}"
tflint
terraform plan -refresh=true
terraform output dbDevEndpoint >> ../dns/terraform.tfvars
cd ../

# Run Terraform Plan for AWS DNS infrastructure
echo 'fiS3Arn = '"$(aws iam list-users | jq '.Users[].Arn' | \
  egrep 'integrates-s3' | head -n 1)" >> dns/terraform.tfvars
terraform output dbEndpoint >> dns/terraform.tfvars
terraform output fwBucket >> dns/terraform.tfvars
terraform output fiBucket >> dns/terraform.tfvars

cd dns/
export TF_VAR_elbDns="$(aws elb --region us-east-1 \
  describe-load-balancers | \
  jq -r '.LoadBalancerDescriptions[].DNSName')"
export TF_VAR_elbZone="$(aws elb --region us-east-1 \
  describe-load-balancers | \
  jq -r '.LoadBalancerDescriptions[].CanonicalHostedZoneNameID')"
terraform init --backend-config="bucket=${FS_S3_BUCKET_NAME}"
tflint
terraform plan -refresh=true
cd ../
