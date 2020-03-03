#! /usr/bin/env sh

set -o errexit

twine_export_credentials() {
      twine check dist/* \
  &&  TWINE_USERNAME='__token__' \
      TWINE_PASSWORD=$( \
        sops \
          --aws-profile continuous-admin \
          --decrypt \
          --extract '["TOOLBOX_PYPI_API_KEY"]' \
          ../../secrets-prod.yaml) \
      twine upload dist/*
}

twine_export_credentials
