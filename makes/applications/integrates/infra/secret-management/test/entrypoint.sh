# shellcheck shell=bash

function main {
  terraform-test -var="projects_forces=$(projects_with_forces)"
}

main
