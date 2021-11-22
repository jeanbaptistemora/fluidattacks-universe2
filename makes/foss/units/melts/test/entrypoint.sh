# shellcheck shell=bash

function start_localstack {
  local time='0'
  local timeout='60'
  local services='s3'

  echo '[INFO] Starting localstack' \
    && docker stop localstack_main || true \
    && ENTRYPOINT=-d SERVICES="${services}" localstack start \
    && while ! docker logs localstack_main | grep -q 'Ready.'; do
      sleep 1 \
        && time=$((time + 1)) \
        && if [ "${time}" = "${timeout}" ]; then
          echo "[ERROR] Timeout reached. Looks like container did not start properly" \
            && return 1
        fi
    done
}

function main {
  export DEV_AWS_ACCESS_KEY_ID="${SERVICES_DEV_AWS_ACCESS_KEY_ID}"
  export DEV_AWS_SECRET_ACCESS_KEY="${SERVICES_DEV_AWS_SECRET_ACCESS_KEY}"

  aws_login_dev \
    && if ! test -n "${CI:-}"; then
      # check if is in local environment
      start_localstack
    fi \
    && use_git_repo_services \
    && melts drills --pull-repos continuoustest \
    && services_path=$(pwd) \
    && popd \
    && cp -r melts/ "${services_path}" \
    && pushd "${services_path}/melts" \
    && pytest \
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
    && popd || return 1 \
    && return 0
}

main "${@}"
