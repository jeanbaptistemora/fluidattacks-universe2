# shellcheck shell=bash

source '__envPythonUtils__'

function setup {
  make_python_path '3.7' '__envPythonRequirements__'
}

setup
