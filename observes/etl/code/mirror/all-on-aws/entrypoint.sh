# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function job_code_mirror_all_groups {
  local groups_file
  export AWS_DEFAULT_REGION="us-east-1"

  groups_file=$(mktemp)

  list_groups "${groups_file}" \
    && while read -r group; do
      echo "[INFO] Submitting: ${group}" \
        && __argCodeEtlMirror__ "${group}" \
        || return 1
    done < "${groups_file}"
}

job_code_mirror_all_groups
