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
    WIRE_GITLAB_BOT_CERT

  # Create secret for TLS communication
  replace_env_vars services/wire-gitlab-bot/secret.yaml
  kubectl apply -f services/wire-gitlab-bot/secret.yaml

  # Create service
  kubectl apply -f services/wire-gitlab-bot/service.yaml

  # Create deployment
  kubectl apply -f services/wire-gitlab-bot/deployment.yaml

  # Create ingress rule
  kubectl apply -f services/wire-gitlab-bot/ingress.yaml
}
