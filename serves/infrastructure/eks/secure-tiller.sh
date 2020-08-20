#!/usr/bin/env bash
set -e

# Check service account was passed as an argument to deploy Tiller
# with RBAC
if [ -z "$1" ]; then
  echo "No service account provided to deploy Tiller"
  exit 1
fi
SERVICE_ACCOUNT="$1"

# Check that all the variables used in the script are defined
vars=("HELM_CA"
"TILLER_KEY"
"TILLER_CERT")
for var in "${vars[@]}"; do
  if [ -z "${!var}" ]; then
    echo "Variable $var is not defined"
    exit 1
  fi
done


# Prepare Tiller certificates for TLS communications between the Helm Client
# and the Tiller server in the cluster
echo "$HELM_CA" | base64 -d > ca-cert.pem
echo "$TILLER_KEY" | base64 -d > tiller-key.pem
echo "$TILLER_CERT" | base64 -d > tiller-cert.pem

# Initialize Tiller server with secure configuration
helm init \
  --tiller-tls \
  --tiller-tls-cert=tiller-cert.pem \
  --tiller-tls-key=tiller-key.pem \
  --tls-ca-cert=ca-cert.pem \
  --service-account="$SERVICE_ACCOUNT"

# Wait until the Tiller Pod is ready
kubectl rollout status -n kube-system deploy tiller-deploy -w

rm tiller*.pem ca*.pem

# Add the Service Account Token to the Tiller Pod to allow communications
# with the Helm Client using the proper permissions
kubectl -n kube-system patch deployment tiller-deploy \
 -p '{"spec": {"template": {"spec": {"automountServiceAccountToken": true}}}}'

sleep 10
