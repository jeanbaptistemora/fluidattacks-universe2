build_exams() {

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
    "registry.gitlab.com/fluidattacks/serves/exams:$CI_COMMIT_REF_NAME" \
    containers/exams \
    --build-arg ANSIBLE_VAULT="$ANSIBLE_VAULT"
}

build_exams
