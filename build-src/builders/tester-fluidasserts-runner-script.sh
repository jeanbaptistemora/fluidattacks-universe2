#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell --pure
#!   nix-shell --cores 0
#!   nix-shell --max-jobs auto
#!   nix-shell --attr testFluidassertsAll
#!   nix-shell --keep fluidassertsModule
#!   nix-shell --keep AWS_ACCESS_KEY_ID
#!   nix-shell --keep AWS_SECRET_ACCESS_KEY
#!   nix-shell --keep AZURE_CLIENT_ID
#!   nix-shell --keep AZURE_CLIENT_SECRET
#!   nix-shell --keep AZURE_SUBSCRIPTION_ID
#!   nix-shell --keep AZURE_TENANT_ID
#!   nix-shell --keep GOOGLE_APPLICATION_CREDENTIALS_CONTENT
#!   nix-shell --keep KUBERNETES_API_SERVER
#!   nix-shell --keep KUBERNETES_API_TOKEN
#!   nix-shell --keep WEBBOT_GMAIL_PASS
#!   nix-shell --keep WEBBOT_GMAIL_USER
#!   nix-shell ./build-src/main.nix
#  shellcheck shell=bash

source "${genericShellOptions}"

PATH="${pyPkgFluidasserts}/site-packages/bin:${PATH}"
PATH="${pyPkgGroupTest}/site-packages/bin:${PATH}"
PYTHONPATH="${PYTHONPATH}:${pyPkgFluidasserts}/site-packages"
PYTHONPATH="${PYTHONPATH}:${pyPkgGroupTest}/site-packages"

function commands_pre {
  pytest \
      --no-cov \
      --capture=no \
      -m prepare \
      --asserts-module "${fluidassertsModule}" \
    test/test_others_prepare.py
}

function commands {
  pytest \
    --cov-branch \
    --asserts-module "${fluidassertsModule}" \
    --random-order-bucket=global
}

function commands_post {
  pytest \
      --no-cov \
      --capture=no \
      -m teardown \
      --asserts-module "${fluidassertsModule}" \
    test/test_others_teardown.py
}

commands_pre
commands
commands_post
