# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

echo "Executing architecture check phase" \
  && lint-imports --config "arch.cfg" \
  && echo "Finished architecture check phase"