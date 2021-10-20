# shellcheck shell=bash
export ANNOUNCEKIT_USER
export ANNOUNCEKIT_PASSWD

aws_login_dev 'observes' \
  && sops_export_vars 'observes/secrets-dev.yaml' \
    "announcekit_user" \
    "announcekit_passwd" \
  && ANNOUNCEKIT_USER="${announcekit_user}" \
  && ANNOUNCEKIT_PASSWD="${announcekit_passwd}" \
  && observes_generic_test "__envSrc__" "__envTestDir__"
