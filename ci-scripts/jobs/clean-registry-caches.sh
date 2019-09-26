#!/usr/bin/env sh

clean_registry_caches() {

  # Remove deps-development, deps-production and deps-mobile registry caches

  set -e

  # Import functions
  . ci-scripts/helpers/others.sh

  # Delete caches if it is saturday
  if [ $(date +%u) -eq 6 ]; then
    delete_reg_repo deps-production/cache
    delete_reg_repo deps-development/cache
    delete_reg_repo deps-mobile/cache
  else
    echo 'Not deleting caches. Waiting until saturday.'
  fi

}

clean_registry_caches
