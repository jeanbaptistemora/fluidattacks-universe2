# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function main {
  local coverage_target=55.00
  local coverage_args=(
    --skip-empty
    -i
  )

  : \
    && pushd skims \
    && coverage combine \
    && coverage report \
      --fail-under="${coverage_target}" \
      --precision=2 \
      "${coverage_args[@]}" \
    && coverage html "${coverage_args[@]}" -d build \
    && coverage xml "${coverage_args[@]}" \
    && if test "${CI_COMMIT_REF_NAME}" = trunk; then
      aws_login "dev" "3600" \
        && sops_export_vars __argSecretsDev__ CODECOV_TOKEN \
        && codecov -B skims -C "${CI_COMMIT_SHA}" -F skims
    fi \
    && popd \
    || return 1
}

main "${@}"
