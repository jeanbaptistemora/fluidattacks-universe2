# shellcheck shell=bash

function main {
  terraform-test -var="projects=$(forces_projects)"
}

main
