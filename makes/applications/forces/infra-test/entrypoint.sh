# shellcheck shell=bash

source '__envUtilsBashLibGit__'
source '__envUtilsMeltsLibCommon__'

function main {
      use_git_repo_services \
  &&  projects="$(forces_projects)" \
  &&  popd \
  &&  '__envTerraformTest__'  -var="projects=${projects}"
}

main
