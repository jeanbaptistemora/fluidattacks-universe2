#!/usr/bin/env bash
set -e

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

# Run Terraform Plan for AWS DNS infrastructure
terraform output fiS3Arn >> dns/terraform.tfvars
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
