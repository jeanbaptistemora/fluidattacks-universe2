# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function main {
  local ports=(
    3000 # front
    8001 # back
    8022 # dynamodb
    9000 # storage
    9200 # opensearch
  )

  kill_port "${ports[@]}"
}

main "${@}"
