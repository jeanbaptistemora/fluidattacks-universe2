# shellcheck shell=bash

function main {
  terraform-apply -var="projects_forces=$(projects_with_forces)"
}

main
