# shellcheck shell=bash

source '__envUtilsMeltsLibCommon__'

function main {
      projects="$(forces_projects)" \
  &&  '__envTerraformTest__' -var="projects=${projects}"
}

main
