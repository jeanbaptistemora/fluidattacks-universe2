#! /bin/sh

# Download worker init script so runner can pass it to docker machine
mkdir -p /etc/gitlab-runner/init
wget \
  https://gitlab.com/fluidattacks/product/-/raw/cf2d5930b33e25f6a8ab0e45716d50c5f43f2676/makes/makes/ci/infra/init/worker.sh \
  -O /etc/gitlab-runner/init/worker.sh
