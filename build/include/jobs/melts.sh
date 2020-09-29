# shellcheck shell=bash

source "${srcIncludeHelpersMelts}"
source "${srcEnv}"

function job_melts_lint_code {
      env_prepare_python_packages \
  &&  helper_test_lint_code_python
}

function __clean_up {
  rm -rf melts/.pytest_cache
  git checkout -- "${STARTDIR}/services/groups/continuoustest"
}

function job_melts_test {
  export DEV_AWS_ACCESS_KEY_ID="${MELTS_DEV_AWS_ACCESS_KEY_ID}"
  export DEV_AWS_SECRET_ACCESS_KEY="${MELTS_DEV_AWS_SECRET_ACCESS_KEY}"
  # needed to do propper clean up
  # shellcheck disable=SC2015
      env_prepare_python_packages \
  &&  helper_melts_aws_login dev \
  &&  if [ "${IS_LOCAL_BUILD}" = 'true' ]
      then
          helper_start_localstack
      fi \
  &&  helper_use_pristine_workdir \
  &&  echo '[INFO] Cloning test repository' \
  &&  helper_clone_test_repo \
  &&  mv melts services \
  &&  pushd services \
  &&  echo '[INFO] Cloning continuoustest repository' \
  &&  melts drills --pull-repos continuoustest \
  &&  pushd melts \
  &&  pytest \
        --verbose \
        --exitfirst \
        --color=yes \
        --capture=fd \
        --durations=0 \
        --failed-first \
        --disable-warnings \
        --cov=toolbox \
        --cov-branch \
        --cov-report term \
        --cov-report html:.coverage-html \
        --no-cov-on-fail \
        --numprocesses=auto \
        --random-order \
        --reruns 10 \
        --reruns-delay 1 \
  &&  echo "[INFO] Checkout results at: ${PWD}/.coverage-html/index.html" \
  &&  popd \
  &&  { __clean_up; return 0; } \
  ||  { __clean_up; return 1; }
}

function job_melts_deploy {
  export TWINE_USERNAME='__token__'
  export TWINE_PASSWORD

  export PROD_AWS_ACCESS_KEY_ID="${MELTS_PROD_AWS_ACCESS_KEY_ID}"
  export PROD="${MELTS_PROD_AWS_SECRET_ACCESS_KEY}"

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_melts_aws_login prod \
  &&  TWINE_PASSWORD=${PYPI_TOKEN} \
  &&  pushd melts || return 1 \
  &&  python3 setup.py sdist --formats=gztar \
  &&  twine check dist/* \
  &&  twine upload dist/* \
  &&  popd || return 1
}