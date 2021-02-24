# shellcheck shell=bash

# Back

function job_integrates_back_lint {
      pushd integrates \
  &&  env_prepare_python_packages \
  &&  mypy --strict --ignore-missing-imports analytics/ \
        back/migrations/ \
        back \
  &&  mypy --strict --ignore-missing-imports --follow-imports=skip \
        back/packages/integrates-back/backend/decorators.py \
        back/packages/integrates-back/backend/api/ \
        back/packages/integrates-back/backend/authz/ \
        back/packages/integrates-back/backend/dal/ \
        back/packages/integrates-back/backend/utils/ \
  &&  mypy --ignore-missing-imports --follow-imports=skip \
        back/packages/integrates-back \
  &&  prospector -F -s veryhigh analytics/ \
  &&  prospector -F -s veryhigh back \
  &&  prospector -F -s veryhigh lambda \
  &&  prospector -F -s veryhigh deploy/permissions-matrix \
  &&  npx graphql-schema-linter \
        --except 'enum-values-have-descriptions,fields-are-camel-cased,fields-have-descriptions,input-object-values-are-camel-cased,relay-page-info-spec,types-have-descriptions,arguments-have-descriptions' \
        back/packages/integrates-back/backend/api/schema/**/*.graphql \
        back/packages/integrates-back/backend/api/schema/types/**/*.graphql \
  &&  popd \
  || return 1
}
