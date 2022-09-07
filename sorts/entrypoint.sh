# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

: \
  && aws_login "prod_sorts" "3600" \
  && sops_export_vars 'sorts/secrets.yaml' \
    'MIXPANEL_API_TOKEN_SORTS' \
    'REDSHIFT_DATABASE' \
    'REDSHIFT_HOST' \
    'REDSHIFT_PASSWORD' \
    'REDSHIFT_PORT' \
    'REDSHIFT_USER'
sorts "${@}"
