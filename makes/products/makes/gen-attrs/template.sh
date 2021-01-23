# shellcheck shell=bash

function main {
      copy '__envApplications__' 'makes/attrs/applications.lst' \
  &&  copy '__envPackages__' 'makes/attrs/packages.lst'
}

main "${@}"
