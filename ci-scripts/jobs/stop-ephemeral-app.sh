#!/usr/bin/env bash

stop_ephemeral_app() {

  # Stop ephemeral application
  # of a specific branch

  set -e

  # Set integrates namespace
  kubectl config set-context \
    "$(kubectl config current-context)" \
    --namespace="${CI_PROJECT_NAME}"

  # Delete deployment, service and ingress.
  kubectl delete deployment "review-${CI_COMMIT_REF_SLUG}"
  kubectl delete service "service-${CI_COMMIT_REF_SLUG}"
  kubectl delete ingress "review-${CI_COMMIT_REF_SLUG}"
  kubectl delete deployment "review-async-${CI_COMMIT_REF_SLUG}"
  kubectl delete service "service-async-${CI_COMMIT_REF_SLUG}"
}

stop_ephemeral_app
