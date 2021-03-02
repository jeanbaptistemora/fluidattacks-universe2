# shellcheck shell=bash

source '__envPythonUtils__'

function setup {
      make_python_path '3.7' '__envPythonRequirements__' \
  &&  make_python_path_plain '__envSrcIntegrates__' \
  &&  make_python_path_plain '__envSrcIntegratesPackagesBack__' \
  &&  make_python_path_plain '__envSrcIntegratesBackModules__'
}

setup
