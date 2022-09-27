# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

# This is a temporary script, used to unify all integrates' buckets into one
function main {
  local bucket_moving="${1}"
  local main_bucket
  main_bucket="s3://integrates"

  aws_login "prod_integrates" "3600" \
    && echo "[INFO] Syncing data from: ${main_bucket}.${bucket_moving} to ${main_bucket}/${bucket_moving}" \
    && aws_s3_sync "${main_bucket}.${bucket_moving}" "${main_bucket}/${bucket_moving}" \
    || return 1
}

main "${@}"
