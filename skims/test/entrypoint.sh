# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function main {
  local RANDOM_DIR
  local success=true
  source __argExtraSrcs__/template extra_srcs

  RANDOM_DIR="$(mktemp -d)" \
    && pushd "${RANDOM_DIR}" \
    && copy __argProject__ __project__ \
    && for extra_src in "${!extra_srcs[@]}"; do
      copy "${extra_srcs[$extra_src]}" "${extra_src}"
    done \
    && pushd __project__/skims \
    && aws_login "dev" "3600" \
    && if ! pytest \
      --cov= \
      --cov-branch \
      --cov-report=term \
      --reruns=1 \
      --skims-test-group=__argCategory__ \
      --capture=tee-sys \
      --disable-pytest-warnings \
      --durations=10 \
      --exitfirst \
      --showlocals \
      --show-capture=no \
      -vvv; then
      success=false
    fi \
    && popd \
    && popd \
    && copy "${RANDOM_DIR}/__project__/skims/.coverage" skims/.coverage.__argCategory__ \
    && if test "${success}" = false; then
      copy "${STATE}" .
      return 1
    fi
}

main "${@}"
