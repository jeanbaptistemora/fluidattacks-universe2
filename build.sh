#! /usr/bin/env bash

source ./build/include/generic/shell-options.sh

function check_nix_version {
  # Check that Nix is installed
  if ! nix --version
  then
    echo 'Please install nix: https://nixos.org/nix/download.html'
    echo '  on most systems this is:'
    echo '    $ curl https://nixos.org/nix/install | sh'
    return 1
  fi
}

function decide_and_call_provisioner {
  local job="${1:-}"
  local provisioner

  # shellcheck disable=2016
      case "${job}" in
        *_infra*) provisioner='tf_infra';;
               *) provisioner='tf_infra';;
      esac \
  &&  provisioner="./build/provisioners/${provisioner}.nix" \
  &&  echo "[INFO] Running with provisioner: ${provisioner}" \
  &&  nix-shell \
        --cores 0 \
        --keep CI \
        --keep CI_COMMIT_REF_NAME \
        --keep DEV_AWS_ACCESS_KEY_ID \
        --keep DEV_AWS_SECRET_ACCESS_KEY \
        --keep PROD_AWS_ACCESS_KEY_ID \
        --keep PROD_AWS_SECRET_ACCESS_KEY \
        --max-jobs auto \
        --option restrict-eval false \
        --option sandbox false \
        --pure \
        --run '
          source "${srcIncludeGenericShellOptions}"
          source "${srcIncludeCli}"
        '"
          cli ${job}
        " \
        --show-trace \
        "${provisioner}"
}

check_nix_version
decide_and_call_provisioner "${@}"
