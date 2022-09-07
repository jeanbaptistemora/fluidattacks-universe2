# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function main {
  local group="${1:-}"
  export CI='true'
  export CI_COMMIT_REF_NAME='trunk'

  : \
    && shopt -s nullglob \
    && ensure_gitlab_env_vars \
      INTEGRATES_API_TOKEN \
    && use_git_repo_services \
    && for root in "${@:2}"; do
      echo "[INFO] cloning ${root} from ${group}" \
        && { USER=nobody melts resources --clone-from-customer-git "${group}" --name "${root}" || true; }
    done \
    && USER=nobody melts drills --push-repos "${group}"
}

main "${@}"
