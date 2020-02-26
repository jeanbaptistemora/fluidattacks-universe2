#!/usr/bin/env bash

# Runs linters on app

# Linters
run_lint () {
    RETVAL=0
    prospector -F -s high -u django -i node_modules app/ || RETVAL=1
    prospector -F -s high -u django -i node_modules django-apps/ || RETVAL=1
    prospector -F -s veryhigh -u django -i node_modules fluidintegrates/ || RETVAL=1
    prospector -F -s veryhigh lambda/ || RETVAL=1
    mypy --ignore-missing-imports \
        django-apps/integrates-back/backend/mailer.py \
        django-apps/integrates-back/backend/scheduler.py \
        django-apps/integrates-back/backend/services.py \
        django-apps/integrates-back/backend/util.py \
        django-apps/integrates-back/backend/exceptions.py \
        django-apps/integrates-back/backend/decorators.py \
        django-apps/integrates-back/backend/utils/* || RETVAL=1
    return $RETVAL
}

run_lint || exit 1
