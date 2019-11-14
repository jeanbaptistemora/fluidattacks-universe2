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
    WIRE_GITLAB_BOT_KEY \
    WIRE_GITLAB_BOT_CERT \
    DW_GITLAB_BOT_BASE_URL \
    DW_GITLAB_BOT_WIRE_SERVICE_TOKEN

  # Create secret for TLS communication
  replace_env_vars services/wire-gitlab-bot/certificate.yaml
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
