#! /usr/bin/env sh

set -o errexit
set -o nounset

export ASSERTS_MODULE=${ASSERTS_MODULE:-all}

commands_pre() {
  pytest \
      --no-cov \
      --capture=no \
      -m prepare \
      --asserts-module "${ASSERTS_MODULE}" \
    test/test_others_prepare.py
}

commands() {
  pytest \
    -n ${CPUS:-auto} \
    --cov-branch \
    --failed-first \
    --dist=loadscope \
    --max-worker-restart=16 \
    --asserts-module "${ASSERTS_MODULE}" \
    --random-order-bucket=global
}

commands_post() {
  pytest \
      --no-cov \
      --capture=no \
      -m teardown \
      --asserts-module "${ASSERTS_MODULE}" \
    test/test_others_teardown.py
}
