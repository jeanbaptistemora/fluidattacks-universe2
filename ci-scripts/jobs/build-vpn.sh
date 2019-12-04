build_vpn() {

  # Build exams container

  set -euov pipefail

  # Import functions
  . ci-scripts/helpers/others.sh

  build_container \
    "registry.gitlab.com/fluidattacks/serves/vpn:$CI_COMMIT_REF_NAME" \
    containers/vpn
}

build_vpn
