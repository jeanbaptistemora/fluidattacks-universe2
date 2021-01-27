# shellcheck shell=bash

source '__envBashLibCommon__'
source '__envSearchPaths__'

function setup_integrates_development_front {
      mkdir -p "${out}/node_modules" \
  &&  copy "__envNodeRequirements__/node_modules" "${out}/node_modules"
}

setup_integrates_development_front
