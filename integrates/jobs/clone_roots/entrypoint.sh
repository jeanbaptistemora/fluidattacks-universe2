# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function main {
  : \
    && source __argPythonEnv__/template \
    && aws_login "prod_integrates" "3600" \
    && ensure_gitlab_env_vars \
      INTEGRATES_API_TOKEN \
    && python3 __argScript__ "${@}"
}

main "${@}"
