# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function observes_generic_test {
  local srcPath="${1}"
  local testDir="${2}"

  echo "[INFO] Testing python package: ${srcPath}" \
    && pushd "${srcPath}" \
    && USER=nobody python -m pytest \
      -p no:cacheprovider \
      --full-trace "${testDir}" \
    && popd \
    && if test "${out+x}"; then
      touch "${out}"
    fi
}
