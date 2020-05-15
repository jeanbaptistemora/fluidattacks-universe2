#! /usr/bin/env bash

source ./build2/include/generic/shell-options.sh
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
      if echo "${job}" | grep -q 'test_asserts_'
      then
        ./build/scripts/odbc/set.sh
      fi \
  &&  provisioner="./build2/provisioners/${job}.nix" \
  &&  if [ ! -f "${provisioner}" ]
      then
        provisioner='./build2/provisioners/build_nix_caches.nix'
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
        --keep NIXPKGS_ALLOW_UNFREE \
        --keep ENCRYPTION_KEY \
        --keep subs \
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
