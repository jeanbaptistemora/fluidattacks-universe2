#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell --cores 0
#!   nix-shell --keep CI
#!   nix-shell --keep CI_COMMIT_REF_NAME
#!   nix-shell --keep CI_COMMIT_REF_SLUG
#!   nix-shell --keep CI_JOB_ID
#!   nix-shell --keep CI_NODE_INDEX
#!   nix-shell --keep CI_NODE_TOTAL
#!   nix-shell --keep CI_PROJECT_DIR
#!   nix-shell --keep CI_REGISTRY_USER
#!   nix-shell --keep CI_REGISTRY_PASSWORD
#!   nix-shell --keep DEV_AWS_ACCESS_KEY_ID
#!   nix-shell --keep DEV_AWS_SECRET_ACCESS_KEY
#!   nix-shell --keep GITLAB_TOKEN
#!   nix-shell --keep JWT_TOKEN
#!   nix-shell --keep KUBECONFIG
#!   nix-shell --keep KUBE_CA_PEM
#!   nix-shell --keep KUBE_CA_PEM_FILE
#!   nix-shell --keep KUBE_INGRESS_BASE_DOMAIN
#!   nix-shell --keep KUBE_NAMESPACE
#!   nix-shell --keep KUBE_TOKEN
#!   nix-shell --keep KUBE_URL
#!   nix-shell --keep PROD_AWS_ACCESS_KEY_ID
#!   nix-shell --keep PROD_AWS_SECRET_ACCESS_KEY
#!   nix-shell --max-jobs auto
#!   nix-shell --option restrict-eval false
#!   nix-shell --option sandbox false
#!   nix-shell --pure
#!   nix-shell --show-trace
#!   nix-shell shell.nix
#  shellcheck shell=bash

source "${srcIncludeGenericShellOptions}"
source "${srcIncludeCli}"

cli "${@}"
