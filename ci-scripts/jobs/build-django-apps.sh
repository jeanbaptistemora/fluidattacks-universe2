#!/usr/bin/env sh

build_django_apps() {
    set -e

    for i in django-apps/integrates-*; do
        cd $i
        python3 setup.py sdist -d ../packages/
        cd "$CI_PROJECT_DIR"
    done
}

build_django_apps
