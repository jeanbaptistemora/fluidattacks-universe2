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

# Import functions
. <(curl -s https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/sops.sh)
. toolbox/others.sh

stage="${1:-test}"

# Set envars

aws_login

aws eks update-kubeconfig --name FluidServes --region us-east-1
kubectl config set-context "$(kubectl config current-context)" --namespace serves

sops_env secrets-prod.yaml default \
  ONELOGIN_SSO \
  ONELOGIN_FINANCE_SSO \
  HELM_KEY \
  HELM_CERT \
  HELM_CA \
  TF_VAR_dbName \
  TF_VAR_dbPass \
  TF_VAR_dbSnapId \
  TF_VAR_dbUser \
  TF_VAR_engineVersion \
  FLUIDATTACKS_TLS_CERT \
  FLUID_TLS_KEY \
  FA_RUNNER_TOKEN \
  FS_RUNNER_TOKEN \
  AUTONOMIC_TLS_CERT \
  AUTONOMIC_TLS_KEY \
  NRIA_LICENSE_KEY \
  TILLER_CERT \
  TILLER_KEY

# Run Terraform Plan for IAM, AWS EKS, RDS and VPC infrastructure
cd infrastructure/
echo "$ONELOGIN_SSO" | base64 -d > SSO.xml
echo "$ONELOGIN_FINANCE_SSO" | base64 -d > SSOFinance.xml
terraform init --backend-config="bucket=servestf"
tflint
terraform plan -refresh=true

if [ "$stage" == "deployment" ]; then
  mkdir -p "$(helm home)"
  echo "$HELM_KEY" | base64 -d > "$(helm home)"/key.pem
  echo "$HELM_CERT" | base64 -d > "$(helm home)"/cert.pem
  echo "$HELM_CA" | base64 -d > "$(helm home)"/ca.pem
  VAULT_KMS_KEY=$(terraform output vaultKmsKey)
  export VAULT_KMS_KEY
  eks/manifests/deploy.sh
fi

# Run Terraform Plan for AWS DNS infrastructure
{
  echo 'fiS3Arn = '"$(aws iam list-users | jq '.Users[].Arn' | \
    grep -E 'integrates-prod' | head -n 1)"
  terraform output dbEndpoint
  terraform output fwBucket
  terraform output fiBucket
} >> dns/terraform.tfvars

cd dns/
get_nginx_elb
terraform init --backend-config="bucket=servestf"
tflint
terraform plan -refresh=true
cd ../
