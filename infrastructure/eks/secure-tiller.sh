#!/bin/bash
set -e

# Import encryption data to PEM files
echo "$CA_CERT" | base64 -d > ca-cert.pem
echo "$TILLER_KEY" | base64 -d > tiller-key.pem
echo "$TILLER_CERT" | base64 -d > tiller-cert.pem

# Initialize Tiller server with secure configuration
helm init \
  --tiller-tls \
  --tiller-tls-verify \
  --tiller-tls-cert=tiller-cert.pem \
  --tiller-tls-key=tiller-key.pem \
  --tls-ca-cert=ca-cert.pem \
  --service-account="$1" \

rm *.pem

echo "$HELM_KEY" | base64 -d > $(helm home)/key.pem
echo "$HELM_CERT" | base64 -d > $(helm home)/cert.pem
echo "$CA_CERT" | base64 -d > $(helm home)/ca.pem

sleep 60

kubectl -n kube-system patch deployment tiller-deploy -p '{"spec": {"template": {"spec": {"automountServiceAccountToken": true}}}}'
