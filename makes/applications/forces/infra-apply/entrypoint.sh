# shellcheck shell=bash

source '__envUtilsMeltsLibCommon__'

function main {
      projects="$(forces_projects)" \
  &&  '__envTerraformApply__' -var="projects=${projects}"
}

main
