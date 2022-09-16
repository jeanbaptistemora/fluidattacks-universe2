# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

alias gitlab-etl="observes-etl-gitlab"

function start_etl {
  local db_creds

  db_creds=$(mktemp) \
    && aws_login "prod_observes" "3600" \
    && json_db_creds "${db_creds}" \
    && export_notifier_key \
    && gitlab-etl \
      'gitlab-ci' \
      '20741933' \
      's3://observes.state/gitlab_etl/product_state.json' \
      "${UNIVERSE_API_TOKEN}" \
      "${db_creds}"
}

start_etl
