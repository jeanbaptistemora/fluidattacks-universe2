# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

echo "Executing functional tests setup" \
  && sops_export_vars '__argSecrets__' \
    snowflake_database \
    snowflake_admin_user \
    snowflake_admin_password \
    snowflake_account \
  && export SNOWFLAKE_DB="${snowflake_database}" \
  && export SNOWFLAKE_USER="${snowflake_admin_user}" \
  && export SNOWFLAKE_PASSWORD="${snowflake_admin_password}" \
  && export SNOWFLAKE_ACCOUNT="${snowflake_account}" \
  && echo "Executing functional tests" \
  && pytest --version \
  && pytest -p no:cacheprovider '__argFxTests__' \
  && echo "Finished test phase"
