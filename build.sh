#! /usr/bin/env bash

source ./build/include/generic/shell-options.sh
source ./.envrc.public

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
      provisioner="./build/provisioners/${job}.nix" \
  &&  if [ ! -f "${provisioner}" ]
      then
        provisioner='./build/provisioners/build_nix_caches.nix'
      fi \
  &&  echo "[INFO] Running with provisioner: ${provisioner}" \
  &&  nix-shell \
        --cores 0 \
        --keep NIX_PATH \
        --keep NIX_PROFILES \
        --keep NIX_SSL_CERT_FILE \
        --keep CI \
        --keep CI_COMMIT_REF_NAME \
        --keep CI_MERGE_REQUEST_DESCRIPTION \
        --keep CI_MERGE_REQUEST_TITLE \
        --keep CI_NODE_INDEX \
        --keep CI_NODE_TOTAL \
        --keep CI_REGISTRY_PASSWORD \
        --keep CI_REGISTRY_USER \
        --keep AWS_ACCESS_KEY_ID \
        --keep AWS_SECRET_ACCESS_KEY \
        --keep GITLAB_API_TOKEN \
        --keep BREAK_BUILD_ID \
        --keep BREAK_BUILD_SECRET \
        --keep CI_JOB_ID \
        --keep CI_PROJECT_DIR \
        --keep GITLAB_CI_PROJECT_DIR \
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
