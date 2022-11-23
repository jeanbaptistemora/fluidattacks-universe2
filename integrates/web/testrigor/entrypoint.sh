# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function main {
  : \
    && sops_export_vars __argSecretsDev__ \
      JWT_ENCRYPTION_KEY \
      JWT_SECRET \
      TEST_E2E_USER_1 \
      TESTRIGOR_AUTH_TOKEN \
      TESTRIGOR_SUITE_ID \
    && pushd integrates/web/testrigor \
    && python3 execute.py \
    && popd \
    || return 1
}

main "${@}"
