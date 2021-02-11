# shellcheck shell=bash

source '__envUtilsMeltsLibCommon__'

function main {
      projects="$(projects_with_forces)" \
  &&  '__envTerraformTest__' -var="projects_forces=${projects}"
}

main
