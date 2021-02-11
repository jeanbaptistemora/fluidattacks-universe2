# shellcheck shell=bash

function main {
      projects="$('__envMelts__' misc --groups-with-forces)" \
  &&  '__envTerraformTest__' -var="projects_forces=${projects}"
}

main
