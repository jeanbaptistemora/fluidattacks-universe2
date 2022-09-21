# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

echo "Executing functional tests" \
  && pytest --version \
  && pytest --pyargs target_snowflake ./tests_functional \
  && echo "Finished test phase"
