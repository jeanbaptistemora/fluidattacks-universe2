# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function main {
  local data="__argData__"
  local endpoint

  : \
    && deploy-terraform-for-integratesStorageDev \
    && endpoint="${CI_COMMIT_REF_NAME}.integrates" \
    && aws_s3_sync \
      "${data}" \
      "s3://${endpoint}" \
      --delete \
    || return 1
}

main "${@}"
