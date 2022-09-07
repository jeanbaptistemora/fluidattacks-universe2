# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

alias tap-announcekit="observes-singer-tap-announcekit-bin"
alias tap-json="observes-singer-tap-json-bin"
alias target-redshift="observes-target-redshift"

function start_etl {
  : \
    && aws_login "dev" "3600" \
    && sops_export_vars 'observes/secrets-dev.yaml' \
      announcekit_user \
      announcekit_passwd \
      announcekit_proj \
    && export ANNOUNCEKIT_USER="${announcekit_user}" \
    && export ANNOUNCEKIT_PASSWD="${announcekit_passwd}" \
    && echo '[INFO] Running tap' \
    && tap-announcekit stream 'ALL' \
      --project "${announcekit_proj}" \
      > .singer
}

start_etl
