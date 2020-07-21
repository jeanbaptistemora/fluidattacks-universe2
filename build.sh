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
  local arg1="${2:-}"
  local provisioner

  # shellcheck disable=2016
      provisioner="./build/provisioners/${job}.nix" \
  &&  if [ ! -f "${provisioner}" ]
      then
        provisioner='./build/provisioners/reset.nix'
      fi \
  &&  echo "[INFO] Running with provisioner: ${provisioner}" \
  &&  nix-shell \
        --cores 0 \
        --keep AWS_SESSION_TOKEN \
        --keep CI \
        --keep CI_COMMIT_REF_NAME \
        --keep CI_COMMIT_REF_SLUG \
        --keep CI_JOB_ID \
        --keep CI_NODE_INDEX \
        --keep CI_NODE_TOTAL \
        --keep CI_PROJECT_DIR \
        --keep CI_REGISTRY_USER \
        --keep CI_REGISTRY_PASSWORD \
        --keep DEV_AWS_ACCESS_KEY_ID \
        --keep DEV_AWS_SECRET_ACCESS_KEY \
        --keep DNS_ZONE_ID \
        --keep GITLAB_TOKEN \
        --keep INTEGRATES_API_TOKEN \
        --keep JWT_TOKEN \
        --keep KUBECONFIG \
        --keep KUBE_CA_PEM \
        --keep KUBE_CA_PEM_FILE \
        --keep KUBE_INGRESS_BASE_DOMAIN \
        --keep KUBE_NAMESPACE \
        --keep KUBE_TOKEN \
        --keep KUBE_URL \
        --keep NIX_PATH \
        --keep NIX_PROFILES \
        --keep NIX_SSL_CERT_FILE \
        --keep PROD_AWS_ACCESS_KEY_ID \
        --keep PROD_AWS_SECRET_ACCESS_KEY \
        --keep SKIMS_PYPI_TOKEN \
        --max-jobs auto \
        --option restrict-eval false \
        --option sandbox false \
        --pure \
        --run '
          source "${srcIncludeGenericShellOptions}"
          source "${srcIncludeCli}"
        '"
          cli ${job} ${arg1}
        " \
        --show-trace \
        "${provisioner}"
}

check_nix_version
decide_and_call_provisioner "${@}"
