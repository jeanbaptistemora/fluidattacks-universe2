# shellcheck shell=bash

function load_base {
      echo '[INFO] Setting up base development environment' \
  &&  source '__envBaseSearchPaths__' \
  &&  echo '[INFO] ---' \
  &&  echo '[INFO] You can now execute `load_<product>`' \
  &&  echo '[INFO]   in order to make available all deps required to develop such product' \
  &&  echo '[INFO]'
}

function load_skims {
      echo '[INFO] Setting up Skims development environment' \
  &&  source '__envSkimsSetupDevelopment__' \
  &&  source '__envSkimsSetupRuntime__'
}

load_base
