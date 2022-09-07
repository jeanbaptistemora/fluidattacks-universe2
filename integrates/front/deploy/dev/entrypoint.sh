# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function main {
  export CI_COMMIT_REF_NAME

  : \
    && if test -z "${CI_COMMIT_REF_NAME:-}"; then
      CI_COMMIT_REF_NAME="$(get_abbrev_rev . HEAD)"
    fi \
    && deploy dev development "${CI_COMMIT_REF_NAME}"
}

main "${@}"
