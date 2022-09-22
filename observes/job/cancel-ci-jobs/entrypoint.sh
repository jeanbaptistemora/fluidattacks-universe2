# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function cancel_jobs {
  local project="${1}"
  local token="${2}"
  local threshold="${3}"

  echo "[INFO] Cancelling jobs older than ${threshold}h for ${project}" \
    && tap-gitlab clean-stuck-jobs \
      --project "${project}" \
      --api-key "${token}" \
      --threshold "${threshold}"
}

cancel_jobs '20741933' "${UNIVERSE_API_TOKEN}" "8"
