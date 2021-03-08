# shellcheck shell=bash

function main {
  terraform-apply -var="projects=$(forces_projects)"
}

main
