# shellcheck shell=bash

# Back

function job_integrates_back_lint {
  export PYTHONPATH="${PWD}/integrates/back/packages/modules:${PYTHONPATH}"
  export PYTHONPATH="${PWD}/makes/packages/makes/python/safe-pickle/src:${PYTHONPATH}"
  export PYTHONPATH="${PWD}/skims/skims/sdk:${PYTHONPATH}"

      pushd integrates \
  &&  env_prepare_python_packages \
  &&  mypy \
        --strict \
        --allow-untyped-decorators \
        --ignore-missing-imports \
        --follow-imports=skip \
        --config-file back/.mypylintignore \
  &&  bandit -r --ini .bandit \
  &&  prospector -F -s veryhigh back \
  &&  prospector -F -s veryhigh lambda \
  &&  prospector -F -s veryhigh deploy/permissions-matrix \
  &&  npx graphql-schema-linter \
        --except 'enum-values-have-descriptions,fields-are-camel-cased,fields-have-descriptions,input-object-values-are-camel-cased,relay-page-info-spec,types-have-descriptions,arguments-have-descriptions' \
        back/packages/modules/api/schema/**/*.graphql \
        back/packages/modules/api/schema/types/**/*.graphql \
  &&  popd \
  || return 1
}
