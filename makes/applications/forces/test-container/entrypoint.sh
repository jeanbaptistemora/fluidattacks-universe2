# shellcheck shell=bash

function main {
      docker pull "fluidattacks/forces:${CI_COMMIT_REF_NAME}" \
  &&  docker run \
        -v "${PWD}:/src" \
        -e CI_COMMIT_REF_NAME="${CI_COMMIT_REF_NAME}" \
        --rm "fluidattacks/forces:${CI_COMMIT_REF_NAME}" \
        forces \
        --token "${INTEGRATES_FORCES_API_TOKEN}" \
        --lax
}

main "$@"
