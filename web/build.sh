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
  export __NIX_PATH="${NIX_PATH}"
  export __NIX_SSL_CERT_FILE="${NIX_SSL_CERT_FILE}"

  # shellcheck disable=2016
      provisioner="./build/provisioners/${job}.nix" \
  &&  if [ ! -f "${provisioner}" ]
      then
        provisioner='./build/provisioners/build_nix_caches.nix'
      fi \
  &&  echo "[INFO] Running with provisioner: ${provisioner}" \
  &&  nix-shell \
        --cores 0 \
        --keep CI \
        --keep CI_COMMIT_REF_NAME \
        --keep CI_MERGE_REQUEST_DESCRIPTION \
        --keep CI_MERGE_REQUEST_TITLE \
        --keep CI_NODE_INDEX \
        --keep CI_NODE_TOTAL \
        --keep CI_REGISTRY_PASSWORD \
        --keep CI_REGISTRY_USER \
        --keep CI_MERGE_REQUEST_IID \
        --keep CI_PIPELINE_ID \
        --keep DEV_AWS_ACCESS_KEY_ID \
        --keep DEV_AWS_SECRET_ACCESS_KEY \
        --keep PROD_AWS_ACCESS_KEY_ID \
        --keep PROD_AWS_SECRET_ACCESS_KEY \
        --keep REVIEWS_TOKEN \
        --keep NIX_PATH \
        --keep NIX_PROFILES \
        --keep NIX_SSL_CERT_FILE \
        --keep NIXPKGS_ALLOW_UNFREE \
        --keep __NIX_PATH \
        --keep __NIX_SSL_CERT_FILE \
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
