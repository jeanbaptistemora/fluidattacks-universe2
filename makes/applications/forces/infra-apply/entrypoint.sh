# shellcheck shell=bash

function main {
  terraforma-apply -var="projects=$(forces_projects)"
}

main
