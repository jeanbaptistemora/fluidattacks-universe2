# shellcheck shell=bash

source "${srcIncludeHelpersMelts}"
source "${srcEnv}"

function job_melts_lint_code {
      env_prepare_python_packages \
  &&  helper_test_lint_code_python
}

function job_melts_deploy {
  export TWINE_USERNAME='__token__'
  export TWINE_PASSWORD
  export PROD_AWS_ACCESS_KEY_ID="${MELTS_PROD_AWS_ACCESS_KEY_ID}"
  export PROD="${MELTS_PROD_AWS_SECRET_ACCESS_KEY}"
  export pyPkgMelts

  local nix_hash

  nix_hash=$(echo "${pyPkgMelts}" | grep -oP '(?<=/)[a-z0-9]{32}')

      helper_common_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_melts_aws_login prod \
  &&  TWINE_PASSWORD=${PYPI_TOKEN} \
  &&  pushd melts || return 1 \
  &&  (echo "nix_hash:${nix_hash}" &&  cat README.md) > README_B.md \
  &&  mv README_B.md README.md \
  &&  python3 setup.py sdist --formats=gztar \
  &&  twine check dist/* \
  &&  twine upload dist/* \
  &&  popd || return 1
}
