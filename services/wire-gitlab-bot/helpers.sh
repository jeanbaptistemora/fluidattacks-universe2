#!/usr/bin/env bash

deploy_wire_gitlab_bot() {

  # Deploy wire-gitlab-bot instance

  # set -Eeuo pipefail

  # Import functions
  . <(curl -s https://gitlab.com/fluidattacks/default/raw/master/sops-source/sops.sh)
  . toolbox/others.sh

  # Set envars
  aws_login
  sops_env secrets-production.yaml default \
    DW_GITLAB_BOT_BASE_URL \
    DW_GITLAB_BOT_WIRE_SERVICE_TOKEN
  DW_GITLAB_BOT_BASE_URL="$(echo -n $DW_GITLAB_BOT_BASE_URL | base64)"
  DW_GITLAB_BOT_WIRE_SERVICE_TOKEN="$(echo -n $DW_GITLAB_BOT_WIRE_SERVICE_TOKEN | base64)"

  # Create secret for TLS communication
  kubectl apply -f services/wire-gitlab-bot/certificate.yaml

  # Create environment
  replace_env_vars services/wire-gitlab-bot/environment.yaml
  kubectl apply -f services/wire-gitlab-bot/environment.yaml

  # Create service
  kubectl apply -f services/wire-gitlab-bot/service.yaml

  # Create deployment
  kubectl apply -f services/wire-gitlab-bot/deployment.yaml

  # Create ingress rule
  kubectl apply -f services/wire-gitlab-bot/ingress.yaml
}
