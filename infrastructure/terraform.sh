#!/usr/bin/env bash

get_nginx_elb() {

  # Get nginx elb name and zone for production

  local ELBS_INFO
  local JQ_QUERY
  local ELBS_NAMES
  local TAGS

  # Terraform vars
  export TF_VAR_elbDns
  export TF_VAR_elbZone

  ELBS_INFO='/tmp/elbs-info.tmp'
  JQ_QUERY='.TagDescriptions[0].Tags[] | select(.Key == "kubernetes.io/cluster/FluidServes")'

  # Get load balancers info
  aws elb --region us-east-1 describe-load-balancers > "$ELBS_INFO"

  # Get load balancers names
  ELBS_NAMES=$(jq -r '.LoadBalancerDescriptions[].LoadBalancerName' "$ELBS_INFO")

  # Iterate over all the available elbs in order to know which one belongs
  # to production nginx.
  # When found, set required envars and return 0
  for NAME in $ELBS_NAMES; do
    TAGS="/tmp/tags-$NAME.tmp"
    aws elb --region us-east-1 describe-tags --load-balancer-names "$NAME" > "$TAGS"
    if jq -e "$JQ_QUERY" "$TAGS" &> /dev/null; then
      TF_VAR_elbDns=$(jq -r ".LoadBalancerDescriptions[] \
        | select(.LoadBalancerName == \"$NAME\") \
        | .DNSName" "$ELBS_INFO")
      TF_VAR_elbZone=$(jq -r ".LoadBalancerDescriptions[] \
        | select(.LoadBalancerName == \"$NAME\") \
        | .CanonicalHostedZoneNameID" "$ELBS_INFO")
      return 0
    fi
  done

  echo "Error: No nginx production load balancer was found."
  return 1

}

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

# Set up asserts projects variable
. infrastructure/helpers.sh
set_subscriptions_terraform_variable

# Run Terraform Plan for IAM, AWS EKS, RDS and VPC infrastructure
cd infrastructure/
export TF_VAR_aws_access_key="$AWS_ACCESS_KEY_ID"
export TF_VAR_aws_secret_key="$AWS_SECRET_ACCESS_KEY"
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

# Run Terraform Plan for AWS DNS infrastructure
echo 'fiS3Arn = '"$(aws iam list-users | jq '.Users[].Arn' | \
  egrep 'integrates-s3' | head -n 1)" >> dns/terraform.tfvars
terraform output dbEndpoint >> dns/terraform.tfvars
terraform output fwBucket >> dns/terraform.tfvars
terraform output fiBucket >> dns/terraform.tfvars

cd dns/
get_nginx_elb
terraform init --backend-config="bucket=${FS_S3_BUCKET_NAME}"
tflint
terraform plan -refresh=true
cd ../
