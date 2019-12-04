build_exams() {

  # Build exams container

  set -euov pipefail

  # Import functions
  . ci-scripts/helpers/others.sh

  build_container \
    "registry.gitlab.com/fluidattacks/serves/exams:$CI_COMMIT_REF_NAME" \
    containers/exams
}

build_exams
