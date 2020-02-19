#!/usr/bin/env bash

check_wednesday() {

  # Check if it is wednesday

  local DAY_NAME

  DAY_NAME="$(date +%A)"

  if [ "$DAY_NAME" == 'Wednesday' ]; then
    return 0
  else
    return 1
  fi
}

issue_review_certificate() {

  # Renew ssl certificate of ephemeral apps

  set -Eeuo pipefail

  if check_wednesday; then

    # Import functions
    . ci-scripts/helpers/sops.sh

    local CERT_CONFIG
    local ISSUER
    local CERTIFICATE
    local SECRET
    local RA_ACCESS_KEY
    local K8S_CONTEXT
    local ENV_NAME

    ENV_NAME='development'
    aws_login "$ENV_NAME"

    K8S_CONTEXT="$(kubectl config current-context)"
    CERT_CONFIG='review-apps/tls.yaml'
    ISSUER='letsencrypt'
    SECRET='ssl-certificate'
    CERTIFICATE='ssl-review-apps'
    RA_ACCESS_KEY="$AWS_ACCESS_KEY_ID"

    kubectl config set-context "$K8S_CONTEXT" --namespace="$CI_PROJECT_NAME"

    # Remove current cert data
    kubectl delete secret "${SECRET}"
    kubectl delete issuer "${ISSUER}"
    kubectl delete certificate "${CERTIFICATE}"

    sed -i "s/\$RA_ACCESS_KEY/$RA_ACCESS_KEY/g" "$CERT_CONFIG"
    sed -i "s/\$CI_PROJECT_NAME/$CI_PROJECT_NAME/g" "$CERT_CONFIG"
    sed -i "s/\$DNS_ZONE_ID/$DNS_ZONE_ID/g" "$CERT_CONFIG"

    kubectl apply -f "${CERT_CONFIG}"
    while ! kubectl describe certificate "${CERTIFICATE}" | tr -s ' ' | grep 'Status: True'; do
      echo "Issuing certificate..."
      sleep 10
    done

    rm review-apps/tls.yaml
  fi
}

issue_review_certificate
