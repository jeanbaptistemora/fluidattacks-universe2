# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function main {
  export DATA
  export TF_VAR_sizes
  export TF_VAR_schedules

  # Environment
  export CI_PROJECT_ID="20741933"

  # Secrets
  export CACHIX_AUTH_TOKEN
  export UNIVERSE_API_TOKEN

  DATA="$(cat "__argSchedules__")" \
    && TF_VAR_schedules="$(python "__argParser__")" \
    && TF_VAR_sizes="$(yq -rec "." "__argSizes__")"
}

main "${@}"
