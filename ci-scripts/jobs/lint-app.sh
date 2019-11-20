#!/usr/bin/env bash

# Runs linters on app

# Linters
run_lint () {
    RETVAL=0
    prospector -F -s high -u django -i node_modules app/ || RETVAL=1
    prospector -F -s veryhigh -u django -i node_modules fluidintegrates/ || RETVAL=1
    return $RETVAL
}

run_lint || exit 1
