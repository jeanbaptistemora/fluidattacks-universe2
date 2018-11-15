#!/usr/bin/env bash
set -e

stage="${1:-test}"

# Run Terraform Plan for AWS EKS, RDS and VPC infrastructure
cd infrastructure/
export TF_VAR_aws_access_key="$AWS_ACCESS_KEY_ID"
export TF_VAR_aws_secret_key="$AWS_SECRET_KEY_ID"
echo "$ONELOGIN_SSO" | base64 -d > SSO.xml
echo "$ONELOGIN_FINANCE_SSO" | base64 -d > SSOFinance.xml
terraform init
tflint --deep --aws-access-key="$AWS_ACCESS_KEY_ID" \
  --aws-secret-key="$AWS_SECRET_KEY_ID" --aws-region='us-east-1'
terraform refresh > /dev/null
terraform plan

if [ "$stage" == "deployment" ]; then
  mkdir -p $(helm home)
  echo "$HELM_KEY" | base64 -d > $(helm home)/key.pem
  echo "$HELM_CERT" | base64 -d > $(helm home)/cert.pem
  echo "$HELM_CA" | base64 -d > $(helm home)/ca.pem
  eks/manifests/deploy.sh
  cd vault/
  ./vault.sh
  cd ../
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
terraform init
tflint --deep --aws-access-key="$AWS_INNOVATION_ACCESS_KEY_ID" \
  --aws-secret-key="$AWS_INNOVATION_SECRET_KEY_ID" --aws-region='us-east-1'
terraform refresh > /dev/null
terraform plan
terraform output dbDevEndpoint >> ../dns/terraform.tfvars
cd ../

# Run Terraform Plan for AWS DNS infrastructure
echo 'fiS3Arn = '"$(aws iam list-users | jq '.Users[].Arn' | \
  egrep 'integrates-s3')" >> dns/terraform.tfvars
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
terraform init
tflint --deep --aws-access-key="$AWS_ACCESS_KEY_ID" \
  --aws-secret-key="$AWS_SECRET_KEY_ID" --aws-region='us-east-1'
terraform refresh > /dev/null
terraform plan
