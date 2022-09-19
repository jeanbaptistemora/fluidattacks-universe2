# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

echo "Executing type check phase" \
  && mypy --version \
  && mypy . --config-file ./mypy.ini \
  && echo "Finished type check phase"
