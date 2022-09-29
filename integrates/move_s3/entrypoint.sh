# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

# This is a temporary script, used to unify all integrates' buckets into one
function main {
  local main_bucket
  main_bucket="s3://integrates"

  aws_login "prod_integrates" "3600" \
    && for item in "$@"; do
      echo "[INFO] Syncing data from: ${main_bucket}.${item} to ${main_bucket}/${item}" \
        && aws_s3_sync "s3://fluidintegrates.${item}" "${main_bucket}/${item}"
    done \
    || return 1
}

main "${@}"
