# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash
export ANNOUNCEKIT_USER
export ANNOUNCEKIT_PASSWD

: \
  && aws_login "dev" "3600" \
  && sops_export_vars 'observes/secrets/dev.yaml' \
    "announcekit_user" \
    "announcekit_passwd" \
  && ANNOUNCEKIT_USER="${announcekit_user}" \
  && ANNOUNCEKIT_PASSWD="${announcekit_passwd}" \
  && observes_generic_test "__argEnvSrc__" "__argEnvTestDir__"
