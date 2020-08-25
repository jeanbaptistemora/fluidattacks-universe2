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
  if [[ $job == "bugsnag_report" ]]
  then
    shift
    arg1="$*"
  fi
  local provisioner
  export __NIX_PATH="${NIX_PATH}"
  export __NIX_SSL_CERT_FILE="${NIX_SSL_CERT_FILE}"

  # shellcheck disable=2016
      provisioner="./build/provisioners/${job}.nix" \
  &&  if [ ! -f "${provisioner}" ]
      then
        provisioner='./build/provisioners/integrates_reset.nix'
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
        --keep CI_MERGE_REQUEST_IID \
        --keep CI_PIPELINE_ID \
        --keep CI_PROJECT_ID \
        --keep DEV_AWS_ACCESS_KEY_ID \
        --keep DEV_AWS_SECRET_ACCESS_KEY \
        --keep DNS_ZONE_ID \
        --keep GITLAB_API_TOKEN \
        --keep GITLAB_API_USER \
        --keep INTEGRATES_API_TOKEN \
        --keep JWT_TOKEN \
        --keep __NIX_PATH \
        --keep __NIX_SSL_CERT_FILE \
        --keep NIX_PATH \
        --keep NIX_PROFILES \
        --keep NIX_SSL_CERT_FILE \
        --keep PROD_AWS_ACCESS_KEY_ID \
        --keep PROD_AWS_SECRET_ACCESS_KEY \
        --keep SERVES_DEV_AWS_ACCESS_KEY_ID \
        --keep SERVES_DEV_AWS_SECRET_ACCESS_KEY \
        --keep SERVES_PROD_AWS_ACCESS_KEY_ID \
        --keep SERVES_PROD_AWS_SECRET_ACCESS_KEY \
        --keep OBSERVES_DEV_AWS_ACCESS_KEY_ID \
        --keep OBSERVES_DEV_AWS_SECRET_ACCESS_KEY \
        --keep OBSERVES_PROD_AWS_ACCESS_KEY_ID \
        --keep OBSERVES_PROD_AWS_SECRET_ACCESS_KEY \
        --keep REVIEWS_TOKEN \
        --keep PYPI_TOKEN \
        --keep INTEGRATES_FORCES_API_TOKEN \
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
if decide_and_call_provisioner "${@}"
then
  decide_and_call_provisioner bugsnag_report &>/dev/null
else
  decide_and_call_provisioner bugsnag_report "${@}" &>/dev/null
fi
