build_vpn() {

  # Build exams container

  set -Eeuo pipefail

  # Import functions
  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/build-container.sh)
  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/sops-source/sops.sh)
  . toolbox/others.sh

  aws_login

  sops_env secrets-production.yaml default \
    ANSIBLE_VAULT

  build_container \
    "registry.gitlab.com/fluidattacks/serves/vpn:$CI_COMMIT_REF_NAME" \
    containers/vpn \
    --build-arg ANSIBLE_VAULT="$ANSIBLE_VAULT"
}

build_vpn
