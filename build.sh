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
        build*           ) provisioner='build';;
        deploy_container_app) provisioner='build-and-docker';;
        deploy_container_deps_mobile) provisioner='deploy_container_deps_mobile';;
        deploy_container*) provisioner='docker';;
        deploy_front     ) provisioner='deploy-front';;
        deploy_mobile    ) provisioner='deploy-mobile';;
        deploy_k8s*      ) provisioner='infra';;
        infra_*          ) provisioner="${job}";;
        functional_tests*) provisioner='selenium';;
        test*            ) provisioner='test';;
                        *) provisioner='full';;
      esac \
  &&  provisioner="./build/provisioners/${provisioner}.nix" \
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
        --keep JWT_TOKEN \
        --keep KUBECONFIG \
        --keep KUBE_CA_PEM \
        --keep KUBE_CA_PEM_FILE \
        --keep KUBE_INGRESS_BASE_DOMAIN \
        --keep KUBE_NAMESPACE \
        --keep KUBE_TOKEN \
        --keep KUBE_URL \
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
