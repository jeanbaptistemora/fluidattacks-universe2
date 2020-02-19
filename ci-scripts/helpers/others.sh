#!/usr/bin/env bash

deploy_integrates() {
  local integrates_id='4620828'

  . toolbox/others.sh
  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/sops.sh)

      aws_login \
  &&  sops_env secrets-prod.yaml default INTEGRATES_PIPELINE_TOKEN \
  &&  curl \
        -X POST \
        -F token="${INTEGRATES_PIPELINE_TOKEN}" \
        -F ref=master \
        "https://gitlab.com/api/v4/projects/${integrates_id}/trigger/pipeline"
}
