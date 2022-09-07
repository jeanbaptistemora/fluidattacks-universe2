# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function from_epoch_to_iso8601 {
  local epoch="${1}"

  date --date "@${epoch}" --iso-8601=seconds --utc
}

function from_iso8601_to_epoch {
  local iso8601="${1}"

  date --date "${iso8601}" +%s
}
