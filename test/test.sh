#! /usr/bin/env sh

set -o errexit
set -o nounset

commands_pre() {
  pytest --no-cov --capture=no -m prepare test/test_others_prepare.py
}

commands() {
  pytest \
    -n ${CPUS:-auto} \
    --failed-first \
    --dist=loadscope \
    --max-worker-restart=16 \
    --random-order-bucket=global \
    --cov-branch
}

commands_post() {
  pytest --no-cov --capture=no -m teardown test/test_others_teardown.py
}
