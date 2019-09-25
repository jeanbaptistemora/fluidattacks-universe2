#!/usr/bin/env bash

install_chart() {

  # Install or update helm chart

  set -e

  local CHART="$1"
  local NAME="$2"
  local NAMESPACE="$3"
  local VALUES="$4"
  local VERSION="$5"

  # Import functions
  . toolbox/others.sh

  # Replace envars in provided values file
  replace_env_vars "$VALUES"

  # Upgrade chart if already installed or just install it
  if helm list --tls | grep -q "$NAME"; then
    echo-blue "Upgrading $CHART"
    helm upgrade "$NAME" "$CHART" \
      --values "$VALUES" \
      --version "$VERSION" \
      --wait \
      --tls
  else
    echo-blue "Installing chart $CHART..."
    helm install "$CHART" \
      --name "$NAME" \
      --namespace "$NAMESPACE" \
      --values "$VALUES" \
      --version "$VERSION" \
      --wait \
      --tls
  fi
}
